#
# A combination of two things makes this much more complicated than it should have to be:
#
#  1. The standard Python interpreter allows threading but has a global lock
#     preventing more than one thread at a time from executing Python code, called the
#     Global Interpreter Lock, GIL. Many libraries like Nympy and blocking IO operations
#     will release the lock when running time consuming operations so that theading still
#     works. However, some things, specifically including drawing a Matplotlib plot with 
#     a complex waveform, is done in Python code and may lock up the interpreter for a
#     long time.
#
#  2. The callback used by the sounddevice library (which is really just a wrapper around
#     the C portaudio library) will time out and loose data if the interpreter is locked
#     for a long time (not exactly sure but something like a couple of 100 ms seems enough)
#     when the callback should be executed. There are no exceptions, the overflow flag is
#     not set, the callback just magically does not happen and data is lost.
#
# The only fix means not using threads but a completely separate OS process running its
# own interpreter. This opens up a whole can of worms related to shared data, and it
# works differently for different OS:es. The overall wisdom from the internet seems to
# be that if it works on Windows it works on Linux and MacOS too. So here we go, this 
# works on Windows, and the complexity is hidden in here. May the Universe forgive us.
#
import multiprocessing as mp
import ctypes
import sounddevice as sd
import numpy as np

class Liverecorder:
    stop_recorder = mp.Event()
    data_updated  = mp.Event()
    live_count    = mp.Value(ctypes.c_long, 0)
    data_lock     = mp.RLock()
    messages      = mp.Queue()
    proc          = None
    max_samples   = 0
    max_bytes     = 0

    shared_buffer = None

    def __init__(self, max_seconds, max_rate):
        self.max_samples = max_seconds * max_rate
        self.max_bytes = self.max_samples * 2
        self.shared_buffer = mp.RawArray(ctypes.c_byte, self.max_bytes)

    def _live_recorder(self, in_device, samplerate, stop_recorder, data_updated, live_count, data_lock, shared_buffer, messages):
        stream_data   = np.ndarray((self.max_samples,), dtype=np.int16, buffer=shared_buffer)
        def _callback(indata, frames, _, status):
            if status.input_overflow:
                raise Exception("Buffer overflow")
            with data_lock:
                stream_data[:-frames] = stream_data[frames:]
                stream_data[-frames:] = indata[:,0]
                live_count.value += frames
                data_updated.set()
        try:
            messages.put("Started live capture")
            with sd.InputStream(device=in_device, channels=1,
                                callback=_callback,
                                blocksize=100, dtype=np.int16,
                                samplerate=samplerate):
                stop_recorder.wait()
            messages.put("Capture ended normally")
        except Exception as err:
            messages.put(f"Capture failed, {err} occurred")
        finally:
            data_updated.set()

    def get_data(self):
        with self.data_lock:
            count = self.live_count.value
            self.live_count.value = 0
            data = np.ndarray((self.max_samples,), dtype=np.int16, buffer=self.shared_buffer).copy()
            self.data_updated.clear()
        return (data, count)

    def get_update_event(self):
        return self.data_updated

    def running(self):
        if self.proc:
            return self.proc.is_alive()
        else:
            return False

    def stop(self):
        self.stop_recorder.set()
        if self.proc:
            self.proc.join()

    def start(self, in_device, samplerate):
        self.stop()
        self.stop_recorder.clear()
        self.messages.put("Will start live capture")
        self.proc = mp.Process(target=self._live_recorder,
                          args=(in_device, samplerate, self.stop_recorder, self.data_updated, 
                                self.live_count, self.data_lock, self.shared_buffer, self.messages),
                          daemon=True)
        self.proc.start()
