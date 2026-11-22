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

/* ---------- v2: beweging en interactie ---------- */
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Verschijnen bij scrollen (ook automatisch voor blokken op andere pagina's)
document.querySelectorAll('main .section .wrap > *:not(.rv), main .grid > *, main .gallery > button, main .faq details').forEach((el, i, all) => {
  if (el.closest('.hx, .rv, .flow, .wiz') || el.tagName === 'SCRIPT') return;
  el.classList.add('rv');
  if (el.parentElement.matches('.grid, .gallery, .faq')) el.style.setProperty('--i', [...el.parentElement.children].indexOf(el) % 4);
});
const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), { rootMargin: '0px 0px -8% 0px' }) : null;
// Bij een sprong naar een anker of zonder ondersteuning: alles meteen tonen
const showAll = () => document.querySelectorAll('.rv, .hx, .stroke').forEach(el => el.classList.add('in'));
if (!io || location.hash) showAll(); else document.querySelectorAll('.rv, .hx, .stroke').forEach(el => io.observe(el));
addEventListener('hashchange', showAll);

// Header: compacter en verbergen bij naar beneden scrollen
const header = document.querySelector('.header');
let lastY = scrollY;
addEventListener('scroll', () => {
  const y = scrollY;
  if (header && !document.body.classList.contains('menu-open')) {
    header.classList.toggle('is-scrolled', y > 30);
    header.classList.toggle('is-hidden', y > 400 && y > lastY + 4);
    if (y < lastY - 4) header.classList.remove('is-hidden');
  }
  lastY = y;
}, { passive: true });

// Tellers
document.querySelectorAll('[data-count]').forEach(el => {
  const end = +el.dataset.count, suf = el.dataset.suffix || '';
  if (reduce || !io) { el.textContent = end + suf; return; }
  el.textContent = '0' + suf;
  const o = new IntersectionObserver(([e]) => {
    if (!e.isIntersecting) return; o.disconnect();
    const t0 = performance.now(), d = 1400;
    const step = t => { const k = Math.min(1, (t - t0) / d); el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))) + suf; if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  });
  o.observe(el);
});

// Parallax van deco-vormen in de hero
const decos = document.querySelectorAll('[data-parallax]');
if (decos.length && !reduce) {
  addEventListener('scroll', () => decos.forEach(d => d.style.transform = `translateY(${scrollY * d.dataset.parallax}px) rotate(${scrollY * d.dataset.parallax * .15}deg)`), { passive: true });
}

// Werkwijze: stappen lichten op tijdens scrollen
document.querySelectorAll('.flow__steps').forEach(ol => {
  const lis = [...ol.children];
  const upd = () => {
    const r = ol.getBoundingClientRect(), mid = innerHeight * .6;
    ol.style.setProperty('--p', Math.max(0, Math.min(1, (mid - r.top) / r.height)));
    lis.forEach(li => li.classList.toggle('on', li.getBoundingClientRect().top < mid));
  };
  addEventListener('scroll', upd, { passive: true }); upd();
});

// Carrousel: knoppen en slepen met de muis
document.querySelectorAll('.rail-wrap').forEach(w => {
  const rail = w.querySelector('.rail');
  const by = dir => rail.scrollBy({ left: dir * rail.clientWidth * .8, behavior: reduce ? 'auto' : 'smooth' });
  w.querySelector('[data-dir="-1"]')?.addEventListener('click', () => by(-1));
  w.querySelector('[data-dir="1"]')?.addEventListener('click', () => by(1));
  let down = false, sx = 0, sl = 0, moved = false;
  rail.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = rail.scrollLeft; });
  addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 5) { moved = true; rail.classList.add('dragging'); } rail.scrollLeft = sl - dx; });
  addEventListener('pointerup', () => { if (!down) return; down = false; setTimeout(() => rail.classList.remove('dragging'), 0); });
  rail.addEventListener('click', e => { if (moved) { e.preventDefault(); moved = false; } }, true);
});

// Offerte-wizard
document.querySelectorAll('.wiz').forEach(wiz => {
  const steps = [...wiz.querySelectorAll('.wiz__step')];
  const bar = wiz.querySelector('.wiz__bar span'), back = wiz.querySelector('.wiz__back'), next = wiz.querySelector('.wiz__next'), err = wiz.querySelector('.wiz__err');
  let i = 0;
  const show = n => {
    i = n; steps.forEach((s, k) => s.classList.toggle('on', k === i));
    bar.style.width = ((i + 1) / steps.length * 100) + '%';
    back.hidden = i === 0; next.textContent = i === steps.length - 1 ? 'Verstuur aanvraag' : 'Volgende';
    err.textContent = '';
  };
  const valid = () => {
    const s = steps[i];
    if (s.querySelector('input[type=checkbox], input[type=radio]') && !s.querySelector('input:checked')) { err.textContent = 'Kies minstens één optie.'; return false; }
    for (const f of s.querySelectorAll('[required]')) if (!f.checkValidity()) { err.textContent = 'Vul de verplichte velden correct in.'; f.focus(); return false; }
    return true;
  };
  back.addEventListener('click', () => show(Math.max(0, i - 1)));
  next.addEventListener('click', () => {
    if (!valid()) return;
    if (i < steps.length - 1) { show(i + 1); steps[i].querySelector('input, textarea')?.focus({ preventScroll: true }); return; }
    if (wiz.querySelector('[name=website]').value) return;
    const d = new FormData(wiz.querySelector('form'));
    const body = [
      'Diensten: ' + d.getAll('dienst').join(', '),
      'Type pand: ' + d.get('pand'),
      'Timing: ' + d.get('timing'),
      '', 'Naam: ' + d.get('naam'), 'Telefoon: ' + d.get('telefoon'), 'E-mail: ' + d.get('email'), 'Gemeente: ' + d.get('gemeente'),
      '', d.get('bericht') || ''
    ].join('\n');
    location.href = 'mailto:info@sdad.be?subject=' + encodeURIComponent('Offerteaanvraag via sdad.be – ' + d.get('naam')) + '&body=' + encodeURIComponent(body);
    wiz.querySelector('.wiz__body').hidden = true; wiz.querySelector('.wiz__done').hidden = false;
  });
  show(0);
});

