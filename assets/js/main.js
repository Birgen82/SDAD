// Mobiel menu
const menuBtn = document.querySelector('.menu-btn');
if (menuBtn) {
  menuBtn.addEventListener('click', () => {
    const open = document.body.classList.toggle('menu-open');
    menuBtn.setAttribute('aria-expanded', open);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && document.body.classList.contains('menu-open')) {
      document.body.classList.remove('menu-open');
      menuBtn.setAttribute('aria-expanded', false);
      menuBtn.focus();
    }
  });
}

// Dropdown met toetsenbord/klik
document.querySelectorAll('.dd > button').forEach(btn => {
  btn.addEventListener('click', () => {
    const dd = btn.parentElement;
    const open = dd.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
});
document.addEventListener('click', e => {
  document.querySelectorAll('.dd.open').forEach(dd => {
    if (!dd.contains(e.target)) { dd.classList.remove('open'); dd.querySelector('button').setAttribute('aria-expanded', false); }
  });
});

// Lightbox voor galerijen
const galleries = document.querySelectorAll('.gallery');
if (galleries.length) {
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', 'Afbeelding vergroot');
  lb.innerHTML = '<button class="lb-close" aria-label="Sluiten">×</button><button class="lb-prev" aria-label="Vorige">‹</button><img alt=""><button class="lb-next" aria-label="Volgende">›</button>';
  document.body.appendChild(lb);
  const img = lb.querySelector('img');
  let items = [], idx = 0, last = null;
  const show = i => { idx = (i + items.length) % items.length; img.src = items[idx].dataset.full; img.alt = items[idx].querySelector('img').alt; };
  const close = () => { lb.classList.remove('open'); if (last) last.focus(); };
  galleries.forEach(g => g.querySelectorAll('button').forEach((b, i, all) => {
    b.addEventListener('click', () => { items = [...all]; last = b; show(i); lb.classList.add('open'); lb.querySelector('.lb-close').focus(); });
  }));
  lb.querySelector('.lb-close').onclick = close;
  lb.querySelector('.lb-prev').onclick = () => show(idx - 1);
  lb.querySelector('.lb-next').onclick = () => show(idx + 1);
  lb.addEventListener('click', e => { if (e.target === lb) close(); });
  document.addEventListener('keydown', e => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });
}

// Filter realisaties
const filter = document.querySelector('.filter');
if (filter) {
  const cards = document.querySelectorAll('[data-cats]');
  filter.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    filter.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b));
    const f = b.dataset.filter;
    cards.forEach(c => c.classList.toggle('is-hidden', f !== 'alle' && !c.dataset.cats.split(' ').includes(f)));
    document.querySelectorAll('[data-group]').forEach(g => {
      const visible = g.querySelectorAll('[data-cats]:not(.is-hidden)').length;
      g.querySelector('.empty').style.display = visible ? 'none' : 'block';
    });
  });
}

// Contactformulier: zonder server opent het formulier een e-mail met de ingevulde gegevens
const form = document.querySelector('#contact-form');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (form.website.value) return; // honeypot
    const d = new FormData(form);
    const body = [
      `Naam: ${d.get('voornaam')} ${d.get('naam')}`,
      `Adres: ${d.get('adres')}, ${d.get('postcode')} ${d.get('stad')}`,
      `Telefoon: ${d.get('telefoon')}`,
      `E-mail: ${d.get('email')}`,
      '',
      d.get('bericht')
    ].join('\n');
    location.href = `mailto:info@sdad.be?subject=${encodeURIComponent('Vraag via sdad.be – ' + d.get('voornaam') + ' ' + d.get('naam'))}&body=${encodeURIComponent(body)}`;
    form.querySelector('.form-note').textContent = 'Uw e-mailprogramma opent nu met uw bericht. Verstuur het daar om uw vraag door te sturen.';
  });
}
