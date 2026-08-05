#!/usr/bin/env bash
set -euo pipefail

# Helper: create a Python 3.11 virtualenv and install photo-processing deps
# Usage: ./scripts/setup-photo-venv.sh [venv-dir] [python-exe]
# Example: ./scripts/setup-photo-venv.sh .venv-photo python3.11

VENV_DIR=${1:-.venv-photo}
PYTHON=${2:-python3.11}
REQ_FILE=${3:-scripts/requirements-photo.txt}

echo "Using python: ${PYTHON}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "${PYTHON} not found. Install Python 3.11 or use pyenv, then re-run." >&2
  exit 2
fi

if [ -d "$VENV_DIR" ]; then
  echo "Virtualenv $VENV_DIR already exists. Activate it with: source $VENV_DIR/bin/activate"
  echo "To recreate: rm -rf $VENV_DIR && $0 $VENV_DIR $PYTHON"
  exit 0
fi

echo "Creating virtualenv in $VENV_DIR..."
$PYTHON -m venv "$VENV_DIR"
echo "Activating and upgrading pip..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel
echo "Installing photo requirements from $REQ_FILE..."
python -m pip install -r "$REQ_FILE"

echo "Done. Activate the venv with: source $VENV_DIR/bin/activate"
