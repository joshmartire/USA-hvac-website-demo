# -*- coding: utf-8 -*-
# Copy for the home page and the standalone pages (about, FAQ, thank-you, legal).
# Items in HTML comments marked CLIENT REVIEW must be confirmed with the client before launch.

GENERAL_FAQS = [
("What areas do you serve?", "We work in {cities}. If your home or building is nearby but outside these communities, contact us and we'll let you know whether we can help."),
("How accurate is the instant system estimate?", "It's a ballpark range for a typical replacement, based on the system you choose, your home's size and the efficiency level. Venting changes, ductwork, electrical upgrades and access can change the final price, which is confirmed in writing after a home visit."),
("Should I repair or replace my furnace or air conditioner?", "A common rule of thumb multiplies the system's age by the repair cost. When the result is well above five thousand dollars, replacement is usually worth pricing out. Frequent breakdowns, discontinued refrigerant and rising energy bills point the same way. We'll show you both options."),
("How long does a furnace or AC installation take?", "Most straightforward replacements take one day. New venting routes, duct changes, heat pumps and furnace and air conditioner combinations can take a day or two longer."),
("What size system do I need?", "It depends on your home's heat loss and heat gain: insulation, windows, air leakage, sun exposure and layout, not just square footage. We size equipment on site rather than copying the old unit, because oversized systems short cycle and leave hot and cold spots."),
("Are heat pumps worth it in Michigan?", "Cold-climate heat pumps heat well below freezing and also replace your air conditioner. Paired with a gas furnace for the coldest nights, they suit many homes. Whether they save money depends on your home and current energy prices, which we walk through with you."),
("Do I need a permit for HVAC work?", "In Michigan, installing or replacing a furnace, air conditioner or heat pump generally requires a mechanical permit and inspection, and the work must be done by a licensed mechanical contractor. New electrical circuits need a licensed electrician and an electrical permit. We pull the permits that apply to your project."),
("Are there rebates for new equipment?", "Utility and government programs for heat pumps, furnaces, thermostats and insulation change often. We check what's currently available for your equipment when we quote, but eligibility and payment are decided by each program."),
("What should I check before hiring any HVAC contractor?", "Ask whether the company is a licensed mechanical contractor that pulls permits, whether its technicians are EPA 608 certified for refrigerant, ask for proof of liability insurance and workers' compensation coverage, and get the equipment, scope and price in writing before work starts."),
("How often should my system be serviced?", "Once a year for each piece of equipment: furnaces and boilers before heating season, air conditioners and heat pumps before cooling season. Change or check filters every one to three months."),
("How do I get started?", "Use the instant system estimate for a ballpark number, call us, or send your details through our quote form. We'll follow up to book a home visit."),
]

