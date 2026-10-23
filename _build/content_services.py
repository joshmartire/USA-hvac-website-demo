# -*- coding: utf-8 -*-
# HVAC services. Each entry becomes a service page (500-600 words of main content together with its
# COSTS entry and FAQs) plus one page per city in content_cities.py.
#
# Tokens: {biz} = business name, {phone} = phone number, [[slug|anchor text]] = link to another service
# (or [[contact|...]], [[estimate|...]], [[area:novi|...]]). Links to services the client does not
# offer become plain text and are listed in _build/removed-service-mentions.txt for rewording.
#
# "cities" holds one short paragraph per city slug. It must be genuinely about that town, not a
# find-and-replace of the city name.
#
# Licensing notes used in the copy (Michigan / US): HVAC and gas appliance work is done by a licensed
# mechanical contractor and generally needs a mechanical permit and inspection; refrigerant work needs
# EPA Section 608 certification; new electrical circuits are done by a licensed electrician under an
# electrical permit. Re-check these if the template is used in another state.

SERVICES = [
# ------------------------------------------------------------------ HEATING
{
"slug": "furnace-installation",
"name": "Furnace Installation",
"cat": "heating",
"icon": "furnace",
"short": "High-efficiency gas furnace replacement, sized to your home and installed with the venting, gas line and ductwork checked.",
"title": "Furnace Installation & Replacement",
"desc": "High-efficiency gas furnace installation and replacement: proper sizing, venting, gas work by licensed technicians and a written, itemized quote.",
"h1": "Furnace Installation",
"lead": "A new furnace should be sized to your house, not to the old unit's sticker. We measure, quote in writing and install it like it has to last.",
"body": """
<p>An older furnace usually tells you it's tired before it quits: rooms that never quite warm up, short cycles, rising gas bills, a yellow flame, rust on the cabinet or repairs every winter. Once a furnace reaches that stage, a well-installed replacement is often the better spend. {biz} installs high-efficiency gas furnaces in homes across the region, and we start by working out what your house actually needs.</p>
<h2>What a proper installation includes</h2>
<ul>
<li><strong>Sizing, not guessing</strong> — we look at square footage, insulation, windows and how the house is used, instead of simply matching the old furnace's size.</li>
<li><strong>Venting</strong> — high-efficiency furnaces vent through PVC pipe with a proper slope and termination outside, and the old chimney is lined or capped if it's no longer used.</li>
<li><strong>Gas and electrical</strong> — the gas line, shut-off and connections are done by licensed technicians, pressure tested and inspected under the mechanical permit.</li>
<li><strong>Condensate</strong> — the drain is routed to a floor drain or a pump, so the water a high-efficiency furnace produces goes where it should.</li>
<li><strong>Return and supply</strong> — we check the plenums, filter rack and duct connections, because a new furnace on a choked duct system will never perform properly.</li>
<li><strong>Start-up and combustion check</strong> — gas pressure, temperature rise and safeties are tested, and the readings are recorded for your file.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Home visit.</strong> We look at the existing equipment, venting, ducts and gas line, and talk through comfort problems room by room.</li>
<li><strong>Written quote.</strong> Equipment, efficiency, venting work, any duct changes and add-ons are listed separately.</li>
<li><strong>Install day.</strong> Most furnace swaps take one day, and we keep the work area protected and tidy.</li>
<li><strong>Walk-through.</strong> We show you the filter, the thermostat and what to watch for, and register the warranty where the manufacturer allows.</li>
</ol>
<h2>Efficiency, explained simply</h2>
<p>High-efficiency furnaces turn most of the gas they burn into heat for your home. Two-stage and modulating models also run on low most of the time, which means quieter operation and fewer temperature swings.</p>
<p>Planning cooling at the same time? Pairing a furnace with [[ac-installation|central air]] or a [[heat-pumps|heat pump]] usually saves a second visit. For a ballpark first, try the [[estimate|instant system estimate]].</p>
""",
"faqs": [
("How long does a furnace installation take?", "Most straightforward replacements are done in one day. New venting routes, duct changes or adding cooling at the same time can add a day."),
("Is a bigger furnace better?", "No. An oversized furnace heats in short bursts, which wastes fuel, wears parts faster and leaves cold spots. Right-sized equipment runs longer, steadier cycles."),
("Will I be without heat?", "Only for part of the install day. In very cold weather we plan the work so heat is restored the same day."),
],
"related": ["furnace-repair", "smart-thermostats", "indoor-air-quality"],
"cities": {
"novi": "Many Novi homes were built during the city's big growth years from the late 1980s through the 2000s, and a lot of those subdivisions still have their first or second furnace. These two-story colonials usually have roomy basements and an easy side-wall route for PVC venting, so most replacements are done in a single day.",
"troy": "Troy's 1960s and 1970s ranches, colonials and tri-levels often have furnaces that were replaced once already, sometimes with a unit sized for a house that has since gained new windows and insulation. We recalculate the size, and on tri-levels we look closely at how the ductwork feeds the upper and lower levels.",
"canton": "Canton grew quickly from the 1980s onward, so whole neighborhoods have furnaces of the same age wearing out together. Larger Canton homes with finished basements often need more careful sizing and return air planning than the original builder setup allowed."
},
},
{
"slug": "furnace-repair",
"name": "Furnace Repair",
"cat": "heating",
"icon": "repair",
"short": "Diagnosis and repair for furnaces that won't start, short cycle, blow cold air or make new noises.",
"title": "Furnace Repair & No-Heat Service",
"desc": "Furnace repair for no heat, short cycling, ignition faults, noisy blowers and error codes. Licensed technicians and written repair prices.",
"h1": "Furnace Repair",
"lead": "No heat, cold air, clicking with no flame or a blinking light on the board. We find the actual cause, explain it and price the fix before we do it.",
"body": """
<p>Furnaces rarely fail at a convenient time. The good news is that many no-heat calls come down to a handful of parts: a dirty flame sensor, a failed igniter, a blocked condensate drain, a tripped pressure switch or a clogged filter that's caused the furnace to overheat and shut itself off. {biz} diagnoses the problem properly, tells you what failed and why, and gives you the repair price before any work starts.</p>
<h2>Common furnace problems we fix</h2>
<ul>
<li><strong>No heat or no ignition</strong> — igniters, flame sensors, gas valves, inducer motors and control boards.</li>
<li><strong>Short cycling</strong> — furnaces that start and stop every few minutes, often from overheating, a dirty filter or sensor issues.</li>
<li><strong>Blowing cold air</strong> — failed ignition, a tripped high-limit switch or a thermostat set to fan only.</li>
<li><strong>Noises and smells</strong> — squealing, banging or rattling blowers, and burning or electrical smells that need to be checked right away.</li>
<li><strong>Water around the furnace</strong> — blocked condensate lines, failed pumps or a leaking humidifier.</li>
<li><strong>Error codes</strong> — we read the board's fault history so the repair addresses the cause, not just the symptom.</li>
</ul>
<h2>What to check before you call</h2>
<ol>
<li><strong>Thermostat.</strong> Make sure it's set to heat, the set point is above room temperature and the batteries aren't dead.</li>
<li><strong>Power.</strong> Check the furnace switch (it often looks like a light switch) and the breaker.</li>
<li><strong>Filter.</strong> A badly clogged filter can shut a furnace down. Replace it if it's gray and caked.</li>
<li><strong>Vents outside.</strong> On high-efficiency furnaces, make sure the intake and exhaust pipes outside aren't blocked by snow or ice.</li>
</ol>
<h2>When a repair stops making sense</h2>
<p>If the furnace is near the end of its expected life, needs an expensive part or has needed several repairs in a few years, we'll show you the replacement price next to the repair so you can decide with real numbers.</p>
<p>If you smell gas, leave the house and call your gas utility's emergency line from outside. If the furnace is old and repairs keep adding up, ask us about [[furnace-installation|furnace replacement]], or keep the next one away with [[hvac-maintenance|annual maintenance]].</p>
""",
"faqs": [
("Should I repair or replace my furnace?", "If the furnace is younger and the repair is modest, repair usually makes sense. When it's older and needs an expensive part, compare the repair against a replacement. We'll show you both numbers."),
("Why does my furnace keep turning off?", "Overheating from a dirty filter or blocked returns, a dirty flame sensor and condensate drain problems are the most common causes. The board's fault codes usually point the way."),
("Is a clicking furnace dangerous?", "Clicking with no flame usually means an ignition problem. Turn the furnace off and have it checked rather than resetting it over and over."),
],
"related": ["furnace-installation", "hvac-maintenance", "smart-thermostats"],
"cities": {
"novi": "On Novi's 1990s and 2000s furnaces, the most common repairs are failed hot surface igniters, dirty flame sensors and worn inducer motors. Deep cold snaps also expose weak parts quickly, which is why calls spike the first week temperatures drop near zero.",
"troy": "Older Troy furnaces, especially in tri-levels and ranches with long duct runs, often overheat because of restricted return air, which looks like random shutdowns. We check airflow as part of the repair, not just the part that failed.",
"canton": "In Canton's subdivisions, many furnaces are at the age where a second major repair is due, such as a control board or blower motor. When that happens, we show you the replacement price alongside the repair so you can compare."
},
},
{
"slug": "heat-pumps",
"name": "Heat Pumps",
"cat": "heating",
"icon": "heatpump",
"short": "Cold-climate air source heat pumps for heating and cooling, on their own or paired with a gas furnace as a hybrid system.",
"title": "Heat Pump Installation: Cold-Climate & Hybrid",
"desc": "Cold-climate heat pump installation for heating and cooling, including hybrid systems paired with a gas furnace. Proper sizing and written quotes.",
"h1": "Heat Pumps",
"lead": "One system that heats and cools. Today's cold-climate heat pumps keep working well below freezing, and a hybrid setup lets the furnace take over on the coldest nights.",
"body": """
<p>A heat pump moves heat instead of making it. In summer it works like an air conditioner, pulling heat out of the house. In winter it runs in reverse, pulling heat from the outdoor air, even when it's well below freezing, and bringing it inside. {biz} installs ducted and ductless heat pumps, and we'll be straight with you about whether one makes sense for your home and your gas and electricity costs.</p>
<h2>Heat pump options</h2>
<ul>
<li><strong>Ducted heat pumps</strong> — replace a central air conditioner and use your existing ductwork to heat and cool the whole house.</li>
<li><strong>Hybrid (dual fuel) systems</strong> — a heat pump paired with a gas furnace. The heat pump handles mild and moderate weather, and the furnace takes over below a set outdoor temperature.</li>
<li><strong>Cold-climate models</strong> — variable-speed units designed to keep producing useful heat in deep cold, not just in shoulder seasons.</li>
<li><strong>Ductless systems</strong> — for homes, additions or garages without ducts, see [[ductless-mini-splits|ductless mini-splits]].</li>
</ul>
<h2>What we look at before recommending one</h2>
<ol>
<li><strong>Heat loss.</strong> How much heat the house needs on a cold night, so the heat pump and backup heat are sized properly.</li>
<li><strong>Ductwork.</strong> Heat pumps move more air at lower supply temperatures, so undersized ducts and weak returns matter more.</li>
<li><strong>Electrical capacity.</strong> Your panel needs room for the new circuit, which is installed by a licensed electrician.</li>
<li><strong>Controls.</strong> A compatible thermostat and a sensible switchover point between the heat pump and the furnace.</li>
<li><strong>Placement.</strong> The outdoor unit needs a raised base above snow, clearance and a spot away from bedroom windows.</li>
</ol>
<h2>Hybrid or all-electric?</h2>
<p>Most homes with gas keep the furnace as backup and let the heat pump do most of the work. Homes without gas often go all-electric with a cold-climate heat pump and electric backup. We'll walk you through both setups using your home's numbers, not a sales pitch.</p>
<p>Rebate and financing programs for heat pumps change often, so we check what's currently available when we quote. Most heat pump jobs are paired with a [[furnace-installation|furnace]] or a [[smart-thermostats|new thermostat]].</p>
""",
"faqs": [
("Do heat pumps work in Michigan winters?", "Cold-climate models keep heating well below freezing. In a hybrid system, the gas furnace takes over during the coldest stretches, so comfort doesn't depend on the outdoor temperature."),
("Can a heat pump replace my air conditioner?", "Yes. A ducted heat pump cools like a central air conditioner in summer and adds efficient heating for the rest of the year."),
("Will my electricity bill go up?", "Usually, while your gas use goes down. Whether you save overall depends on the equipment, your home and current energy prices, which we walk through with you."),
],
"related": ["ac-installation", "ductless-mini-splits", "furnace-installation"],
"cities": {
"novi": "Novi's newer two-story homes are often strong heat pump candidates: ducted systems in good shape, newer electrical panels and central air conditioners near the end of their life. Replacing that air conditioner with a heat pump and keeping the gas furnace for the coldest nights is the setup we quote most here.",
"troy": "In Troy's older ranches and tri-levels, a heat pump usually means a closer look at duct sizing and the electrical panel first. A hybrid setup that keeps the furnace for deep cold snaps suits Michigan winters and keeps comfort steady when temperatures drop below zero.",
"canton": "Canton's 1990s homes often have an air conditioner and furnace aging together, which makes it a natural time to consider a heat pump. We place the outdoor unit on a raised stand above drifting snow and away from bedroom windows."
},
},
{
"slug": "boiler-services",
"name": "Boiler Services",
"cat": "heating",
"icon": "boiler",
"short": "Repair, maintenance and replacement for hot water boilers and radiant heating systems, including high-efficiency combi boilers.",
"title": "Boiler Repair, Maintenance & Replacement",
"desc": "Hot water boiler repair, maintenance and replacement, including high-efficiency and combi boilers for radiators and in-floor radiant heating.",
"h1": "Boiler Services",
"lead": "Radiators and in-floor heat give the most even warmth there is, when the boiler behind them is set up right. We service, repair and replace hot water boilers.",
"body": """
<p>Hot water heating is quiet, even and comfortable, and a lot of older homes and newer custom builds still rely on it. Boilers also have their own set of problems: air in the lines, cold radiators, pressure that keeps climbing, leaking valves and pumps that hum but don't move water. {biz} works on hot water boiler systems, from cast iron radiators to in-floor radiant loops.</p>
<h2>Boiler work we do</h2>
<ul>
<li><strong>Repairs</strong> — circulator pumps, zone valves, pressure relief valves, expansion tanks, ignition and controls.</li>
<li><strong>Annual maintenance</strong> — combustion check, cleaning, safety testing, pressure and expansion tank checks, and bleeding air from the system.</li>
<li><strong>Replacement</strong> — high-efficiency condensing boilers sized to the actual heat loss, often much smaller than the original boiler.</li>
<li><strong>Combi boilers</strong> — one wall-hung unit that heats the house and supplies on-demand hot water, freeing up floor space.</li>
<li><strong>Radiant floors</strong> — mixing valves, zoning and controls for in-floor heating in basements, bathrooms and additions.</li>
</ul>
<h2>Signs your boiler needs attention</h2>
<ol>
<li><strong>Cold radiators or zones.</strong> Often trapped air, a stuck zone valve or a failing circulator.</li>
<li><strong>Pressure creeping up.</strong> A waterlogged expansion tank or a leaking fill valve, which can make the relief valve discharge.</li>
<li><strong>Banging or gurgling.</strong> Air in the system or scale in the boiler.</li>
<li><strong>Frequent short cycling.</strong> Common with oversized boilers and poorly set controls.</li>
<li><strong>Leaks or rust.</strong> Around fittings, valves or the boiler itself.</li>
</ol>
<h2>Why replacement boilers are often smaller</h2>
<p>Many older boilers were sized generously for drafty houses with single-pane windows. After insulation and window upgrades, the house needs much less heat. A modern condensing boiler sized to today's heat loss, with outdoor reset control, runs longer and cooler cycles, which is exactly where it's most efficient. That's why we calculate the load rather than matching the old nameplate, and why we check the radiators and piping before choosing equipment. Good piping and controls matter as much as the boiler itself.</p>
<p>Thinking about adding cooling to a house with radiators? [[ductless-mini-splits|Ductless mini-splits]] are the usual answer. For hot water on its own, see our [[water-heaters|water heater]] services.</p>
""",
"faqs": [
("How often should a boiler be serviced?", "Once a year, ideally before the heating season. A yearly check catches pressure, expansion tank and combustion problems before they turn into a no-heat call."),
("Why are some radiators cold?", "Trapped air is the most common reason, followed by stuck valves and circulator problems. Bleeding radiators helps, but repeated air usually points to another issue."),
("Can I switch from a boiler to a furnace?", "It's possible but involves installing ductwork throughout the house. Most homeowners keep hot water heat and add ductless cooling instead."),
],
"related": ["water-heaters", "ductless-mini-splits", "hvac-maintenance"],
"cities": {
"novi": "Novi boiler work is often on radiant floor systems in custom homes, finished basements and garages, along with the occasional older lakefront home with baseboard hot water heat. Mixing valves, zone controls and expansion tanks are the parts that most often need attention.",
"troy": "A number of Troy's older homes and custom builds still use hot water baseboard or radiant heat. Many are running on boilers sized decades ago, and a properly sized high-efficiency boiler can cut fuel use noticeably.",
"canton": "Boilers are less common in Canton's forced-air subdivisions, but custom homes and older farmhouses at the edges of the township do use them. On those, we check the venting, the boiler's age and whether a combi boiler could also replace the water heater."
},
},
# ------------------------------------------------------------------ COOLING
{
"slug": "ac-installation",
"name": "AC Installation",
"cat": "cooling",
"icon": "ac",
"short": "Central air conditioner installation and replacement, matched to your furnace and ductwork and installed by certified refrigerant technicians.",
"title": "Air Conditioner Installation & Replacement",
"desc": "Central air conditioner installation and replacement: proper sizing, matched coil, refrigerant work by certified technicians and written quotes.",
"h1": "AC Installation",
"lead": "Central air that cools the whole house evenly and pulls the humidity out, not just a loud box that runs all afternoon.",
"body": """
<p>Air conditioners usually don't fail in May. They fail in the first real heat wave, when everyone else's does too. If your air conditioner is old, uses the phased-out R-22 refrigerant, struggles to keep up or needs refrigerant topped up every summer, planning a replacement before the hot weather saves a lot of sweating. {biz} installs central air conditioners matched to your furnace, your ductwork and the way your home gains heat.</p>
<h2>What a proper AC installation includes</h2>
<ul>
<li><strong>Sizing</strong> — based on the house, its windows and sun exposure, not just square footage. An oversized unit cools quickly but leaves the air damp.</li>
<li><strong>Matched indoor coil</strong> — the coil on top of the furnace is matched to the outdoor unit, so the system reaches its rated efficiency.</li>
<li><strong>Line set</strong> — refrigerant lines are replaced or flushed, insulated and properly supported.</li>
<li><strong>Refrigerant work</strong> — pressure tested, evacuated with a vacuum pump and charged to the manufacturer's specification by certified technicians.</li>
<li><strong>Electrical and pad</strong> — a proper disconnect, a level pad and clearance around the outdoor unit for airflow.</li>
<li><strong>Drainage</strong> — the coil's condensate drain is routed properly so summer moisture doesn't end up on the basement floor.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Home visit.</strong> We check the furnace, ductwork, electrical and where the outdoor unit can go.</li>
<li><strong>Written quote.</strong> Equipment options, efficiency levels and any electrical or duct work are listed separately.</li>
<li><strong>Install day.</strong> Most replacements are done in a day, including start-up and testing.</li>
<li><strong>Walk-through.</strong> We show you the filter, thermostat settings and how to keep the outdoor unit clear.</li>
</ol>
<h2>Refrigerant and efficiency</h2>
<p>New air conditioners use newer refrigerants and are rated for seasonal efficiency. Higher-efficiency and variable-speed models cost more up front but run more quietly, remove more humidity and cost less to operate through a long, hot summer.</p>
<p>If you're replacing the air conditioner anyway, a [[heat-pumps|heat pump]] adds efficient heating for not much more. For homes without ducts, see [[ductless-mini-splits|ductless mini-splits]], or get a ballpark with the [[estimate|instant system estimate]].</p>
""",
"faqs": [
("What size air conditioner do I need?", "It depends on the house, not just square footage. Insulation, windows, sun exposure and ductwork all matter, which is why we size on site."),
("Can I replace just the outdoor unit?", "Usually not. Modern outdoor units need a matched indoor coil and often a new or flushed line set to work properly and keep their warranty."),
("When should I replace an air conditioner?", "Spring and fall, before the rush. Installations are easier to schedule and you aren't waiting in the heat."),
],
"related": ["ac-repair", "heat-pumps", "indoor-air-quality"],
"cities": {
"novi": "Novi's larger two-story homes often have a hot second floor in July and August. Proper sizing, return air upstairs and a variable-speed blower solve that more reliably than simply installing a bigger outdoor unit.",
"troy": "Many Troy air conditioners are older units on discontinued R-22 refrigerant, especially in 1970s and 1980s homes. With the furnace often the same age, replacing both together, or switching to a heat pump, is worth pricing out.",
"canton": "Metro Detroit summers are humid, and Canton's newer, tighter homes feel it when an oversized air conditioner cools quickly but leaves the air clammy. We size equipment to run steady cycles that pull out the humidity."
},
},
{
"slug": "ac-repair",
"name": "AC Repair",
"cat": "cooling",
"icon": "acrepair",
"short": "Air conditioner repair for warm air, frozen coils, leaks, tripped breakers and outdoor units that hum but won't start.",
"title": "Air Conditioner Repair & No-Cool Service",
"desc": "Air conditioner repair for warm air, frozen coils, refrigerant leaks, failed capacitors and noisy outdoor units. Written repair prices before work.",
"h1": "AC Repair",
"lead": "Warm air from the vents, ice on the lines or an outdoor unit that just hums. We diagnose it properly and tell you whether it's worth fixing.",
"body": """
<p>Most air conditioner breakdowns come from a short list of causes: a failed capacitor or contactor, a dirty outdoor coil, a clogged filter freezing the indoor coil, a blocked drain or a slow refrigerant leak. {biz} finds the cause, explains it in plain language and gives you the price before we start, along with an honest opinion on whether the system is worth repairing.</p>
<h2>Common air conditioner problems we fix</h2>
<ul>
<li><strong>Blowing warm air</strong> — failed capacitors, contactors or outdoor fan motors, and compressors that won't start.</li>
<li><strong>Frozen lines or coil</strong> — usually poor airflow from a dirty filter or coil, or low refrigerant.</li>
<li><strong>Refrigerant leaks</strong> — leaks are found and repaired before recharging, rather than topping up year after year.</li>
<li><strong>Water leaks indoors</strong> — blocked condensate drains, cracked pans and failed condensate pumps.</li>
<li><strong>Tripped breakers</strong> — electrical faults and failing components that pull too much current.</li>
<li><strong>Noise</strong> — rattling panels, failing fan motors and banging at start-up.</li>
</ul>
<h2>What to check before you call</h2>
<ol>
<li><strong>Thermostat.</strong> Set to cool, set below room temperature, fan on auto.</li>
<li><strong>Filter.</strong> A clogged filter can freeze the coil. If the lines are iced, turn cooling off and run the fan to thaw.</li>
<li><strong>Power.</strong> Check the breaker and the disconnect switch beside the outdoor unit.</li>
<li><strong>Outdoor unit.</strong> Clear away grass clippings, leaves and anything stacked against it.</li>
</ol>
<h2>Repair or replace?</h2>
<p>A failed capacitor or contactor on a younger system is an easy repair. A compressor failure, a large leak or an older system on discontinued R-22 refrigerant is different. In those cases, we'll give you the repair price and a replacement option side by side, explain the trade-offs and let you decide. We don't recharge a leaking system over and over without telling you where the refrigerant is going. If the system is worth keeping, we'll also suggest the maintenance that helps it last.</p>
<p>If your system is old and needs a major part, compare the repair against [[ac-installation|a new air conditioner]] or a [[heat-pumps|heat pump]]. Yearly [[hvac-maintenance|maintenance]] catches most of these problems early.</p>
""",
"faqs": [
("Why is my AC running but not cooling?", "A failed outdoor fan or capacitor, a dirty coil, a frozen indoor coil and low refrigerant are the most common causes. Turn the system off if the lines are iced."),
("Is it worth recharging an old R-22 system?", "R-22 has been phased out, so recharging is expensive and the leak will likely return. For older R-22 systems, replacement usually makes more sense."),
("How fast can you come out?", "It depends on the season and the schedule. Call us and we'll give you an honest time rather than a vague window."),
],
"related": ["ac-installation", "hvac-maintenance", "ductless-mini-splits"],
"cities": {
"novi": "During Novi heat waves, outdoor units run almost nonstop, and capacitors and contactors are the parts that fail first. Cottonwood fluff and grass clippings also clog outdoor coils, which pushes pressures up and shortens component life.",
"troy": "On Troy's older air conditioners, we often find R-22 systems with slow leaks, worn contactors and condensate drains that clog every summer. When the repair involves refrigerant on an older system, we show you the replacement option alongside it.",
"canton": "Canton's builder-installed air conditioners from the 1990s and 2000s commonly need capacitors, fan motors and drain line repairs. On larger homes, we also see frozen coils caused by too little return air upstairs."
},
},
{
"slug": "ductless-mini-splits",
"name": "Ductless Mini-Splits",
"cat": "cooling",
"icon": "minisplit",
"short": "Ductless heat pumps for additions, garages, finished basements and homes with radiators, with one or several indoor zones.",
"title": "Ductless Mini-Split Heat Pumps & AC",
"desc": "Ductless mini-split heat pumps and air conditioners for homes with radiators, additions, garages and basements. Single and multi-zone installations.",
"h1": "Ductless Mini-Splits",
"lead": "Heating and cooling with no ductwork. One outdoor unit, one or more slim indoor heads, and each room controlled on its own.",
"body": """
<p>A ductless mini-split is a heat pump that delivers heating and cooling straight into the room through an indoor head mounted on the wall or ceiling. It's the most practical way to cool a house with radiators, fix a room that's always too hot or cold, or heat and cool an addition, garage or sunroom without extending ductwork. {biz} installs single-zone and multi-zone systems and plans the layout around how you use each space.</p>
<h2>Where mini-splits make the most sense</h2>
<ul>
<li><strong>Homes with radiators</strong> — central-air comfort without opening walls to run ducts.</li>
<li><strong>Additions and sunrooms</strong> — rooms the existing system was never sized to handle.</li>
<li><strong>Bonus rooms and upper floors</strong> — the hot room over the garage or the top floor that never cools down.</li>
<li><strong>Finished basements and garages</strong> — workshops, gyms and suites that need their own control.</li>
<li><strong>Homes on electric baseboard</strong> — far more efficient heating, plus cooling as a bonus.</li>
</ul>
<h2>How we plan an install</h2>
<ol>
<li><strong>Room by room.</strong> We work out the heating and cooling each space needs, so heads aren't oversized for small rooms.</li>
<li><strong>Head placement.</strong> Wall, ceiling or floor units placed for even airflow, not just where the wall is easiest.</li>
<li><strong>Line set routing.</strong> Refrigerant lines and drains run neatly, with exterior line covers to protect and tidy them.</li>
<li><strong>Outdoor unit.</strong> On a raised stand or wall bracket, clear of snow and drip lines.</li>
<li><strong>Electrical.</strong> A dedicated circuit by a licensed electrician.</li>
</ol>
<h2>Living with a mini-split</h2>
<p>Each indoor head has its own remote or app control, so a bedroom can stay cooler at night while the living room stays comfortable. The indoor filters should be rinsed every few weeks during heavy use, and the outdoor unit kept clear of snow and debris. Because these systems are heat pumps, they also provide efficient heating in spring and fall, which can take a lot of load off the main heating system and lower what it costs to run.</p>
<p>For whole-home systems that use existing ducts, see [[heat-pumps|ducted heat pumps]]. Mini-splits are a common partner for [[boiler-services|hot water heating]].</p>
""",
"faqs": [
("How many indoor heads do I need?", "Usually one per room or open area you want to control. Open-concept spaces may need just one; separate bedrooms usually need their own."),
("Can a mini-split heat in winter?", "Yes. Cold-climate mini-splits heat well below freezing. In very cold weather, the house's existing heat can supplement it."),
("Do mini-splits need cleaning?", "Yes. Indoor filters should be rinsed regularly, and the coils and blower wheel need professional cleaning periodically to keep airflow and air quality up."),
],
"related": ["heat-pumps", "boiler-services", "ac-installation"],
"cities": {
"novi": "In Novi, mini-split calls are usually for rooms the main system doesn't handle well: a hot bonus room over the garage, a finished basement suite or a sunroom. A single-zone unit solves the problem without oversizing the whole system for one room.",
"troy": "Troy homes with hot water heat and no ductwork are good mini-split candidates, along with additions and converted garages. A two- or three-zone ductless system adds real central-air comfort without opening walls and ceilings.",
"canton": "Canton homeowners often add ductless systems to finished basements, home offices and garages used as gyms or workshops. Because they are heat pumps, they also provide efficient heat in spring and fall."
},
},
# ------------------------------------------------------------------ AIR QUALITY & DUCTWORK
{
"slug": "indoor-air-quality",
"name": "Indoor Air Quality",
"cat": "air",
"icon": "air",
"short": "Filtration, humidifiers, dehumidifiers, ventilation and air cleaners that work with your furnace to improve the air you breathe.",
"title": "Indoor Air Quality: Filtration, Humidity & Ventilation",
"desc": "Whole-home air filtration, humidifiers, dehumidifiers, HRVs and ERVs that work with your furnace. Practical air quality upgrades with written quotes.",
"h1": "Indoor Air Quality",
"lead": "Dry winter air, damp summer basements, dust that comes back the day after you clean. Most of it can be fixed at the furnace.",
"body": """
<p>Your heating and cooling system moves all the air in your house several times an hour, which makes it the ideal place to clean it, add moisture or take moisture out. {biz} installs whole-home air quality equipment that works with your furnace and ductwork, and we start by finding out what's actually bothering you instead of selling every product at once.</p>
<h2>Air quality upgrades we install</h2>
<ul>
<li><strong>Better filtration</strong> — media air cleaners with deep pleated filters that trap far more dust and pollen than a thin filter, without choking airflow.</li>
<li><strong>Whole-home humidifiers</strong> — bypass, fan-powered and steam models that ease dry skin, static and cracking wood floors in winter.</li>
<li><strong>Dehumidification</strong> — whole-home dehumidifiers for damp basements and sticky summers, and proper cooling setup to remove more moisture.</li>
<li><strong>Fresh air ventilation</strong> — heat and energy recovery ventilators (HRVs and ERVs) that bring in outside air while keeping most of the heat.</li>
<li><strong>UV lights</strong> — mounted at the cooling coil to keep it clean and limit growth on wet surfaces.</li>
</ul>
<h2>How we figure out what you need</h2>
<ol>
<li><strong>Symptoms first.</strong> Dust, dryness, condensation on windows, musty smells, allergies or stuffiness each point to a different fix.</li>
<li><strong>Measure humidity.</strong> We check indoor humidity, because too much moisture causes as many problems as too little.</li>
<li><strong>Check the system.</strong> Filter fit, duct leaks and return air paths often matter more than any add-on.</li>
<li><strong>Recommend the fewest products.</strong> Usually one or two well-chosen upgrades solve the problem.</li>
</ol>
<h2>What we won't sell you</h2>
<p>Air quality is an easy place to oversell. We don't recommend equipment without a clear reason, and we'll tell you when a simple fix, such as a properly fitted filter, a sealed return or running the fan differently, will do more than another gadget. If something we install isn't solving the problem you called about, we want to know, so we can make it right.</p>
<p>Dirty or leaky ducts can undo good filtration, so we may suggest [[duct-cleaning|duct cleaning]] or [[ductwork|duct repairs]] first. Most air quality equipment can be added during a [[furnace-installation|furnace installation]].</p>
""",
"faqs": [
("What indoor humidity should I aim for?", "Roughly 30 to 45 percent in winter, lower on very cold days to avoid window condensation, and under about 50 percent in summer."),
("Will a better filter hurt my furnace?", "A thick media filter in a proper cabinet improves filtration without restricting airflow. Forcing a dense filter into a thin slot can, which is why the cabinet matters."),
("Do I need an HRV?", "Tighter homes and newer builds often benefit from one, especially if you see condensation, stale air or lingering odours. We check before recommending it."),
],
"related": ["duct-cleaning", "ductwork", "hvac-maintenance"],
"cities": {
"novi": "Novi's newer, tighter homes tend to struggle with stale air, window condensation in winter and dry air from long heating cycles. Fresh air ventilation and properly controlled humidifiers do the most good in these houses.",
"troy": "Older Troy homes can have the opposite issue: damp basements in humid summers and musty smells drawn into the return air. Dehumidification and better cooling setup usually help more than any air purifier.",
"canton": "Canton homes near open land and new construction see more dust and pollen during building seasons and spring, which makes filtration upgrades popular. We check filter fit and return air leaks before recommending equipment."
},
},
{
"slug": "ductwork",
"name": "Ductwork",
"cat": "air",
"icon": "duct",
"short": "Duct design, repair, sealing and new runs that fix hot and cold rooms, weak airflow and noisy vents.",
"title": "Ductwork Installation, Repair & Sealing",
"desc": "Ductwork design, new runs, repairs and sealing to fix hot and cold rooms, weak airflow, noisy vents and undersized returns. Written quotes.",
"h1": "Ductwork",
"lead": "The furnace makes the heat. The ducts decide where it goes. Fix the ducts and the rooms that never feel right usually start behaving.",
"body": """
<p>Hot and cold rooms, whistling vents, a basement that's warm while the bedrooms freeze, a furnace that sounds like a jet engine: these are often duct problems, not equipment problems. Undersized returns, crushed or disconnected runs, long flexible ducts and leaky joints all rob airflow before it reaches the rooms. {biz} designs, repairs and modifies ductwork so the system you paid for can actually deliver.</p>
<h2>Ductwork services</h2>
<ul>
<li><strong>Airflow diagnosis</strong> — we measure what's coming out of the registers and check static pressure to find where the system is choking.</li>
<li><strong>Return air upgrades</strong> — adding or enlarging returns is one of the most effective fixes for hot upper floors and noisy systems.</li>
<li><strong>New runs and relocations</strong> — for renovations, finished basements, additions and rooms that never had enough supply.</li>
<li><strong>Sealing and insulation</strong> — sealing joints with mastic or foil tape, and insulating ducts that pass through unheated spaces.</li>
<li><strong>Balancing dampers</strong> — so air can be split properly between floors as the seasons change.</li>
<li><strong>Zoning</strong> — motorized dampers and separate thermostats for homes with very different needs from floor to floor.</li>
</ul>
<h2>How we approach it</h2>
<ol>
<li><strong>Find the problem.</strong> We look at the rooms, the registers, the returns and the duct layout before suggesting changes.</li>
<li><strong>Fix the biggest restriction first.</strong> Often a single return or a crushed trunk line makes the largest difference.</li>
<li><strong>Quote in writing.</strong> Each change is listed so you can do the work in stages if you prefer.</li>
<li><strong>Re-test.</strong> After the work, we measure again so you know it made a difference.</li>
</ol>
<h2>Signs your ducts are the problem</h2>
<p>Rooms far from the furnace that never get enough air, a system that roars when the blower starts, dust collecting around registers and big temperature differences between floors all point to ductwork rather than equipment. In many homes, fixing the ducts costs less than the new furnace someone else quoted.</p>
<p>Replacing equipment? That's the ideal time to correct the ducts too, whether that's a new [[furnace-installation|furnace]] or a [[heat-pumps|heat pump]], which is more sensitive to airflow. Older ducts may also need [[duct-cleaning|a cleaning]].</p>
""",
"faqs": [
("Why is my upstairs always hotter?", "Heat rises, but weak return air upstairs is often the bigger cause. Adding returns, balancing dampers and running the fan more usually help a lot."),
("Is flexible duct bad?", "Short, well-supported runs are fine. Long, sagging or crushed flex duct restricts airflow badly and is a common cause of weak rooms."),
("Can ductwork be added to a finished basement?", "Usually, by tapping into existing trunks and routing through bulkheads or joist spaces. We check that the furnace can handle the extra load."),
],
"related": ["duct-cleaning", "indoor-air-quality", "furnace-installation"],
"cities": {
"novi": "In Novi's two-story subdivision homes, the classic complaint is a hot second floor and a cold basement. Builder duct systems often have too few returns upstairs and no balancing dampers, both of which are fixable without major work.",
"troy": "Troy's tri-levels and ranches with additions often have rooms at the far end of long duct runs that never get enough air. Adding returns, resizing a branch or balancing the system usually makes the biggest difference.",
"canton": "Canton homes with finished basements and bonus rooms often have spaces that were tacked onto the duct system as an afterthought. We look at whether the existing trunks can carry the extra air or whether a separate solution makes more sense."
},
},
{
"slug": "duct-cleaning",
"name": "Duct Cleaning",
"cat": "air",
"icon": "ductclean",
"short": "Whole-system duct cleaning with negative air pressure, including returns, supplies, the blower and the furnace cabinet.",
"title": "Air Duct Cleaning for Homes",
"desc": "Air duct cleaning with negative air pressure: supply and return ducts, registers, blower and furnace cabinet. Honest advice on when it's worth it.",
"h1": "Duct Cleaning",
"lead": "Renovation dust, years of pet hair, a new house full of drywall debris. When ducts really need cleaning, we clean the whole system, not just the vents you can see.",
"body": """
<p>Duct cleaning isn't something every home needs every year, and we'll tell you if yours doesn't. It does make a real difference after renovations, in new homes full of construction dust, when you move into a house with pets or smokers before you, or when you can see debris and buildup in the ducts. {biz} cleans the entire air system so the dust doesn't simply get blown back into the house.</p>
<h2>What a proper duct cleaning includes</h2>
<ul>
<li><strong>Negative air pressure</strong> — a powerful vacuum connected to the system keeps loosened debris moving out, not into your rooms.</li>
<li><strong>Agitation</strong> — brushes, air whips and compressed air break buildup loose from the inside of supply and return ducts.</li>
<li><strong>Every run</strong> — supply and return ducts, trunk lines and the branch runs to each room.</li>
<li><strong>Registers and grilles</strong> — removed where practical and cleaned.</li>
<li><strong>Blower and cabinet</strong> — the furnace blower wheel and cabinet, which collect some of the heaviest buildup.</li>
<li><strong>A fresh filter</strong> — so the clean system starts with clean filtration.</li>
</ul>
<h2>When duct cleaning makes sense</h2>
<ol>
<li><strong>After renovations.</strong> Drywall and sawdust gets into ducts even when registers are covered.</li>
<li><strong>New construction.</strong> Builders' debris is common in brand-new duct systems.</li>
<li><strong>Visible buildup.</strong> Dust or debris you can see inside the registers or ducts.</li>
<li><strong>Pests or odours.</strong> Signs of rodents or insects, or persistent smells from the vents.</li>
<li><strong>Moving in.</strong> A fresh start in a home where you don't know the history.</li>
</ol>
<h2>What we won't do</h2>
<p>We don't sell duct cleaning as an automatic yearly service, and we don't use scare tactics about mold or air quality to sell it. If your ducts are reasonably clean, we'll tell you so and suggest a better use of your money, such as a filter upgrade. If they do need cleaning, you'll see photos of the buildup before and after the work, so you know exactly what you paid for.</p>
<p>Cleaning pays off most alongside good [[indoor-air-quality|filtration]]. If we find disconnected or leaky runs while cleaning, we'll show you photos and quote [[ductwork|duct repairs]] separately.</p>
""",
"faqs": [
("How often should ducts be cleaned?", "There's no fixed schedule. Clean them after renovations, when you can see buildup or when there's a specific problem, rather than on an automatic yearly basis."),
("How long does duct cleaning take?", "Most homes take a few hours, depending on the size of the house, the number of runs and how much buildup there is."),
("Will duct cleaning fix allergies?", "It can help when the ducts are dirty, but filtration and humidity control usually have a bigger long-term effect on airborne allergens."),
],
"related": ["indoor-air-quality", "ductwork", "hvac-maintenance"],
"cities": {
"novi": "New construction and recent renovations are the most common reasons we clean ducts in Novi. Drywall dust and builders' debris turn up in brand-new systems, and cleaning them before you move in is worthwhile.",
"troy": "Troy's older homes have often been through several rounds of remodeling, each adding plaster dust, drywall or sawdust to the ductwork. Large old return ducts in these homes can hold buildup that a quick vent cleaning won't reach.",
"canton": "In Canton, duct cleaning calls often follow basement finishing projects or move-ins to homes with pets or smokers before you. We'll tell you honestly if your ducts don't need it."
},
},
# ------------------------------------------------------------------ MAINTENANCE & MORE
{
"slug": "hvac-maintenance",
"name": "HVAC Maintenance",
"cat": "care",
"icon": "maint",
"short": "Annual furnace and air conditioner tune-ups with safety checks, cleaning and a written report on the system's condition.",
"title": "Furnace & AC Maintenance and Tune-Ups",
"desc": "Annual furnace and air conditioner maintenance: combustion and safety checks, cleaning, airflow and refrigerant checks, with a written condition report.",
"h1": "HVAC Maintenance",
"lead": "A yearly check costs far less than a breakdown. It catches the small stuff before it becomes a no-heat call in January.",
"body": """
<p>Most heating and cooling breakdowns start as something small: a dirty flame sensor, a weak capacitor, a partly blocked drain or a filter that's been in too long. A proper tune-up finds those before they leave you without heat or cooling, keeps the equipment running efficiently and gives you a record of its condition. {biz} services furnaces, air conditioners, heat pumps and boilers, and every visit comes with a written summary of what we found.</p>
<h2>Furnace maintenance</h2>
<ul>
<li><strong>Combustion and safety</strong> — burners, flame sensor, ignition, heat exchanger inspection, venting, pressure switches and safety limits.</li>
<li><strong>Gas pressure and temperature rise</strong> — checked against the manufacturer's specifications.</li>
<li><strong>Blower and airflow</strong> — blower wheel, motor and filter checked so the system isn't straining.</li>
<li><strong>Condensate</strong> — drain lines, trap and pump cleared before winter.</li>
<li><strong>Carbon monoxide</strong> — we check for CO at the appliance and remind you to keep detectors working on every floor.</li>
</ul>
<h2>Air conditioner and heat pump maintenance</h2>
<ul>
<li><strong>Coils</strong> — outdoor coil cleaned and indoor coil checked for dirt and airflow problems.</li>
<li><strong>Electrical</strong> — capacitors, contactors and connections tested.</li>
<li><strong>Refrigerant</strong> — system performance checked for signs of leaks or incorrect charge.</li>
<li><strong>Drainage</strong> — drain lines and pans cleared to prevent summer water damage.</li>
</ul>
<h2>Maintenance plans</h2>
<p>Many homeowners prefer a yearly plan that books a fall furnace check and a spring cooling check automatically. Ask us what's included in our current plans.</p>
<h2>What you can do between visits</h2>
<p>Check the filter monthly during heavy use and change it when it's gray. Keep the outdoor unit clear of leaves, grass clippings and snow, and keep at least two feet of clearance around it. Make sure supply registers and return grilles aren't blocked by furniture or rugs. After a heavy snowfall, check that the intake and exhaust pipes for a high-efficiency furnace are clear. Test your carbon monoxide and smoke alarms regularly, and replace them at the end of their rated life.</p>
<p>If a tune-up turns up a problem, you'll get a written price for the [[furnace-repair|furnace repair]] or [[ac-repair|AC repair]] before anything else is done. Maintenance pairs well with [[indoor-air-quality|filter upgrades]].</p>
""",
"faqs": [
("How often should my furnace be serviced?", "Once a year, ideally in late summer or fall before heating season. Air conditioners and heat pumps should be checked in spring."),
("Does maintenance affect my warranty?", "Many manufacturers expect regular professional maintenance, and some require proof of it for warranty claims. Keep your service records."),
("How often should I change my filter?", "Thin filters usually every one to three months; thick media filters every six to twelve months. Check monthly during heavy use."),
],
"related": ["furnace-repair", "ac-repair", "indoor-air-quality"],
"cities": {
"novi": "Many Novi homes have furnaces and air conditioners that were installed together and are now aging together. Yearly checks give you a clear picture of both, so replacements can be planned instead of rushed in January.",
"troy": "Troy's older systems benefit most from regular maintenance, especially combustion and venting checks on furnaces that have run through many Michigan winters. Spring coil cleaning keeps older air conditioners running through humid summers.",
"canton": "With so many Canton homes built in the same era, equipment ages in waves across whole neighborhoods. A fall furnace check and a spring cooling check catch most problems before the busiest weeks of the year."
},
},
{
"slug": "water-heaters",
"name": "Water Heaters",
"cat": "care",
"icon": "tank",
"short": "Tank and tankless water heater installation, replacement and repair, including high-efficiency and power-vented models.",
"title": "Water Heater Installation: Tank & Tankless",
"desc": "Tank and tankless water heater installation, replacement and repair, including power-vented and high-efficiency models. Written quotes before work.",
"h1": "Water Heaters",
"lead": "Endless hot water from a tankless unit, or a properly installed tank that just works. Either way, sized to how your household actually uses it.",
"body": """
<p>Running out of hot water halfway through a shower, rusty water, a tank that's rumbling or leaking at the base, or a water heater that's simply old: these are the usual reasons people call us. {biz} installs and replaces gas tank water heaters and tankless units, and we'll help you choose based on your family's hot water use, your venting options and your budget.</p>
<h2>Water heater options</h2>
<ul>
<li><strong>Conventional gas tanks</strong> — simple and affordable, vented into an existing chimney where that venting is still suitable.</li>
<li><strong>Power-vented tanks</strong> — a fan pushes exhaust through PVC pipe out a side wall, useful when the chimney is gone or no longer suitable.</li>
<li><strong>Tankless (on-demand)</strong> — heats water as you use it, so it doesn't run out, and frees up floor space. Sizing depends on how many fixtures run at once.</li>
<li><strong>Combi boilers</strong> — one unit for home heating and hot water, see [[boiler-services|boiler services]].</li>
</ul>
<h2>What we check on every install</h2>
<ol>
<li><strong>Sizing.</strong> Household size, fixtures and peak use, so the tank or tankless unit keeps up.</li>
<li><strong>Venting.</strong> Chimney condition, or a new PVC vent route for power-vented and tankless units.</li>
<li><strong>Gas supply.</strong> Tankless units need a larger gas supply, which we check before quoting.</li>
<li><strong>Safety.</strong> Relief valve and discharge line, expansion tank where needed, and proper clearances.</li>
<li><strong>Removal.</strong> The old tank is drained and taken away.</li>
</ol>
<h2>Signs it's time to replace</h2>
<p>Water pooling around the base, rust-colored hot water, rumbling or popping from sediment, and hot water that runs out faster than it used to are the most common signs. A leaking tank should be replaced soon, before it fails completely and floods the basement. If your tank is older than its warranty, it's worth planning the replacement now.</p>
<p>Electric tank and heat pump water heaters are options too, especially where gas isn't available. When we replace a [[furnace-installation|furnace]] that shared a chimney with the water heater, we check the water heater's venting at the same time.</p>
""",
"faqs": [
("Is tankless worth it?", "If you run out of hot water often, want the floor space or plan to stay in the house a long time, it often is. Upfront cost is higher, and the gas line may need upgrading."),
("How long do water heaters last?", "Tanks commonly last around 8 to 12 years, depending on water quality and maintenance. Tankless units usually last longer with annual descaling."),
("Can you switch me from gas to electric, or the reverse?", "Often, yes. It depends on your electrical panel, gas supply and venting, which we check before quoting."),
],
"related": ["boiler-services", "furnace-installation", "hvac-maintenance"],
"cities": {
"novi": "Many Novi families have outgrown the 40- or 50-gallon tank the builder installed. Larger households and newly finished bathrooms are the most common reasons we upsize tanks or switch to tankless here.",
"troy": "When an older Troy home's furnace is replaced with a high-efficiency model, the water heater is sometimes left alone in a chimney that's now too large for it. That can cause venting and condensation problems, so we check it whenever the furnace changes.",
"canton": "Canton's 1990s and 2000s homes have many original water heaters that are well past their expected life. We help homeowners choose between a like-for-like tank, a power-vented model or tankless based on household size and venting."
},
},
{
"slug": "smart-thermostats",
"name": "Smart Thermostats",
"cat": "care",
"icon": "thermostat",
"short": "Smart and programmable thermostat installation, wired and set up correctly for furnaces, heat pumps, hybrid systems and humidifiers.",
"title": "Smart Thermostat Installation & Setup",
"desc": "Smart and programmable thermostat installation for furnaces, heat pumps, hybrid systems and humidifiers. Wired, configured and tested properly.",
"h1": "Smart Thermostats",
"lead": "A smart thermostat only saves money when it's wired and configured for your system. We install it, set it up and show you how to use it.",
"body": """
<p>Smart thermostats can learn your schedule, adjust from your phone and show how much your system runs. They can also cause trouble when they're installed without the right wiring or settings: short cycling, a heat pump that leans on backup heat, a humidifier that never runs or a system that won't cool at all. {biz} installs and configures thermostats for the equipment you actually have.</p>
<h2>What we handle</h2>
<ul>
<li><strong>Wiring</strong> — adding a common wire (C-wire) when the thermostat needs constant power, instead of relying on adapters that cause problems.</li>
<li><strong>Heat pumps and hybrids</strong> — correct reversing valve settings, auxiliary heat lockouts and the switchover temperature between the heat pump and the furnace.</li>
<li><strong>Multi-stage and variable equipment</strong> — staging set up so the system runs at the right capacity.</li>
<li><strong>Accessories</strong> — humidifier, dehumidifier and ventilation control where the thermostat supports them.</li>
<li><strong>Remote sensors</strong> — room sensors that help even out temperature between floors.</li>
<li><strong>Setup and walkthrough</strong> — Wi-Fi, schedules and app setup, then we show you how it all works.</li>
</ul>
<h2>Choosing a thermostat</h2>
<ol>
<li><strong>Compatibility.</strong> Some equipment, especially variable-speed and some heat pump systems, works most reliably with the manufacturer's own control.</li>
<li><strong>Features you'll use.</strong> Remote access, scheduling and room sensors are the ones most people value.</li>
<li><strong>Utility programs.</strong> Some utility programs offer incentives for connected thermostats. We can tell you which models qualify for current programs.</li>
</ol>
<h2>Getting the settings right</h2>
<p>The most common smart thermostat problems we fix aren't hardware failures. They're settings: cycle rates that are too aggressive for the equipment, heat pump systems calling for expensive auxiliary heat too early, or schedules with recovery times that work against the system. A few minutes of proper setup avoids months of uneven comfort and higher bills. We'll also show you which features are worth turning on and which you can safely ignore, so the thermostat works for you instead of the other way around. Setup is included whenever we install one.</p>
<p>Thermostats are often installed along with a new [[furnace-installation|furnace]] or [[heat-pumps|heat pump]]. If rooms are uneven no matter what the thermostat says, the issue may be [[ductwork|the ductwork]].</p>
""",
"faqs": [
("Will a smart thermostat lower my bills?", "It can, mostly by reducing heating and cooling when you're asleep or away. Savings depend on your habits and how the schedule is set up."),
("What if I don't have a C-wire?", "We can usually add one using a spare wire in the existing cable or by running a new cable, which is more reliable than a power adapter."),
("Can I install it myself?", "Many people do on simple systems. Heat pumps, hybrid systems and accessories are where professional setup avoids comfort and efficiency problems."),
],
"related": ["heat-pumps", "furnace-installation", "hvac-maintenance"],
"cities": {
"novi": "Novi's two-story homes often have one thermostat in the main hallway and a hot upper floor. Smart thermostats with remote room sensors, combined with the right fan settings, are a practical first step before any duct changes.",
"troy": "In older Troy homes, thermostat wiring is often a thin two-wire cable with no common wire available. We run new cable where needed so the smart thermostat has steady power and the system behaves reliably.",
"canton": "Canton homeowners adding heat pumps to existing furnaces need a thermostat that manages the hybrid system properly. We set the switchover temperature and auxiliary heat settings so the system uses the cheaper fuel at the right times."
},
},
{
"slug": "commercial-hvac",
"name": "Commercial HVAC",
"cat": "care",
"icon": "commercial",
"short": "Rooftop units, split systems and maintenance programs for offices, shops, restaurants and light commercial buildings.",
"title": "Commercial HVAC: Rooftop Units & Maintenance",
"desc": "Commercial HVAC for offices, retail, restaurants and light industrial buildings: rooftop unit service, replacement and planned maintenance.",
"h1": "Commercial HVAC",
"lead": "Your tenants and customers notice when the HVAC fails. We service, replace and maintain light commercial equipment with minimal disruption to your business.",
"body": """
<p>For a business, a failed rooftop unit isn't just uncomfortable. It can mean a closed dining room, unhappy tenants or spoiled stock. {biz} works on light commercial heating and cooling for offices, retail stores, restaurants, clinics, churches and small industrial buildings, with clear written scopes so owners and property managers can plan and budget.</p>
<h2>Commercial services</h2>
<ul>
<li><strong>Rooftop units</strong> — service, repair and replacement of packaged rooftop units, including curb adapters and crane lifts when needed.</li>
<li><strong>Split systems and furnaces</strong> — commercial furnaces, split air conditioners and heat pumps in smaller buildings and units.</li>
<li><strong>Make-up air and exhaust</strong> — coordination for kitchens and spaces with exhaust needs.</li>
<li><strong>Ductless systems</strong> — server rooms, offices and spaces that need their own cooling.</li>
<li><strong>Planned maintenance</strong> — scheduled filter changes, coil cleaning, belt and safety checks with written reports for your records.</li>
<li><strong>Controls</strong> — programmable and networked thermostats to manage schedules across multiple units.</li>
</ul>
<h2>How we work with businesses</h2>
<ol>
<li><strong>Site review.</strong> We document equipment, ages, model numbers and condition.</li>
<li><strong>Written scope.</strong> Clear options and prices, including what can wait and what can't.</li>
<li><strong>Scheduling around you.</strong> Replacements and major work planned for slower hours where possible.</li>
<li><strong>Records.</strong> Maintenance and service reports that property managers can keep on file.</li>
</ol>
<h2>Planning ahead for replacements</h2>
<p>Rooftop units rarely fail at a convenient time, and replacement equipment for larger units isn't always in stock. We help owners and property managers build a simple equipment list with ages, condition and expected replacement timing, so budgets can be set in advance and replacements scheduled in spring or fall instead of during a heat wave or a cold snap.</p>
<h2>Who we work with</h2>
<p>Our commercial clients include small business owners who manage their own buildings, property managers responsible for several sites, and landlords with mixed residential and commercial units. Whatever the setup, you get clear scopes, honest timelines and records you can rely on. Ask us about scheduled maintenance for every unit on your property, with one point of contact for service calls.</p>
<p>Many smaller buildings use residential-style equipment, so our [[furnace-repair|furnace repair]] and [[ac-repair|AC repair]] work applies there too. Ask us about [[hvac-maintenance|maintenance plans]] for multiple units.</p>
""",
"faqs": [
("Do you offer maintenance contracts?", "Yes. We set up scheduled maintenance based on your equipment and how the building is used, with written reports after each visit."),
("Can you replace a rooftop unit without closing my business?", "Usually. We plan the lift and changeover for quieter hours and keep the downtime as short as possible."),
("Do you work with property managers?", "Yes. We provide written scopes, equipment lists and service records to make approvals and budgeting easier."),
],
"related": ["hvac-maintenance", "ductless-mini-splits", "ac-repair"],
"cities": {
"novi": "Novi's commercial areas, from the retail around Twelve Oaks to the office and light industrial parks along the expressway corridors, include a lot of rooftop units added over the years. Planning replacements before summer avoids emergency changeouts during a heat wave.",
"troy": "Troy's office buildings, medical suites and retail centers along Big Beaver Road and its side streets run a wide range of equipment. Regular maintenance, especially coil cleaning and belt checks, keeps rooftop units efficient through long cooling seasons.",
"canton": "Canton's commercial work is mostly retail plazas, restaurants and service businesses along Ford Road and its surrounding corridors. Maintenance plans with seasonal visits work well for owners managing several units across a property."
},
},
]
