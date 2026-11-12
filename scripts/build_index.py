#!/usr/bin/env python3
"""Wrap src/tahoe-field-guide.html (the claude.ai artifact source, a page fragment)
into a standalone index.html for static hosting (GitHub Pages, Cloudflare Pages).

The artifact host adds a doctype, viewport meta and a small CSS reset at publish time;
this script adds the same so the page renders identically anywhere."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
body = (root / "src" / "tahoe-field-guide.html").read_text()

head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
  :root { color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  body { margin: 0; font: 14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
  img { max-width: 100%; }
  [hidden] { display: none !important; }
</style>
</head>
<body>
"""
(root / "index.html").write_text(head + body + "\n</body>\n</html>\n")
print("wrote index.html")