def _and(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def home(cfg, cities, services=None, all_offered=True):
    names = [c["name"] for c in cities]
    city_text = _and(names)
    d = {
        "desc": f"Heating and cooling serving {city_text}: furnaces, air conditioners, heat pumps, repairs, maintenance and an instant system estimate.",
        "eyebrow": f"Heating & Cooling · {cfg['region_label']}",
        "lead": "Furnaces, air conditioners and heat pumps, sized to your home, installed by licensed technicians and priced in writing. See a ballpark for a new system in about a minute.",
        # CLIENT REVIEW: confirm these badges describe how the client actually works.
        "tags": ["Written, itemized quotes", "Licensed & EPA-certified techs", "Start-up readings recorded"],
        "statement_eyebrow": "Comfort is engineered.",
        "statement": "The box in the basement is only part of it. Sizing, venting, ductwork and setup decide whether a system keeps you comfortable for years, so that's where we put the most care.",
        "statement_points": [
            ("Sized to your house", "We work out what your home actually needs instead of copying the sticker on the old unit."),
            ("Priced in writing", "Equipment, venting, ductwork and add-ons listed separately, so you can compare quotes properly."),
            ("Tested at start-up", "Gas pressure, temperature rise and safeties checked and recorded before we leave."),
        ],
        "services_lead": "Heating, cooling, air quality and the equipment around them. Pick a service to see what's included and what to ask before you hire.",
        # pinned "inside the system" sequence: one step per stage, following the air
        "layers": [
            ("Return & filter", "Air comes back from the rooms through the return ducts and passes through the filter, where dust and debris are caught before they reach the equipment."),
            ("Blower", "A variable-speed blower moves the air through the system, ramping up and down quietly instead of slamming on and off."),
            ("Burners & heat exchanger", "The burners heat a sealed heat exchanger. Combustion gases stay inside it and vent outdoors, so they never mix with the air you breathe."),
            ("Cooling coil", "In summer, refrigerant in the coil above the furnace pulls heat and humidity out of the air before it's sent back to the rooms."),
            ("Supply to every room", "Conditioned air travels through balanced supply ducts to every room, with the thermostat keeping the whole house where you set it."),
        ],
        "process": [
            ("Estimate online", "Use the instant estimate for a ballpark, or call us. No pressure either way."),
            ("Home visit", "We look at your equipment, venting, ductwork and comfort problems, room by room."),
            ("Quote in writing", "Equipment options, efficiency levels and every line item, to review on your own time."),
            ("Install & start-up", "Installed, tested and walked through with you, with the start-up readings recorded."),
        ],
        "why_lead": "Heating and cooling work happens behind walls and in basements. These are the standards every job runs on, so you always know what you're paying for.",
        # CLIENT REVIEW: confirm these working standards with the client.
        "features": [
            ("Straight answers", "If a repair makes sense, we'll say so. If the system is done, we'll show you why."),
            ("Written, itemized quotes", "Equipment, labor, venting, ductwork and extras listed separately, every time."),
            ("Licensed where it counts", "A licensed mechanical contractor, permits pulled, and EPA 608 certified technicians on refrigerant work."),
            ("Clean, tested installs", "Work areas protected, old equipment removed and start-up readings recorded for your file."),
        ],
        "faqs": [(q.replace("{cities}", city_text), a.replace("{cities}", city_text)) for q, a in GENERAL_FAQS[1:5]],
    }
    if not all_offered and services:
        low = [x["name"].lower() for x in services]
        d["desc"] = f"Heating and cooling company serving {city_text}: " + (", ".join(low[:5]) + " and more." if len(low) > 5 else _and(low) + ".")
        if len(d["desc"]) > 158:
            d["desc"] = f"Heating and cooling company serving {city_text}: " + ", ".join(low[:3]) + " and more."
        d["services_lead"] = "Pick a service to see what's included, how the work runs and what to ask before you hire."
    return d


def simple_pages(cfg, cities, services, city_text, all_offered=True):
    biz = cfg["business_name"]
    offered = {x["slug"]: x for x in services}

    def links(slugs, limit=None):
        out = [f"[[{sl}|{offered[sl]['name'].lower()}]]" for sl in dict.fromkeys(slugs) if sl in offered]
        return out[:limit] if limit else out
    faqs = [(q.replace("{cities}", city_text), a.replace("{cities}", city_text)) for q, a in GENERAL_FAQS]
    est_on = (cfg.get("estimator") or {}).get("enabled", True)

    def about(here):
        work = _and(links([x["slug"] for x in services], 6) or ["heating and cooling"])
        return f"""
<!-- CLIENT REVIEW: replace or extend with the client's real story: founding year, owner names, team, mechanical contractor license number, manufacturer dealer status, memberships and real project photos. Do not add claims that can't be verified. -->
<h2>Who we are</h2>
<p>{biz} is a heating and cooling company serving {city_text}. We work on homes and light commercial buildings, and our work includes {work}.</p>
<p>Most people only think about their furnace or air conditioner when it stops working. That's why we explain what we find, put our prices in writing and record how the equipment is running, so you know what's in your basement and why.</p>
<h2>How we work</h2>
<ul>
<li><strong>Sized to the house.</strong> We work out what your home needs instead of copying the old equipment's rating.</li>
<li><strong>Clear, written quotes.</strong> Equipment, labor, venting, ductwork and anything that isn't included, spelled out.</li>
<li><strong>Honest about repairs.</strong> If a repair is the smart move, we'll tell you. If the system is finished, we'll show you why.</li>
<li><strong>Respect for your home.</strong> Protected floors, a tidy work area and old equipment taken away.</li>
</ul>
<h2>Where we work</h2>
<p>We work across {city_text}. Each community has its own housing, climate exposure and permit office, which we cover on our pages for [[area:{cities[0]['slug']}|{cities[0]['name']}]], [[area:{cities[1]['slug']}|{cities[1]['name']}]] and [[area:{cities[2]['slug']}|{cities[2]['name']}]].</p>
<h2>Before you hire anyone</h2>
<p>Whoever you choose, check that the company is a licensed mechanical contractor that pulls permits and its technicians are EPA 608 certified for refrigerant work, ask for proof of liability insurance and workers' compensation coverage, and get the equipment, scope and price in writing. Good contractors are glad to answer those questions. When you're ready, {"try our [[estimate|instant system estimate]] or " if est_on else ""}[[contact|request a quote]].</p>
"""

    def faq(here):
        out = '<h2>Frequently asked questions</h2><div class="faq">'
        for q, a in faqs:
            if "instant system estimate" in q.lower() and not est_on:
                continue
            out += f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="faq__a"><p>{a}</p></div></details>'
        l = links(["furnace-installation", "furnace-repair", "heat-pumps", "ac-installation"] + [x["slug"] for x in services], 4) or ["our services"]
        out += '</div><h2>Service-specific questions</h2><p>Each service page answers common questions about that type of work. Start with ' + (
            l[0] if len(l) == 1 else ", ".join(l[:-1]) + " or " + l[-1]) + ', or browse [[services|all services]].</p>'
        return out

    def thanks(here):
        return f"""<h2>We've received your request</h2>
<p>Thanks for contacting {biz}. We'll review your details and follow up by phone or email to book a visit.</p>
<p>If you have no heat or no cooling right now, call us at <a href="tel:{cfg['phone_e164']}">{cfg['phone_display']}</a>. If you smell gas, leave the building and call your gas utility's emergency line from outside.</p>
<p>While you wait, you can browse [[services|our services]] or read our [[faq|frequently asked questions]].</p>"""

    tool_privacy = ""
    if est_on:
        tool_privacy = """<p><strong>Instant system estimate.</strong> The instant system estimate runs entirely in your web browser. The choices you make, such as system type and home size, are not sent to us or to anyone else unless you choose to submit the estimate form.</p>"""

    def privacy(here):
        return f"""
<!-- CLIENT REVIEW / LEGAL REVIEW REQUIRED: This is a draft based on the website as built (quote and estimate forms via {cfg['form_provider_name']}, static hosting, estimate calculated in the browser, no analytics or advertising). Confirm actual data handling, retention periods, email provider and any CRM, financing or other tools before publishing. If analytics, advertising pixels, chat or booking tools are added, this policy must be updated. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<p>This Privacy Policy explains how {cfg['legal_name']} ("we", "us") collects, uses and protects personal information through this website and when you contact us about heating, cooling or related services. We handle personal information in accordance with applicable United States and {cfg['legal_jurisdiction']} law.</p>
<h2>Information we collect</h2>
<p><strong>Information you give us.</strong> When you submit our quote form or send us an instant estimate, we collect your name, phone number, email address, property area, the service you're interested in and any details you choose to share. Estimate submissions also include the system, home size, efficiency level and options you selected, and the estimated price range shown to you. If you call or email us, we collect the information you provide in that conversation.</p>
{tool_privacy}
<p><strong>Technical information.</strong> When you visit, our hosting provider's servers may automatically log technical information such as your IP address and browser details for security and operational purposes. We do not use this website to collect analytics, and we do not use advertising or tracking cookies.</p>
<h2>How we use your information</h2>
<ul>
<li>To respond to your inquiry and book a home visit or service call.</li>
<li>To prepare quotes, contracts and work schedules.</li>
<li>To communicate with you about your project or service before, during and after the work.</li>
<li>To register equipment warranties where you ask us to, and to meet legal, accounting and tax obligations.</li>
</ul>
<p>We do not sell your personal information, and we do not use it for unrelated marketing without your consent.</p>
<h2>Who we share it with</h2>
<p>Quote and estimate requests submitted through this website are transmitted through {cfg['form_provider_name']}, a third-party form service that delivers submissions to our email. Your information may also be shared with equipment manufacturers for warranty registration, with suppliers or subcontractors when needed to deliver your project, and with professional advisors or authorities where required by law. Service providers we use may store or process information in other states or countries, where it may be subject to the laws of those jurisdictions.</p>
<h2>How long we keep it</h2>
<p>We keep personal information only as long as needed for the purposes above, including any period required for legal, tax or warranty reasons, and then securely delete or destroy it.</p>
<h2>How we protect it</h2>
<p>We use reasonable administrative, technical and physical safeguards appropriate to the sensitivity of the information. No method of transmission or storage is completely secure, so we cannot promise absolute security. Please don't include sensitive information, such as financial details, in our website forms.</p>
<h2>Your choices and rights</h2>
<p>You may ask to access the personal information we hold about you, ask us to correct it, or withdraw your consent to our use of it, subject to legal and contractual restrictions. To make a request, contact us using the details below. We will respond within a reasonable time.</p>
<h2>Cookies</h2>
<p>This website does not set cookies. See our [[cookies|Cookie Policy]] for details on the limited browser storage the site uses.</p>
<h2>Contact us</h2>
<p>Questions about privacy can be sent to <a href="mailto:{cfg['privacy_contact']}">{cfg['privacy_contact']}</a> or by phone at <a href="tel:{cfg['phone_e164']}">{cfg['phone_display']}</a>.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The effective date above shows when it was last changed.</p>
"""

    def terms(here):
        est = """<h2>Instant system estimates</h2>
<p>The instant system estimate is an automated ballpark for a typical equipment replacement, calculated from the options you choose and our general pricing. It is not a quote or an offer. The actual price is confirmed only in a written quote after a home visit, and can differ because of equipment selection, sizing, venting, gas and electrical work, ductwork, access, permits and other factors. Any repair-or-replace guidance on the estimate page is a general rule of thumb, not a recommendation for your specific equipment.</p>
""" if est_on else ""
        return f"""
<!-- CLIENT REVIEW / LEGAL REVIEW REQUIRED: Draft website terms. Project-specific terms (payment schedules, deposits, warranties, financing, cancellations, maintenance plan terms) belong in the client's written contracts, not here. Have the limitation of liability and governing-law sections reviewed by a lawyer. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<p>These Terms and Conditions apply to your use of this website, operated by {cfg['legal_name']} ("we", "us"). By using the website, you agree to these terms.</p>
<h2>Use of this website</h2>
<p>You may use this website for lawful purposes, such as learning about our services and contacting us. You agree not to misuse the website, attempt to interfere with its operation, or submit false or misleading information through our forms.</p>
<h2>Information on this website</h2>
<p>Content on this website is general information about heating, cooling and related services. It is not professional, engineering, legal or code-compliance advice for your specific property, and it does not replace an inspection by a qualified technician. Gas, electrical, building code and permit requirements vary by project and change over time. If you smell gas, leave the building and contact your gas utility's emergency line. While we try to keep information accurate and current, we don't warrant that it is complete or error-free.</p>
{est}<h2>Quotes and project agreements</h2>
<p>Nothing on this website is an offer, quote or contract. Pricing, scope, schedules, payment terms, warranties and cancellation terms for any project or maintenance plan are set out only in a written quote or contract provided to you. If there is a conflict between this website and your written contract, the contract applies.</p>
<h2>Intellectual property</h2>
<p>The text, design, graphics and logos on this website belong to us or our licensors. You may view and print pages for personal, non-commercial use, but you may not copy, reproduce or republish website content for commercial purposes without our written permission.</p>
<h2>Third-party links and services</h2>
<p>This website may link to third-party websites or use third-party services, such as our form provider. We aren't responsible for the content, terms or privacy practices of those third parties.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, we are not liable for any indirect or consequential loss arising from your use of this website or reliance on its general information or automated estimates. Nothing in these terms limits any rights you have under applicable consumer protection law.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the State of {cfg['legal_jurisdiction']} and applicable federal law of the United States.</p>
<h2>Changes and contact</h2>
<p>We may update these terms from time to time. Questions can be sent to <a href="mailto:{cfg['email']}">{cfg['email']}</a>. Our [[privacy|Privacy Policy]] explains how we handle personal information.</p>
"""

    def cookies(here):
        return f"""
<!-- CLIENT REVIEW: accurate for the template as built (no cookies, no analytics, no pixels; the instant estimate runs in the browser). If Google Analytics, Meta Pixel, Google Ads tags, chat widgets, financing or booking embeds are added, update this page and add a consent mechanism that blocks non-essential tags until the visitor agrees, where required. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<h2>Does this website use cookies?</h2>
<p>No. This website does not set cookies, and it does not use analytics, advertising pixels or other tracking technologies.</p>
<h2>Browser storage we use</h2>
<p>The website uses your browser's <em>session storage</em> to remember that the opening animation has already played during your visit, so it isn't shown again on every page. This stores a single value with no personal information, isn't shared with us or anyone else, and is cleared automatically when you close your browser tab. Because it's needed only to provide the website as you'd expect, it doesn't require consent.</p>
<h2>Third-party services</h2>
<p>When you submit one of our forms, your browser sends it to {cfg['form_provider_name']}, which delivers it to us by email. That service may display its own pages, such as a spam-protection check, and may use cookies on its own domain under its own policies. Our hosting provider may log technical information such as IP addresses for security purposes, as explained in our [[privacy|Privacy Policy]].</p>
<h2>Managing storage</h2>
<p>You can clear or block site data at any time through your browser settings. The website will continue to work, although the opening animation may play again.</p>
<h2>Changes</h2>
<p>If we add tools that use cookies or similar technologies, we will update this policy and, where required, ask for your consent before those tools run.</p>
"""

    return {
        "about": dict(title=f"About {biz}", desc=f"{biz} is a heating and cooling company serving {city_text}. Learn how we size, quote, install and service HVAC systems.", eyebrow="About us", h1="About Us", lead="A heating and cooling company built around straight answers, written prices and systems sized to the house.", inner=about, active="about"),
        "faq": dict(title="Heating & Cooling FAQ", desc=f"Answers about furnaces, air conditioners, heat pumps, repair or replace, sizing, permits, rebates and hiring an HVAC company in {city_text}.", eyebrow="FAQ", h1="Frequently Asked Questions", lead="Straight answers about heating, cooling and how we work, before you commit to anything.", inner=faq, active="faq"),
        "thanks": dict(title="Thank You", desc="Your request has been sent.", eyebrow="Request sent", h1="Thank You", lead="Your details are on their way to us.", inner=thanks, noindex=True, aside=False, cta=False, hero_ctas=False),
        "privacy": dict(title="Privacy Policy", desc=f"How {biz} collects, uses and protects personal information submitted through this website, its forms and the instant system estimate.", eyebrow="Legal", h1="Privacy Policy", lead="How we collect, use and protect your personal information.", inner=privacy, mark="doc", aside=False, cta=False, hero_ctas=False),
        "terms": dict(title="Terms and Conditions", desc=f"Terms and conditions for using the {biz} website and its instant system estimate.", eyebrow="Legal", h1="Terms and Conditions", lead="The terms that apply when you use this website.", inner=terms, mark="doc", aside=False, cta=False, hero_ctas=False),
        "cookies": dict(title="Cookie Policy", desc=f"How the {biz} website uses cookies and browser storage.", eyebrow="Legal", h1="Cookie Policy", lead="What this website stores in your browser, and what it doesn't.", inner=cookies, mark="doc", aside=False, cta=False, hero_ctas=False),
    }
