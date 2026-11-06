/* Site D — Headspace.
   Three small things only: the audio player, the FAQ accordion, the sticky-nav
   hairline. No dependencies, no build step. */

(function () {
  'use strict';

  /* ------------------------------------------------------------ year */
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ------------------------------------------------- store links
     There is no iPhone app yet, so on iPhone and iPad a Play link is a dead end.
     Those buttons open the iPhone list form below. The nav button goes to
     the free meditation, which does play on iPhone. */
  var ua = navigator.userAgent || '';
  var isIOS = /iPhone|iPad|iPod/.test(ua) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var playLinks = document.querySelectorAll('a[href*="play.google.com/store/apps"]');
  var IOS_LIST = 'mailto:trichreset@gmail.com?subject=iPhone%20list&body=Please%20email%20me%20when%20Trich%20Reset%20is%20on%20iPhone.';

  /* ------------------------------------------------- iPhone list form
     Writes to the insert-only ios_waitlist table. The anon key is public by
     design (the app ships it too); row-level security is what protects the list.
     Whatever goes wrong, the person gets the mailto link instead. */
  var SUPABASE_URL = 'https://crphixuxwfecypcukxia.supabase.co';
  var SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNycGhpeHV4d2ZlY3lwY3VreGlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1MTE4MjYsImV4cCI6MjA5NTA4NzgyNn0.ssaSEYksU4KGAzIC9rlIAF-gQWDPBCzl63uUPEbPMUQ';
  var LIST_LABEL = 'Tell me when it\u2019s on iPhone';
  var formCount = 0;

  function listSource() {
    var src = (new URLSearchParams(location.search).get('utm_source') || '').toLowerCase();
    return /^[a-z0-9_.-]{1,40}$/.test(src) ? src : null;
  }

  function buildListForm(buttonClass) {
    var id = 'iphone-email-' + (++formCount);
    var form = document.createElement('form');
    form.className = 'waitlist';
    form.noValidate = true;

    var label = document.createElement('label');
    label.htmlFor = id;
    label.textContent = 'Your email';

    var input = document.createElement('input');
    input.id = id;
    input.type = 'email';
    input.name = 'email';
    input.required = true;
    input.maxLength = 254;
    input.autocomplete = 'email';
    input.setAttribute('autocapitalize', 'off');
    input.setAttribute('autocorrect', 'off');
    input.spellcheck = false;

    /* Hidden from people. A bot that fills it gets a success message and nothing is sent. */
    var trap = document.createElement('input');
    trap.className = 'waitlist-trap';
    trap.type = 'text';
    trap.name = 'website';
    trap.tabIndex = -1;
    trap.autocomplete = 'off';
    trap.setAttribute('aria-hidden', 'true');

    var button = document.createElement('button');
    button.type = 'submit';
    button.className = buttonClass;
    button.textContent = LIST_LABEL;

    var fine = document.createElement('p');
    fine.className = 'waitlist-fine';
    fine.append('One email when it\u2019s ready, then we delete your address. ');
    var privacy = document.createElement('a');
    privacy.href = '/privacy';
    privacy.textContent = 'Privacy';
    fine.append(privacy);

    var msg = document.createElement('p');
    msg.className = 'waitlist-msg';
    msg.setAttribute('role', 'status');

    form.append(label, input, trap, button, fine, msg);

    function joined() {
      var done = document.createElement('p');
      done.className = 'waitlist-done';
      done.setAttribute('role', 'status');
      done.tabIndex = -1;
      done.textContent = 'You\u2019re on the list. We\u2019ll email you once, when it\u2019s on iPhone.';
      form.replaceWith(done);
      done.focus();
    }

    function failed() {
      button.disabled = false;
      button.textContent = LIST_LABEL;
      msg.textContent = 'That didn\u2019t go through. ';
      var mail = document.createElement('a');
      mail.href = IOS_LIST;
      mail.textContent = 'Email us instead';
      msg.append(mail, ' and we\u2019ll add you.');
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (button.disabled) return;
      if (trap.value) { joined(); return; }

      var email = input.value.trim();
      if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        msg.textContent = 'That email doesn\u2019t look right. Check it and try again.';
        input.focus();
        return;
      }

      msg.textContent = '';
      button.disabled = true;
      button.textContent = 'Sending\u2026';

      var controller = new AbortController();
      var timer = setTimeout(function () { controller.abort(); }, 10000);
      fetch(SUPABASE_URL + '/rest/v1/ios_waitlist', {
        method: 'POST',
        headers: {
          apikey: SUPABASE_ANON_KEY,
          Authorization: 'Bearer ' + SUPABASE_ANON_KEY,
          'Content-Type': 'application/json',
          Prefer: 'return=minimal'
        },
        body: JSON.stringify({ email: email, source: listSource() }),
        signal: controller.signal
      }).then(function (res) {
        /* 409 is two people sending one address in the same instant: they're on the list. */
        if (res.ok || res.status === 409) joined(); else failed();
      }).catch(failed).then(function () {
        clearTimeout(timer);
      });
    });

    return { form: form, input: input };
  }

  /* Swaps a button for the form, or adds the form under a link in a sentence.
     Until then the link's own mailto works, so a script failure loses nobody. */
  function wireListLink(a) {
    a.href = IOS_LIST;
    if (!window.fetch || !window.AbortController) return;
    var isButton = a.classList.contains('btn');
    var built = null;
    a.addEventListener('click', function (e) {
      e.preventDefault();
      if (!built) {
        var buttonClass = isButton ? a.className.replace(/\bbtn-(ghost|lg)\b/g, '').trim() : 'btn btn-primary';
        if (a.classList.contains('btn-ghost')) buttonClass += ' btn-primary';
        built = buildListForm(buttonClass.replace(/\s+/g, ' '));
        if (isButton) a.replaceWith(built.form);
        else a.closest('p').after(built.form);
      }
      built.input.focus();
    });
  }

  document.querySelectorAll('a[data-iphone-list]').forEach(wireListLink);

  if (isIOS) {
    document.querySelectorAll('[data-ios-text]').forEach(function (el) {
      el.textContent = el.getAttribute('data-ios-text');
    });
    playLinks.forEach(function (a) {
      if (a.classList.contains('nav-cta')) {
        a.href = document.getElementById('listen') ? '#listen' : '/#listen';
        a.textContent = 'Hear one free';
      } else {
        a.textContent = LIST_LABEL;
        wireListLink(a);
      }
    });
  } else {
    /* trichreset.com/?utm_source=instagram carries through to Play, so Play Console's
       acquisition report can tell Instagram from TikTok. */
    var src = new URLSearchParams(location.search).get('utm_source');
    if (src) {
      playLinks.forEach(function (a) {
        var u = new URL(a.href);
        u.searchParams.set('utm_source', src);
        u.searchParams.set('utm_medium', 'social');
        a.href = u.toString();
      });
    }
  }

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
    btn.setAttribute('aria-label', 'Pause the meditation Boredom and the Body');
    hint.textContent = 'Playing: Boredom and the Body.';
  });

  audio.addEventListener('pause', function () {
    btn.classList.remove('is-playing');
    btn.setAttribute('aria-label', 'Play the meditation Boredom and the Body');
    if (!audio.ended) hint.textContent = 'Paused.';
  });

  audio.addEventListener('ended', function () {
    btn.classList.remove('is-playing');
    btn.setAttribute('aria-label', 'Play the meditation Boredom and the Body');
    scrub.value = 0;
    tCur.textContent = '0:00';
    hint.textContent = isIOS ? 'That was one. The rest are in the app, coming soon to iPhone.' : 'That was one. The rest are in the app, 7 days free.';
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