// Dienstpagina's: header-status doorgeven (voor de plakkende paginanavigatie)
if (header) addEventListener('scroll', () => document.body.classList.toggle('hdr-hidden', header.classList.contains('is-hidden')), { passive: true });

// Hero van dienstpagina's laten verschijnen
document.querySelectorAll('.sh').forEach(el => io ? io.observe(el) : el.classList.add('in'));

// Paginanavigatie: actief hoofdstuk markeren
document.querySelectorAll('.subnav').forEach(nav => {
  const links = [...nav.querySelectorAll('a')];
  const targets = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const upd = () => {
    let cur = null;
    targets.forEach(t => { if (t.getBoundingClientRect().top < 200) cur = t; });
    links.forEach(a => {
      const on = cur && a.getAttribute('href') === '#' + cur.id;
      if (on && !a.classList.contains('on')) a.scrollIntoView({ block: 'nearest', inline: 'center' });
      a.classList.toggle('on', on);
    });
  };
  addEventListener('scroll', upd, { passive: true }); upd();
});

// Tabbladen (decoratieve technieken)
document.querySelectorAll('.tabs').forEach(tabs => {
  const btns = [...tabs.querySelectorAll('[role=tab]')];
  const select = b => btns.forEach(x => {
    const on = x === b; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
    document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
  });
  btns.forEach((b, i) => {
    b.addEventListener('click', () => select(b));
    b.addEventListener('keydown', e => {
      const k = { ArrowRight: 1, ArrowLeft: -1 }[e.key]; if (!k) return;
      const n = btns[(i + k + btns.length) % btns.length]; select(n); n.focus();
    });
  });
});

// Realisaties: filteren op type en dienst
document.querySelectorAll('.mosaic').forEach(m => {
  const bar = document.querySelector('.fbar'); if (!bar) return;
  let type = 'alle', cat = 'alle';
  const items = [...m.children], count = bar.querySelector('.fcount'), empty = m.nextElementSibling;
  const apply = () => {
    let n = 0;
    items.forEach(el => {
      const ok = (type === 'alle' || el.dataset.type === type) && (cat === 'alle' || el.dataset.cats.split(' ').includes(cat));
      el.hidden = !ok; if (ok) { n++; el.classList.add('in'); }
    });
    if (count) count.textContent = n + (n === 1 ? ' realisatie' : ' realisaties');
    empty.style.display = n ? 'none' : 'block';
  };
  bar.querySelectorAll('[data-type]').forEach(b => b.addEventListener('click', () => { type = b.dataset.type; bar.querySelectorAll('[data-type]').forEach(x => x.setAttribute('aria-pressed', x === b)); apply(); }));
  bar.querySelectorAll('[data-cat]').forEach(b => b.addEventListener('click', () => { cat = b.dataset.cat; bar.querySelectorAll('[data-cat]').forEach(x => x.setAttribute('aria-pressed', x === b)); apply(); }));
});

// Blog: zoeken en filteren op onderwerp
document.querySelectorAll('.bgrid').forEach(g => {
  const input = document.querySelector('.bsearch input'), chips = document.querySelectorAll('.btool [data-topic]'), empty = g.nextElementSibling;
  let topic = 'alle';
  const apply = () => {
    const q = (input.value || '').trim().toLowerCase(); let n = 0;
    [...g.children].forEach(c => { const ok = (topic === 'alle' || c.dataset.topics.split(' ').includes(topic)) && (!q || c.dataset.search.includes(q)); c.hidden = !ok; if (ok) { n++; c.classList.add('in'); } });
    empty.style.display = n ? 'none' : 'block';
  };
  input.addEventListener('input', apply);
  chips.forEach(b => b.addEventListener('click', () => { topic = b.dataset.topic; chips.forEach(x => x.setAttribute('aria-pressed', x === b)); apply(); }));
});

// Blogartikel: leesvoortgang en actieve inhoudstafel
const prog = document.querySelector('.progress span');
const artBody = document.querySelector('.art__body');
if (prog && artBody) {
  const tocLinks = [...document.querySelectorAll('.toc a')];
  const heads = tocLinks.map(a => document.querySelector(a.getAttribute('href')));
  const upd = () => {
    const r = artBody.getBoundingClientRect();
    prog.style.transform = `scaleX(${Math.max(0, Math.min(1, (innerHeight * .5 - r.top) / r.height))})`;
    let cur = -1; heads.forEach((h, i) => { if (h && h.getBoundingClientRect().top < 160) cur = i; });
    tocLinks.forEach((a, i) => a.classList.toggle('on', i === cur));
  };
  addEventListener('scroll', upd, { passive: true }); upd();
}
