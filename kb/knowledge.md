# CarDoctor knowledge records

Version 0.1; checked 11 October 2026. These are source-linked triage candidates, not confirmed diagnoses. English guidance includes initial Uzbek/Russian search terms that still need native-language validation. Structured JSON blocks inside this Markdown are the canonical machine-readable records. `source_checked` means page-to-summary checking only; mechanic review remains pending.

Each record separates published guidance from possible causes, conditional urgency and application limits. No frequency claims, automatic severity probabilities, repair quotes or image examples are invented. PDF locators use one-based file pages plus printed-page labels where available.

## K001: Possible superficial clearcoat scratch

[Primary source](https://www.3m.com/3M/en_US/p/d/v000087447/)

```json
{
  "id": "K001",
  "title": "Possible superficial clearcoat scratch",
  "part": "body",
  "vision_labels": [
    "scratch"
  ],
  "search_terms": [
    "scratch",
    "scuff",
    "clearcoat",
    "tirnalish",
    "царапина"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "3M describes minor clearcoat marks as candidates for its scratch-removal system.",
  "possible_causes": [
    "Surface abrasion; depth unconfirmed"
  ],
  "urgency": {
    "level": "inspect",
    "condition": "Cosmetic only if coating depth and panel condition are confirmed.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Paint inspection / possible polishing",
  "actions": [
    "Ask a refinisher to assess coating depth before choosing treatment."
  ],
  "follow_up_questions": [
    "Which panel? Is metal exposed?"
  ],
  "limits": [
    "A photo cannot establish coating depth or guarantee polishing success."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S05",
      "locator": "Product description and applications"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K002: Possible deeper paint scratch

[Primary source](https://www.3m.com/3M/en_US/p/d/v000087447/)

```json
{
  "id": "K002",
  "title": "Possible deeper paint scratch",
  "part": "body",
  "vision_labels": [
    "scratch"
  ],
  "search_terms": [
    "scratch",
    "deep paint",
    "exposed metal",
    "tirnalish",
    "царапина"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "3M notes that scratches extending beyond clearcoat may need panel repainting.",
  "possible_causes": [
    "Abrasion penetrating the coating; not confirmed by appearance alone"
  ],
  "urgency": {
    "level": "inspect",
    "condition": "Extent and substrate need inspection.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Paint assessment / possible repaint",
  "actions": [
    "Obtain a panel-specific paint assessment."
  ],
  "follow_up_questions": [
    "Is the coating missing or substrate visible?"
  ],
  "limits": [
    "No automated paint-depth measurement or repaint price."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S05",
      "locator": "Product limitations"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K003: Cosmetic plastic bumper scuff

[Primary source](https://www.3m.com/3M/en_US/collision-repair-us/applications/bumper-and-plastic-repair/)

```json
{
  "id": "K003",
  "title": "Cosmetic plastic bumper scuff",
  "part": "body",
  "vision_labels": [
    "scratch"
  ],
  "search_terms": [
    "bumper",
    "scuff",
    "gouge",
    "plastic",
    "bamper",
    "бампер"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "3M distinguishes surface plastic damage from tears through the material and requires repair suitability checks.",
  "possible_causes": [
    "Surface contact damage to plastic"
  ],
  "urgency": {
    "level": "inspect",
    "condition": "Only applicable to a confirmed plastic bumper.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Plastic surface repair assessment",
  "actions": [
    "Ask a body shop to check material and manufacturer repair guidance."
  ],
  "follow_up_questions": [
    "Is the bumper plastic? Are mounts loose?"
  ],
  "limits": [
    "Scratch detection does not establish hidden attachment or sensor condition."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S06",
      "locator": "Cosmetic repair and OEM applicability"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K004: Crack or tear through a plastic bumper

[Primary source](https://www.3m.com/3M/en_US/collision-repair-us/applications/bumper-and-plastic-repair/)

```json
{
  "id": "K004",
  "title": "Crack or tear through a plastic bumper",
  "part": "body",
  "vision_labels": [
    "crack"
  ],
  "search_terms": [
    "bumper",
    "crack",
    "tear",
    "plastic",
    "yoriq",
    "трещина",
    "бампер"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "3M describes through-plastic cracks and tears as requiring a different repair process from surface scuffs.",
  "possible_causes": [
    "Possible impact-related plastic break"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "Loose components or affected functions require assessment before use.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Plastic repair versus replacement assessment",
  "actions": [
    "Have a repairer inspect attachments and OEM repair eligibility."
  ],
  "follow_up_questions": [
    "Any loose pieces or affected lights/sensors?"
  ],
  "limits": [
    "The photo cannot establish through-thickness, structural safety or replacement necessity."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S06",
      "locator": "Two-sided bumper repair"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K005: Dent and paintless repair assessment

[Primary source](https://rts.i-car.com/10616.html)

```json
{
  "id": "K005",
  "title": "Dent and paintless repair assessment",
  "part": "body",
  "vision_labels": [
    "dent"
  ],
  "search_terms": [
    "dent",
    "pdr",
    "paintless",
    "panel",
    "botiq",
    "вмятина"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "I-CAR warns that PDR tools can disturb backside corrosion protection, which must be restored.",
  "possible_causes": [
    "Panel deformation; hidden damage unknown"
  ],
  "urgency": {
    "level": "inspect",
    "condition": "Repair suitability depends on panel and coating inspection.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Dent / PDR suitability assessment",
  "actions": [
    "Ask whether backside corrosion protection will be restored if PDR is selected."
  ],
  "follow_up_questions": [
    "Which panel? Any cracked paint or changed panel gaps?"
  ],
  "limits": [
    "This source does not prove that a photographed dent is suitable for PDR."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S07",
      "locator": "Backside corrosion protection after PDR"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K006: Windscreen chip needs repairability inspection

[Primary source](https://www3.safelite.com/damaged-windshield-repair-replace)

```json
{
  "id": "K006",
  "title": "Windscreen chip needs repairability inspection",
  "part": "windshield",
  "vision_labels": [
    "crack"
  ],
  "search_terms": [
    "chip",
    "windscreen",
    "windshield",
    "stone",
    "oyna",
    "скол",
    "лобовое"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "Safelite considers size, depth, location and glass type; some small chips can be repaired.",
  "possible_causes": [
    "Possible stone impact; not proven"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "Prompt assessment can help address spreading damage.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Glass repair assessment",
  "actions": [
    "Arrange a glass technician assessment."
  ],
  "follow_up_questions": [
    "Where is the chip? Any obstructed vision or spreading?"
  ],
  "limits": [
    "No automatic size or depth measurement and no repair guarantee."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S04",
      "locator": "Damage shape, size and depth"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K007: Windscreen crack with visibility or edge involvement

[Primary source](https://www3.safelite.com/damaged-windshield-repair-replace)

```json
{
  "id": "K007",
  "title": "Windscreen crack with visibility or edge involvement",
  "part": "windshield",
  "vision_labels": [
    "crack"
  ],
  "search_terms": [
    "crack",
    "windscreen",
    "windshield",
    "edge",
    "visibility",
    "yoriq",
    "трещина",
    "лобовое"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "Safelite identifies deep damage, obscured driver vision and edge-spanning cracks as reasons replacement may be needed.",
  "possible_causes": [
    "Possible impact or spreading glass damage"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "If visibility is impaired, do not treat a photo result as clearance to drive.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Glass replacement assessment",
  "actions": [
    "Ask a glass technician to assess replacement and visibility."
  ],
  "follow_up_questions": [
    "Does it obstruct the driver view or reach the edges?"
  ],
  "limits": [
    "Commercial assessment guidance is not Uzbekistan law or a universal threshold."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S04",
      "locator": "Replacement indicators"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K008: Shattered side-window glass

[Primary source](https://www3.safelite.com/damaged-windshield-repair-replace)

```json
{
  "id": "K008",
  "title": "Shattered side-window glass",
  "part": "side_window",
  "vision_labels": [
    "glass shatter"
  ],
  "search_terms": [
    "shatter",
    "broken glass",
    "side window",
    "oyna singan",
    "разбитое стекло"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "Safelite notes that tempered side/rear glass is more likely to fragment and require replacement.",
  "possible_causes": [
    "Possible impact; glass material must be confirmed"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "Loose glass and an unsecured opening need attention.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Side-window replacement assessment",
  "actions": [
    "Arrange glass service; avoid handling fragments as a diagnostic step."
  ],
  "follow_up_questions": [
    "Which window and glass type? Any injuries?"
  ],
  "limits": [
    "Not all side windows are tempered; do not infer crash cause from fragments."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S04",
      "locator": "Glass material differences"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K009: Visibly flat tyre or rapid pressure loss

[Primary source](https://www.nhtsa.gov/vehicle-safety/tires)

```json
{
  "id": "K009",
  "title": "Visibly flat tyre or rapid pressure loss",
  "part": "tire",
  "vision_labels": [
    "tire flat"
  ],
  "search_terms": [
    "flat",
    "deflated",
    "pressure loss",
    "tire",
    "tyre",
    "shina",
    "спущенная",
    "шина"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "NHTSA explains that rapid pressure loss can affect control; visible shape alone does not identify its cause.",
  "possible_causes": [
    "Puncture, valve or wheel issue are assessment candidates, not a diagnosis"
  ],
  "urgency": {
    "level": "stop_and_assess",
    "condition": "Confirmed flat/rapid loss needs safe stopping and assistance.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Tyre / wheel inspection",
  "actions": [
    "If moving, regain stable control and pull over safely; arrange tyre assessment."
  ],
  "follow_up_questions": [
    "Is it fully flat? Was pressure measured?"
  ],
  "limits": [
    "No puncture location, repair eligibility or tyre pressure from pixels."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S03",
      "locator": "Tyre blowouts and tyre pressure"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K010: Possible repairable tread puncture

[Primary source](https://www.michelinman.com/auto/auto-tips-and-advice/tire-maintenance/can-my-tire-be-repaired)

```json
{
  "id": "K010",
  "title": "Possible repairable tread puncture",
  "part": "tire",
  "vision_labels": [],
  "search_terms": [
    "tread",
    "nail",
    "puncture",
    "teshik",
    "прокол"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "Michelin limits repair candidates to eligible tread punctures up to 6 mm, with conditions including not having been driven flat and internal inspection.",
  "possible_causes": [
    "Possible tread penetration"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "Eligibility is decided after professional inspection.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Professional puncture repair assessment",
  "actions": [
    "Have the tyre removed and inspected by a tyre professional."
  ],
  "follow_up_questions": [
    "Tread or sidewall? Driven flat? Measured hole diameter?"
  ],
  "limits": [
    "A nail photo cannot prove diameter, internal condition or eligibility."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S02",
      "locator": "Repair eligibility"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K011: Sidewall puncture or cut

[Primary source](https://www.michelinman.com/auto/auto-tips-and-advice/tire-maintenance/can-my-tire-be-repaired)

```json
{
  "id": "K011",
  "title": "Sidewall puncture or cut",
  "part": "tire",
  "vision_labels": [
    "crack"
  ],
  "search_terms": [
    "sidewall",
    "puncture",
    "cut",
    "yon",
    "kesik",
    "боковина",
    "порез"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "Michelin states that sidewall damage is not safely repaired and requires replacement.",
  "possible_causes": [
    "Possible cut or sidewall penetration"
  ],
  "urgency": {
    "level": "stop_and_assess",
    "condition": "Applies to confirmed sidewall damage.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Tyre replacement assessment",
  "actions": [
    "Arrange professional replacement and safe assistance."
  ],
  "follow_up_questions": [
    "Is damage on the sidewall rather than tread?"
  ],
  "limits": [
    "A visible line can be a surface mark; confirmation is needed."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S02",
      "locator": "Sidewall repair restrictions"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K012: Outward tyre-sidewall bulge

[Primary source](https://www.michelinman.com/auto/auto-tips-and-advice/tire-damage/sidewall-problems)

```json
{
  "id": "K012",
  "title": "Outward tyre-sidewall bulge",
  "part": "tire",
  "vision_labels": [],
  "search_terms": [
    "bulge",
    "bubble",
    "outward",
    "sidewall",
    "shish",
    "грыжа",
    "вздутие"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "Michelin links an outward sidewall bulge to internal structural damage and calls for immediate replacement.",
  "possible_causes": [
    "Internal cord damage is the cited concern for a confirmed bulge"
  ],
  "urgency": {
    "level": "stop_and_assess",
    "condition": "Confirmed outward bulge: arrange assistance and replacement.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Tyre replacement",
  "actions": [
    "Do not continue normal driving on a confirmed bulging tyre."
  ],
  "follow_up_questions": [
    "Does it protrude outward? Could this be an inward indentation?"
  ],
  "limits": [
    "Image similarity cannot establish cord condition or distinguish every shape."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S01",
      "locator": "Bulge versus indentation"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K013: Inward tyre-sidewall indentation

[Primary source](https://www.michelinman.com/auto/auto-tips-and-advice/tire-damage/sidewall-problems)

```json
{
  "id": "K013",
  "title": "Inward tyre-sidewall indentation",
  "part": "tire",
  "vision_labels": [],
  "search_terms": [
    "indentation",
    "inward",
    "sidewall",
    "depression",
    "ichkariga",
    "впадина"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "Michelin distinguishes normal inward cord-overlap indentations from outward bulges.",
  "possible_causes": [
    "A cord-overlap manufacturing feature is one possibility"
  ],
  "urgency": {
    "level": "inspect",
    "condition": "Only the confirmed normal feature fits this guidance.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Tyre shape assessment",
  "actions": [
    "If the shape is uncertain, ask a tyre professional to distinguish it."
  ],
  "follow_up_questions": [
    "Inward or outward? Any pressure loss or cracks?"
  ],
  "limits": [
    "Do not label every depression harmless or confuse it with a body-panel dent."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S01",
      "locator": "Indentation versus bulge"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K014: Tyre-sidewall cracking

[Primary source](https://www.michelinman.com/auto/auto-tips-and-advice/tire-damage/sidewall-problems)

```json
{
  "id": "K014",
  "title": "Tyre-sidewall cracking",
  "part": "tire",
  "vision_labels": [
    "crack"
  ],
  "search_terms": [
    "crack",
    "cracking",
    "sidewall",
    "rubber",
    "yoriq",
    "трещины"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "Michelin differentiates shallow age-related surface cracks from deeper or extensive cracking needing replacement.",
  "possible_causes": [
    "Rubber ageing is a possibility; depth and distribution matter"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "Severe/deep cracking needs replacement assessment.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Tyre condition / replacement assessment",
  "actions": [
    "Have crack depth and distribution assessed professionally."
  ],
  "follow_up_questions": [
    "Tyre age? Widespread cracks or pressure loss?"
  ],
  "limits": [
    "No depth measurement or tyre-age inference from a photo; do not flex it for the app."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S01",
      "locator": "FAQ: small sidewall cracks"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K015: Tyre pressure or TPMS warning

[Primary source](https://www.nhtsa.gov/vehicle-safety/tires)

```json
{
  "id": "K015",
  "title": "Tyre pressure or TPMS warning",
  "part": "tire",
  "vision_labels": [],
  "search_terms": [
    "tpms",
    "pressure",
    "inflation",
    "bosim",
    "давление"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "NHTSA recommends manufacturer cold-pressure values from the vehicle label/manual; TPMS does not replace pressure checks.",
  "possible_causes": [
    "Low pressure needs measurement; a photo is insufficient"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "Measured pressure and the applicable manual determine next steps.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Pressure / tyre assessment",
  "actions": [
    "Use the vehicle placard/manual and a gauge; do not use sidewall maximum as the target."
  ],
  "follow_up_questions": [
    "What does the placard say? Cold gauge reading?"
  ],
  "limits": [
    "No universal pressure value; US TPMS fitment law is not applied locally."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S03",
      "locator": "Tyre pressure and TPMS"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K016: Clear water beneath a car after air conditioning

[Primary source](https://www.theaa.com/breakdown-cover/advice/why-is-my-car-leaking-water)

```json
{
  "id": "K016",
  "title": "Clear water beneath a car after air conditioning",
  "part": "fluid",
  "vision_labels": [],
  "search_terms": [
    "clear",
    "water",
    "drip",
    "air conditioning",
    "condensation",
    "suv",
    "вода",
    "конденсат"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "AA describes air-conditioning condensation as a possible explanation for occasional water drips.",
  "possible_causes": [
    "AC condensation is possible, not confirmed"
  ],
  "urgency": {
    "level": "inspect",
    "condition": "Reassuring only with supporting timing, location and no other warning signs.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Fluid-source assessment",
  "actions": [
    "Record location and timing safely; seek inspection if persistent or uncertain."
  ],
  "follow_up_questions": [
    "After AC use? Warning lights or changing fluid level?"
  ],
  "limits": [
    "Clear appearance does not prove harmless water. Do not taste or touch unidentified fluid."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S08",
      "locator": "AC condensation"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K017: Unidentified coloured fluid under the vehicle

[Primary source](https://www.theaa.com/breakdown-cover/advice/why-is-my-car-leaking-water)

```json
{
  "id": "K017",
  "title": "Unidentified coloured fluid under the vehicle",
  "part": "fluid",
  "vision_labels": [],
  "search_terms": [
    "fluid",
    "leak",
    "green",
    "red",
    "brown",
    "black",
    "coolant",
    "oil",
    "oqish",
    "течь",
    "жидкость"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "AA lists several automotive liquids and possible leak sources; colour and location are clues rather than proof.",
  "possible_causes": [
    "Coolant, oil or other fluid are possibilities requiring assessment"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "Warnings, rapid loss or overheating change urgency.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Leak diagnosis",
  "actions": [
    "Record colour/location without contact and arrange inspection."
  ],
  "follow_up_questions": [
    "Where is it? Any overheating, pressure or brake warnings?"
  ],
  "limits": [
    "Colour alone cannot identify the fluid or failed component."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S08",
      "locator": "Different fluids and investigation"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K018: Water or dampness inside the cabin

[Primary source](https://www.theaa.com/breakdown-cover/advice/why-is-my-car-leaking-water)

```json
{
  "id": "K018",
  "title": "Water or dampness inside the cabin",
  "part": "fluid",
  "vision_labels": [],
  "search_terms": [
    "cabin",
    "wet carpet",
    "water",
    "drain",
    "seal",
    "salon",
    "nam",
    "салон",
    "мокрый"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "AA includes blocked drains, sealing issues and heater-related leaks among possible cabin-water sources.",
  "possible_causes": [
    "Drain, seal or heater-related source; none confirmed"
  ],
  "urgency": {
    "level": "inspect",
    "condition": "Persistent dampness or other symptoms warrant inspection.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Ingress / cabin leak assessment",
  "actions": [
    "Record whether rain or AC use precedes the dampness."
  ],
  "follow_up_questions": [
    "Rain-related? Where is the damp patch?"
  ],
  "limits": [
    "The KB does not infer a heater fault from carpet colour."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S08",
      "locator": "Water inside the cabin"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K019: Electric or hybrid vehicle crash with possible high-voltage damage

[Primary source](https://www.nhtsa.gov/vehicle-safety/electric-and-hybrid-vehicles)

```json
{
  "id": "K019",
  "title": "Electric or hybrid vehicle crash with possible high-voltage damage",
  "part": "ev",
  "vision_labels": [],
  "search_terms": [
    "collision",
    "crash",
    "battery",
    "orange cable",
    "high voltage",
    "avariya",
    "аккумулятор",
    "дтп"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [
      "ev",
      "phev",
      "hev"
    ],
    "confirmed_manual_source": null
  },
  "source_summary": "NHTSA warns that damaged high-voltage batteries/wiring can remain energised and present immediate or delayed hazards.",
  "possible_causes": [
    "Possible high-voltage damage after impact; not established visually"
  ],
  "urgency": {
    "level": "emergency_if_hazard",
    "condition": "Fire, smoke, injury or suspected high-voltage damage needs professional emergency handling.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Qualified EV emergency / recovery assessment",
  "actions": [
    "Keep clear of damaged HV parts; contact emergency services for an active hazard and follow manufacturer recovery guidance."
  ],
  "follow_up_questions": [
    "Exact model and EV/PHEV/HEV variant? Smoke, heat or exposed wiring?"
  ],
  "limits": [
    "No battery safety clearance, charging clearance or DIY electrical repair instructions."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S09",
      "locator": "Damaged electric/hybrid vehicles"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K020: Electric or hybrid vehicle affected by flooding

[Primary source](https://www.nhtsa.gov/vehicle-safety/electric-and-hybrid-vehicles)

```json
{
  "id": "K020",
  "title": "Electric or hybrid vehicle affected by flooding",
  "part": "ev",
  "vision_labels": [],
  "search_terms": [
    "flood",
    "water",
    "submerged",
    "battery",
    "suv bosgan",
    "затопление"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [
      "ev",
      "phev",
      "hev"
    ],
    "confirmed_manual_source": null
  },
  "source_summary": "NHTSA warns that flooded high-voltage batteries can pose shock and fire risks.",
  "possible_causes": [
    "Possible water-related high-voltage damage"
  ],
  "urgency": {
    "level": "stop_and_assess",
    "condition": "Flood exposure requires qualified assessment and recovery guidance.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Qualified EV recovery assessment",
  "actions": [
    "Keep clear of suspect electrical damage and contact qualified recovery/service personnel."
  ],
  "follow_up_questions": [
    "Powertrain variant? How high was the water?"
  ],
  "limits": [
    "No water-resistance rating, safe-restart or safe-charge conclusion from images."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S09",
      "locator": "Flooded electric/hybrid vehicles"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K021: Cobalt oil-pressure warning while engine is running

[Primary source](https://chevrolet.uz/storage/images/exp_files_uz/17/gtUbSsqgxGKTYDVaC2TOyK8ZHnfeJvk4hiiR23wU.pdf)

```json
{
  "id": "K021",
  "title": "Cobalt oil-pressure warning while engine is running",
  "part": "dashboard",
  "vision_labels": [],
  "search_terms": [
    "oil pressure",
    "oil lamp",
    "oil warning",
    "moy",
    "давление масла"
  ],
  "scope": {
    "vehicle_models": [
      "Cobalt"
    ],
    "propulsion": [],
    "confirmed_manual_source": "S11"
  },
  "source_summary": "The Cobalt manual distinguishes the normal pre-start lamp check from a warning persisting while running; it directs safe stopping and engine shutdown.",
  "possible_causes": [
    "An oil-pressure system problem is possible; exact cause is not established"
  ],
  "urgency": {
    "level": "stop_engine",
    "condition": "Only when the lamp persists with the engine running.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Engine oil-pressure assessment",
  "actions": [
    "Stop safely, switch off the engine and arrange service."
  ],
  "follow_up_questions": [
    "Engine running or key-on only? Exact manual confirmed?"
  ],
  "limits": [
    "Not evidence of a failed pump, low oil quantity or a common Cobalt fault."
  ],
  "required_context": {
    "engine_running": true
  },
  "source_refs": [
    {
      "source_id": "S11",
      "locator": "PDF page 63 (printed 4-13)"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K022: Cobalt overheating with steam or persistent temperature warning

[Primary source](https://chevrolet.uz/storage/images/exp_files_uz/17/gtUbSsqgxGKTYDVaC2TOyK8ZHnfeJvk4hiiR23wU.pdf)

```json
{
  "id": "K022",
  "title": "Cobalt overheating with steam or persistent temperature warning",
  "part": "engine",
  "vision_labels": [],
  "search_terms": [
    "overheat",
    "steam",
    "temperature",
    "qizish",
    "перегрев",
    "пар"
  ],
  "scope": {
    "vehicle_models": [
      "Cobalt"
    ],
    "propulsion": [],
    "confirmed_manual_source": "S11"
  },
  "source_summary": "The Cobalt manual warns about burns from steam and opening a hot coolant cap; leaks require repair before continued operation.",
  "possible_causes": [
    "Cooling-system issue is possible; component diagnosis pending"
  ],
  "urgency": {
    "level": "stop_and_assess",
    "condition": "Steam or a persistent overheat warning needs safe stopping and cooling.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Cooling-system inspection",
  "actions": [
    "Stop safely; avoid steam and do not open a hot coolant cap; arrange service."
  ],
  "follow_up_questions": [
    "Steam or persistent warning? Exact manual confirmed?"
  ],
  "limits": [
    "No coolant-leak source or safe restart conclusion from colour alone."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S11",
      "locator": "PDF page 143 (printed 9-13)"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K023: Lacetti brake warning after parking-brake release

[Primary source](https://chevrolet.uz/storage/images/exp_files_uz/18/avtomobildan-foydalanish-qollanmasi-lacetti.pdf)

```json
{
  "id": "K023",
  "title": "Lacetti brake warning after parking-brake release",
  "part": "dashboard",
  "vision_labels": [],
  "search_terms": [
    "brake warning",
    "brake lamp",
    "tormoz",
    "тормоз"
  ],
  "scope": {
    "vehicle_models": [
      "Lacetti"
    ],
    "propulsion": [],
    "confirmed_manual_source": "S14"
  },
  "source_summary": "The Lacetti manual differentiates the parking-brake indication from a warning persisting after release and advises service for brake-system faults.",
  "possible_causes": [
    "Possible brake-system fault; the lamp does not identify a failed part"
  ],
  "urgency": {
    "level": "stop_and_assess",
    "condition": "Confirmed persistent warning with parking brake released requires assessment.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Brake-system assessment",
  "actions": [
    "Arrange brake-system assessment; do not continue with a confirmed brake-system fault."
  ],
  "follow_up_questions": [
    "Parking brake released? Engine state and pedal behaviour?"
  ],
  "limits": [
    "Do not apply this automatically to Gentra or interpret a key-on photo as a fault."
  ],
  "required_context": {
    "parking_brake_released": true,
    "engine_running": true
  },
  "source_refs": [
    {
      "source_id": "S14",
      "locator": "PDF pages 36-37 (printed 2-7 to 2-8)"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K024: Lacetti charging warning persisting after engine start

[Primary source](https://chevrolet.uz/storage/images/exp_files_uz/18/avtomobildan-foydalanish-qollanmasi-lacetti.pdf)

```json
{
  "id": "K024",
  "title": "Lacetti charging warning persisting after engine start",
  "part": "dashboard",
  "vision_labels": [],
  "search_terms": [
    "charging",
    "battery lamp",
    "charge warning",
    "zaryad",
    "зарядка"
  ],
  "scope": {
    "vehicle_models": [
      "Lacetti"
    ],
    "propulsion": [],
    "confirmed_manual_source": "S14"
  },
  "source_summary": "The Lacetti manual describes a charging warning that should clear after starting; persistent illumination requires service.",
  "possible_causes": [
    "A charging-system issue is possible; battery failure is not proven"
  ],
  "urgency": {
    "level": "stop_and_assess",
    "condition": "Only for a warning persisting with the engine running.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Charging-system assessment",
  "actions": [
    "Stop safely and arrange charging-system inspection."
  ],
  "follow_up_questions": [
    "Engine running or just ignition on?"
  ],
  "limits": [
    "A lit battery symbol alone does not establish a faulty battery or alternator."
  ],
  "required_context": {
    "engine_running": true
  },
  "source_refs": [
    {
      "source_id": "S14",
      "locator": "PDF page 37 (printed 2-8)"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K025: Nexia frozen or worn windscreen wipers

[Primary source](https://chevrolet.uz/storage/images/exp_files_uz/16/avtomobildan-foydalanish-qollanmasi-nexia.pdf)

```json
{
  "id": "K025",
  "title": "Nexia frozen or worn windscreen wipers",
  "part": "wiper",
  "vision_labels": [],
  "search_terms": [
    "wiper",
    "frozen",
    "blade",
    "dvorni",
    "дворники",
    "замерзшие"
  ],
  "scope": {
    "vehicle_models": [
      "Nexia"
    ],
    "propulsion": [],
    "confirmed_manual_source": "S12"
  },
  "source_summary": "The Nexia manual warns against operating frozen blades and calls for replacement when worn blades impair visibility.",
  "possible_causes": [
    "Frozen attachment or worn blades are possible with supporting context"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "Impaired visibility needs correction before travel.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Wiper condition assessment",
  "actions": [
    "Free frozen blades safely before operating; arrange blade assessment if wiping remains poor."
  ],
  "follow_up_questions": [
    "Frozen to the glass or worn? Exact manual confirmed?"
  ],
  "limits": [
    "Not a diagnosis of wiper-motor failure from streaks."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S12",
      "locator": "PDF pages 43-44 (printed 2-15 to 2-16)"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K026: Damas fuel-refuelling precautions

[Primary source](https://chevrolet.uz/storage/images/exp_files_uz/14/CX6TIKfPdzMg6L0JySFHnz8VrJzoCc4136JwJomn.pdf)

```json
{
  "id": "K026",
  "title": "Damas fuel-refuelling precautions",
  "part": "fuel",
  "vision_labels": [],
  "search_terms": [
    "fuel",
    "refuel",
    "petrol",
    "filling",
    "benzin",
    "заправка"
  ],
  "scope": {
    "vehicle_models": [
      "Damas"
    ],
    "propulsion": [],
    "confirmed_manual_source": "S13"
  },
  "source_summary": "The Damas manual instructs engine shutdown and avoidance of smoking or flames during refuelling.",
  "possible_causes": [
    "Fuel vapour is a hazard during refuelling; not a detected vehicle fault"
  ],
  "urgency": {
    "level": "precaution",
    "condition": "Applies during refuelling; a reported spill needs appropriate professional handling.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Refuelling precaution / assessment",
  "actions": [
    "Switch off the engine and keep ignition sources away during refuelling."
  ],
  "follow_up_questions": [
    "Refuelling now or a suspected leak? Exact manual confirmed?"
  ],
  "limits": [
    "This record cannot diagnose a fuel leak or recommend a fuel grade."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S13",
      "locator": "PDF page 65 (printed 6-3)"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K027: Broken or damaged lamp cover

[Primary source](https://www.hella.com/techworld/en/technical/automotive-lighting/headlight-adjustment/)

```json
{
  "id": "K027",
  "title": "Broken or damaged lamp cover",
  "part": "lamp",
  "vision_labels": [
    "lamp broken"
  ],
  "search_terms": [
    "lamp",
    "headlight",
    "broken",
    "cover",
    "fara",
    "фара",
    "разбита"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "HELLA recommends checking lighting function and cover-lens damage; beam adjustment requires a controlled test setup.",
  "possible_causes": [
    "Possible lens or housing damage; function must be checked"
  ],
  "urgency": {
    "level": "prompt_inspection",
    "condition": "Loss of required lighting or insecure parts needs attention before affected driving conditions.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Lamp repair / replacement assessment",
  "actions": [
    "Have lamp function, attachment and beam aim checked professionally."
  ],
  "follow_up_questions": [
    "Which lamp? Does it work? Any loose parts?"
  ],
  "limits": [
    "A photo cannot establish electrical function, beam alignment or legal compliance."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S15",
      "locator": "Preparing the vehicle and beamsetter adjustment"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

## K028: Lamp fogging versus accumulated water

[Primary source](https://www.hella.com/techworld/sg/technical/automotive-lighting/condensation-in-headlight/)

```json
{
  "id": "K028",
  "title": "Lamp fogging versus accumulated water",
  "part": "lamp",
  "vision_labels": [],
  "search_terms": [
    "fog",
    "condensation",
    "water",
    "lamp",
    "headlight",
    "nam",
    "фара",
    "конденсат"
  ],
  "scope": {
    "vehicle_models": [],
    "propulsion": [],
    "confirmed_manual_source": null
  },
  "source_summary": "HELLA distinguishes transient fogging from droplets or accumulated water, which call for seal and ventilation checks.",
  "possible_causes": [
    "Environmental condensation or water ingress are possibilities"
  ],
  "urgency": {
    "level": "inspect",
    "condition": "Persistent droplets/pooled water need inspection.",
    "basis": "Source-informed conditional triage; not a calibrated severity prediction."
  },
  "repair_type": "Lamp seal / ventilation assessment",
  "actions": [
    "Record whether fog clears; have persistent water accumulation inspected."
  ],
  "follow_up_questions": [
    "Light mist or water droplets/pooling? Repeated after rain?"
  ],
  "limits": [
    "Do not classify all condensation as a broken lamp."
  ],
  "required_context": {},
  "source_refs": [
    {
      "source_id": "S16",
      "locator": "Normal condensation and excessive water"
    }
  ],
  "checked_at": "2026-10-11",
  "review_status": "source_checked",
  "expert_review": "pending",
  "cost_estimate": null
}
```

