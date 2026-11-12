#!/usr/bin/env python3
"""Merge Wikimedia/agency thumbnail manifests into data/thumbs-data.json and
inject the result into src/tahoe-field-guide.html between the THUMBS markers.

Usage: python3 scripts/thumbs_inject.py path/to/manifest.json [more.json ...]
Each manifest is an array of entries with query_title, status, thumb, width, height,
artist, license, license_url, file_page and optional note. Entries whose status
isn't "ok" are removed from the data. Copy the thumbnail files into thumbs/ separately."""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
data_path = root / "data" / "thumbs-data.json"
page_path = root / "src" / "tahoe-field-guide.html"
KEEP = ["thumb", "width", "height", "artist", "license", "license_url", "file_page", "note"]

data = json.loads(data_path.read_text()) if data_path.exists() else {}
for mf in sys.argv[1:]:
    for e in json.loads(Path(mf).read_text()):
        key = e["query_title"].replace("’", "'")   # normalize curly apostrophes
        if e.get("status") != "ok":
            data.pop(key, None)
            continue
        data[key] = {k: e.get(k) for k in KEEP}
data_path.write_text(json.dumps(data, indent=1, sort_keys=True))

page = page_path.read_text()
block = ("// THUMBS:BEGIN (generated from Wikimedia Commons manifests)\nconst THUMBS = "
         + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + ";\n// THUMBS:END")
page, n = re.subn(r"// THUMBS:BEGIN.*?// THUMBS:END", lambda m: block, page, flags=re.S)
assert n == 1, "THUMBS markers not found in page"
page_path.write_text(page)
print(f"{len(data)} thumbnails in page")
