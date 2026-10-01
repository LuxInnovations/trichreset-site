/* Site D — Headspace.
   Three small things only: the audio player, the FAQ accordion, the sticky-nav
   hairline. No dependencies, no build step. */

(function () {
  'use strict';

  /* ------------------------------------------------------------ year */
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ------------------------------------------------- sticky nav hairline */
  var nav = document.getElementById('nav');
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('is-stuck', window.scrollY > 8);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ----------------------------------------------------------- FAQ */
  document.querySelectorAll('.qa button').forEach(function (btn) {
    var panel = btn.parentElement.nextElementSibling;
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      panel.classList.toggle('is-open', !open);
    });
  });

  /* ------------------------------------------------- elastic gallery
     Hover expands a panel on pointer devices; click/Enter sets it as the
     active panel too, so touch and keyboard get the same result. */
  var elastic = document.getElementById('elastic');
  if (elastic) {
    var panels = elastic.querySelectorAll('[data-panel]');
    var activate = function (panel) {
      panels.forEach(function (p) { p.classList.toggle('is-active', p === panel); });
    };
    panels.forEach(function (panel) {
      panel.addEventListener('mouseenter', function () { activate(panel); });
      panel.addEventListener('click', function () { activate(panel); });
      panel.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(panel); }
      });
    });
  }

  /* --------------------------------------------------------- the player
     The mp3 ships at ~10 MB, so preload="none" and the file is only fetched
     on the first press. Everything below assumes it may not be loaded yet. */
  var audio  = document.getElementById('audio');
  var btn    = document.getElementById('playBtn');
  var scrub  = document.getElementById('scrub');
  var tCur   = document.getElementById('tCur');
  var tDur   = document.getElementById('tDur');
  var hint   = document.getElementById('playerHint');
  if (!audio || !btn) return;

  var seeking = false;

  function fmt(s) {
    if (!isFinite(s) || s < 0) return '—:—';
    var m = Math.floor(s / 60);
    var r = Math.floor(s % 60);
    return m + ':' + (r < 10 ? '0' : '') + r;
  }

  btn.addEventListener('click', function () {
    if (audio.paused) {
      hint.textContent = 'Loading…';
      var p = audio.play();
      if (p && p.catch) {
        p.catch(function () {
          hint.textContent = 'That didn’t start. Try again, or hear it in the app.';
          btn.classList.remove('is-playing');
        });
      }
    } else {
      audio.pause();
    }
  });

  audio.addEventListener('play', function () {
    btn.classList.add('is-playing');
    btn.setAttribute('aria-label', 'Pause the meditation Right now');
    hint.textContent = 'Playing — Right now.';
  });

  audio.addEventListener('pause', function () {
    btn.classList.remove('is-playing');
    btn.setAttribute('aria-label', 'Play the meditation Right now');
    if (!audio.ended) hint.textContent = 'Paused.';
  });

  audio.addEventListener('ended', function () {
    btn.classList.remove('is-playing');
    btn.setAttribute('aria-label', 'Play the meditation Right now');
    scrub.value = 0;
    tCur.textContent = '0:00';
    hint.textContent = 'That was one of eight. The rest are in the app.';
  });

  audio.addEventListener('loadedmetadata', function () {
    tDur.textContent = fmt(audio.duration);
  });

  audio.addEventListener('timeupdate', function () {
    if (seeking || !audio.duration) return;
    scrub.value = String(Math.round((audio.currentTime / audio.duration) * 1000));
    tCur.textContent = fmt(audio.currentTime);
  });

  audio.addEventListener('error', function () {
    hint.textContent = 'The audio couldn’t load here. It’s in the app.';
    btn.classList.remove('is-playing');
  });

  scrub.addEventListener('input', function () {
    seeking = true;
    if (audio.duration) tCur.textContent = fmt((scrub.value / 1000) * audio.duration);
  });

  scrub.addEventListener('change', function () {
    if (audio.duration) audio.currentTime = (scrub.value / 1000) * audio.duration;
    seeking = false;
  });
})();
