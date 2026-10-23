#!/usr/bin/env python3
"""Browser QA (headless Chromium via Playwright). Run after build.py and qa.py:

    pip install playwright && python3 -m playwright install chromium
    python3 _build/qa_browser.py [--axe path/to/axe.min.js]

Checks the opening animation (landing on any page, once per session, #hash and reduced-motion skips),
the hero airflow, the pinned "inside the system" sequence, menus, form validation, the instant system
estimate end to end (prices recalculated here from site.config.json and compared with what the page shows),
the repair-or-replace check, console errors and horizontal overflow on phones.
With --axe, runs axe-core (WCAG 2.1 A/AA) on key pages. Exits non-zero on failures."""
import asyncio, functools, http.server, socketserver, threading, json, os, sys
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "site.config.json")))
E = CFG.get("estimator") or {}
AXE = sys.argv[sys.argv.index("--axe") + 1] if "--axe" in sys.argv else None
res = []
def rec(ok, msg, extra=""): res.append(("PASS" if ok else "FAIL", msg + (f"  [{extra}]" if extra and not ok else "")))

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def handle(self):
        try: super().handle()
        except (ConnectionResetError, BrokenPipeError): pass
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 8822), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
B = "http://127.0.0.1:8822"
OFFERED = CFG.get("services") or []
SVC_PAGE = f"/services/{OFFERED[0]}/" if OFFERED else "/services/"
sys.path.insert(0, HERE)
from content_cities import CITIES
C0 = CITIES[0]["slug"]
SVC_CITY = f"/services/{OFFERED[0]}/{C0}/" if OFFERED and os.path.exists(os.path.join(ROOT, f"services/{OFFERED[0]}/{C0}")) else None

def by(lst, i): return next(x for x in lst if x["id"] == i)
def expected(system, size=None, tier=None, addons=(), zones=1):
    s = by(E["systems"], system); z = by(E["home_sizes"], size or E["default_size"]); t = by(E["tiers"], tier or E["default_tier"])
    ductless = bool(s.get("extra_zone"))
    base = s["base"] + (zones - 1) * s["extra_zone"] if ductless else s["base"] * z["price_mult"]
    extra = 0 if ductless else sum(by(E["addons"], a)["price"] for a in addons)
    mid = max(E.get("minimum_job", 0), base * t["price_mult"] + extra)
    pct = E.get("range_pct", 12) / 100; r = E.get("round_to", 100)
    rnd = lambda n: int(round(n / r) * r)
    lo, hi = rnd(mid * (1 - pct)), rnd(mid * (1 + pct))
    lo = max(lo, rnd(E.get("minimum_job", 0)))
    return f"${lo:,}", f"${hi:,}"

