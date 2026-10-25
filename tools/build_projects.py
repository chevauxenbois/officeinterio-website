import html
OUT = '/home/claude/officeinterio-website/public/projects/'

P = {
 'alfa': dict(
  name='Alfa', no='01', type='Workplace',
  lede='Long, calm rows of desks under an even ceiling, a boardroom for the whole team and quiet cabins finished in oak.',
  cover=('open-workspace', 'Open workspace'),
  facts=[('Type', 'Workplace'), ('Spaces', 'Open workspace, boardroom, cabins, reception'), ('Scope', 'Workplace planning, interior design, 3D visuals'), ('Images', 'Design visuals')],
  chapters=[
   ('Open workspace', 'Desks run the full length of the floor in white, with soft green screens to give each person a little privacy.', [('workstations', 'Workstation rows', 'full')]),
   ('Boardroom', 'One long table seats the whole team, with a screen at the head and frosted glass along one side.', [('boardroom', 'Boardroom', 'half'), ('boardroom-2', 'Boardroom from the screen end', 'half')]),
   ('Cabins', 'Private cabins in oak panelling and warm white, each with a desk, a visitor chair and a pendant light.', [('cabin', 'Cabin', 'full'), ('cabin-2', 'Cabin, second view', 'half'), ('cabin-3', 'Cabin with glass front', 'half')]),
   ('Reception', 'A marble-topped desk on an oak base, framed by black steel and glass.', [('reception', 'Reception', 'full')]),
  ]),
 'gamma': dict(
  name='Gamma', no='02', type='Workplace',
  lede='A soft reception lounge, glass-fronted meeting rooms, timber-arched booths for focused work and bright open desks.',
  cover=('reception', 'Reception lounge'),
  facts=[('Type', 'Workplace'), ('Spaces', 'Reception, meeting rooms, cabins, booths, open workspace'), ('Scope', 'Workplace planning, interior design, 3D visuals'), ('Images', 'Design visuals')],
  chapters=[
   ('Reception', 'A curved desk, a timber slat wall and a deep blue sofa set the tone at the door.', [('reception-2', 'Reception desk and lounge', 'full'), ('feature-wall', 'Lit feature wall', 'half')]),
   ('Open workspace', 'Oak desks in long rows along the windows, broken up by planters so every desk can see green.', [('open-workspace', 'Open workspace', 'full'), ('open-workspace-2', 'Desks along the windows', 'full')]),
   ('Meeting rooms and cabins', 'Frosted glass fronts keep meetings private. Cabins open to daylight with tan leather chairs.', [('meeting-room', 'Meeting room', 'half'), ('cabin', 'Cabin', 'half'), ('cabin-2', 'Cabin, second view', 'full')]),
   ('Booths', 'Arched timber booths give small groups a quiet place to talk away from the desks.', [('booths', 'Timber-arched booths', 'full'), ('booths-2', 'Booths, wider view', 'full')]),
   ('Washrooms', 'Stone-look tiles, a floating vanity and warm pendant lights.', [('washroom', 'Washroom vanity', 'full')]),
  ]),
}
ORDER = ['alfa', 'gamma']
e = html.escape

def shot(slug, key, cap, cls=''):
    return (f'<figure class="shot {cls}"><button type="button" data-full="../images/projects/{slug}/{key}.jpg" data-cap="Design visual · {e(cap)}" aria-label="Enlarge: {e(cap)}">'
            f'<img src="../images/projects/{slug}/{key}-sm.jpg" srcset="../images/projects/{slug}/{key}-sm.jpg 900w, ../images/projects/{slug}/{key}.jpg 2000w" sizes="(max-width: 960px) 100vw, 66vw" alt="{e(cap)}" loading="lazy"></button>'
            f'<figcaption>Design visual · {e(cap)}</figcaption></figure>')

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
    </nav>
    <a class="pill" href="../index.html#visit">Book a site visit</a>
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

    <p class="disclaim">All images on this page are design visuals, not photographs of the finished space.</p>

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
    <a class="pill light" href="../index.html#visit">Book a site visit</a>
  </div>
</section>

<footer>
  <div class="wrap">
    <img src="../images/brand/logo-horizontal-ink.png" alt="Office Interio" width="636" height="85">
    <span>Office interiors in Pune · a brand of Omnaad Studio</span>
  </div>
</footer>

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
