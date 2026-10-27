import html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from links import USED
from build_products import BY as PRODUCTS, draw
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'projects') + os.sep
os.makedirs(OUT, exist_ok=True)

P = {
 'alfa': dict(
  name='Alfa', no='01', type='Workplace',
  lede='A bright, open floor of red and yellow workstations in long rows, with a warm, timber-lined cafeteria for breaks.',
  cover=('workstations', 'Open workspace'),
  facts=[('Type', 'Workplace'), ('Spaces', 'Open workspace, cafeteria'), ('Scope', 'Planning, design and fit-out'), ('Images', 'Photographs of the finished space')],
  chapters=[
   ('Open workspace', 'Workstations run the length of the floor in clusters, with red and yellow screens that give every team its own patch of colour.',
    [('open-workspace', 'Workstation rows', 'full'), ('workstations-3', 'Cluster workstations', 'half'), ('workstations-4', 'Desks beside the glass partition', 'half'), ('workstations-2', 'The full floor', 'full')]),
   ('Cafeteria', 'A calm room for lunch and breaks, with timber slats, cane chairs and artwork on warm white walls.',
    [('cafeteria', 'Cafeteria', 'full'), ('cafeteria-2', 'Cafeteria behind glass', 'half')]),
  ]),
 'gamma': dict(
  name='Gamma', no='02', type='Workplace',
  lede='Deep blue and orange booths, glass-walled meeting rooms and long rows of light oak desks, all filled with daylight.',
  cover=('booths', 'Booths'),
  facts=[('Type', 'Workplace'), ('Spaces', 'Reception, open workspace, meeting rooms, cabins, booths'), ('Scope', 'Planning, design and fit-out'), ('Images', 'Photographs of the finished space')],
  chapters=[
   ('Arrival', 'A curved blue sofa and a slatted wall at reception, then a bright corridor lined with booths.',
    [('reception', 'Reception', 'half'), ('booth-corridor', 'Booth corridor', 'half')]),
   ('Open workspace', 'Rows of oak desks with soft screens, running along a wall of windows.',
    [('open-workspace', 'Open workspace', 'full'), ('workstations', 'Workstations', 'half'), ('workstations-2', 'Desks beside the meeting rooms', 'half')]),
   ('Meeting rooms and cabins', 'Black-framed glass keeps meeting rooms and cabins open to the light and connected to the floor.',
    [('conference-room', 'Conference room', 'full'), ('meeting-rooms', 'Meeting rooms', 'half'), ('meeting-room', 'Meeting room', 'half'), ('cabins', 'Glass cabins', 'full')]),
  ]),
 'marathon-futurex': dict(
  name='Marathon Futurex', no='03', type='Workplace',
  lede='Warm light, long timber desks and glass-fronted cabins under an open ceiling, with a quiet reception at the door.',
  cover=('open-workspace', 'Open workspace'),
  facts=[('Type', 'Workplace'), ('Spaces', 'Reception, open workspace, cabins, meeting room'), ('Scope', 'Planning, design and fit-out'), ('Images', 'Photographs of the finished space')],
  chapters=[
   ('Arrival', 'A glass entrance door opens onto a backlit reception desk in white and oak.',
    [('entrance', 'Entrance', 'half'), ('reception', 'Reception', 'half')]),
   ('Open workspace', 'Long benches of timber desks with low screens, lit by continuous linear lights.',
    [('workstations', 'Workstations beside the cabins', 'full'), ('workstations-2', 'Open workspace', 'half'), ('workstations-3', 'Team corner', 'half')]),
   ('Cabins and meeting room', 'Glass-fronted rooms with frosted bands, from a two-person cabin to a lounge room and a meeting room.',
    [('cabin', 'Cabin', 'full'), ('glass-cabin', 'Glass cabin', 'half'), ('lounge-room', 'Lounge room', 'half'), ('cabin-seating', 'Cabin seating', 'half'), ('meeting-room', 'Meeting room', 'half')]),
  ]),
}
ORDER = ['alfa', 'gamma', 'marathon-futurex']
e = html.escape

def shot(slug, key, cap, cls=''):
    return (f'<figure class="shot {cls}"><button type="button" data-full="../images/projects/{slug}/{key}.jpg" data-cap="{e(cap)}" aria-label="Enlarge: {e(cap)}">'
            f'<img src="../images/projects/{slug}/{key}-sm.jpg" srcset="../images/projects/{slug}/{key}-sm.jpg 1000w, ../images/projects/{slug}/{key}.jpg 2400w" sizes="(max-width: 960px) 100vw, 66vw" alt="{e(cap)}" loading="lazy"></button>'
            f'<figcaption>{e(cap)}</figcaption></figure>')

