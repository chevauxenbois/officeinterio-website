"""Build one detailed page per catalogue item into public/products/.

Run: python3 tools/build_products.py
Values marked typical are common specifications, not a factory's confirmed data.
When a partner factory confirms a product, replace them and add real photos under
public/images/products/<slug>/ (detail-1.jpg, space-1.jpg, white-1.jpg ...).
"""
import html, os, re, json

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
OUT = os.path.join(ROOT, 'products')
os.makedirs(OUT, exist_ok=True)
e = html.escape

# Reuse the plan-view drawings from the home page so every page matches.
idx = open(os.path.join(ROOT, 'index.html')).read()
D = dict(re.findall(r"^  (\w+):'(.*?)',?$", idx[idx.index('const D = {'):idx.index('};', idx.index('const D = {'))], re.M))

LAM = ['Natural oak', 'Light walnut', 'Frosty white', 'Grey stone']
LAM_HEX = {'Natural oak': '#C9A77C', 'Light walnut': '#8B6A4C', 'Frosty white': '#EEEDE8', 'Grey stone': '#9A958C',
           'Black': '#1E1E1E', 'White': '#F2F2F0', 'Silver grey': '#B8B8B4', 'Charcoal': '#3A3A3A', 'Navy': '#28344A',
           'Sage': '#8E9C86', 'Sand': '#D8CBB4', 'Rust': '#9A5A3C', 'Clear': '#DDE6E6', 'Frosted': '#E8ECEB', 'Ink blue': '#26344F'}
FRAME = ['Black', 'White', 'Silver grey']
FABRIC = ['Charcoal', 'Navy', 'Sage', 'Sand', 'Rust']

