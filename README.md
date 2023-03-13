# EITA10 Electronics course at LU/EIT

This repository contains examples, notebooks, software etc for the EITA10 Electronics course at LU/EIT

## Install git and Python

Install git from its home page https://git-scm.com/, see to it that the git binaries are added to your shell/command PATH

Install Python from its home page https://www.python.org/, also for Python, see to it that binaries are added to your shell/command PATH

All software packages needed for exercises and labs are straightforward to install using the Python package manager, pip. For full functionality, specifically generated schematic diagrams and zoomable plots some additional software needs to be installed as described below.

## Steps after installing git and Python

Open a new shell/command promt (to make sure git, pip, etc are found on the PATH) and clone this repository:

    git clone https://github.com/PalePrime/eita10.git

This command creates a new directory called "eita10". Move down into this directory and let it be the default directory for all subsequent commands.

Install the required Python packages:

    pip install jupyterlab ipympl lcapy sounddevice

## Supporting schematic diagrams

To produce schematic diagrams Lcapy needs to have LaTeX, the CircuiTikZ package, and either GhostScript or ImageMagick installed.

The TeX Live 2021 distribution from https://tug.org/texlive/ works on all platforms and has an interactive package manager that can pull in CircuiTikZ. It is, however, a bulky install and may take hours to complete(!).

ImageMagick is available for all platforms from https://imagemagick.org/index.php

## Supporting interactive, zoomable plots

We will often plot diagrams in notebooks. There is built-in support in the Python packages we use to make such diagrams interactively zoomable. However, this functionality requires that you have Node.js installed. Download and install from https://nodejs.org/en/

## Notebook server start

Everything should now be in place, and we are ready to give it a go. Start the notebook server using the command:

    jupyter-lab

The notebook server should start and will write log messages in the shell/command window. It will display a URL to access the server (only localhost access by default), and normally it also automatically opens a tab in your web browser.

## Check that it works

Use the file panel on the web UI to open

 > notebooks/lcapy_first.ipynb
 
Run one code section at a time (shortcut is shift+enter). The first section should silently return after a few seconds. Subsequent sections should display:

1. A simple schematic diagram

2. An equation for the voltage across the capacitor as a function of time

3. A plot illustrating the voltage for 0<t<30 ms

## Links to documentation

We will use Python mostly for scripting and calling library code, you may want to check out https://www.w3schools.com/python/default.asp as an introduction.

For general documentation for notebooks look at https://jupyter.org/ and its Python kernel (engine) at https://ipython.org/

The Lcapy package provides really powerful tools for mathematical modelling of electronic circuits see https://lcapy.readthedocs.io/en/latest/index.html

Two Python packages provide the underlying mathematical foundations for Lcapy, Numpy https://numpy.org/doc/stable/index.html for numerical computation and SymPy https://www.sympy.org/en/index.html for symbolic math.

For plotting we rely on Matplotlib https://matplotlib.org/stable/index.html#

In general Google is your friend, prefer answers from sites like https://stackoverflow.com/

Don't spend too much time on this, you will pick up most of what is needed through examples. Just keep in mind that the links are here for reference.

## Suggestions, issues, etc

Please use the Q&A section on the course Canvas page as the main means of reporting problems, suggesting improvements, helping each other out with tips and tricks etc.
