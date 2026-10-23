/* HVAC Template — instant system estimate + repair-or-replace check (no dependencies).
   Pricing comes from site.config.json ("estimator"), written into the page as #est-config by the build.
   Everything is calculated in the browser; nothing is sent until the visitor submits the lead form. */
(function () {
  "use strict";
  var cfgEl = document.getElementById("est-config");
  var form = document.getElementById("est-form");
  if (!cfgEl || !form) return;
  var C = JSON.parse(cfgEl.textContent);
  var $ = function (id) { return document.getElementById(id); };
  var byId = function (list, id) { for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i]; return list[0]; };
  var money = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };
  var round = function (n) { var r = C.round_to || 100; return Math.round(n / r) * r; };
  var zonesBox = $("est-zones"), zoneIn = $("est-zone-n"), result = $("est-result"), arc = $("est-arc");
  var low = $("est-low"), high = $("est-high"), sum = $("est-sum");

  /* show each add-on's price, from config */
  Array.prototype.forEach.call(document.querySelectorAll(".chk__price"), function (el) {
    el.textContent = "+" + money(+el.getAttribute("data-price"));
  });

  /* deep link from the home page picker: ?system=heat-pump */
  try {
    var q = new URLSearchParams(location.search).get("system");
    if (q) { var r = form.querySelector('input[name="system"][value="' + q.replace(/[^a-z0-9\-]/gi, "") + '"]'); if (r) r.checked = true; }
  } catch (e) {}

  var val = function (name) { var el = form.querySelector('input[name="' + name + '"]:checked'); return el ? el.value : null; };

  var state = {};
  var calc = function () {
    var sys = byId(C.systems, val("system"));
    var size = byId(C.home_sizes, val("size"));
    var tier = byId(C.tiers, val("tier"));
    var ductless = !!sys.extra_zone;
    var zones = 1;
    if (zonesBox) {
      zonesBox.hidden = !ductless;
      if (ductless) {
        var max = sys.max_zones || 5;
        zones = Math.max(1, Math.min(max, parseInt(zoneIn.value, 10) || 1)); zoneIn.value = zones;
      }
    }
    /* add-ons only apply to ducted systems (furnace / AC / heat pump), not ductless heads */
    var addons = [], extra = 0;
    Array.prototype.forEach.call(form.querySelectorAll(".chk"), function (lab) {
      lab.hidden = ductless;
      var cb = lab.querySelector("input");
      if (ductless) { cb.checked = false; return; }
      if (cb.checked) { var a = byId(C.addons || [], cb.value); addons.push(a.label); extra += a.price; }
    });
    var sizeBox = $("est-size"); if (sizeBox) sizeBox.hidden = ductless;
    var extrasCard = $("est-extras-card"); if (extrasCard) extrasCard.hidden = ductless || !(C.addons || []).length;
    /* ductless is priced per head, so home size doesn't scale it */
    var base = ductless ? sys.base + (zones - 1) * sys.extra_zone : sys.base * size.price_mult;
    var mid = Math.max(C.minimum_job || 0, base * tier.price_mult + extra);
    var pct = (C.range_pct || 12) / 100;
    var lo = round(mid * (1 - pct)), hi = round(mid * (1 + pct));
    if (lo < (C.minimum_job || 0)) lo = round(C.minimum_job);
    state = { sys: sys, size: size, tier: tier, zones: zones, addons: addons, lo: lo, hi: hi };
    low.textContent = money(lo); high.textContent = money(hi);
    var lv = $("est-live-v"); if (lv) lv.textContent = money(lo) + " – " + money(hi);
    sum.textContent = sys.label + (ductless ? " · " + zones + " zone" + (zones > 1 ? "s" : "") : " · " + size.label) + " · " + tier.label + (addons.length ? " · +" + addons.length + " extra" + (addons.length > 1 ? "s" : "") : "");
    /* dial: fill relative to the most expensive combination, tinted toward heat as the price rises */
    var maxMid = 0;
    C.systems.forEach(function (s) {
      var b = s.extra_zone ? s.base + ((s.max_zones || 5) - 1) * s.extra_zone : s.base * C.home_sizes[C.home_sizes.length - 1].price_mult;
      var t = C.tiers[C.tiers.length - 1].price_mult;
      maxMid = Math.max(maxMid, b * t + (C.addons || []).reduce(function (a, x) { return a + x.price; }, 0));
    });
    var f = Math.max(0.08, Math.min(1, mid / maxMid));
    if (arc) { arc.style.setProperty("--arc", (1 - f).toFixed(3)); arc.style.stroke = f > 0.55 ? "var(--heat)" : "var(--accent)"; }
    if (result) { result.style.setProperty("--heatv", f.toFixed(2)); result.classList.remove("is-new"); void result.offsetWidth; result.classList.add("is-new"); }
    /* keep the lead form's hidden fields in sync */
    var set = function (id, v) { var el = $(id); if (el) el.value = v; };
    set("lead-system", sys.label);
    set("lead-home-size", ductless ? "n/a (ductless)" : size.label);
    set("lead-efficiency", tier.label);
    set("lead-zones", ductless ? String(zones) : "n/a");
    set("lead-add-ons", addons.join(", ") || "none");
    set("lead-estimate-shown", money(lo) + " – " + money(hi) + " " + (C.currency || "USD"));
  };
  form.addEventListener("change", calc);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  if (zoneIn) {
    zoneIn.addEventListener("input", calc);
    Array.prototype.forEach.call(document.querySelectorAll(".stepper__b"), function (b) {
      b.addEventListener("click", function () { zoneIn.value = (parseInt(zoneIn.value, 10) || 1) + (+b.getAttribute("data-step")); calc(); });
    });
  }
  calc();

  /* phones: show the live price bar while the result card is off screen */
  var live = $("est-live");
  if (live && result && "IntersectionObserver" in window) {
    var tool = document.getElementById("estimator"), inTool = false, resVis = false;
    var upLive = function () { live.classList.toggle("is-visible", inTool && !resVis); };
    new IntersectionObserver(function (en) { resVis = en[0].isIntersecting; upLive(); }).observe(result);
    new IntersectionObserver(function (en) { inTool = en[0].isIntersecting; upLive(); }).observe(tool);
  }

  /* reveal the lead form */
  var open = $("est-lead-open"), lead = $("est-lead");
  if (open && lead) open.addEventListener("click", function () {
    lead.hidden = false;
    open.setAttribute("aria-expanded", "true");
    lead.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    setTimeout(function () { var n = $("lead-name"); if (n) n.focus({ preventScroll: true }); }, 350);
  });

  /* ---------- repair-or-replace rule of thumb ---------- */
  var rr = document.querySelector("[data-rr]");
  if (rr) {
    var T = +rr.getAttribute("data-threshold") || 5000;
    var age = $("rr-age"), cost = $("rr-cost"), out = $("rr-out"), meter = rr.querySelector(".rr__meter");
    var scale = T * 2;
    if (meter) meter.style.setProperty("--mark", "50%");
    var upd = function () {
      var a = parseFloat(age.value), c = parseFloat(cost.value);
      if (!(a >= 0) || !(c >= 0) || age.value === "" || cost.value === "") {
        out.className = "rr__out"; out.textContent = "Enter the age and repair price to see where you land.";
        if (meter) meter.style.setProperty("--rr", 0); return;
      }
      var score = a * c, pos = Math.max(0, Math.min(99, score / scale * 100));
      if (meter) meter.style.setProperty("--rr", pos.toFixed(1));
      var n = Math.round(score).toLocaleString("en-US");
      if (score >= T) {
        out.className = "rr__out is-replace";
        out.innerHTML = "<strong>" + n + "</strong>: over the " + T.toLocaleString("en-US") + " mark. Replacement is worth pricing out before you approve the repair.";
      } else if (score >= T * 0.7) {
        out.className = "rr__out";
        out.innerHTML = "<strong>" + n + "</strong>: getting close. The repair can make sense, but start planning for a replacement.";
      } else {
        out.className = "rr__out";
        out.innerHTML = "<strong>" + n + "</strong>: under the mark. A repair usually makes sense here.";
      }
    };
    age.addEventListener("input", upd); cost.addEventListener("input", upd);
  }
})();
