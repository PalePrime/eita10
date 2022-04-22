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

stop_recorder = mp.Event()
data_updated  = mp.Event()
live_count    = mp.Value(ctypes.c_long, 0)
data_lock     = mp.RLock()
proc          = None
max_samples   = 96000 * 5        # 5 seconds of data at 96000 Hz sampling
max_bytes     = max_samples * 2  # two bytes per 16-bit sample

shared_buffer = mp.RawArray(ctypes.c_byte, max_bytes)

def live_recorder(in_device, samplerate, stop_recorder, data_updated, live_count, data_lock, shared_buffer):
    stream_data   = np.ndarray((max_samples,), dtype=np.int16, buffer=shared_buffer)
    stream_data[0] = 42
    def _callback(indata, frames, time, status):
        if status.input_overflow:
            raise Exception("overflow")
        with data_lock:
            stream_data[:-frames] = stream_data[frames:]
            stream_data[-frames:] = indata[:,0]
            live_count.value += frames
            data_updated.set()

    with sd.InputStream(device=in_device, channels=1,
                        callback=_callback,
                        blocksize=100, dtype=np.int16,
                        samplerate=samplerate):
            stop_recorder.wait()

def get_data():
    with data_lock:
        count = live_count.value
        live_count.value = 0
        data = np.ndarray((max_samples,), dtype=np.int16, buffer=shared_buffer).copy()
        data_updated.clear()
    return (data, count)

def get_update_event():
    return data_updated

def running():
    if proc:
        return proc.is_alive()
    else:
        return False

def stop():
    stop_recorder.set()
    if proc:
        proc.join()

def start(in_device, samplerate):
    global proc
    stop()
    stop_recorder.clear()
    proc = mp.Process(target=live_recorder,
                      args=(in_device, samplerate, stop_recorder, data_updated, live_count, data_lock, shared_buffer),
                      daemon=True)
    proc.start()
