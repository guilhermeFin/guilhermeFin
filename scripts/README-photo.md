# Photo-processing setup (Python 3.11 virtualenv)

This repository separates heavy, platform-sensitive photo-processing dependencies
into `scripts/requirements-photo.txt`. Install those packages in a Python 3.11
virtual environment (recommended) to avoid conflicting `numpy` / `onnxruntime`
requirements on newer interpreters.

Two easy options:

1) System Python 3.11 (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-distutils
python3.11 -m venv .venv-py311
source .venv-py311/bin/activate
pip install --upgrade pip
pip install -r scripts/requirements-photo.txt
```

2) pyenv (portable, recommended if you manage multiple Python versions)

```bash
# install pyenv (if you don't have it)
curl https://pyenv.run | bash
# follow pyenv post-install steps, then:
pyenv install 3.11.4
pyenv virtualenv 3.11.4 pf-photo-venv
pyenv local pf-photo-venv
python -m pip install --upgrade pip
pip install -r scripts/requirements-photo.txt
```

Quick checks

```bash
# activate your venv if needed, then
python -c "import rembg, cv2, onnxruntime; print('photo deps OK')"
# run the prep + ascii workflow (adjust input/output paths as needed)
python scripts/prep_photo.py path/to/input.jpg path/to/output-prepped.png
python scripts/make_ascii_svg.py path/to/output-prepped.png path/to/avi-ascii.svg
```

Notes

- `onnxruntime` and `rembg` may have additional system requirements (libjpeg,
  libpng, etc.) on some Linux distributions. If installation fails, prefer a
  clean Python 3.11 virtualenv and consult the error message for missing
  system packages.
- If you only need to generate ASCII SVGs from the already prepped PNG, you
  only need `Pillow` (already in `scripts/requirements-dev.txt`).
