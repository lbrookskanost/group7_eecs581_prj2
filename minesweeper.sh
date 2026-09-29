#!/usr/bin/env bash
set -e

# jump to the folder this script lives in (follows symlinks too)
cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

# use a venv if u have one
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

exec python3 main.py "$@"