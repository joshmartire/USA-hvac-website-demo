/* HVAC Template — interactions & animation (no dependencies) */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) doc.classList.add("reduced");

  /* Match the layout offset to the demo banner's real height (it can wrap on small screens). */
  var demo = document.querySelector(".demo-bar");
  if (demo) {
    var setDemo = function () { doc.style.setProperty("--demo-h", demo.offsetHeight + "px"); };
    setDemo(); window.addEventListener("resize", setDemo);
  }

  /* ---------- Split headline words ---------- */
  document.querySelectorAll("[data-split]").forEach(function (el) {
    var i = 0;
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var parts = child.textContent.split(/(\s+)/);
          var frag = document.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(" ")); return; }
            var w = document.createElement("span"); w.className = "w";
            var inner = document.createElement("span"); inner.textContent = p;
            w.style.setProperty("--wi", i++);
            w.appendChild(inner); frag.appendChild(w);
          });
          child.parentNode.replaceChild(frag, child);
        } else if (child.nodeType === 1) { walk(child); }
      });
    };
    walk(el);
    el.classList.add("split");
  });

  /* ---------- Opening animation ----------
     The overlay is in the HTML of every indexable page and is visible from the first paint unless the inline
     head script added "no-intro" (already played this session, #hash in the URL, reduced motion).
     It plays once per browser session on whichever page the visitor lands on first, then is removed.
     A tap, click or key press skips it. */
  var ready = function () { doc.classList.add("is-ready"); };
  var intro = document.querySelector(".intro");
  var playing = intro && !doc.classList.contains("no-intro") && getComputedStyle(intro).display !== "none";
  if (playing) {
    try { sessionStorage.setItem("hv-intro", "1"); } catch (e) {}
    doc.classList.add("intro-on");
    var count = intro.querySelector(".intro__count");
    var start = performance.now(), dur = 1900, finished = false;
    var finish = function () {
      if (finished) return; finished = true;
      intro.classList.add("is-done");
      setTimeout(ready, 380);
      setTimeout(function () {
        doc.classList.remove("intro-on"); doc.classList.add("intro-done");
        if (intro.parentNode) intro.parentNode.removeChild(intro);
      }, 1250);
    };
    var tick = function (now) {
      if (finished) return;
      var t = Math.min(1, (now - start) / dur);
      var e = 1 - Math.pow(1 - t, 3);
      intro.style.setProperty("--t", e.toFixed(3));
      if (count) {
        var from = parseFloat(count.getAttribute("data-from")), to = parseFloat(count.getAttribute("data-to"));
        var v = from + (to - from) * e;
        count.textContent = (v < 10 ? "0" : "") + v.toFixed(1);
      }
      if (t < 1) requestAnimationFrame(tick); else setTimeout(finish, 180);
    };
    requestAnimationFrame(tick);
    var skip = function () { finish(); window.removeEventListener("pointerdown", skip); window.removeEventListener("keydown", skip); };
    window.addEventListener("pointerdown", skip); window.addEventListener("keydown", skip);
  } else {
    if (intro && intro.parentNode) intro.parentNode.removeChild(intro);
    requestAnimationFrame(function () { requestAnimationFrame(ready); });
  }

  /* ---------- Hero airflow: canvas streamlines, cool on the left warming to heat on the right ----------
     Drawn after first paint, paused off screen and in background tabs, a single still frame for reduced motion,
     fewer particles on phones. The pointer bends the flow nearby. */
  (function () {   /* own scope: keeps its helper names away from the rest of this file */
  var cv = document.querySelector(".hero__fx");
  if (cv && cv.getContext) {
    var ctx = cv.getContext("2d"), W = 0, H = 0, DPR = Math.min(window.devicePixelRatio || 1, 1.5), parts = [], run = false, visible = true, mouse = { x: -9999, y: -9999 };
    var css = getComputedStyle(doc), hex = function (h, d) { h = (h || d).trim().replace("#", ""); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; };
    var C1 = hex(css.getPropertyValue("--accent"), "#3cb4ff"), C2 = hex(css.getPropertyValue("--heat"), "#ff6a2b");
    var N = window.innerWidth < 760 ? 70 : 180;
    var size = function () {
      var r = cv.getBoundingClientRect(); W = r.width; H = r.height;
      cv.width = Math.round(W * DPR); cv.height = Math.round(H * DPR); ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    };
    var spawn = function (p, anywhere) {
      p.x = anywhere ? Math.random() * W : -20; p.y = Math.random() * H; p.v = 0.6 + Math.random() * 1.6; p.l = 0; p.max = 220 + Math.random() * 380; p.w = 0.8 + Math.random() * 1.6; p.px = p.x; p.py = p.y; return p;
    };
    var field = function (x, y, t) {   /* gentle, layered sine flow: mostly left-to-right with drifting waves */
      return Math.sin(y * 0.006 + t * 0.00035) * 0.9 + Math.sin(x * 0.004 - t * 0.0005 + y * 0.002) * 0.6;
    };
    var frame = function (t, still) {
      ctx.globalCompositeOperation = "destination-out";
      ctx.fillStyle = still ? "rgba(0,0,0,1)" : "rgba(0,0,0,0.06)"; ctx.fillRect(0, 0, W, H);
      ctx.globalCompositeOperation = "lighter";
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i], steps = still ? 120 : 1;
        for (var s = 0; s < steps; s++) {
          var a = field(p.x, p.y, t) * 0.55;
          var dx = p.x - mouse.x, dy = p.y - mouse.y, d2 = dx * dx + dy * dy;
          if (d2 < 22000) { var f = (1 - d2 / 22000) * 1.6; a += (dy > 0 ? 1 : -1) * f; }
          p.px = p.x; p.py = p.y;
          p.x += Math.cos(a) * p.v * 1.6; p.y += Math.sin(a) * p.v * 1.1; p.l++;
          var k = Math.max(0, Math.min(1, p.x / W));
          var r = Math.round(C1[0] + (C2[0] - C1[0]) * k), g = Math.round(C1[1] + (C2[1] - C1[1]) * k), b = Math.round(C1[2] + (C2[2] - C1[2]) * k);
          var life = Math.min(1, p.l / 40) * Math.max(0, 1 - p.l / p.max);
          ctx.strokeStyle = "rgba(" + r + "," + g + "," + b + "," + (0.8 * life).toFixed(3) + ")";
          ctx.lineWidth = p.w;
          ctx.beginPath(); ctx.moveTo(p.px, p.py); ctx.lineTo(p.x, p.y); ctx.stroke();
          if (p.x > W + 20 || p.y < -20 || p.y > H + 20 || p.l > p.max) spawn(p, false);
        }
      }
    };
    var loop = function (t) { if (!run) return; frame(t, false); requestAnimationFrame(loop); };
    var start = function () {
      size(); parts = []; for (var i = 0; i < N; i++) parts.push(spawn({}, true));
      cv.classList.add("is-on");
      if (reduced) { frame(0, true); return; }
      run = true; requestAnimationFrame(loop);
    };
    var setRun = function (on) { if (reduced) return; if (on && !run && visible && !document.hidden) { run = true; requestAnimationFrame(loop); } else if (!on) run = false; };
    if (document.readyState === "complete") setTimeout(start, 120); else window.addEventListener("load", function () { setTimeout(start, 120); });
    window.addEventListener("resize", function () { if (!W) return; var w = W; size(); if (Math.abs(w - W) > 40) parts.forEach(function (p) { spawn(p, true); }); if (reduced) frame(0, true); });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible); }).observe(cv);
    document.addEventListener("visibilitychange", function () { setRun(!document.hidden); });
    var hero = cv.closest(".hero");
    if (hero && window.matchMedia("(hover: hover)").matches) {
      hero.addEventListener("pointermove", function (e) { var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
      hero.addEventListener("pointerleave", function () { mouse.x = mouse.y = -9999; });
    }
  }
  })();

  /* ---------- Header: scrolled state, hide on scroll down, progress bar ---------- */
  var header = document.querySelector(".site-header");
  var progress = document.querySelector(".progress");
  var callbar = document.querySelector(".callbar");
  var lastY = window.scrollY, menuOpen = false;

  /* ---------- Reveal on scroll ---------- */
  document.querySelectorAll("[data-stagger]").forEach(function (group) {
    Array.prototype.forEach.call(group.querySelectorAll("[data-reveal]"), function (el, i) { el.style.setProperty("--i", i % 8); });
  });
  var revealEls = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var t = en.target._revealTarget || en.target;
        t.classList.add("is-in"); io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0 });
    revealEls.forEach(function (el) {
      var mode = el.getAttribute("data-reveal");
      if ((mode === "wipe" || mode === "rise") && el.parentElement) {
        var proxy = el.parentElement;
        if (proxy._revealTarget) { proxy = el; } else { proxy._revealTarget = el; }
        io.observe(proxy);
      } else { io.observe(el); }
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Scroll-driven effects ---------- */
  var parallax = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  var fills = Array.prototype.slice.call(document.querySelectorAll("[data-fill]"));
  fills.forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(function (w) { return '<span class="fw">' + w.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</span>"; }).join(" ");
  });
  var seq = document.querySelector(".sequence");
  var seqSvg = seq && seq.querySelector(".system");
  var seqSticky = seq && seq.querySelector(".sequence__sticky");
  var seqSteps = seq ? Array.prototype.slice.call(seq.querySelectorAll(".sequence__step")) : [];
  var nSteps = seqSteps.length || 1;
  var seqLayers = seqSvg ? seqSteps.map(function (_, i) { return seqSvg.querySelectorAll('[data-layer="' + (i + 1) + '"]'); }) : [];
  var seqPct = seq && seq.querySelector(".sequence__pct");
  var seqTags = seqSvg ? Array.prototype.slice.call(seqSvg.querySelectorAll(".sys-tag")) : [];
  var seqRail = seq && seq.querySelector(".sequence__rail");
  var heroMedia = document.querySelector(".hero__media");
  var marquee = document.querySelector(".marquee__track");
  var mx = 0, mVel = 1, mWidth = 0;
  if (marquee) { var g = marquee.querySelector(".marquee__group"); mWidth = g ? g.offsetWidth : 0; window.addEventListener("resize", function () { mWidth = g ? g.offsetWidth : 0; }); }

  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight;
    var dy = y - lastY;
    if (header) {
      header.classList.toggle("is-scrolled", y > 30);
      if (!menuOpen && dy > 6 && y > 400) header.classList.add("is-hidden");
      if (dy < -6 || y <= 400) header.classList.remove("is-hidden");
    }
    if (progress) {
      var max = document.documentElement.scrollHeight - vh;
      progress.style.transform = "scaleX(" + (max > 0 ? y / max : 0) + ")";
    }
    if (callbar) callbar.classList.toggle("is-visible", y > vh * 0.6);
    if (!reduced) {
      mVel = Math.max(-6, Math.min(6, dy * 0.25)) || mVel;
      if (heroMedia && y < vh * 1.2) heroMedia.style.transform = "translate3d(0," + (y * 0.28).toFixed(1) + "px,0) scale(" + (1 + y / vh * 0.06).toFixed(4) + ")";
      parallax.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var speed = parseFloat(el.getAttribute("data-parallax")) || 0.15;
        el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - vh / 2) * -speed).toFixed(1) + "px,0)";
      });
      fills.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var p = Math.max(0, Math.min(1, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
        var ws = el.querySelectorAll(".fw"), n = Math.round(p * ws.length);
        for (var i = 0; i < ws.length; i++) ws[i].classList.toggle("on", i < n);
      });
      if (seq) {   /* desktop: side by side; phones: drawing pinned above one step card (see main.css) */
        var r = seq.getBoundingClientRect();
        var p = Math.max(0, Math.min(1, -r.top / (r.height - vh)));
        var stage = Math.min(nSteps - 1, Math.floor(p * nSteps * 0.999));
        seqLayers.forEach(function (els, idx) {
          var lp = Math.max(0, Math.min(1, (p * nSteps - idx) * 1.25));
          els.forEach(function (e) { e.style.setProperty("--l", lp.toFixed(3)); e.classList.toggle("is-live", lp > 0.9); });
        });
        seqSteps.forEach(function (s, i) { s.classList.toggle("is-active", i === stage); });
        seqTags.forEach(function (t) { t.classList.toggle("is-on", +t.getAttribute("data-layer") === stage + 1 && p > 0.02); });
        if (seqRail) seqRail.style.setProperty("--p", p.toFixed(3));
        if (seqSticky) seqSticky.style.setProperty("--heat-on", stage >= 2 ? "1" : "0");
        if (seqPct) seqPct.textContent = String(Math.round(p * 100)).padStart(2, "0") + "%";
      }
    }
    lastY = y;
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ---------- Marquee loop (velocity reacts to scroll) ---------- */
  if (marquee && !reduced) {
    var loop = function () {
      mVel += ((mVel > 0 ? 1 : -1) - mVel) * 0.04;
      mx -= mVel;
      if (mWidth) { if (mx <= -mWidth) mx += mWidth; if (mx > 0) mx -= mWidth; }
      marquee.style.transform = "translate3d(" + mx.toFixed(2) + "px,0,0)";
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  /* ---------- Card spotlight ---------- */
  document.querySelectorAll(".svc-card, .hero__est").forEach(function (c) {
    c.addEventListener("pointermove", function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty("--mx", (e.clientX - r.left) + "px");
      c.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  });

  /* ---------- Desktop dropdown menus ---------- */
  var items = document.querySelectorAll(".nav__item[data-dropdown]");
  var closeAll = function (except) { items.forEach(function (it) { if (it !== except) { it.classList.remove("is-open"); var b = it.querySelector("[aria-expanded]"); if (b) b.setAttribute("aria-expanded", "false"); } }); };
  items.forEach(function (it) {
    var btn = it.querySelector("button.nav__link");
    var timer;
    var panel = it.querySelector(".mega");
    /* keep the dropdown inside the window: it is centred under its menu item, then nudged so it never hangs off either edge */
    var fit = function () {
      if (!panel) return;
      /* calculated from the menu item's position and the panel's width (neither is affected by the panel's slide
         animation), so reopening the menu mid-animation can never measure a stale position */
      var ir = it.getBoundingClientRect(), W = document.documentElement.clientWidth, pad = 16;
      var width = panel.offsetWidth, left = ir.left + ir.width / 2 - width / 2, shift = 0;
      if (left < pad) shift = pad - left; else if (left + width > W - pad) shift = (W - pad) - (left + width);
      panel.style.setProperty("--shift", Math.round(shift) + "px");
    };
    window.addEventListener("resize", fit);
    var openedAt = 0;
    var open = function () { clearTimeout(timer); if (!it.classList.contains("is-open")) openedAt = Date.now(); closeAll(it); fit(); it.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); };
    var close = function () { timer = setTimeout(function () { it.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }, 160); };
    /* a click right after hover opened the menu keeps it open (otherwise hover-then-click would close it) */
    btn.addEventListener("click", function () {
      if (it.classList.contains("is-open")) { if (Date.now() - openedAt < 600) return; it.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }
      else open();
    });
    if (window.matchMedia("(hover: hover)").matches) { it.addEventListener("mouseenter", open); it.addEventListener("mouseleave", close); }
    it.addEventListener("focusout", function (e) { if (!it.contains(e.relatedTarget)) { it.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); } });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      var openItem = document.querySelector(".nav__item.is-open");
      closeAll(null);
      if (openItem) openItem.querySelector("button.nav__link").focus();
      if (menuOpen) toggleMenu(false);
    }
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav__item")) closeAll(null); });

  /* ---------- Mobile menu ---------- */
  var burger = document.querySelector(".burger");
  var mnav = document.getElementById("mobile-nav");
  var toggleMenu = function (state) {
    menuOpen = state;
    burger.setAttribute("aria-expanded", String(state));
    burger.setAttribute("aria-label", state ? "Close menu" : "Open menu");
    mnav.classList.toggle("is-open", state);
    document.body.style.overflow = state ? "hidden" : "";
    if (state) { header.classList.remove("is-hidden"); header.classList.add("is-scrolled"); var f = mnav.querySelector("a,summary"); if (f) setTimeout(function () { f.focus(); }, 50); }
    else { burger.focus(); onScroll(); }
  };
  if (burger && mnav) {
    burger.addEventListener("click", function () { toggleMenu(!menuOpen); });
    mnav.addEventListener("click", function (e) { if (e.target.closest("a")) { menuOpen = false; burger.setAttribute("aria-expanded", "false"); mnav.classList.remove("is-open"); document.body.style.overflow = ""; } });
  }

  /* ---------- Form validation ---------- */
  document.querySelectorAll("form[data-validate]").forEach(function (form) {
    var status = form.querySelector(".form__status");
    var setErr = function (field, msg) {
      var err = document.getElementById(field.id + "-error");
      field.setAttribute("aria-invalid", msg ? "true" : "false");
      if (err) err.textContent = msg || "";
    };
    var check = function (field) {
      var v = field.value.trim();
      if (field.required && !v) return "Please enter your " + (field.getAttribute("data-label") || "information") + ".";
      if (v && field.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return "Please enter a valid email address, like name@example.com.";
      if (v && field.type === "tel" && v.replace(/\D/g, "").length < 10) return "Please enter a 10-digit phone number.";
      return "";
    };
    form.querySelectorAll("input,select,textarea").forEach(function (f) {
      if (f.classList.contains("hp-input") || f.type === "hidden") return;
      f.addEventListener("blur", function () { if (f.value) setErr(f, check(f)); });
    });
    form.addEventListener("submit", function (e) {
      var first = null, n = 0;
      form.querySelectorAll("input,select,textarea").forEach(function (f) {
        if (f.classList.contains("hp-input") || f.type === "hidden" || !f.id) return;
        var m = check(f); setErr(f, m);
        if (m) { n++; if (!first) first = f; }
      });
      if (first) {
        e.preventDefault();
        if (status) { status.textContent = "Please fix " + n + (n === 1 ? " field" : " fields") + " highlighted below and try again."; status.classList.add("is-visible"); }
        first.focus();
      } else if (status) { status.classList.remove("is-visible"); }
    });
  });
})();