for i, slug in enumerate(ORDER):
    p = P[slug]; nxt = ORDER[(i + 1) % len(ORDER)]; n = P[nxt]
    chapters = ''.join(
        f'''
  <section class="chapter">
    <div class="intro"><span class="overline">Space · {ci+1:02d}</span><h2>{e(t)}</h2><p>{e(d)}</p></div>
    <div class="shots">{''.join(shot(slug, k, c, cls) for k, c, cls in imgs)}</div>
  </section>''' for ci, (t, d, imgs) in enumerate(p['chapters']))
    facts = ''.join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in p['facts'])
    cover = shot(slug, p['cover'][0], p['cover'][1]).replace('loading="lazy"', 'fetchpriority="high"').replace('sizes="(max-width: 960px) 100vw, 66vw"', 'sizes="100vw"')
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{p['name']} · Office Interio</title>
<meta name="description" content="{e(p['name'])}, an Office Interio project: {e(p['lede'])}">
<meta property="og:title" content="{e(p['name'])} · Office Interio">
<meta property="og:image" content="../images/projects/{slug}/{p['cover'][0]}.jpg">
<link rel="icon" type="image/png" href="../favicon.png">
<link rel="apple-touch-icon" href="../images/brand/symbol-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500&display=swap">
<link rel="stylesheet" href="../css/site.css">
<link rel="stylesheet" href="../css/project.css">
</head>
<body>

<header class="bar">
  <div class="wrap">
    <a class="logo" href="../index.html" aria-label="Office Interio home"><img src="../images/brand/logo-horizontal-ink.png" alt="Office Interio" width="636" height="85"></a>
    <nav class="tabs" aria-label="Site sections">
      <a href="../index.html#projects" aria-current="page">Projects</a>
      <a href="../index.html#catalogue">Catalogue</a>
      <a href="../why.html">Why us</a>
    </nav>
    <a class="pill" href="../enquiry.html">Book a site visit</a>
  </div>
</header>

<main>
  <div class="wrap">
    <div class="crumb"><a href="../index.html#projects">← All projects</a></div>
    <section class="p-title">
      <div class="left">
        <span class="overline">Project · {p['no']} · {e(p['type'])}</span>
        <hr class="hair">
        <h1 class="display">{e(p['name'])}</h1>
      </div>
      <p class="lede">{e(p['lede'])}</p>
    </section>
  </div>

  <div class="cover">{cover}</div>

  <div class="wrap">
    <dl class="facts-row">{facts}</dl>
{chapters}

    <section class="chapter used-in">
      <div class="intro"><span class="overline">Furniture</span><h2>Pieces in this project</h2><p>Similar pieces from our catalogue, with sizes, finishes and specifications.</p></div>
      <div class="used">{''.join(f'<a href="../products/{k}.html" target="_blank" rel="noopener"><div class="ph">{draw(PRODUCTS[k]["i"])}</div><span class="overline">{e(PRODUCTS[k]["c"])}</span><h3>{e(PRODUCTS[k]["n"])}</h3></a>' for k in USED[slug])}</div>
    </section>

    <a class="next" href="{nxt}.html">
      <div class="row">
        <div><span class="overline">Next project</span><h2>{e(n['name'])}</h2><p class="muted">{e(n['lede'])}</p><span class="more">View project →</span></div>
        <div class="img"><img src="../images/projects/{nxt}/{n['cover'][0]}-sm.jpg" alt="" loading="lazy"></div>
      </div>
    </a>
  </div>
</main>

<section class="visit" style="margin-top:var(--s12)">
  <div class="wrap" style="grid-template-columns:1fr auto;align-items:center">
    <div class="copy">
      <span class="overline">Planning a similar office?</span>
      <h2 class="h2">We'll walk the space with you.</h2>
    </div>
    <a class="pill light" href="../enquiry.html">Book a site visit</a>
  </div>
</section>

<footer>
  <div class="wrap">
    <img src="../images/brand/logo-horizontal-ink.png" alt="Office Interio" width="636" height="85">
    <span>Office interiors in Pune · a brand of Omnaad Studio</span>
  </div>
</footer>
<script src="../js/site.js"></script>

<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Image viewer">
  <img id="lb-img" alt="">
  <span class="cap" id="lb-cap"></span>
  <button class="x" type="button" aria-label="Close">×</button>
  <button class="prev" type="button" aria-label="Previous image">←</button>
  <button class="nxt" type="button" aria-label="Next image">→</button>
</div>

<script>
// Simple image viewer: click any image to enlarge; arrows and Esc work.
const shots=[...document.querySelectorAll('figure.shot button')];
const lb=document.getElementById('lb'), im=document.getElementById('lb-img'), cap=document.getElementById('lb-cap');
let cur=0, opener=null;
function open(i){{cur=(i+shots.length)%shots.length;const b=shots[cur];im.src=b.dataset.full;im.alt=b.querySelector('img').alt;cap.textContent=b.dataset.cap;lb.hidden=false;document.body.style.overflow='hidden';lb.querySelector('.x').focus();}}
function close(){{lb.hidden=true;document.body.style.overflow='';if(opener)opener.focus();}}
shots.forEach((b,i)=>b.addEventListener('click',()=>{{opener=b;open(i);}}));
lb.querySelector('.x').addEventListener('click',close);
lb.querySelector('.prev').addEventListener('click',()=>open(cur-1));
lb.querySelector('.nxt').addEventListener('click',()=>open(cur+1));
lb.addEventListener('click',ev=>{{if(ev.target===lb)close();}});
document.addEventListener('keydown',ev=>{{if(lb.hidden)return;if(ev.key==='Escape')close();if(ev.key==='ArrowLeft')open(cur-1);if(ev.key==='ArrowRight')open(cur+1);}});
</script>
</body>
</html>
'''
    open(OUT + slug + '.html', 'w').write(page)
    print('wrote', slug)
