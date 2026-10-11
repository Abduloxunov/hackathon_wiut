# Starter knowledge notes

These three short summaries were checked against primary sources on 11 October 2026. They are paraphrases, not quotations. The team should review applicability and wording before integrating them into the shared product.

Run `seed_knowledge.py` to add them locally. The command is idempotent: repeated runs do not duplicate records. They contain no local repair prices or model-specific manual guidance. All three have generic vehicle applicability and require the matching component selection.

## Tire sidewall appearance

Michelin distinguishes inward indentation from outward bulging and gives different guidance for them. Its discussion of cracking also distinguishes superficial aging from deeper or extensive cracks. The photo baseline cannot measure depth or internal damage. Use these notes to locate relevant source guidance after the user has identified the component; do not treat the nearest reference label as confirmation. [Michelin: Sidewall Problems](https://www.michelinman.com/auto/auto-tips-and-advice/tire-damage/sidewall-problems)

## Windshield damage

Safelite describes a technician considering damage geometry, dimensions, depth, glass type and position when choosing between repair and replacement. A single similarity result cannot supply those measurements. This is a commercial provider's general guidance, with no claim that it covers Uzbek requirements or every vehicle. [Safelite: Windshield Damage, Repair vs Replace](https://www3.safelite.com/damaged-windshield-repair-replace)

## Try the retrieval

1. Upload a photo you own.
2. Select `Tire / wheel` and describe `sidewall bulge`, or select `Windshield` and describe `glass crack`.
3. Click **Find similar evidence**. The corresponding note should appear with its source link.
4. Add reviewed reference photos from other incidents to activate meaningful image comparison.

The source notes work before reference photos are added. No car-damage reference dataset or trained damage classifier is bundled.
