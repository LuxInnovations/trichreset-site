/* Card fan for the "Inside the app" screens.
   Vanilla port of the 21st.dev card-fan-carousel (React + GSAP): same fan
   positions, easing and hover push. Builds itself from the .screens list, so
   without GSAP or with reduced motion the plain scroll strip stays. */

(function () {
  'use strict';

  var list = document.querySelector('#screens .screens');
  if (!list || !window.gsap) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var gsap = window.gsap;

  var MAX_VISIBLE = 7, HALF = 3;
  var FAN = [
    { rot: -21, scale: 0.7756, x: -30, y: 7.3, z: 1 },
    { rot: -14, scale: 0.8498, x: -22, y: 4.0, z: 2 },
    { rot: -7,  scale: 0.9346, x: -11, y: 1.3, z: 3 },
    { rot: 0,   scale: 1.0,    x: 0,   y: 0.0, z: 10 },
    { rot: 7,   scale: 0.9346, x: 11,  y: 1.3, z: 3 },
    { rot: 14,  scale: 0.8498, x: 22,  y: 4.0, z: 2 },
    { rot: 21,  scale: 0.7756, x: 30,  y: 7.3, z: 1 }
  ];

  function widthMult() {
    var w = window.innerWidth;
    if (w < 480) return 0.28;
    if (w < 640) return 0.38;
    if (w < 768) return 0.5;
    if (w < 1024) return 0.75;
    return 1;
  }

  /* Shrinks y-offsets when the viewport is shorter than the ideal layout. */
  function heightMult() {
    var w = window.innerWidth, ideal;
    if (w < 480) ideal = 22 * 16;
    else if (w < 640) ideal = 26 * 16;
    else if (w < 768) ideal = 28 * 16;
    else if (w < 1024) ideal = 34 * 16;
    else ideal = 38 * 16;
    var avail = window.innerHeight * 0.7;
    return avail >= ideal ? 1 : avail / ideal;
  }

  /* The original only shrinks y on short viewports, so on phones the outer
     cards dropped into the arrow row. Scale the drop with width too. */
  function yMult() { return heightMult() * Math.max(widthMult(), 0.5); }

  /* ------------------------------------------- build from the existing list */
  var items = Array.prototype.slice.call(list.children);
  var total = items.length;
  if (!total) return;
  var paged = total > MAX_VISIBLE;
  var slotCount = paged ? MAX_VISIBLE : total;

  function slotConfig(slot) {
    if (slotCount >= MAX_VISIBLE) return FAN[slot];
    var c = slotCount >> 1;
    var d = slotCount > 1 ? (slot - c) / c : 0, a = Math.abs(d);
    return { rot: d * 21, scale: 1 - 0.2244 * a * a, x: d * 30, y: a * a * 7.3, z: 10 - Math.abs(slot - c) };
  }

  var wrap = document.createElement('div');
  wrap.className = 'fan';
  var layout = document.createElement('div');
  layout.className = 'fan-layout';
  layout.tabIndex = 0;
  layout.setAttribute('role', 'group');
  layout.setAttribute('aria-roledescription', 'carousel');
  layout.setAttribute('aria-label', 'Screens from the Trich Reset app.' +
    (paged ? ' Use the arrow keys or buttons to see more.' : ''));
  wrap.appendChild(layout);

  var cards = items.map(function (li) {
    var card = document.createElement('div');
    card.className = 'fan-card';
    while (li.firstChild) card.appendChild(li.firstChild);
    var img = card.querySelector('img');
    if (img) img.loading = 'eager';
    layout.appendChild(card);
    return card;
  });

  var dots = [];
  if (paged) {
    var controls = document.createElement('div');
    controls.className = 'fan-controls';
    var arrow = function (dir) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'fan-arrow';
      b.setAttribute('aria-label', dir === 'left' ? 'Previous screen' : 'Next screen');
      b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="' +
        (dir === 'left' ? '15 18 9 12 15 6' : '9 18 15 12 9 6') + '"/></svg>';
      b.addEventListener('click', function () { cycle(dir); });
      return b;
    };
    var dotRow = document.createElement('div');
    dotRow.className = 'fan-dots';
    dotRow.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < total; i++) dots.push(dotRow.appendChild(document.createElement('span')));
    controls.appendChild(arrow('left'));
    controls.appendChild(dotRow);
    controls.appendChild(arrow('right'));
    wrap.appendChild(controls);
  }

  list.parentNode.replaceChild(wrap, list);

  /* ------------------------------------------------------------- state */
  var center = paged ? HALF : total >> 1;
  var animating = false, entered = false, dir = null;
  var prevVisible = {};
  var visible = [];            // [{ el, slot }] sorted by slot
  var activeSlot = null, leaveTimer = null;

  function visibleMap(c) {
    var m = {};
    if (!paged) { for (var i = 0; i < total; i++) m[i] = i; return m; }
    for (var s = 0; s < MAX_VISIBLE; s++) m[((c + s - HALF) % total + total) % total] = s;
    return m;
  }

  function render() {
    var map = visibleMap(center);
    var first = !entered;
    var wm = widthMult(), hm = yMult();
    var done = 0, count = Object.keys(map).length;
    var onDone = function () {
      if (++done >= count) { animating = false; if (first) entered = true; }
    };
    animating = true;

    cards.forEach(function (card, i) {
      var slot = map[i];
      var was = !!prevVisible[i];
      card.setAttribute('aria-hidden', slot === undefined ? 'true' : 'false');
      if (slot !== undefined) {
        var c = slotConfig(slot);
        var target = { x: c.x * wm + 'rem', y: c.y * hm + 'rem', rotation: c.rot, scale: c.scale, opacity: 1, zIndex: c.z };
        if (first) {
          gsap.set(card, { x: 0, y: 12 * hm + 'rem', rotation: 0, scale: 0.5, opacity: 0 });
          gsap.to(card, Object.assign({}, target, { duration: 1.2, ease: 'elastic.out(1.05,.78)', delay: 0.2 + slot * 0.06, onComplete: onDone }));
        } else if (!was) {
          gsap.set(card, { x: (dir === 'right' ? 40 : -40) + 'rem', y: c.y * hm + 'rem', rotation: dir === 'right' ? 30 : -30, scale: 0.5, opacity: 0 });
          gsap.to(card, Object.assign({}, target, { duration: 0.6, ease: 'power2.out', onComplete: onDone }));
        } else {
          gsap.to(card, Object.assign({}, target, { duration: 0.5, ease: 'power2.out', onComplete: onDone }));
        }
      } else if (was) {
        gsap.to(card, { x: (dir === 'right' ? -40 : 40) + 'rem', opacity: 0, scale: 0.5, rotation: dir === 'right' ? -30 : 30, duration: 0.4, ease: 'power2.in', zIndex: 0 });
      } else if (first) {
        gsap.set(card, { opacity: 0, scale: 0.3, x: 0, y: 0, zIndex: 0 });
      }
    });

    prevVisible = map;
    visible = cards.map(function (el, i) { return { el: el, slot: map[i] }; })
      .filter(function (e) { return e.slot !== undefined; })
      .sort(function (a, b) { return a.slot - b.slot; });
    activeSlot = null;
    dots.forEach(function (d, i) { d.classList.toggle('is-active', i === center); });
  }

  function hoverLayout(hovered) {
    var wm = widthMult(), hm = yMult();
    var mid = visible.length >> 1;
    visible.forEach(function (e) {
      var b = slotConfig(e.slot);
      var x = b.x * wm, y = b.y * hm, rot = b.rot, scale = b.scale, delay;
      if (hovered !== null) {
        var dist = Math.abs(e.slot - hovered);
        delay = dist * 0.02;
        if (e.slot === hovered) { y -= 2.5 * hm; scale *= 1.08; }
        else {
          var n = mid > 0 ? (e.slot - mid) / mid : 0;
          var push = 8 * (1 - Math.abs(n)) * (1 + 0.2 * Math.max(0, 3 - dist));
          if (e.slot < hovered) { x -= push * wm; rot -= 3 / (dist + 1); }
          else { x += push * wm; rot += 3 / (dist + 1); }
          if (e.slot === visible.length - 1 && hovered < mid) y -= hm;
          if (e.slot === 0 && hovered > mid) y -= hm;
        }
      } else {
        delay = Math.abs(e.slot - mid) * 0.02;
      }
      gsap.to(e.el, { x: x + 'rem', y: y + 'rem', rotation: rot, scale: scale, duration: 0.5, delay: delay, ease: 'elastic.out(1,.75)', overwrite: 'auto' });
      gsap.set(e.el, { zIndex: b.z });
    });
  }

  function cycle(direction) {
    if (animating || !paged) return;
    dir = direction;
    center = direction === 'right' ? (center + 1) % total : (center - 1 + total) % total;
    render();
  }

  /* ------------------------------------------------------ interactions
     Hover push for mouse, arrow keys for keyboard, swipe for touch. */
  cards.forEach(function (card) {
    card.addEventListener('mouseenter', function () {
      if (animating) return;
      var e = visible.find(function (v) { return v.el === card; });
      if (!e) return;
      if (leaveTimer) { clearTimeout(leaveTimer); leaveTimer = null; }
      if (activeSlot !== e.slot) { activeSlot = e.slot; hoverLayout(e.slot); }
    });
  });
  layout.addEventListener('mouseleave', function () {
    if (animating) return;
    if (leaveTimer) clearTimeout(leaveTimer);
    leaveTimer = setTimeout(function () { activeSlot = null; hoverLayout(null); }, 50);
  });
  window.addEventListener('resize', function () { if (!animating) hoverLayout(activeSlot); });

  layout.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); cycle('left'); }
    if (e.key === 'ArrowRight') { e.preventDefault(); cycle('right'); }
  });

  var startX = null;
  layout.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
  layout.addEventListener('touchend', function (e) {
    if (startX === null) return;
    var dx = e.changedTouches[0].clientX - startX;
    startX = null;
    if (Math.abs(dx) > 40) cycle(dx < 0 ? 'right' : 'left');
  });

  /* ------------------- play the entry animation when it scrolls into view */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { io.disconnect(); render(); }
    }, { threshold: 0.25 });
    io.observe(layout);
  } else {
    render();
  }
})();
