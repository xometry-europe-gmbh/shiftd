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

* Clone *ShiftD* repo (via PowerShell console)::

    PS C:\Users\Administrator\dev> git clone --recurse-submodules https://github.com/shift-gmbh/shiftd.git
    Cloning into 'shiftd'...
    <...>

* Run the bootstrap script (via MinGW64 console)::

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

* Check consistency and requirements (via MinGW64 console)::

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make

    Health checking Fusion's deploy...1 OK
    Makefile:145: Can't find Docker executable
    AUTODESK_PATH -> /c/Documents\ and\ Settings/Administrator/AppData/Local/Autodesk/
    FUSION_PYTHON -> /c/Documents and Settings/Administrator/AppData/Local/Autodesk//webdeploy/shared/PYTHON/3.5.3c/win64_sp/Python
    FUSION_PYTHON_SCRIPTS -> /c/Documents\ and\ Settings/Administrator/AppData/Local/Autodesk//webdeploy/shared/PYTHON/3.5.3c/win64_sp/Python/Scripts
    FUSION_SITE_PACKAGES -> /c/Documents\ and\ Settings/Administrator/AppData/Local/Autodesk//webdeploy/production/d114930713fc09ae573cf2ada6f60182d13cd0ed/Api/Python/packages
    FUSION_ADDINS -> /c/Users/Administrator/AppData/Roaming/Autodesk/Autodesk\ Fusion\ 360/API/AddIns
    PYTHON -> /c/Documents\ and\ Settings/Administrator/AppData/Local/Autodesk//webdeploy/shared/PYTHON/3.5.3c/win64_sp/Python/python.exe
    PYTHON_LOCAL -> /c/Python37/python.exe
    PYTHON_LOCAL_SCRIPTS -> /c/Python37/Scripts

* Prepare a new virtual environment for the addin based on Fusion-hosted version of Python (via MinGW64 console)::

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make mostlyclean

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make clean-site

    Cleaning Fusion's site packages...DONE

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make new-host-venv

    Create a new virtual environment (Fusion-hosted)...

    Python facility:
    ===
    Python 3.5.3

    Ensure an empty `/c/Users/Administrator/dev/shiftd/.tmp_venv`...OK
    <...>

    pip 19.1.1 from c:\documents and settings\administrator\appdata\local\autodesk\webdeploy\shared\python\3.5.3c\win64_sp\python\lib\site-packages\pip (python 3.5)

    Requirement already up-to-date: virtualenv in c:\documents and settings\administrator\appdata\local\autodesk\webdeploy\shared\python\3.5.3c\win64_sp\python\lib\site-packages (16.6.0)
    Virtualenv 16.6.0

    Using base prefix 'c:\\documents and settings\\administrator\\appdata\\local\\autodesk\\webdeploy\\shared\\python\\3.5.3c\\win64_sp\\python'
    <...>
    DONE

    Stuff Fusion's site with the installed packages...

    total 272
    drwxr-xr-x 1 Administrator None      0 Jun 11 07:28 .
    drwxr-xr-x 1 Administrator None      0 Jun  7 12:50 ..
    -rwxr-xr-x 1 Administrator None 174592 Jun 11 07:28 _cffi_backend.cp35-win_amd64.pyd
    drwxr-xr-x 1 Administrator None      0 Jun  9 11:40 adsk
    drwxr-xr-x 1 Administrator None      0 Jun 10 06:29 cffi
    drwxr-xr-x 1 Administrator None      0 Jun 10 06:29 future
    drwxr-xr-x 1 Administrator None      0 Jun 10 06:29 gevent
    -rwxr-xr-x 1 Administrator None  28672 Jun 11 07:28 greenlet.cp35-win_amd64.pyd
    drwxr-xr-x 1 Administrator None      0 Jun 10 06:29 msgpack
    drwxr-xr-x 1 Administrator None      0 Jun 10 06:29 pycparser
    drwxr-xr-x 1 Administrator None      0 Jun 10 06:29 zerorpc
    drwxr-xr-x 1 Administrator None      0 Jun 10 06:29 zmq
    DONE

