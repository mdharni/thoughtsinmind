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

  // Contact form → opens the visitor's email client with a pre-filled message
  var form = document.getElementById('inquiry');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var subject = 'Workshop inquiry from ' + (d.get('facility') || d.get('name') || 'your website');
      var body = [
        'Name: ' + d.get('name'),
        'Role: ' + d.get('role'),
        'Facility / community: ' + d.get('facility'),
        'Email: ' + d.get('email'),
        'Phone: ' + (d.get('phone') || '—'),
        'Approximate number of residents: ' + (d.get('residents') || '—'),
        '',
        d.get('message')
      ].join('\n');
      window.location.href = 'mailto:thoughtsinmind2@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var note = document.getElementById('form-status');
      if (note) note.textContent = 'Your email app should open with the message ready to send. If it does not, email us directly at thoughtsinmind2@gmail.com.';
    });
  }

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
