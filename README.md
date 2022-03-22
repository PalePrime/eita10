# EITA10 Electronics course at LU/EIT

This repository contains examples, notebooks, software etc for the EITA10 Electronics course at LU/EIT

## Install git and Python

Install git from its home page https://git-scm.com/, see to it that the git binaries are added to your shell/command PATH

Install Python from its home page https://www.python.org/, also for Python, see to it that binaries are added to your shell/command PATH

With one exception, the Lcapy package, all software packages needed for exercises and labs are straightforward to install using the Python package manager, pip. For Lcapy there are two quirks:

1. The published Lcapy package has problems displaying nicely formatted equations in notebooks when running on Windows. The forked version of Lcapy referenced by this repository takes care of that and should run on all platforms. The sequence of steps below will install this modified version.

2. Lcapy's nice capability to draw schematic diagrams rely on having LaTeX plus some LaTeX packages and support software installed, please follow the instructions below.

## Steps after installing git and Python

Open a new shell/command promt (to make sure git, pip, etc are found on the PATH) and clone this repository:

    git clone https://github.com/PalePrime/eita10.git

This creates a subdirectory called eita10. Move down into this subdirectory and let that be the default directory for the following commands. First recursively init and update submodules:

    git submodule update --init

Install Python packages, including the modified Lcapy:

    pip install -r requirements.txt
    pip install -e ./lcapy

The second command builds and installs the modified Lcapy package.

## Supporting schematic diagrams

To produce schematic diagrams Lcapy needs to have LaTeX, the CircuiTikZ package, and either GhostScript or ImageMagick installed.

The TeX Live 2021 distribution from https://tug.org/texlive/ works on all platforms and has an interactive package manager that can pull in CircuiTikZ.

ImageMagick is also available for all platforms from https://imagemagick.org/index.php

## Supporting interactive, zoomable plots

We will often plot diagrams in notebooks. There is built-in support in the Python packages we use to make such diagrams interactively zoomable. However, this functionality requires that you have Node.js installed. Download and install from https://nodejs.org/en/

We also need to enable two extensions in the notebook server by the command:

    jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib

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

3. A plot illustrating the voltage for $0<t<30\ ms$

## Links to documentation

We will use Python mostly for scripting and calling library code, you may want to check out https://www.w3schools.com/python/default.asp as an introduction.

For general documentation for notebooks look at https://jupyter.org/ and its Python kernel (engine) at https://ipython.org/

The Lcapy package provides really powerfull tools for mathematical modelling of electronic circuits see https://lcapy.readthedocs.io/en/latest/index.html a brief introduction is found at https://blog.ouseful.info/2018/08/07/an-easier-approach-to-electrical-circuit-diagram-generation-lcapy/

Two Python packages provide the underlaying mathematical foundations for Lcapy, Numpy https://numpy.org/doc/stable/index.html for numerical computation and SymPy https://www.sympy.org/en/index.html for symbolic math.

For plotting we rely on Matplotlib https://matplotlib.org/stable/index.html#

In general Google is your friend, prefer answers from sites like https://stackoverflow.com/

Don't spend too much time on this, you will pick up most of what is needed through examples. Just keep in mind that the links are here for reference.

## Updates and new material

During the course there will be updates and additions to the material published here. Just issue the following command to bring your local copy up to date:

    git pull
    git submodule update

## Suggestions, issues, etc

Please use the Q&A section on the course Canvas page https://canvas.education.lu.se/courses/17247/discussion_topics/189854 as the main means of reporting problems, suggesting improvements, helping each other out with tips and tricks etc.