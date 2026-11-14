# Build the one-page printable flyer (HTML -> PDF via Playwright).
import re, os
here = os.path.dirname(os.path.abspath(__file__))
page = open(os.path.join(here, "..", "src", "tahoe-field-guide.html")).read()

# Reuse the habitat cross-section from the guide, with print-safe literal colors
# The flyer uses its own frozen copy of the cross-section (the web page labels zones
# on the chart; the flyer has a separate key), so page edits don't change the print layout.
svg = open(os.path.join(here, "transect.svg")).read()
COL = {"--z-alpine": "#c3cad0", "--z-sub": "#93aa90", "--z-mont": "#4c7855", "--z-wet": "#b59a3c",
       "--z-near": "#63b6c9", "--z-open": "#2c80b6", "--z-deep": "#113c66",
       "--rock": "#e6e0d4",          # light ground fill to save ink
       "--muted": "#6b5d4f", "--on-water": "#ffffff", "--mono": "'TeX Gyre Pagella'"}
for k, v in COL.items():
    svg = svg.replace(f"var({k})", v)
svg = re.sub(r'\s(id|class)="(tsvg|band)"', "", svg)
svg = svg.replace('font-size="10.5"', 'font-size="17"')
svg = svg.replace('>1,645 ft deep<', '>1,645 ft<')  # fits inside the lake shape
svg = svg.replace('class="tick"', 'class="tk"').replace('class="lab"', 'class="lb"')

qr = open(os.path.join(here, "qr.svg")).read()

ZONES = [("#c3cad0", "Alpine", "above ~10,000 ft"), ("#93aa90", "Subalpine", "~8,000–10,000 ft"),
         ("#4c7855", "Montane forest", "6,225–8,000 ft"), ("#b59a3c", "Shore, marsh, meadow & stream", "wet ground, any elevation"),
         ("#63b6c9", "Nearshore shallows", "rocky & sandy margin"), ("#2c80b6", "Open water", "surface to ~300 ft"),
         ("#113c66", "Deep lake", "300 to 1,645 ft")]
key = "".join(f'<li><i style="background:{c}"></i><span><b>{n}</b><em>{r}</em></span></li>' for c, n, r in ZONES)

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Tahoe Basin Field Guide</title>
<style>
@page {{ size: 8.5in 11in; margin: 0 }}
:root {{ --ink:#2b2118; --sepia:#6b5d4f; --rust:#8a4b2a; --rule:#b8a88f;
        --serif:'TeX Gyre Pagella','Palatino Linotype',Palatino,'Lora',serif; }}
* {{ box-sizing:border-box; margin:0; padding:0 }}
html,body {{ width:8.5in; height:11in; background:#fff; color:var(--ink); font-family:var(--serif);
            -webkit-print-color-adjust:exact; print-color-adjust:exact }}
