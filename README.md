<div align="center">
<h3><code>guilhermeFin@github ~ $ ./contributions.sh</code></h3>
<img src="./contrib-heatmap.svg" width="860" />
<br><br>
<h3><code>guilhermeFin@github ~ $ whoami</code></h3>
<table>
<tr>
<td valign="top"><img src="./avi-ascii.svg" width="370" /></td>
<td valign="top"><img src="./info-card.svg" width="490" /></td>
</tr>
</table>
</div>

Notes
- Replace the placeholder lines in scripts/make_info_card.py (Role, Stack, Highlights) with your real info.
- The Action re-scrapes your public contributions daily and commits data/contributions.json + contrib-heatmap.svg.
- Locally: if you want to regenerate the portrait, create a venv and install dev deps:
  - python -m venv .venv
  - source .venv/bin/activate
  - pip install -r scripts/requirements-dev.txt
  - python scripts/prep_photo.py /path/to/photo.jpg
  - python scripts/make_ascii_svg.py
  - python scripts/make_info_card.py
- The CI workflow only installs the small deps (requests, beautifulsoup4) so rembg/opencv are not required in Actions.