P = [
 dict(slug='linear-workstation', code='OI-WS-01', n='Linear workstation, 4 seats', c='Workstations', i='workstation', pk=['Starter', 'Professional'],
  sum='A straight run of four desks on a shared frame. The simplest way to seat a team, and easy to extend in pairs.',
  feat=['Shared frame, so runs can be extended two seats at a time', 'Low divider screen between facing desks', 'Cable tray under the top with a flip-up access flap', 'Levelling feet for uneven floors'],
  sizes=[('Per seat', '1200 × 600 mm'), ('Per seat (compact)', '1050 × 600 mm'), ('Desk height', '750 mm'), ('Screen height above top', '300 to 350 mm')], dim=(2400, 1200, 'Four seats, two facing two'),
  fin={'Top laminate': LAM, 'Frame': FRAME, 'Screen fabric': FABRIC},
  spec=[('Top', '25 mm pre-laminated particle board, 2 mm PVC edge band'), ('Frame', 'Powder-coated mild steel'), ('Screen', 'Fabric-covered pin-up board or toughened glass'), ('Cable management', 'Under-top tray and vertical riser'), ('Power', 'Optional socket box on the screen')],
  rel=['workstation-with-screens', 'task-chair', 'pedestal-storage', 'acoustic-panels']),
 dict(slug='workstation-with-screens', code='OI-WS-02', n='Workstation with privacy screens', c='Workstations', i='workstation', pk=['Professional', 'Executive'],
  sum='A deeper desk with taller screens on three sides for people who need focus or take calls all day.',
  feat=['Taller screens for visual privacy', 'Pin-up fabric face on the inside', 'Integrated socket box at desk height', 'Pairs with a mobile pedestal under each desk'],
  sizes=[('Per seat', '1400 × 700 mm'), ('Per seat (wide)', '1500 × 750 mm'), ('Desk height', '750 mm'), ('Screen height above top', '450 to 600 mm')], dim=(1400, 700, 'One seat'),
  fin={'Top laminate': LAM, 'Frame': FRAME, 'Screen fabric': FABRIC},
  spec=[('Top', '25 mm pre-laminated particle board, 2 mm PVC edge band'), ('Frame', 'Powder-coated mild steel'), ('Screen', 'Fabric-covered acoustic board, optional glass top strip'), ('Cable management', 'Under-top tray and vertical riser'), ('Power', 'Socket box with power and data points')],
  rel=['linear-workstation', 'ergonomic-chair', 'pedestal-storage', 'phone-booth']),
 dict(slug='task-chair', code='OI-ST-01', n='Task chair', c='Seating', i='chair', pk=['Starter'],
  sum='A light mesh-back chair for everyday desk work, with the adjustments most people need and nothing more.',
  feat=['Breathable mesh back', 'Seat height adjustment and tilt lock', 'Fixed arms', 'Nylon base on twin-wheel castors'],
  sizes=[('Overall width', '600 mm'), ('Seat height', '420 to 520 mm'), ('Overall height', '920 to 1020 mm'), ('Seat depth', '470 mm')], dim=(600, 600, 'Footprint'),
  fin={'Mesh': ['Black', 'Charcoal', 'Navy'], 'Seat fabric': FABRIC, 'Base': ['Black']},
  spec=[('Back', 'Mesh on a moulded frame'), ('Seat', 'Moulded foam with fabric cover'), ('Mechanism', 'Synchro tilt with lock'), ('Base', '5-star nylon base'), ('Castors', 'Twin-wheel nylon, 50 mm')],
  rel=['ergonomic-chair', 'linear-workstation', 'meeting-table', 'pantry-set']),
 dict(slug='ergonomic-chair', code='OI-ST-02', n='Ergonomic chair', c='Seating', i='chair', pk=['Professional', 'Executive'],
  sum='A fully adjustable chair for long days at the desk, with lumbar support and arms that move with you.',
  feat=['Adjustable lumbar support', 'Seat depth slider', '3D or 4D adjustable arms', 'Optional headrest'],
  sizes=[('Overall width', '650 mm'), ('Seat height', '430 to 530 mm'), ('Overall height', '1000 to 1200 mm with headrest'), ('Seat depth', '460 to 520 mm')], dim=(650, 650, 'Footprint'),
  fin={'Mesh': ['Black', 'Charcoal', 'Navy'], 'Seat fabric': FABRIC, 'Base': ['Black', 'Silver grey']},
  spec=[('Back', 'High-tension mesh with lumbar pad'), ('Seat', 'Moulded foam on a sliding seat plate'), ('Mechanism', 'Multi-lock synchro tilt'), ('Base', 'Aluminium or nylon 5-star base'), ('Castors', 'Twin-wheel PU, 60 mm, for hard floors')],
  rel=['task-chair', 'workstation-with-screens', 'manager-desk', 'boardroom-table']),
 dict(slug='meeting-table', code='OI-MT-01', n='Meeting table, 6 seats', c='Meeting', i='meeting', pk=['Starter', 'Professional'],
  sum='A rectangular table for six, sized for a small meeting room with space to walk around.',
  feat=['Seats six comfortably', 'Central flip-up box for power and HDMI', 'Cable spine down one leg', 'Rounded or square corners'],
  sizes=[('Top', '1800 × 900 mm'), ('Top (large)', '2100 × 1000 mm'), ('Height', '750 mm'), ('Room size needed', 'About 3.6 × 2.7 m')], dim=(1800, 900, 'Six seats'),
  fin={'Top laminate': LAM, 'Legs': FRAME},
  spec=[('Top', '25 mm pre-laminated particle board, 2 mm PVC edge band'), ('Legs', 'Powder-coated steel panel or loop legs'), ('Power', 'Flip-up box with 2 sockets, USB and HDMI'), ('Cable management', 'Under-top tray and leg spine')],
  rel=['boardroom-table', 'ergonomic-chair', 'acoustic-panels', 'linear-workstation']),
 dict(slug='boardroom-table', code='OI-MT-02', n='Boardroom table, 10 to 12 seats', c='Meeting', i='meeting', pk=['Executive'],
  sum='A long table for the whole leadership team, built in sections so it can travel through standard doors.',
  feat=['Seats ten to twelve', 'Two power boxes along the centre line', 'Modular top joined on site', 'Veneer or laminate top'],
  sizes=[('Top', '3600 × 1200 mm'), ('Top (large)', '4200 × 1350 mm'), ('Height', '750 mm'), ('Room size needed', 'About 6.0 × 3.6 m')], dim=(3600, 1200, 'Ten to twelve seats'),
  fin={'Top': ['Natural oak', 'Light walnut', 'Grey stone'], 'Base': ['Black', 'Silver grey']},
  spec=[('Top', 'Veneer or laminate on 25 mm board, in two or three sections'), ('Base', 'Powder-coated steel or wooden panel base'), ('Power', 'Two flip-up boxes with sockets, USB and HDMI'), ('Cable management', 'Cable spine in each base')],
  rel=['meeting-table', 'ergonomic-chair', 'acoustic-panels', 'executive-cabin']),
 dict(slug='manager-desk', code='OI-CB-01', n='Manager desk with side return', c='Cabins', i='cabin', pk=['Professional'],
  sum='An L-shaped desk for a manager cabin, with a side return for a screen or files and a pedestal underneath.',
  feat=['Left or right hand return', 'Built-in pedestal with lock', 'Modesty panel at the front', 'Grommets for cables'],
  sizes=[('Main desk', '1500 × 750 mm'), ('Side return', '900 × 450 mm'), ('Height', '750 mm'), ('Cabin size needed', 'About 3.0 × 3.0 m')], dim=(1500, 750, 'Main desk'),
  fin={'Top laminate': LAM, 'Frame': FRAME},
  spec=[('Top', '25 mm pre-laminated particle board, 2 mm PVC edge band'), ('Return', '18 mm board with lockable pedestal'), ('Frame', 'Panel ends or powder-coated steel legs'), ('Cable management', 'Grommets and under-top tray')],
  rel=['executive-cabin', 'ergonomic-chair', 'pedestal-storage', 'meeting-table']),
 dict(slug='executive-cabin', code='OI-CB-02', n='Executive cabin set', c='Cabins', i='cabin', pk=['Executive'],
  sum='A desk, back credenza and two visitor chairs, chosen to work together in a director or founder cabin.',
  feat=['Desk, credenza and visitor chairs as one set', 'Veneer or premium laminate', 'Concealed cable routing', 'Soft-close drawers in the credenza'],
  sizes=[('Desk', '1800 × 900 mm'), ('Credenza', '1800 × 450 × 750 mm'), ('Height', '750 mm'), ('Cabin size needed', 'About 3.6 × 3.6 m')], dim=(1800, 900, 'Desk'),
  fin={'Top': ['Natural oak', 'Light walnut', 'Grey stone'], 'Visitor chairs': FABRIC},
  spec=[('Desk top', 'Veneer or laminate on 25 mm board'), ('Credenza', 'Board carcass with soft-close drawers and shutters'), ('Base', 'Wooden panel or steel base'), ('Visitor chairs', 'Upholstered, fixed base')],
  rel=['manager-desk', 'ergonomic-chair', 'lounge-set', 'boardroom-table']),
 dict(slug='pedestal-storage', code='OI-SG-01', n='Pedestal and low storage', c='Storage', i='storage', pk=['Starter', 'Professional', 'Executive'],
  sum='A lockable three-drawer pedestal that slides under a desk, and low cabinets that double as a team counter.',
  feat=['Three drawers, one file drawer', 'Central lock', 'Mobile on castors or fixed', 'Low cabinets with a top cushion option'],
  sizes=[('Pedestal', '400 × 500 × 600 mm'), ('Low cabinet', '800 × 450 × 750 mm'), ('Drawer load', 'File drawer for A4 hanging files'), ('Lock', 'Central lock, two keys')], dim=(400, 500, 'Pedestal footprint'),
  fin={'Body laminate': LAM, 'Handles': ['Black', 'Silver grey']},
  spec=[('Body', '18 mm pre-laminated particle board'), ('Drawers', 'Metal or board drawers on ball-bearing runners'), ('Lock', 'Central locking'), ('Base', 'Castors or plinth')],
  rel=['linear-workstation', 'workstation-with-screens', 'manager-desk', 'pantry-set']),
 dict(slug='reception-desk', code='OI-RC-01', n='Reception desk', c='Reception', i='reception', pk=['Professional', 'Executive'],
  sum='The first thing visitors see. Straight or curved, with a raised counter and a panel for your logo.',
  feat=['Raised visitor counter', 'Space for one or two people behind', 'Logo panel at the front', 'Optional LED strip under the counter'],
  sizes=[('Length', '1800 to 2400 mm'), ('Depth', '800 mm'), ('Work surface height', '750 mm'), ('Counter height', '1050 to 1100 mm')], dim=(2100, 800, 'Typical footprint'),
  fin={'Front panel': ['Natural oak', 'Grey stone', 'Frosty white'], 'Counter top': ['Frosty white', 'Grey stone', 'Light walnut']},
  spec=[('Body', 'Board carcass, laminate or veneer finish'), ('Counter', 'Solid surface, quartz or laminate'), ('Lighting', 'Optional LED strip'), ('Storage', 'Drawers and a shutter cabinet behind')],
  rel=['lounge-set', 'acoustic-panels', 'executive-cabin', 'pantry-set']),
 dict(slug='lounge-set', code='OI-LG-01', n='Lounge sofa and coffee table', c='Lounge', i='lounge', pk=['Executive'],
  sum='A soft seating corner for reception or a break area, with a low table to set down a cup or a laptop.',
  feat=['Two or three seats', 'Removable cushion covers', 'Round or rectangular coffee table', 'Steel or wooden legs'],
  sizes=[('Two-seater', '1400 × 750 mm'), ('Three-seater', '1900 × 750 mm'), ('Seat height', '430 mm'), ('Coffee table', '600 mm round or 1000 × 500 mm')], dim=(1900, 750, 'Three-seater'),
  fin={'Upholstery': FABRIC, 'Legs': ['Black', 'Natural oak']},
  spec=[('Frame', 'Hardwood and plywood'), ('Cushions', 'High-density foam'), ('Upholstery', 'Commercial-grade fabric or leatherette'), ('Table', 'Laminate, veneer or stone top on steel legs')],
  rel=['reception-desk', 'phone-booth', 'pantry-set', 'acoustic-panels']),
 dict(slug='phone-booth', code='OI-LG-02', n='Phone booth', c='Lounge', i='pod', pk=['Executive'],
  sum='A one-person booth for calls and video meetings, so the open floor stays quiet.',
  feat=['Sound-absorbing walls', 'Built-in fan and light', 'Power and USB at the shelf', 'Glass door'],
  sizes=[('Footprint', '1000 × 1000 mm'), ('Height', '2200 mm'), ('Occupants', 'One person'), ('Clearance needed', '200 mm above, for the fan')], dim=(1000, 1000, 'Footprint'),
  fin={'Outer shell': ['Frosty white', 'Charcoal', 'Natural oak'], 'Inner acoustic fabric': FABRIC},
  spec=[('Shell', 'Steel or board panels'), ('Acoustics', 'Acoustic felt lining'), ('Door', 'Toughened glass'), ('Services', 'Fan, LED light, power socket and USB')],
  rel=['acoustic-panels', 'workstation-with-screens', 'lounge-set', 'meeting-table']),
 dict(slug='acoustic-panels', code='OI-AC-01', n='Acoustic wall panels', c='Acoustics', i='acoustic', pk=['Professional', 'Executive'],
  sum='Fabric-wrapped panels that soak up echo in meeting rooms and open floors, in colours to suit the space.',
  feat=['Cuts echo in hard-finished rooms', 'Wall or ceiling mounted', 'Cut to size and pattern', 'Pin-up surface'],
  sizes=[('Standard panel', '600 × 600 mm'), ('Large panel', '1200 × 600 mm'), ('Thickness', '25 mm'), ('Coverage', 'Planned per room')], dim=(1200, 600, 'Large panel'),
  fin={'Fabric': FABRIC + ['Ink blue']},
  spec=[('Core', 'Acoustic board or polyester fibre'), ('Finish', 'Fabric-wrapped'), ('Fixing', 'Concealed clips or adhesive'), ('Sizes', 'Standard or cut to size')],
  rel=['phone-booth', 'meeting-table', 'boardroom-table', 'workstation-with-screens']),
 dict(slug='pantry-set', code='OI-PT-01', n='Pantry tables and stools', c='Pantry', i='pantry', pk=['Starter', 'Professional', 'Executive'],
  sum='Café-height tables and stools for a pantry or break area, easy to wipe clean and to rearrange.',
  feat=['Café or bar height', 'Round or square tops', 'Stackable stools', 'Easy-clean tops'],
  sizes=[('Round table', '600 or 750 mm diameter'), ('Square table', '700 × 700 mm'), ('Table height', '750 or 1050 mm'), ('Stool seat height', '450 or 750 mm')], dim=(700, 700, 'Square table'),
  fin={'Top laminate': LAM, 'Frame': FRAME},
  spec=[('Top', 'Laminate, compact board or solid surface'), ('Base', 'Powder-coated steel'), ('Stools', 'Moulded seat on steel legs'), ('Care', 'Wipe clean with a damp cloth')],
  rel=['lounge-set', 'pedestal-storage', 'task-chair', 'reception-desk']),
]
BY = {p['slug']: p for p in P}