.sheet {{ position:absolute; inset:.4in; border:1.6pt solid var(--ink); padding:4pt }}
.inner {{ height:100%; border:.5pt solid var(--ink); padding:.24in .3in .2in; display:flex; flex-direction:column; gap:.12in }}
.caps {{ text-transform:uppercase; letter-spacing:.16em; font-size:8.5pt; color:var(--rust) }}
header {{ text-align:center; display:flex; flex-direction:column; gap:4pt }}
h1 {{ font-size:38pt; font-weight:400; letter-spacing:.01em; line-height:1 }}
.sub {{ font-style:italic; font-size:13.5pt; color:var(--sepia) }}
.orn {{ display:flex; align-items:center; gap:8pt; justify-content:center; color:var(--rule); margin-top:2pt }}
.orn::before,.orn::after {{ content:""; height:.5pt; width:1.6in; background:var(--rule) }}
.orn span {{ font-size:9pt }}
.main {{ display:grid; grid-template-columns:3.15in 1fr; gap:.28in; align-items:start }}
figure.plate img {{ width:100%; display:block; border:.5pt solid var(--rule) }}
figure.plate figcaption {{ text-align:center; margin-top:6pt; line-height:1.3 }}
.pn {{ font-size:8pt; letter-spacing:.18em; text-transform:uppercase; color:var(--rust) }}
.cn {{ font-size:13pt }}
.sn {{ font-style:italic; font-size:10.5pt; color:var(--sepia) }}
.pf {{ font-size:9pt; color:var(--sepia); margin-top:3pt }}
.zones h2 {{ font-weight:400; font-size:15pt; margin-bottom:2pt }}
.zones p.lead {{ font-size:9.5pt; color:var(--sepia); font-style:italic; margin-bottom:6pt; line-height:1.3 }}
.zones svg {{ height:2.9in; width:auto; max-width:100%; display:block; margin:0 auto }}
.tk,.lb {{ font-family:var(--serif); font-size:17px }}
.tk {{ fill:var(--sepia) }} .lb {{ fill:var(--ink); font-style:italic }}
ul.key {{ list-style:none; display:grid; grid-template-columns:1fr 1fr; gap:5pt 10pt; margin-top:8pt }}
ul.key li {{ display:grid; grid-template-columns:9pt 1fr; gap:5pt; align-items:start; font-size:8.6pt; line-height:1.2 }}
ul.key i {{ width:9pt; height:9pt; margin-top:1pt; border:.4pt solid rgba(0,0,0,.25) }}
ul.key b {{ font-weight:700; display:block }} ul.key em {{ color:var(--sepia) }}
.figs {{ display:grid; grid-template-columns:repeat(4,1fr); border-top:.5pt solid var(--rule); border-bottom:.5pt solid var(--rule); padding:7pt 0 }}
.figs div {{ text-align:center; border-left:.5pt solid var(--rule) }} .figs div:first-child {{ border-left:0 }}
.figs b {{ display:block; font-size:24pt; font-weight:400; line-height:1 }}
.figs span {{ font-size:7.8pt; letter-spacing:.14em; text-transform:uppercase; color:var(--sepia) }}
.bottom {{ display:grid; grid-template-columns:1.5in 2.3in 1fr; gap:.22in; align-items:center }}
.qr svg {{ width:1.5in; height:1.5in; display:block }}
.scan h3 {{ font-weight:400; font-size:15.5pt; line-height:1.1 }}
.scan p {{ font-size:9.5pt; line-height:1.35; color:var(--sepia); margin-top:5pt }}
.scan .url {{ font-size:10.5pt; color:var(--ink); letter-spacing:.02em }}
.trail h4 {{ font-weight:400; margin-bottom:4pt }}
.trail ol {{ list-style:none; display:flex; flex-direction:column; gap:5pt; counter-reset:t }}
.trail li {{ font-size:9.4pt; line-height:1.3; padding-left:15pt; position:relative; counter-increment:t }}
.trail li::before {{ content:counter(t, upper-roman) "."; position:absolute; left:0; color:var(--rust); font-size:8.5pt }}
footer {{ margin-top:auto; font-size:7.2pt; color:var(--sepia); text-align:center; line-height:1.35; font-style:italic }}
</style></head><body><div class="sheet"><div class="inner">
<header>
  <div class="caps">Lake Tahoe Basin &nbsp;·&nbsp; California &amp; Nevada</div>
  <h1>Tahoe Basin Field Guide</h1>
  <div class="sub">The plants &amp; animals of the lake and its mountains, from the lake floor to Freel Peak</div>
  <div class="orn"><span>✦</span></div>
</header>
<section class="main">
  <figure class="plate">
    <img src="../img/mountain-bluebird.jpg" alt="Painted plate of a mountain bluebird">
    <figcaption>
      <div class="pn">Plate XVII</div>
      <div class="cn">Mountain Bluebird</div>
      <div class="sn">Sialia currucoides</div>
      <div class="pf">Nevada's state bird. The sky-blue male hovers over open high meadows and slopes, subalpine to alpine.</div>
    </figcaption>
  </figure>
  <div class="zones">
    <div class="caps" style="margin-bottom:3pt">Where to look</div>
    <h2>Seven habitat zones</h2>
    <p class="lead">Every species in the guide is tagged by zone. Vertical scale is true; the lake is 22 miles long.</p>
    {svg}
    <ul class="key">{key}</ul>
  </div>
</section>
<section class="figs">
  <div><b>143</b><span>plants &amp; animals</span></div>
  <div><b>25</b><span>painted plates</span></div>
  <div><b>117</b><span>photographs</span></div>
  <div><b>7</b><span>habitat zones</span></div>
</section>
<section class="bottom">
  <div class="qr">{qr}</div>
  <div class="scan">
    <h3>Scan to carry the guide on your hike</h3>
    <p>Free in any phone browser, no app. Search 143 species by name, group or status.</p>
    <p class="url">jonoisart.com/tahoe-field-guide</p>
    <p><b>Open it at the trailhead.</b> Signal is spotty on many trails.</p>
  </div>
  <div class="trail">
    <div class="caps">On the trail</div>
    <ol>
      <li>Never feed bears. Use bear boxes and lock your trash.</li>
      <li>Clean, drain and dry boats, paddles and waders. Invasive New Zealand mudsnails are already in the lake.</li>
      <li>Stay out of fenced beach plots. Tahoe yellow cress grows nowhere else on Earth.</li>
    </ol>
  </div>
</section>
<footer>Painted plates were generated with Google Gemini in the style of nineteenth-century natural history plates; they are not works by John James Audubon.
Photographs in the online guide come from Wikimedia Commons and public agencies and are credited there. Free to copy and share.</footer>
</div></div></body></html>"""
open(os.path.join(here, "flyer.html"), "w").write(html)
print("ok")
