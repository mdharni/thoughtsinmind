/* Thoughts in Mind — shared behavior */
(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  var links = document.querySelector('.nav-links');
  if (btn && links) {
    btn.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Mail forms (contact + volunteer).
  // If data-key is set, the message is delivered through Web3Forms straight to the inbox.
  // Otherwise it falls back to opening the visitor's email app, and always shows the composed message on the page.
  var TO = 'thoughtsinmind2@gmail.com';
  Array.prototype.forEach.call(document.querySelectorAll('form[data-mail]'), function (form) {
    var status = form.querySelector('.form-status');
    var panel = form.querySelector('.sent-panel');
    var sentText = form.querySelector('.sent-text');
    var mailLink = form.querySelector('.mail-link');
    var copyBtn = form.querySelector('.copy-btn');

    function labelFor(el) {
      var l = el.id && form.querySelector('label[for="' + el.id + '"]');
      if (!l) { var fs = el.closest('fieldset'); l = fs && fs.querySelector('legend'); }
      if (!l) return el.name;
      var c = l.cloneNode(true); Array.prototype.forEach.call(c.querySelectorAll('.hint'), function (h) { h.remove(); });
      return c.textContent.trim().replace(/\s+/g, ' ');
    }
    function compose(d) {
      var subject = (form.dataset.subject || 'Message from thoughtsinmind.org').replace(/\{(\w+)\}/g, function (_, k) { return d.get(k) || ''; }).replace(/\s+/g, ' ').trim();
      var lines = [], seen = {}, msg = '';
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || seen[el.name] || el.type === 'submit' || el.type === 'button') return;
        seen[el.name] = true;
        var v = d.get(el.name);
        if (el.name === 'message') { msg = v || ''; return; }
        lines.push(labelFor(el) + ': ' + (v || '\u2014'));
      });
      return { subject: subject, body: lines.join('\n') + (msg ? '\n\n' + msg : '') };
    }
    function mailto(msg) { return 'mailto:' + TO + '?subject=' + encodeURIComponent(msg.subject) + '&body=' + encodeURIComponent(msg.body); }
    function showFallback(msg) {
      sentText.textContent = 'To: ' + TO + '\nSubject: ' + msg.subject + '\n\n' + msg.body;
      mailLink.href = mailto(msg);
      panel.hidden = false;
      status.textContent = 'Message prepared below.';
      panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var msg = compose(d);
      var btn = form.querySelector('button[type="submit"]');
      var endpoint = form.dataset.endpoint, key = form.dataset.key;

      if (endpoint && key) {
        btn.disabled = true; status.textContent = 'Sending\u2026';
        var payload = { access_key: key, subject: msg.subject, from_name: d.get('name'), replyto: d.get('email'), message: msg.body };
        fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(payload) })
          .then(function (r) { return r.json(); })
          .then(function (r) {
            if (r && r.success) {
              form.reset(); btn.disabled = false;
              status.textContent = 'Thank you. Your message has been sent, and we will reply to ' + payload.replyto + ' soon.';
              panel.hidden = true;
            } else { throw new Error('send failed'); }
          })
          .catch(function () { btn.disabled = false; showFallback(msg); status.textContent = 'We could not send this automatically. Please use one of the options below.'; });
        return;
      }
      showFallback(msg);
      try { window.location.href = mailto(msg); } catch (err) {}
    });

    if (copyBtn) copyBtn.addEventListener('click', function () {
      var t = sentText.textContent;
      function done() { copyBtn.textContent = 'Copied'; setTimeout(function () { copyBtn.textContent = 'Copy message'; }, 2000); }
      function fallbackCopy() { var ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (err) {} document.body.removeChild(ta); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, function () { fallbackCopy(); done(); });
      else { fallbackCopy(); done(); }
    });
  });

  // Home hero: a slowly drifting "constellation" — nodes connecting and reconnecting, like memory.
  var canvas = document.getElementById('constellation');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var W, H, nodes = [], N = 46, raf;

  function colors() {
    var cs = getComputedStyle(document.documentElement);
    return { plum: cs.getPropertyValue('--plum').trim(), gold: cs.getPropertyValue('--marigold').trim(), sage: cs.getPropertyValue('--sage').trim() };
  }
  function resize() {
    var r = canvas.getBoundingClientRect();
    W = r.width; H = r.height;
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!nodes.length) seed();
    if (reduce) draw(0);
  }
  function seed() {
    nodes = [];
    for (var i = 0; i < N; i++) {
      var a = Math.random() * Math.PI * 2, rr = Math.sqrt(Math.random()) * 0.42;
      nodes.push({ x: 0.5 + Math.cos(a) * rr, y: 0.5 + Math.sin(a) * rr, vx: (Math.random() - .5) * .0006, vy: (Math.random() - .5) * .0006, r: 2 + Math.random() * 3.2, k: i % 7 === 0 ? 'gold' : (i % 5 === 0 ? 'sage' : 'plum'), ph: Math.random() * Math.PI * 2 });
    }
  }
  function hex2rgba(hex, a) {
    hex = hex.replace('#', ''); if (hex.length === 3) hex = hex.split('').map(function (c) { return c + c; }).join('');
    var n = parseInt(hex, 16); return 'rgba(' + (n >> 16 & 255) + ',' + (n >> 8 & 255) + ',' + (n & 255) + ',' + a + ')';
  }
  function draw(t) {
    var c = colors();
    ctx.clearRect(0, 0, W, H);
    var cx = W / 2, cy = H / 2, R = Math.min(W, H) * 0.47;
    for (var i = 0; i < nodes.length; i++) {
      var p = nodes[i];
      if (!reduce) {
        p.x += p.vx; p.y += p.vy;
        var dx = p.x - .5, dy = p.y - .5, d = Math.sqrt(dx * dx + dy * dy);
        if (d > .44) { p.vx -= dx * .00004; p.vy -= dy * .00004; }
      }
    }
    // links
    for (i = 0; i < nodes.length; i++) {
      for (var j = i + 1; j < nodes.length; j++) {
        var a = nodes[i], b = nodes[j];
        var ddx = (a.x - b.x) * W, ddy = (a.y - b.y) * H, dist = Math.sqrt(ddx * ddx + ddy * ddy);
        var lim = R * .42;
        if (dist < lim) {
          var alpha = (1 - dist / lim) * .55;
          ctx.strokeStyle = hex2rgba(c.plum, alpha);
          ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(a.x * W, a.y * H); ctx.lineTo(b.x * W, b.y * H); ctx.stroke();
        }
      }
    }
    // nodes
    for (i = 0; i < nodes.length; i++) {
      p = nodes[i];
      var pulse = reduce ? 1 : (1 + Math.sin(t * .0012 + p.ph) * .18);
      var col = p.k === 'gold' ? c.gold : (p.k === 'sage' ? c.sage : c.plum);
      ctx.fillStyle = hex2rgba(col, .18);
      ctx.beginPath(); ctx.arc(p.x * W, p.y * H, p.r * 3 * pulse, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = col;
      ctx.beginPath(); ctx.arc(p.x * W, p.y * H, p.r * pulse, 0, Math.PI * 2); ctx.fill();
    }
    if (!reduce) raf = requestAnimationFrame(draw);
  }
  resize();
  window.addEventListener('resize', function () { resize(); });
  if (!reduce) raf = requestAnimationFrame(draw);
  document.addEventListener('visibilitychange', function () {
    if (reduce) return;
    if (document.hidden) cancelAnimationFrame(raf); else raf = requestAnimationFrame(draw);
  });
})();
