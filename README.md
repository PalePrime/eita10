# EITA10 Electronics course at LU/EIT

This repository contains examples, notebooks, software etc for the EITA10 Electronics course at LU/EIT

## Easiest way forward

Install git from its home page https://git-scm.com/, see to it that the git binaries are added to your shell/command PATH

Install Python from its home page https://www.python.org/, also for Python, see to it that binaries are added to your shell/command PATH

With one exception, the Lcapy package, all software packages needed for exercises and labs are straightforward to install using the Python package manager, pip. For Lcapy there are two quirks:

1. The published Lcapy package has problems displaying nicely formatted equations in notebooks when running on Windows. The forked version of Lcapy referenced by this repository takes care of that and should run on all platforms. The sequence of steps below will install this modified version.

2. Lcapy's nice capability to draw schematic diagrams rely on having LaTeX plus some LaTeX packages and support software installed. Installing this is platform dependent, please follow the instructions below.

## Step by step after installing git and Python

Open a shell/command promt, create a new directory, move into it and do the following:

    git clone https://github.com/PalePrime/eita10.git

