// CX Institute SA – shared site scripts (menu, year, enquiry form)
(function () {
    var t = document.querySelector('.nav-toggle'), n = document.getElementById('nav');
    t.addEventListener('click', function () {
      var o = n.classList.toggle('open');
      t.setAttribute('aria-expanded', o ? 'true' : 'false');
    });
    n.addEventListener('click', function (e) {
      if (e.target.closest('a')) { n.classList.remove('open'); t.setAttribute('aria-expanded', 'false'); }
    });
    var yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();
  })();

  (function () {
    var form = document.getElementById('enquire-form');
    if (!form) return;
    var started = Date.now();
    var status = form.querySelector('.form-status');
    var btn = form.querySelector('button[type=submit]');
    var fallback = 'Please email <a href="mailto:lynn@cx-company.com">lynn@cx-company.com</a> or call +27 82 457 5752.';

    function pick(v) {
      var r = form.querySelector('input[name=interest][value="' + v + '"]');
      if (r) r.checked = true;
    }
    if (form.getAttribute('data-default-interest')) pick(form.getAttribute('data-default-interest'));
    document.querySelectorAll('a[data-interest]').forEach(function (a) {
      a.addEventListener('click', function () { pick(a.getAttribute('data-interest')); });
    });

    function show(kind, html) {
      status.className = 'form-status ' + kind;
      status.innerHTML = html;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.querySelectorAll('.invalid').forEach(function (el) { el.classList.remove('invalid'); });
      var fd = new FormData(form);
      var data = {};
      fd.forEach(function (v, k) { data[k] = String(v).trim(); });
      data.elapsed = Date.now() - started;

      var bad = [];
      if (!data.interest) bad.push('interest');
      if ((data.name || '').length < 2) bad.push('name');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email || '')) bad.push('email');
      if ((data.company || '').length < 2) bad.push('company');
      if ((data.message || '').length < 10) bad.push('message');
      if (bad.length) { mark(bad); return; }

      btn.disabled = true;
      btn.textContent = 'Sending…';
      show('', '');
      fetch('/api/enquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (r) {
        return r.json().catch(function () { return { ok: false }; }).then(function (j) { return { status: r.status, body: j }; });
      }).then(function (res) {
        if (res.body && res.body.ok) {
          form.reset();
          show('ok', '<b>Thank you – your enquiry has been sent.</b> Lynn will be in touch shortly.');
        } else if (res.body && res.body.error === 'invalid') {
          mark(res.body.fields || []);
        } else {
          show('err', '<b>Sorry, your enquiry could not be sent just now.</b> ' + fallback);
        }
      }).catch(function () {
        show('err', '<b>Sorry, your enquiry could not be sent just now.</b> ' + fallback);
      }).then(function () {
        btn.disabled = false;
        btn.textContent = 'Send enquiry';
      });
    });

    function mark(fields) {
      fields.forEach(function (n) {
        var el = n === 'interest' ? form.querySelector('.interest') : form.querySelector('[name=' + n + ']');
        if (el) (n === 'interest' ? el : el.closest('.field')).classList.add('invalid');
      });
      show('err', 'Please complete the highlighted fields.');
      var first = form.querySelector('.invalid input, .invalid textarea, .interest.invalid input');
      if (first) first.focus();
    }
  })();

// Showreel: load YouTube only when the visitor clicks play
(function () {
  document.querySelectorAll('.video[data-youtube]').forEach(function (box) {
    var btn = box.querySelector('.video-play');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + box.getAttribute('data-youtube') + '?autoplay=1&rel=0';
      f.title = 'Lynn Baker showreel';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      box.innerHTML = '';
      box.appendChild(f);
    });
  });
})();
