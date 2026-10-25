// Shared footer and floating enquiry button for every page.
// Contact details live here only: fill them in once and every page updates.
const SITE = {
  phone: '',        // e.g. '+91 98765 43210'
  email: '',        // e.g. 'hello@officeinterio.com'
  whatsapp: '',     // digits with country code, e.g. '919876543210'
  address: '',      // e.g. 'Office 4, Baner Road, Pune 411045'
  instagram: '',    // full profile URL
  linkedin: '',     // full page URL
  hours: 'Monday to Saturday, 10 am to 7 pm',
};

(function () {
  const me = document.currentScript && document.currentScript.src;
  const base = me ? me.replace(/js\/site\.js(\?.*)?$/, '') : '';
  const u = p => base + p;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const wa = SITE.whatsapp ? 'https://wa.me/' + SITE.whatsapp.replace(/\D/g, '') + '?text=' + encodeURIComponent('Hello Office Interio, I would like to discuss an office fit-out.') : '';

  const contact = [
    SITE.phone && `<li><span>Phone</span><a href="tel:${esc(SITE.phone.replace(/\s/g, ''))}">${esc(SITE.phone)}</a></li>`,
    SITE.email && `<li><span>Email</span><a href="mailto:${esc(SITE.email)}">${esc(SITE.email)}</a></li>`,
    wa && `<li><span>WhatsApp</span><a href="${wa}" target="_blank" rel="noopener">Message us</a></li>`,
    SITE.address && `<li><span>Studio</span><span>${esc(SITE.address)}</span></li>`,
  ].filter(Boolean).join('') || `<li><span>Contact</span><a href="${u('index.html#visit')}">Book a site visit</a></li>`;

  const social = [
    SITE.instagram && `<a href="${esc(SITE.instagram)}" target="_blank" rel="noopener">Instagram</a>`,
    SITE.linkedin && `<a href="${esc(SITE.linkedin)}" target="_blank" rel="noopener">LinkedIn</a>`,
  ].filter(Boolean).join('');

  const footer = document.querySelector('footer');
  if (footer) {
    footer.className = 'site-footer';
    footer.innerHTML = `
  <div class="wrap">
    <div class="f-brand">
      <img src="${u('images/brand/logo-horizontal-ink.png')}" alt="Office Interio" width="636" height="85">
      <p>Spaces that work. Office interiors in Pune, from first sketch to handover.</p>
      <a class="pill" href="${u('index.html#visit')}">Book a site visit</a>
    </div>
    <nav class="f-col" aria-label="Explore">
      <h2>Explore</h2>
      <a href="${u('index.html#projects')}">Projects</a>
      <a href="${u('index.html#catalogue')}">Catalogue</a>
      <a href="${u('why.html')}">Why Office Interio</a>
      <a href="${u('downloads/office-interio-catalogue.pdf')}" target="_blank" rel="noopener">Download the catalogue (PDF)</a>
    </nav>
    <div class="f-col">
      <h2>Contact</h2>
      <ul>${contact}</ul>
      ${SITE.hours ? `<p class="hours">${esc(SITE.hours)}</p>` : ''}
    </div>
    <div class="f-col">
      <h2>For partners</h2>
      <a href="${u('index.html#visit')}">Refer a tenant</a>
      <a href="${u('why.html#brokers')}">Brokers and building managers</a>
      ${social ? `<div class="social">${social}</div>` : ''}
    </div>
  </div>
  <div class="wrap f-base"><span>© ${new Date().getFullYear()} Office Interio, a brand of Omnaad Studio</span><span>Pune, India</span></div>`;
  }

  // Floating enquiry button: WhatsApp when a number is set, otherwise the site visit form.
  if (!document.querySelector('.fab')) {
    const a = document.createElement('a');
    a.className = 'fab';
    if (wa) { a.href = wa; a.target = '_blank'; a.rel = 'noopener'; a.innerHTML = '<span class="dot" aria-hidden="true"></span>WhatsApp us'; }
    else { a.href = u('index.html#visit'); a.innerHTML = '<span class="dot" aria-hidden="true"></span>Quick enquiry'; }
    document.body.appendChild(a);
    // Hide it while the enquiry form itself is on screen.
    const visit = document.getElementById('visit');
    if (visit && 'IntersectionObserver' in window) {
      new IntersectionObserver(es => es.forEach(en => a.classList.toggle('away', en.isIntersecting))).observe(visit);
    }
  }
})();