async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        errors = []
        async def page(w=1440, h=900, reduced=False, seen=True):
            ctx = await br.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference")
            if seen: await ctx.add_init_script("try{sessionStorage.setItem('hv-intro','1')}catch(e){}")
            pg = await ctx.new_page()
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            return ctx, pg

        # ---- opening animation
        if CFG.get("intro", True):
            land = SVC_PAGE if CFG.get("intro_scope", "all") == "all" else "/"
            ctx, pg = await page(seen=False)
            await pg.goto(B + land, wait_until="commit"); await pg.wait_for_timeout(700)
            showing = await pg.evaluate("!!document.querySelector('.intro') && !document.documentElement.classList.contains('no-intro')")
            reading = await pg.evaluate("(document.querySelector('.intro__count')||{}).textContent")
            await pg.wait_for_timeout(3200)
            gone = await pg.evaluate("!document.querySelector('.intro') && document.documentElement.classList.contains('is-ready')")
            rec(showing and gone, f"Opening animation plays when landing on {land} and clears itself", f"showing={showing} gone={gone}")
            rec(bool(reading) and reading != "05.0", "Intro dial counts up while playing", f"reading={reading}")
            await pg.goto(B + "/about/", wait_until="commit"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.documentElement.classList.contains('no-intro')"), "Intro does not replay on the next page in the same session")
            await ctx.close()
            ctx, pg = await page(seen=False)
            await pg.goto(B + "/#faq-title", wait_until="commit"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.documentElement.classList.contains('no-intro')"), "Intro skipped when the URL has a #hash")
            await ctx.close()
            ctx, pg = await page(seen=False, reduced=True)
            await pg.goto(B + "/"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.documentElement.classList.contains('no-intro')"), "Intro skipped for reduced motion")
            await ctx.close()
            ctx, pg = await page(seen=False)
            await pg.goto(B + "/", wait_until="commit"); await pg.wait_for_timeout(500)
            await pg.mouse.click(10, 500); await pg.wait_for_timeout(1500)
            rec(await pg.evaluate("!document.querySelector('.intro')"), "A click skips the intro")
            await ctx.close()

        # ---- home: hero airflow + sequence + CLS
        ctx, pg = await page()
        await pg.goto(B + "/"); await pg.wait_for_timeout(1500)
        if CFG.get("hero_fx", True):
            px = await pg.evaluate("(()=>{var c=document.querySelector('.hero__fx');if(!c)return -1;var d=c.getContext('2d').getImageData(0,0,c.width,c.height).data,n=0;for(var i=3;i<d.length;i+=16)if(d[i]>0)n++;return n})()")
            rec(px > 500, "Hero airflow canvas is drawing", f"pixels={px}")
        cls = await pg.evaluate("""new Promise(r=>{let v=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true});setTimeout(()=>r(v),300)})""")
        rec(cls < 0.1, f"Home page layout shift (CLS) {cls:.3f} < 0.1")
        top = await pg.evaluate("document.querySelector('.sequence').offsetTop"); hgt = await pg.evaluate("document.querySelector('.sequence').offsetHeight")
        await pg.evaluate(f"window.scrollTo(0,{top + hgt * 0.15})"); await pg.wait_for_timeout(500)
        first = await pg.evaluate("[...document.querySelectorAll('.sequence__step')].findIndex(s=>s.classList.contains('is-active'))")
        await pg.evaluate(f"window.scrollTo(0,{top + hgt - 1000})"); await pg.wait_for_timeout(600)
        last = await pg.evaluate("[...document.querySelectorAll('.sequence__step')].findIndex(s=>s.classList.contains('is-active'))")
        built = await pg.evaluate("[...document.querySelectorAll('.system .layer')].every(l=>parseFloat(l.style.getPropertyValue('--l'))>=0.99)")
        rec(first == 0 and last == 4 and built, "Pinned sequence steps through all five stages and builds the drawing", f"first={first} last={last} built={built}")
        # desktop menu
        await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(400)
        await pg.click(".nav__item[data-dropdown] button"); await pg.wait_for_timeout(500)
        rec(await pg.evaluate("document.querySelector('.nav__item[data-dropdown]').classList.contains('is-open') && document.querySelector('#mega-services').getBoundingClientRect().right <= innerWidth"), "Services dropdown opens and stays inside the window")
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(200)
        rec(await pg.evaluate("!document.querySelector('.nav__item.is-open')"), "Escape closes the dropdown")
        # hero picker (no-JS GET form) hands off to the estimate
        if E.get("enabled", True):
            await pg.check(".pick:nth-child(4) input", force=True); await pg.click(".picker__go"); await pg.wait_for_load_state(); await pg.wait_for_timeout(400)
            chosen = await pg.evaluate("(document.querySelector('#est-form input[name=system]:checked')||{}).value")
            rec("system-estimate" in pg.url and chosen == E["systems"][3]["id"], "Hero system picker opens the estimate with that system selected", f"url={pg.url} chosen={chosen}")
        await ctx.close()

        # ---- estimator maths
        if E.get("enabled", True):
            ctx, pg = await page()
            await pg.goto(B + "/system-estimate/"); await pg.wait_for_timeout(400)
            async def shown():
                return [await pg.text_content("#est-low"), await pg.text_content("#est-high")]
            got = await shown(); exp = expected(E["default_system"])
            rec(got == list(exp), f"Default estimate matches config ({exp[0]} – {exp[1]})", f"got {got}")
            allok, bad = True, []
            for s in E["systems"]:
                for z in E["home_sizes"]:
                    for t in E["tiers"]:
                        await pg.check(f'#est-form input[name=system][value="{s["id"]}"]', force=True)
                        if not s.get("extra_zone"): await pg.check(f'#est-form input[name=size][value="{z["id"]}"]', force=True)
                        await pg.check(f'#est-form input[name=tier][value="{t["id"]}"]', force=True)
                        g = await shown(); x = expected(s["id"], z["id"], t["id"])
                        if g != list(x): allok = False; bad.append(f'{s["id"]}/{z["id"]}/{t["id"]}: {g} vs {x}')
            rec(allok, f"Every system × home size × efficiency combination matches the config ({len(E['systems']) * len(E['home_sizes']) * len(E['tiers'])} checked)", "; ".join(bad[:3]))
            ducted = next(x for x in E["systems"] if not x.get("extra_zone"))
            await pg.check(f'#est-form input[name=system][value="{ducted["id"]}"]', force=True)
            await pg.check('#est-form input[name=size][value="m"]', force=True); await pg.check(f'#est-form input[name=tier][value="{E["tiers"][0]["id"]}"]', force=True)
            ids = [a["id"] for a in E.get("addons", [])[:2]]
            for a in ids: await pg.check(f'#est-form input[name=addon][value="{a}"]', force=True)
            rec(await shown() == list(expected(ducted["id"], "m", E["tiers"][0]["id"], ids)), "Add-ons are added to the estimate")
            ms = next((x for x in E["systems"] if x.get("extra_zone")), None)
            if ms:
                await pg.check(f'#est-form input[name=system][value="{ms["id"]}"]', force=True); await pg.wait_for_timeout(100)
                await pg.click('.stepper__b[data-step="1"]'); await pg.click('.stepper__b[data-step="1"]')
                g = await shown(); x = expected(ms["id"], tier=E["tiers"][0]["id"], zones=3)
                hid = await pg.evaluate("[document.getElementById('est-size').hidden, [...document.querySelectorAll('.chk')].every(c=>c.hidden)]")
                rec(g == list(x) and hid == [True, True], "Ductless: priced per zone; home size and duct add-ons hidden", f"{g} vs {x}, hidden={hid}")
            await pg.click("#est-lead-open"); await pg.wait_for_timeout(500)
            fields = await pg.evaluate("Object.fromEntries([...document.querySelectorAll('#est-lead input[type=hidden]')].map(i=>[i.name,i.value]))")
            rec(not await pg.evaluate("document.getElementById('est-lead').hidden") and fields.get("System") and "$" in fields.get("Estimate shown", ""), "Lead form opens with the system, options and estimate filled in", json.dumps(fields))
            await pg.click("#est-lead button[type=submit]"); await pg.wait_for_timeout(200)
            rec(await pg.evaluate("document.querySelector('#est-lead .form__status').classList.contains('is-visible') && document.activeElement.id==='lead-name'"), "Empty estimate form shows errors and focuses the first field")
            if (E.get("repair_rule") or {}).get("enabled", True):
                T = E["repair_rule"]["threshold"]
                await pg.fill("#rr-age", "16"); await pg.fill("#rr-cost", str(int(T / 16) + 100))
                over = await pg.evaluate("document.getElementById('rr-out').classList.contains('is-replace')")
                await pg.fill("#rr-cost", "100")
                under = await pg.evaluate("!document.getElementById('rr-out').classList.contains('is-replace')")
                rec(over and under, "Repair-or-replace check flips at the configured threshold")
            await ctx.close()
            ctx, pg = await page(390, 844)
            await pg.goto(B + "/system-estimate/"); await pg.wait_for_timeout(300)
            await pg.evaluate("document.querySelector('.opts--sys').scrollIntoView()"); await pg.evaluate("window.scrollBy(0,-120)"); await pg.wait_for_timeout(800)
            rec(await pg.evaluate("document.getElementById('est-live').classList.contains('is-visible') && document.getElementById('est-live-v').textContent.includes('$')"), "Phones: live price bar shows while the result card is off screen")
            await ctx.close()

        # ---- contact form validation
        ctx, pg = await page()
        await pg.goto(B + "/contact/"); await pg.click(".form button[type=submit]"); await pg.wait_for_timeout(200)
        rec(await pg.evaluate("document.querySelector('.form .form__status').classList.contains('is-visible') && document.querySelectorAll('.form [aria-invalid=true]').length>=5"), "Contact form: empty submit shows errors on required fields")
        await pg.fill("#email", "not-an-email"); await pg.click(".form button[type=submit]")
        rec("valid email" in (await pg.text_content("#email-error")), "Contact form: invalid email message")
        await ctx.close()

        # ---- phones: menu, overflow, call bar
        ctx, pg = await page(390, 844)
        over = []
        pages = ["/", "/system-estimate/", SVC_PAGE, "/services/", "/service-areas/", f"/service-areas/{C0}/", "/contact/", "/faq/", "/about/", "/privacy-policy.html", "/404.html"] + ([SVC_CITY] if SVC_CITY else [])
        for u in pages:
            await pg.goto(B + u); await pg.wait_for_timeout(250)
            if await pg.evaluate("document.documentElement.scrollWidth > innerWidth + 1"): over.append(u)
        rec(not over, f"No horizontal scrolling at 390px on {len(pages)} key pages", ", ".join(over))
        await pg.goto(B + "/"); await pg.click(".burger"); await pg.wait_for_timeout(800)
        rec(await pg.evaluate("document.getElementById('mobile-nav').classList.contains('is-open') && document.querySelector('.burger').getAttribute('aria-expanded')==='true'"), "Mobile menu opens from the burger button")
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(300)
        await pg.evaluate("window.scrollTo(0,1400)"); await pg.wait_for_timeout(600)
        rec(await pg.evaluate("document.querySelector('.callbar').classList.contains('is-visible')"), "Mobile call bar appears after scrolling")
        await ctx.close()

        # ---- axe
        if AXE:
            src = open(AXE).read()
            ctx, pg = await page()
            for u in ["/", "/system-estimate/", SVC_PAGE, "/contact/", f"/service-areas/{C0}/"]:
                await pg.goto(B + u); await pg.wait_for_timeout(1500); await pg.add_script_tag(content=src)
                v = await pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21a','wcag21aa']}).then(r=>r.violations.map(v=>v.id+' ('+v.nodes.length+')'))")
                rec(not v, f"axe WCAG 2.1 AA on {u}: {len(v)} violations", ", ".join(v))
            await ctx.close()

        rec(not errors, f"No JavaScript errors in the console ({len(errors)})", " | ".join(errors[:4]))
        await br.close()
    for s, m in res: print(s, m)
    f = sum(1 for s, _ in res if s == "FAIL")
    print(f"\n{len(res) - f} passed, {f} failed")
    sys.exit(1 if f else 0)

asyncio.run(main())
