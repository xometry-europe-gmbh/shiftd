#!/usr/bin/env bash

set -eo pipefail

PLATFORM="$(uname -s)"
if ! echo "${PLATFORM}" | grep MINGW64_NT; then
    echo "ERROR: Unsupported platform (${PLATFORM})"
    exit 1
fi

PACMAN="$(which pacman)"

PACMAN_PACKAGES=(
    "git"
    "mc"
    "base-devel"
    "mingw-w64-x86_64-toolchain"
    "mingw-w64-x86_64-cmake"
)


echo -e "\nBootstraping MinGW64...\n"

echo -e "Updating packages (restart may be needed)\n==="
"${PACMAN}" -Syuu
echo

echo -e "Setting up the development toolchain\n==="
"${PACMAN}" -S --needed ${PACMAN_PACKAGES[*]}
echo

echo -e "Installing the latest Pip and Virtualenv\n==="
if [[ ! -f "get-pip.py" ]]; then
    curl -s "https://bootstrap.pypa.io/get-pip.py" -o get-pip.py
fi
python get-pip.py
echo
pip --version
echo
pip install -U virtualenv
echo
pip list

echo -e "\nDONE"