FAQ = [
 ('Can the size or finish be changed?', 'Usually, yes. Partner factories can adjust sizes and finishes within their range. Tell us what you need and we confirm it in the quote.'),
 ('How long does delivery take?', 'Lead time depends on the factory, the finish and the quantity. We give you a confirmed date with the quote.'),
 ('Who installs it?', 'The factory or its installation partner fits it on site, and we coordinate the visit and the snag list.'),
 ('What warranty do I get?', 'The warranty is the factory\'s. We share its terms in writing with the quote and help with any service request.'),
 ('Can I see it before ordering?', 'Yes. We can show you a sample, take you to the factory or showroom, or send a 3D view of it in your layout.'),
]


def draw(k):
    return f'<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">{D[k]}</svg>'


def dims(w, d, label):
    # Top view with dimension lines, drawn to the product's proportions.
    W, H = 360, 220
    s = min(220 / w, 120 / d)
    rw, rh = w * s, d * s
    x, y = (W - 60 - rw) / 2, 40 + (120 - rh) / 2
    t = 'font-family="Jost, sans-serif" font-size="11" letter-spacing=".5" fill="currentColor" stroke="none"'
    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-label="Top view, {w} by {d} millimetres" fill="none" stroke="currentColor" stroke-width="1.2">
<rect x="{x:.1f}" y="{y:.1f}" width="{rw:.1f}" height="{rh:.1f}"/>
<line x1="{x:.1f}" y1="{y-16:.1f}" x2="{x+rw:.1f}" y2="{y-16:.1f}"/><line x1="{x:.1f}" y1="{y-21:.1f}" x2="{x:.1f}" y2="{y-11:.1f}"/><line x1="{x+rw:.1f}" y1="{y-21:.1f}" x2="{x+rw:.1f}" y2="{y-11:.1f}"/>
<text {t} x="{x+rw/2:.1f}" y="{y-22:.1f}" text-anchor="middle">{w} mm</text>
<line x1="{x+rw+16:.1f}" y1="{y:.1f}" x2="{x+rw+16:.1f}" y2="{y+rh:.1f}"/><line x1="{x+rw+11:.1f}" y1="{y:.1f}" x2="{x+rw+21:.1f}" y2="{y:.1f}"/><line x1="{x+rw+11:.1f}" y1="{y+rh:.1f}" x2="{x+rw+21:.1f}" y2="{y+rh:.1f}"/>
<text {t} x="{x+rw+26:.1f}" y="{y+rh/2+4:.1f}">{d} mm</text>
<text {t} x="{W/2:.1f}" y="{H-12}" text-anchor="middle">TOP VIEW · {e(label.upper())}</text>
</svg>'''


def page(p):
    rel = [BY[r] for r in p['rel']]
    w, d, lab = p['dim']
    swatches = ''.join(
        f'<div class="fin-group"><h3>{e(g)}</h3><ul>' + ''.join(
            f'<li><span class="sw" style="background:{LAM_HEX.get(o, "#ccc")}"></span>{e(o)}</li>' for o in opts) + '</ul></div>'
        for g, opts in p['fin'].items())
    gallery_tabs = [('detail', 'Detail'), ('space', 'In a space'), ('white', 'On white')]
    gal = ''.join(
        f'<div class="gal-panel" id="g-{k}" role="tabpanel" aria-labelledby="t-{k}"{"" if j == 0 else " hidden"}>'
        f'<div class="gal-main">{draw(p["i"])}<span class="caption">{"Drawing" if j == 0 else "Photo"} · {e(lab if j == 0 else "from the partner factory, to come")}</span></div></div>'
        for j, (k, _) in enumerate(gallery_tabs))
    tabs = ''.join(f'<button role="tab" id="t-{k}" aria-controls="g-{k}" aria-selected="{"true" if j == 0 else "false"}" type="button">{t}</button>' for j, (k, t) in enumerate(gallery_tabs))
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p['n'], "sku": p['code'], "category": p['c'],
                         "description": p['sum'], "brand": {"@type": "Brand", "name": "Office Interio"}})
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p['n'])} · Office Interio</title>
<meta name="description" content="{e(p['sum'])}">
<link rel="icon" type="image/png" href="../favicon.png">
<link rel="apple-touch-icon" href="../images/brand/symbol-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500&display=swap">
<link rel="stylesheet" href="../css/site.css">
<link rel="stylesheet" href="../css/project.css">
<link rel="stylesheet" href="../css/product.css">
<script type="application/ld+json">{jsonld}</script>
</head>
<body>

<header class="bar">
  <div class="wrap">
    <a class="logo" href="../index.html" aria-label="Office Interio home"><img src="../images/brand/logo-horizontal-ink.png" alt="Office Interio" width="636" height="85"></a>
    <nav class="tabs" aria-label="Site sections">
      <a href="../index.html#projects">Projects</a>
      <a href="../index.html#catalogue" aria-current="page">Catalogue</a>
    </nav>
    <a class="pill" href="../index.html?item={p['slug']}#visit">Book a site visit</a>
  </div>
</header>

<main class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../index.html#catalogue">Catalogue</a><span>/</span><a href="../index.html#catalogue">{e(p['c'])}</a><span>/</span><span aria-current="page">{e(p['n'])}</span></nav>

  <section class="pd-top">
    <div class="gallery">
      <div class="gal-tabs" role="tablist" aria-label="Images">{tabs}</div>
      {gal}
    </div>
    <div class="pd-info">
      <span class="overline">{e(p['c'])} · {p['code']}</span>
      <hr class="hair">
      <h1 class="h1">{e(p['n'])}</h1>
      <p class="lede">{e(p['sum'])}</p>
      <ul class="feat">{''.join(f'<li>{e(f)}</li>' for f in p['feat'])}</ul>
      <dl class="mini">
        <div><dt>Fits packages</dt><dd>{' · '.join(p['pk'])}</dd></div>
        <div><dt>Typical size</dt><dd>{e(p['sizes'][0][1])}</dd></div>
        <div><dt>Price</dt><dd>On request, quoted for your quantity</dd></div>
      </dl>
      <div class="actions">
        <a class="pill" href="../index.html?item={p['slug']}#visit">Request a quote</a>
        <a class="pill line" href="#specs">See full specification</a>
      </div>
    </div>
  </section>

  <nav class="jump" aria-label="On this page"><a href="#finishes">Materials and finishes</a><a href="#specs">Specifications</a><a href="#sizes">Sizes</a><a href="#downloads">Downloads</a><a href="#faq">Questions</a></nav>

  <section class="pd-sec" id="finishes">
    <div class="sec-head"><span class="overline">Materials and finishes</span><h2>Choose your finish</h2><p class="muted">Typical options. The exact range depends on the partner factory, and we bring physical samples to your site visit.</p></div>
    <div class="fins">{swatches}</div>
  </section>

  <section class="pd-sec" id="specs">
    <div class="sec-head"><span class="overline">Specifications</span><h2>What it's made of</h2><p class="muted">Typical specification. The factory's confirmed specification comes with your quote.</p></div>
    <table class="spec"><tbody>{''.join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in p['spec'])}</tbody></table>
  </section>

  <section class="pd-sec" id="sizes">
    <div class="sec-head"><span class="overline">Sizes</span><h2>Dimensions</h2><p class="muted">All sizes in millimetres. Other sizes can usually be made to order.</p></div>
    <div class="size-grid">
      <table class="spec"><tbody>{''.join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in p['sizes'])}</tbody></table>
      <figure class="dims">{dims(w, d, lab)}</figure>
    </div>
  </section>

  <section class="pd-sec" id="downloads">
    <div class="sec-head"><span class="overline">Downloads</span><h2>Drawings and documents</h2><p class="muted">Sent by email once the partner factory is confirmed for your project.</p></div>
    <ul class="dl">
      <li><span><b>Specification sheet</b><small>PDF</small></span><a href="../index.html?item={p['slug']}#visit">Request</a></li>
      <li><span><b>2D CAD block</b><small>DWG, for your layout</small></span><a href="../index.html?item={p['slug']}#visit">Request</a></li>
      <li><span><b>3D model</b><small>SKP or 3DS</small></span><a href="../index.html?item={p['slug']}#visit">Request</a></li>
      <li><span><b>Installation guide</b><small>PDF</small></span><a href="../index.html?item={p['slug']}#visit">Request</a></li>
      <li><span><b>Warranty terms</b><small>PDF, from the factory</small></span><a href="../index.html?item={p['slug']}#visit">Request</a></li>
    </ul>
  </section>

  <section class="pd-sec" id="faq">
    <div class="sec-head"><span class="overline">Questions</span><h2>Before you order</h2></div>
    <div class="faq">{''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)}</div>
  </section>

  <section class="pd-sec">
    <div class="sec-head"><span class="overline">Pairs well with</span><h2>Complete the space</h2></div>
    <div class="rel">{''.join(f'<a href="{r["slug"]}.html"><div class="img">{draw(r["i"])}</div><span class="overline">{e(r["c"])}</span><h3>{e(r["n"])}</h3></a>' for r in rel)}</div>
  </section>
</main>

<section class="visit" style="margin-top:var(--s12)">
  <div class="wrap" style="grid-template-columns:1fr auto;align-items:center">
    <div class="copy">
      <span class="overline">Furnishing a floor?</span>
      <h2 class="h2">We'll quote for your seat count.</h2>
    </div>
    <a class="pill light" href="../index.html?item={p['slug']}#visit">Request a quote</a>
  </div>
</section>

<footer>
  <div class="wrap">
    <img src="../images/brand/logo-horizontal-ink.png" alt="Office Interio" width="636" height="85">
    <span>Office interiors in Pune · a brand of Omnaad Studio</span>
  </div>
</footer>

<script>
// Gallery tabs
const tabs=[...document.querySelectorAll('.gal-tabs [role=tab]')];
tabs.forEach(t=>t.addEventListener('click',()=>{{tabs.forEach(x=>{{const on=x===t;x.setAttribute('aria-selected',on);document.getElementById(x.getAttribute('aria-controls')).hidden=!on;}});}}));
</script>
</body>
</html>
'''


for p in P:
    open(os.path.join(OUT, p['slug'] + '.html'), 'w').write(page(p))
print('wrote', len(P), 'product pages')
print('SLUGS', json.dumps([p['slug'] for p in P]))
