#!/usr/bin/env python3
"""Generate flyer/qr.svg for the guide URL and verify it decodes.
Needs reportlab (encoder) and opencv-python (decoder check)."""
import sys
from pathlib import Path
import cv2, numpy as np
from reportlab.graphics.barcode import qrencoder as q

URL = sys.argv[1] if len(sys.argv) > 1 else "https://research.jonoisart.com/tahoe-field-guide/"

# Smallest QR version that fits at error level Q (tolerant of print wear)
for v in range(2, 15):
    try:
        c = q.QRCode(v, q.QRErrorCorrectLevel.Q); c.addData(URL); c.make(); break
    except Exception:
        continue
n, quiet = c.getModuleCount(), 4
N = n + 2 * quiet
d = "".join(f"M{x+quiet},{y+quiet}h1v1h-1z" for y in range(n) for x in range(n) if c.isDark(y, x))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {N} {N}" shape-rendering="crispEdges">'
       f'<rect width="{N}" height="{N}" fill="#fff"/><path d="{d}" fill="#1f1812"/></svg>')
(Path(__file__).parent / "qr.svg").write_text(svg)

# Rasterize and decode to prove the code scans to URL
s = 10
img = np.full((N * s, N * s), 255, np.uint8)
for y in range(n):
    for x in range(n):
        if c.isDark(y, x):
            img[(y+quiet)*s:(y+quiet+1)*s, (x+quiet)*s:(x+quiet+1)*s] = 30
val, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
print(f"version {v}, decoded: {val}", "OK" if val == URL else "MISMATCH")
sys.exit(0 if val == URL else 1)
