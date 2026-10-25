"""Build the downloadable catalogue PDF into public/downloads/.

Run: python3 tools/build_catalogue.py   (needs Playwright with Chromium)
It reads the same product data as the product pages, so rebuild it after
changing tools/build_products.py.
"""
import base64, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_products import P, ROOT, LAM_HEX, draw, dims, e

SITE_URL = 'https://officeinterio.harshkahateprojects.workers.dev'  # change to https://officeinterio.com once the domain is live
OUT = os.path.join(ROOT, 'downloads', 'office-interio-catalogue.pdf')


def img(path):
    return 'data:image/png;base64,' + base64.b64encode(open(os.path.join(ROOT, path), 'rb').read()).decode()


def product(p, n):
    w, d, lab = p['dim']
    feats = ''.join(f'<li>{e(f)}</li>' for f in p['feat'])
    sizes = ''.join(f'<tr><th>{e(k)}</th><td>{e(v)}</td></tr>' for k, v in p['sizes'])
    spec = ''.join(f'<tr><th>{e(k)}</th><td>{e(v)}</td></tr>' for k, v in p['spec'])
    fins = ''.join(
        f'<div class="fg"><h4>{e(g)}</h4><ul>' + ''.join(
            f'<li><i style="background:{LAM_HEX.get(c, "#E3DDD1")}"></i>{e(c)}</li>' for c in cs) + '</ul></div>'
        for g, cs in p['fin'].items())
    return f'''<section class="pg prod">
  <header class="run"><span>Office Interio · Catalogue</span><span>{n:02d}</span></header>
  <div class="ptop">
    <div class="pic">{draw(p["i"])}<span class="cap">Plan view</span></div>
    <div class="pinfo">
      <span class="over">{e(p["c"])} · {e(p["code"])}</span>
      <h2>{e(p["n"])}</h2>
      <p class="lede">{e(p["sum"])}</p>
      <ul class="feat">{feats}</ul>
      <p class="pk">Packages: {e(", ".join(p["pk"]))}</p>
    </div>
  </div>
  <div class="pbot">
    <div><h3>Sizes <small>typical</small></h3><table>{sizes}</table><div class="dims">{dims(w, d, lab)}</div></div>
    <div><h3>Specification <small>typical</small></h3><table>{spec}</table><h3 class="mt">Finishes</h3>{fins}</div>
  </div>
  <footer class="pf"><span>Details and quote: {e(SITE_URL.split("//")[1])}/products/{p["slug"]}.html</span></footer>
</section>'''


CSS = '''
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Jost,sans-serif;font-weight:400;color:#111;background:#F5F5F3;font-size:10pt;line-height:1.5}
h1,h2,h3,h4,.over,th{font-weight:500}
.pg{width:210mm;height:297mm;padding:16mm 16mm 14mm;position:relative;page-break-after:always;overflow:hidden;background:#F5F5F3}
.over{font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:#6B4F32}
.cover{display:flex;flex-direction:column;justify-content:space-between;background:#111;color:#F5F5F3}
.cover .logo{width:70mm}
.cover h1{font-size:40pt;line-height:1.08;letter-spacing:-.01em;max-width:150mm}
.cover .sq{width:62mm;aspect-ratio:1/1;background:#E3DDD1;display:grid;place-items:center;color:#111}
.cover .sq svg{width:62%}
.cover .meta{display:flex;justify-content:space-between;font-size:9pt;color:#E3DDD1;border-top:1px solid #605D58;padding-top:5mm}
.cover .over{color:#E3DDD1}
.run{display:flex;justify-content:space-between;font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:#605D58;border-bottom:1px solid #111;padding-bottom:3mm;margin-bottom:9mm}
.intro h2{font-size:24pt;line-height:1.15;margin:3mm 0 6mm;max-width:150mm}
.intro p.l{font-size:12pt;line-height:1.55;max-width:150mm;margin-bottom:9mm;color:#111}
.toc{width:100%;border-collapse:collapse;border-top:1px solid #111;margin-bottom:9mm}
.toc td{padding:2.4mm 0;border-bottom:1px solid #E3DDD1}
.toc td.c{color:#605D58;width:34mm}.toc td.n{text-align:right;width:12mm;color:#605D58}
.pkgs{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.pkgs div{background:#E3DDD1;padding:5mm}
.pkgs h3{font-size:12pt;margin:1mm 0}
.pkgs p{font-size:8.5pt;color:#605D58}
.ptop{display:grid;grid-template-columns:78mm 1fr;gap:9mm;margin-bottom:8mm}
.pic{aspect-ratio:1/1;background:#E3DDD1;display:grid;place-items:center;position:relative}
.pic svg{width:60%;color:#111}
.pic .cap{position:absolute;left:4mm;bottom:3mm;font-size:7pt;letter-spacing:.14em;text-transform:uppercase;color:#605D58}
.pinfo h2{font-size:20pt;line-height:1.15;margin:2mm 0 3mm}
.lede{font-size:10.5pt;margin-bottom:4mm}
.feat{list-style:none;border-top:1px solid #E3DDD1}
.feat li{padding:1.6mm 0 1.6mm 6mm;border-bottom:1px solid #E3DDD1;position:relative;font-size:9pt}
.feat li::before{content:"";position:absolute;left:0;top:4.2mm;width:3mm;height:1px;background:#111}
.pk{font-size:8.5pt;color:#605D58;margin-top:3mm}
.pbot{display:grid;grid-template-columns:1fr 1fr;gap:9mm}
.pbot h3{font-size:10pt;margin-bottom:2mm}.pbot h3 small{font-weight:400;color:#605D58;font-size:8pt}
.pbot h3.mt{margin-top:5mm}
table{width:100%;border-collapse:collapse;border-top:1px solid #111}
th,td{text-align:left;vertical-align:top;padding:1.8mm 2mm 1.8mm 0;border-bottom:1px solid #E3DDD1;font-size:8.5pt;line-height:1.45}
.pbot th{width:42%}
.dims{background:#E3DDD1;padding:3mm;margin-top:4mm}.dims svg{width:100%;height:auto;color:#111}
.fg{margin-bottom:2.5mm}.fg h4{font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:#605D58;margin-bottom:1.5mm}
.fg ul{list-style:none;display:flex;flex-wrap:wrap;gap:1.5mm 4mm}
.fg li{display:flex;align-items:center;gap:1.5mm;font-size:8pt}
.fg i{width:4mm;height:4mm;border-radius:50%;border:1px solid rgba(17,17,17,.15);display:inline-block}
.pf{position:absolute;left:16mm;right:16mm;bottom:10mm;border-top:1px solid #E3DDD1;padding-top:2.5mm;font-size:7.5pt;color:#605D58;display:flex;justify-content:space-between}
.back{background:#111;color:#F5F5F3;display:flex;flex-direction:column;justify-content:space-between}
.back h2{font-size:30pt;line-height:1.1;max-width:150mm;margin-top:4mm}
.back ol{list-style:none;border-top:1px solid #605D58;margin-top:10mm}
.back li{display:grid;grid-template-columns:12mm 1fr;padding:3mm 0;border-bottom:1px solid #605D58;font-size:10.5pt}
.back li span{color:#E3DDD1;font-size:8pt;letter-spacing:.14em;padding-top:.8mm}
.back .over{color:#E3DDD1}
.back a{color:#F5F5F3}
.back .cta{display:inline-block;border:1px solid #F5F5F3;border-radius:999px;padding:3mm 7mm;font-weight:500;text-decoration:none;margin-top:6mm}
.back .note{font-size:8pt;color:#E3DDD1}
'''