* Prepare a new virtual environment for the standalone app based on latest Python version (via MinGW64 console)::

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make new-local-venv

    Create a new virtual environment (local)...

    Python facility:
    ===
    Python 3.7.3

    Requirement already up-to-date: pip in c:\python37\lib\site-packages (19.1.1)
    pip 19.1.1 from c:\python37\lib\site-packages\pip (python 3.7)

    Requirement already up-to-date: virtualenv in c:\python37\lib\site-packages (16.6.0)
    Virtualenv 16.6.0

    Using base prefix 'c:\\python37'
    New python executable in C:\Users\Administrator\dev\shiftd\.venv\Scripts\python.exe
    Installing setuptools, pip, wheel...
    done.

    OpenSSL 1.1.0j  20 Nov 2018
    <...>
    DONE

    Package            Version
    ------------------ -------
    astroid            2.2.5
    atomicwrites       1.3.0
    <...>

* Install the logistic app onto a local environment (via MinGW64 console)::

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make install
    running develop
    running egg_info
    creating ShiftD.egg-info
    writing ShiftD.egg-info\PKG-INFO
    writing dependency_links to ShiftD.egg-info\dependency_links.txt
    writing entry points to ShiftD.egg-info\entry_points.txt
    writing requirements to ShiftD.egg-info\requires.txt
    writing top-level names to ShiftD.egg-info\top_level.txt
    writing manifest file 'ShiftD.egg-info\SOURCES.txt'
    reading manifest file 'ShiftD.egg-info\SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    warning: no previously-included files matching '__pycache__' found anywhere in distribution
    warning: no previously-included files matching '*.py[cod]' found anywhere in distribution
    no previously-included directories found matching '.venv'
    writing manifest file 'ShiftD.egg-info\SOURCES.txt'
    running build_ext
    Creating c:\users\administrator\dev\shiftd\.venv\lib\site-packages\ShiftD.egg-link (link to .)
    Adding ShiftD 0.1.0 to easy-install.pth file
    Installing shiftapp-script.py script to C:\Users\Administrator\dev\shiftd\.venv\Scripts
    Installing shiftapp.exe script to C:\Users\Administrator\dev\shiftd\.venv\Scripts
    <...>
    Using c:\users\administrator\dev\shiftd\.venv\lib\site-packages
    Finished processing dependencies for ShiftD==0.1.0

* Run tests (via MinGW64 console)::

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make check
    running test
    running egg_info
    writing ShiftD.egg-info\PKG-INFO
    writing dependency_links to ShiftD.egg-info\dependency_links.txt
    writing entry points to ShiftD.egg-info\entry_points.txt
    writing requirements to ShiftD.egg-info\requires.txt
    writing top-level names to ShiftD.egg-info\top_level.txt
    reading manifest file 'ShiftD.egg-info\SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    warning: no previously-included files matching '__pycache__' found anywhere in distribution
    warning: no previously-included files matching '*.py[cod]' found anywhere in distribution
    no previously-included directories found matching '.venv'
    writing manifest file 'ShiftD.egg-info\SOURCES.txt'
    running build_ext
    ============================= test session starts =============================
    platform win32 -- Python 3.7.3, pytest-4.6.2, py-1.8.0, pluggy-0.12.0 -- C:\Users\Administrator\dev\shiftd\.venv\Scripts\python.exe
    cachedir: .pytest_cache
    rootdir: C:\Users\Administrator\dev\shiftd
    plugins: sugar-0.9.2
    collecting ... collected 1 item

    shiftd/tests/test_shiftd.py::TestShiftd::test_shiftd PASSED              [100%]

    ========================== 1 passed in 0.11 seconds ===========================

* Install addin to the Fusion's host (via MinGW64 console)::

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make remove-addin

    Removing addin: shiftd...NOT FOUND

    Administrator@EC2AMAZ-T9F6NAP MINGW64 /c/Users/Administrator/dev/shiftd
    # make install-addin

    Installing addin: shiftd...
    shiftd.py (DONE)
    shiftd.manifest (DONE)
