#!/usr/bin/env bash
set -e

# jump to the folder this script lives in (follows symlinks too)
cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

# create the venv only if it doesn't exist yet
if [ ! -f .venv/bin/activate ]; then
    python3 -m venv .venv || {
        echo "couldn't create a venv. on debian/ubuntu try: sudo apt install python3-venv" >&2
        exit 1
    }
fi
source .venv/bin/activate

# install pyqt5 only if it's missing
python -c "import PyQt5" 2>/dev/null || pip install pyqt5
exec python3 main.py "$@"