def build():
    toc = ''.join(f'<tr><td>{e(p["n"])}</td><td class="c">{e(p["c"])}</td><td class="n">{i + 3:02d}</td></tr>' for i, p in enumerate(P))
    body = f'''<section class="pg cover">
  <img class="logo" src="{img("images/brand/logo-horizontal-paper.png")}" alt="Office Interio">
  <div>
    <div class="sq">{draw("workstation")}</div>
    <p class="over" style="margin:10mm 0 4mm">Furniture catalogue</p>
    <h1>Furniture for every part of the floor.</h1>
  </div>
  <div class="meta"><span>Spaces that work.</span><span>Pune · {e(SITE_URL.split("//")[1])}</span></div>
</section>
<section class="pg intro">
  <header class="run"><span>Office Interio · Catalogue</span><span>02</span></header>
  <span class="over">Contents</span>
  <h2>Workstations, seating, cabins and storage from our partner factories.</h2>
  <p class="l">Pick what you need and we'll quote for your seat count. Sizes and specifications here are typical. Final details, finishes and prices come from the partner factory for your order.</p>
  <table class="toc">{toc}</table>
  <div class="pkgs">
    <div><span class="over">10 to 25 seats</span><h3>Starter</h3><p>Workstations, task chairs, one meeting table and storage.</p></div>
    <div><span class="over">25 to 75 seats</span><h3>Professional</h3><p>Better workstations, ergonomic chairs, cabins, meeting rooms and reception.</p></div>
    <div><span class="over">50 seats and up</span><h3>Executive</h3><p>Premium finishes, executive cabins, branded reception and lounge areas.</p></div>
  </div>
</section>
{"".join(product(p, i + 3) for i, p in enumerate(P))}
<section class="pg back">
  <img class="logo" src="{img("images/brand/logo-horizontal-paper.png")}" alt="Office Interio" style="width:56mm">
  <div>
    <span class="over">How we work</span>
    <h2>One team from first sketch to handover.</h2>
    <ol>
      <li><span>01</span>Brief and site visit</li><li><span>02</span>Layout of your floor</li><li><span>03</span>3D view before you order</li>
      <li><span>04</span>Quotes from partner factories, side by side</li><li><span>05</span>Delivery and installation, coordinated by us</li><li><span>06</span>Handover and warranty in writing</li>
    </ol>
    <a class="cta" href="{SITE_URL}/index.html#visit">Book a site visit</a>
  </div>
  <p class="note">{e(SITE_URL.split("//")[1])} · Office Interio, a brand of Omnaad Studio, Pune</p>
</section>'''
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Office Interio furniture catalogue</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500&display=swap"><style>{CSS}</style></head><body>{body}</body></html>'
    tmp = os.path.join(tempfile.mkdtemp(), 'catalogue.html')
    open(tmp, 'w').write(doc)
    js = f'''const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{tmp}',{{waitUntil:'networkidle'}}).catch(()=>{{}});await p.evaluate(()=>document.fonts.ready);
console.log('jost', await p.evaluate(()=>document.fonts.check('500 12px Jost')));
await p.pdf({{path:{OUT!r},format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close();}})();'''
    subprocess.run(['node', '-e', js], check=True)
    print('wrote', OUT, os.path.getsize(OUT) // 1024, 'KB')


if __name__ == '__main__':
    build()
