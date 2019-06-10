======
shiftd
======

Shift GmbH Dispatcher

The Autodesk Fusion 360 Dispatcher addin that communicates with an external apps using
ZMQ/RPC server.

Makefile facility
-----------------

* Getting help::

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make help

* Prepare requirements file::

    requirements - Compile Pip requirements

* Virtual environments::

    venv - Create the virtual environment (macOS/Linux)

    new-local-venv – Create local virtual environment (MinGW64)
    new-host-venv - Create Fusion-hosted virtual environment (macOS/MinGW64)

* Building and packaging::

    dist - Create a binary (wheel) distribution
    sdist - Create a source distribution

    install - Install project sources in "development mode"
    uninstall - Uninstall project sources

* Testing::

    check - Run tests

* Documentation::

    apidoc - Create one reST file with automodule directives per package
    html - Render standalone HTML files
    pdf - Generate LaTeX files and run them through pdflatex

* Autodesk Fusion 360 deployment::

    healthcheck - Health check Fusion's deploy
    clean-site - Remove all packages from Fusion's site except builtins and clean temporary files

    install-addin - Install addin to the Fusion's host
    remove-addin - Remove addin from the Fusion's host

* Docker facility (macOS only)::

    docker-info - Display system-wide information
    docker-stats - Show all images and containers
    docker-statsall - Same as `stats`, but more details provided

    docker-build - Build image from scratch
    docker-run - Run temporary container in an interactive mode

    docker-clean - Clean dangling images
    docker-distclean - Clean built containers
    docker-mostlyclean - Remove all unused images, built containers and volumes

* Auxiliary targets::

    help - Display all callable targets

    clean - Clean the project's directrory
    distclean - Clean the project's build output
    mostlyclean - Delete almost everything

Get started with MinGW64
------------------------

* Clone *ShiftD* repo::

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev
    # pwd
    /c/Users/Administrator/dev

    # git clone --recurse-submodules https://github.com/shift-gmbh/shiftd.git
    Cloning into 'shiftd'...
    <...>

* Run the bootstrap script::

    # cd shiftd/

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # ./scripts/bootstrap_mingw64.sh
    MINGW64_NT-10.0-17763

    Bootstraping MinGW64...

    Updating packages (restart may be needed)
    ===
    <...>

    Setting up the development toolchain
    ===
    <...>

    Installing the latest Pip and Virtualenv
    ===
    <...>

    pip 19.1.1 from /usr/lib/python3.7/site-packages/pip (python 3.7)

    Requirement already up-to-date: virtualenv in /usr/lib/python3.7/site-packages (16.6.0)

    Package    Version
    ---------- -------
    pip        19.1.1
    setuptools 41.0.1
    virtualenv 16.6.0
    wheel      0.33.4

    DONE
