/*
 * SDAD – gedrag van de drie sites (sdad.be, offerteschilderwerken.be, offertegordijnen.be)
 *
 * Elk onderdeel start alleen als de bijhorende HTML op de pagina staat.
 * Formulieren hebben nog geen server: ze openen het e-mailprogramma van de bezoeker
 * (zie sendByMail). Vervang dat bij livegang door een formulierdienst.
 */
(() => {
  'use strict';

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const onScroll = fn => { addEventListener('scroll', fn, { passive: true }); fn(); };
  const MAIL = 'info@sdad.be';

  /** Opent het e-mailprogramma met een ingevulde aanvraag. */
  function sendByMail(subject, body) {
    location.href = `mailto:${MAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  }

  /* ---------- Menu ---------- */

  function initMobileMenu() {
    const btn = $('.menu-btn');
    if (!btn) return;
    const setOpen = open => {
      document.body.classList.toggle('menu-open', open);
      document.documentElement.classList.toggle('menu-lock', open); // scrollen blokkeren
      btn.setAttribute('aria-expanded', open);
    };
    btn.addEventListener('click', () => setOpen(!document.body.classList.contains('menu-open')));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) { setOpen(false); btn.focus(); }
    });
  }

  /** Uitklapmenu "Diensten": opent bij muis (CSS) én bij klik/toetsenbord. */
  function initDropdown() {
    $$('.dd > button').forEach(btn => btn.addEventListener('click', () => {
      btn.setAttribute('aria-expanded', btn.parentElement.classList.toggle('open'));
    }));
    document.addEventListener('click', e => $$('.dd.open').forEach(dd => {
      if (!dd.contains(e.target)) { dd.classList.remove('open'); $('button', dd).setAttribute('aria-expanded', false); }
    }));
  }

  /** Fijne lijn onder de menubalk zodra er gescrold is (enkel desktop). */
  function initHeaderShadow() {
    const header = $('.header');
    if (!header) return;
    const desktop = matchMedia('(min-width: 981px)');
    onScroll(() => {
      const scrolled = desktop.matches && scrollY > 30;
      if (scrolled !== header.classList.contains('is-scrolled')) header.classList.toggle('is-scrolled', scrolled);
    });
  }

  /* ---------- Beweging ---------- */

  /** Blokken verschijnen bij scrollen (.rv krijgt .in). Bij een sprong naar een anker: alles meteen tonen. */
  function initReveal() {
    $$('main .section .wrap > *:not(.rv), main .grid > *, main .gallery > button, main .faq details').forEach(el => {
      if (el.closest('.hx, .rv, .flow, .wiz') || el.tagName === 'SCRIPT') return;
      el.classList.add('rv');
      if (el.parentElement.matches('.grid, .gallery, .faq')) el.style.setProperty('--i', [...el.parentElement.children].indexOf(el) % 4);
    });
    const targets = $$('.rv, .hx, .stroke, .sh');
    const showAll = () => targets.forEach(el => el.classList.add('in'));
    if (!('IntersectionObserver' in window) || location.hash) return showAll();
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    targets.forEach(el => io.observe(el));
    addEventListener('hashchange', showAll);
  }

  /** Cijfers in de hero tellen op (data-count, optioneel data-suffix). */
  function initCounters() {
    $$('[data-count]').forEach(el => {
      const end = +el.dataset.count, suffix = el.dataset.suffix || '';
      if (reducedMotion || !('IntersectionObserver' in window)) { el.textContent = end + suffix; return; }
      el.textContent = '0' + suffix;
      const io = new IntersectionObserver(([e]) => {
        if (!e.isIntersecting) return;
        io.disconnect();
        const t0 = performance.now(), duration = 1400;
        const step = t => {
          const k = Math.min(1, (t - t0) / duration);
          el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))) + suffix;
          if (k < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
      io.observe(el);
    });
  }

  /** Achtergrondvideo: geen autoplay bij 'minder beweging'; tikken op de hero pauzeert of hervat. */
  function initHeroVideo() {
    $$('.hx__video').forEach(video => {
      if (reducedMotion) { video.removeAttribute('autoplay'); video.pause(); }
      video.closest('.hx--full, .lp-hero')?.addEventListener('click', e => {
        if (e.target.closest('a, button, input, label, textarea, form')) return;
        video.paused ? video.play() : video.pause();
      });
    });
  }

  /** Werkwijze: stappen lichten op en de lijn groeit mee tijdens het scrollen. */
  function initProcessSteps() {
    $$('.flow__steps').forEach(list => {
      const items = [...list.children];
      onScroll(() => {
        const r = list.getBoundingClientRect(), mid = innerHeight * 0.6;
        list.style.setProperty('--p', Math.max(0, Math.min(1, (mid - r.top) / r.height)));
        items.forEach(li => li.classList.toggle('on', li.getBoundingClientRect().top < mid));
      });
    });
  }

  /* ---------- Foto's ---------- */

  /** Lightbox voor elke .gallery (knoppen met data-full). */
  function initLightbox() {
    const galleries = $$('.gallery');
    if (!galleries.length) return;
    const lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Afbeelding vergroot');
    lb.innerHTML = '<button class="lb-close" aria-label="Sluiten">×</button><button class="lb-prev" aria-label="Vorige">‹</button><img alt=""><button class="lb-next" aria-label="Volgende">›</button>';
    document.body.appendChild(lb);
    const img = $('img', lb);
    let items = [], index = 0, opener = null;
    const show = i => {
      index = (i + items.length) % items.length;
      img.src = items[index].dataset.full;
      img.alt = $('img', items[index]).alt;
    };
    const close = () => { lb.classList.remove('open'); opener?.focus(); };
    galleries.forEach(g => $$('button', g).forEach((btn, i, all) => btn.addEventListener('click', () => {
      items = all; opener = btn; show(i); lb.classList.add('open'); $('.lb-close', lb).focus();
    })));
    $('.lb-close', lb).onclick = close;
    $('.lb-prev', lb).onclick = () => show(index - 1);
    $('.lb-next', lb).onclick = () => show(index + 1);
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    document.addEventListener('keydown', e => {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
  }

  /** Carrousel: pijlknoppen en slepen met de muis (aanraken = gewoon vegen). */
  function initCarousels() {
    $$('.rail-wrap').forEach(wrap => {
      const rail = $('.rail', wrap);
      const by = dir => rail.scrollBy({ left: dir * rail.clientWidth * 0.8, behavior: reducedMotion ? 'auto' : 'smooth' });
      $('[data-dir="-1"]', wrap)?.addEventListener('click', () => by(-1));
      $('[data-dir="1"]', wrap)?.addEventListener('click', () => by(1));
      let down = false, startX = 0, startScroll = 0, moved = false;
      rail.addEventListener('pointerdown', e => {
        if (e.pointerType !== 'mouse') return;
        down = true; moved = false; startX = e.clientX; startScroll = rail.scrollLeft;
      });
      addEventListener('pointermove', e => {
        if (!down) return;
        const dx = e.clientX - startX;
        if (Math.abs(dx) > 5) { moved = true; rail.classList.add('dragging'); }
        rail.scrollLeft = startScroll - dx;
      });
      addEventListener('pointerup', () => { if (down) { down = false; setTimeout(() => rail.classList.remove('dragging'), 0); } });
      rail.addEventListener('click', e => { if (moved) { e.preventDefault(); moved = false; } }, true); // geen klik na slepen
    });
  }

  /* ---------- Pagina-onderdelen ---------- */

  /** Dienstpagina's: navigatie "Op deze pagina" markeert het hoofdstuk in beeld. */
  function initSubnav() {
    $$('.subnav').forEach(nav => {
      const links = $$('a', nav);
      const sections = links.map(a => $(a.getAttribute('href'))).filter(Boolean);
      onScroll(() => {
        let current = null;
        sections.forEach(s => { if (s.getBoundingClientRect().top < 200) current = s; });
        links.forEach(a => {
          const on = !!current && a.getAttribute('href') === '#' + current.id;
          if (on && !a.classList.contains('on')) { const box = a.parentElement; box.scrollLeft = a.offsetLeft - (box.clientWidth - a.offsetWidth) / 2; }
          a.classList.toggle('on', on);
        });
      });
    });
  }

  /** Tabbladen (decoratieve technieken), ook met pijltjestoetsen. */
  function initTabs() {
    $$('.tabs').forEach(tabs => {
      const buttons = $$('[role=tab]', tabs);
      const select = btn => buttons.forEach(b => {
        const on = b === btn;
        b.setAttribute('aria-selected', on);
        b.tabIndex = on ? 0 : -1;
        document.getElementById(b.getAttribute('aria-controls')).hidden = !on;
      });
      buttons.forEach((btn, i) => {
        btn.addEventListener('click', () => select(btn));
        btn.addEventListener('keydown', e => {
          const step = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
          if (!step) return;
          const next = buttons[(i + step + buttons.length) % buttons.length];
          select(next); next.focus();
        });
      });
    });
  }

  /** Realisaties: filteren op type (particulier/project) en dienst. */
  function initRealisationFilter() {
    const mosaic = $('.mosaic'), bar = $('.fbar');
    if (!mosaic || !bar) return;
    const items = [...mosaic.children], count = $('.fcount', bar), empty = mosaic.nextElementSibling;
    let type = 'alle', cat = 'alle';
    const apply = () => {
      let n = 0;
      items.forEach(el => {
        const ok = (type === 'alle' || el.dataset.type === type) && (cat === 'alle' || el.dataset.cats.split(' ').includes(cat));
        el.hidden = !ok;
        if (ok) { n++; el.classList.add('in'); }
      });
      if (count) count.textContent = n + (n === 1 ? ' realisatie' : ' realisaties');
      empty.style.display = n ? 'none' : 'block';
    };
    const bind = (attr, set) => $$(`[data-${attr}]`, bar).forEach(btn => btn.addEventListener('click', () => {
      set(btn.dataset[attr]);
      $$(`[data-${attr}]`, bar).forEach(b => b.setAttribute('aria-pressed', b === btn));
      apply();
    }));
    bind('type', v => { type = v; });
    bind('cat', v => { cat = v; });
  }

  /** Blog: zoeken en filteren op onderwerp. */
  function initBlogFilter() {
    const grid = $('.bgrid');
    if (!grid) return;
    const input = $('.bsearch input'), chips = $$('.btool [data-topic]'), empty = grid.nextElementSibling;
    let topic = 'alle';
    const apply = () => {
      const q = input.value.trim().toLowerCase();
      let n = 0;
      [...grid.children].forEach(card => {
        const ok = (topic === 'alle' || card.dataset.topics.split(' ').includes(topic)) && (!q || card.dataset.search.includes(q));
        card.hidden = !ok;
        if (ok) { n++; card.classList.add('in'); }
      });
      empty.style.display = n ? 'none' : 'block';
    };
    input.addEventListener('input', apply);
    chips.forEach(btn => btn.addEventListener('click', () => {
      topic = btn.dataset.topic;
      chips.forEach(b => b.setAttribute('aria-pressed', b === btn));
      apply();
    }));
  }

  /** Blogartikel: leesvoortgang bovenaan en actief hoofdstuk in de inhoudstafel. */
  function initReadingProgress() {
    const bar = $('.progress span'), article = $('.art__body');
    if (!bar || !article) return;
    const links = $$('.toc a');
    const headings = links.map(a => $(a.getAttribute('href')));
    onScroll(() => {
      const r = article.getBoundingClientRect();
      bar.style.transform = `scaleX(${Math.max(0, Math.min(1, (innerHeight * 0.5 - r.top) / r.height))})`;
      let current = -1;
      headings.forEach((h, i) => { if (h && h.getBoundingClientRect().top < 160) current = i; });
      links.forEach((a, i) => a.classList.toggle('on', i === current));
    });
  }

  /* ---------- Formulieren ---------- */

  /**
   * Offerteformulier in stappen (.wiz). Elk veld met een name komt automatisch in de aanvraag.
   * - data-need op een groep keuzes: minstens één keuze verplicht (tekst = foutmelding)
   * - data-show-if="Veld=Waarde": blok enkel tonen bij die keuze
   * - data-subject / data-submit op .wiz: onderwerp van de mail / tekst van de laatste knop
   */
  function initWizards() {
    $$('.wiz').forEach(wiz => {
      const form = $('form', wiz), steps = $$('.wiz__step', wiz);
      const bar = $('.wiz__bar span', wiz), back = $('.wiz__back', wiz), next = $('.wiz__next', wiz), error = $('.wiz__err', wiz);
      let step = 0;
      const show = n => {
        step = n;
        steps.forEach((s, i) => s.classList.toggle('on', i === step));
        bar.style.width = ((step + 1) / steps.length * 100) + '%';
        back.hidden = step === 0;
        next.textContent = step === steps.length - 1 ? (wiz.dataset.submit || 'Verstuur aanvraag') : 'Volgende';
        error.textContent = '';
      };
      const valid = () => {
        for (const group of $$('[data-need]', steps[step])) {
          if (!$('input:checked', group)) { error.textContent = group.dataset.need; return false; }
        }
        for (const field of $$('[required]', steps[step])) {
          if (!field.closest('[hidden]') && !field.checkValidity()) { error.textContent = 'Vul de verplichte velden correct in.'; field.focus(); return false; }
        }
        return true;
      };
      form.addEventListener('change', () => $$('[data-show-if]', wiz).forEach(el => {
        const [name, value] = el.dataset.showIf.split('=');
        el.hidden = !$(`[name="${name}"][value="${value}"]:checked`, form);
      }));
      back.addEventListener('click', () => show(Math.max(0, step - 1)));
      next.addEventListener('click', () => {
        if (!valid()) return;
        if (step < steps.length - 1) { show(step + 1); $('input, textarea', steps[step])?.focus({ preventScroll: true }); return; }
        if (form.website?.value) return; // honeypot tegen spam
        const data = new FormData(form), lines = [], row = {};
        for (const [name, value] of data) {
          if (name === 'website' || name === 'privacy' || !String(value).trim()) continue;
          if ($(`[name="${name}"]`, form)?.closest('[hidden]')) continue;
          if (name in row) { lines[row[name]] += ', ' + value; continue; }
          row[name] = lines.push(`${name}: ${value}`) - 1;
        }
        const who = [data.get('Voornaam'), data.get('Achternaam')].filter(Boolean).join(' ') || data.get('Naam') || '';
        sendByMail(`${wiz.dataset.subject || 'Offerteaanvraag'} – ${who}`, lines.join('\n'));
        $('.wiz__body', wiz).hidden = true;
        $('.wiz__done', wiz).hidden = false;
      });
      show(0);
    });
  }

  /** Offerteformulieren: ingevulde gegevens bewaren tijdens het bezoek (bij herladen of terugkeren). */
  function initFormMemory() {
    $$('.lp-wiz form').forEach(form => {
      const key = 'sdad-offerte-' + location.pathname;
      const fields = () => $$('input, textarea', form).filter(el => el.name && el.name !== 'website');
      try {
        const saved = JSON.parse(sessionStorage.getItem(key) || '{}');
        fields().forEach(el => {
          const v = saved[el.name];
          if (v === undefined) return;
          if (el.type === 'checkbox' || el.type === 'radio') el.checked = Array.isArray(v) && v.includes(el.value);
          else el.value = v;
        });
        form.dispatchEvent(new Event('change'));
      } catch { /* opslag niet beschikbaar: geen probleem */ }
      const save = () => {
        try {
          const data = {};
          fields().forEach(el => {
            if (el.type === 'checkbox' || el.type === 'radio') { if (el.checked) (data[el.name] ||= []).push(el.value); }
            else data[el.name] = el.value;
          });
          sessionStorage.setItem(key, JSON.stringify(data));
        } catch { /* idem */ }
      };
      form.addEventListener('input', save);
      form.addEventListener('change', save);
    });
  }

  /** Terugbelformulier op de offertepagina's. */
  function initCallback() {
    $$('.callback').forEach(form => form.addEventListener('submit', e => {
      e.preventDefault();
      sendByMail('Graag terugbellen', `Gelieve mij terug te bellen op ${$('input[type=tel]', form).value}.`);
      $('.callback__ok', form).hidden = false;
    }));
  }

  /* ---------- Start ---------- */

  [initMobileMenu, initDropdown, initHeaderShadow, initReveal, initCounters, initHeroVideo, initProcessSteps,
    initLightbox, initCarousels, initSubnav, initTabs, initRealisationFilter, initBlogFilter, initReadingProgress,
    initWizards, initFormMemory, initCallback].forEach(init => init());
})();
