# Service contacts and quote collection

These five entries are an initial contact directory: two providers publish repair services, two are dealer contacts and one is a manufacturer customer contact. This is not five verified workshops. No one was contacted, booked or sent data. No coordinate, nearest-shop ranking or price has been inferred. Recheck phone/address and relevant capability before referral.

## W01: BYD MEGAWATT service

[Published source](https://byd.megawatt.uz/byd_service/uz)

```json
{
  "id": "W01",
  "name": "BYD MEGAWATT service",
  "kind": "service_provider",
  "brands": [
    "BYD"
  ],
  "address": "Toshkent sh., yo‘l politsiyasi postidan 1,5 km, Quyoshli mavzesi; mo‘ljal: Kanselyariya bozori",
  "phone": "+998555101111",
  "published_services": [
    "Body repair",
    "Maintenance",
    "Tyre fitting",
    "Alignment",
    "Electrical diagnostics",
    "Air-conditioning service"
  ],
  "source_id": "S17",
  "limitations": "Provider-published address/claims only; exact repair capability and visit availability require confirmation.",
  "coordinates": null,
  "price_ranges": null,
  "checked_at": "2026-10-11",
  "contact_verified_by_call": false,
  "review_status": "provider_page_checked"
}
```

## W02: BYD Royal Motors / Chigatoy

[Published source](https://byd-rm.uz/service)

```json
{
  "id": "W02",
  "name": "BYD Royal Motors / Chigatoy",
  "kind": "service_provider",
  "brands": [
    "BYD"
  ],
  "address": null,
  "phone": "+998781401111",
  "published_services": [
    "Maintenance and repair"
  ],
  "source_id": "S18",
  "limitations": "Published service claim and phone only; workshop address and specific repair capability not verified.",
  "coordinates": null,
  "price_ranges": null,
  "checked_at": "2026-10-11",
  "contact_verified_by_call": false,
  "review_status": "provider_page_checked"
}
```

## W03: BYDZone Yashnobod

[Published source](https://bydzone.uz/kontaktlar/)

```json
{
  "id": "W03",
  "name": "BYDZone Yashnobod",
  "kind": "dealer_contact",
  "brands": [
    "BYD"
  ],
  "address": "Toshkent, Mahtumquli 79",
  "phone": "+998555200990",
  "published_services": [],
  "source_id": "S19",
  "limitations": "Contacts page confirms dealer location, not branch-specific workshop capabilities.",
  "coordinates": null,
  "price_ranges": null,
  "checked_at": "2026-10-11",
  "contact_verified_by_call": false,
  "review_status": "provider_page_checked"
}
```

## W04: BYDZone Lunacharsky

[Published source](https://bydzone.uz/kontaktlar/)

```json
{
  "id": "W04",
  "name": "BYDZone Lunacharsky",
  "kind": "dealer_contact",
  "brands": [
    "BYD"
  ],
  "address": "Toshkent, Buyuk Ipak Yo‘li 299",
  "phone": "+998555200990",
  "published_services": [],
  "source_id": "S19",
  "limitations": "Contacts page confirms dealer location, not branch-specific workshop capabilities.",
  "coordinates": null,
  "price_ranges": null,
  "checked_at": "2026-10-11",
  "contact_verified_by_call": false,
  "review_status": "provider_page_checked"
}
```

## W05: Chevrolet Uzbekistan customer contact

[Published source](https://chevrolet.uz/dealer)

```json
{
  "id": "W05",
  "name": "Chevrolet Uzbekistan customer contact",
  "kind": "manufacturer_contact",
  "brands": [
    "Chevrolet"
  ],
  "address": null,
  "phone": "+998781417777",
  "published_services": [],
  "source_id": "S20",
  "limitations": "Customer contact and dealer locator only; not an individual workshop or booking confirmation.",
  "coordinates": null,
  "price_ranges": null,
  "checked_at": "2026-10-11",
  "contact_verified_by_call": false,
  "review_status": "provider_page_checked"
}
```

## Quote intake template (unfilled)

Collect only after the team decides who contacts shops. A comparison needs the same vehicle, part, damage scope, labour/parts/tax treatment and quote validity period.

| Field | Value |
|---|---|
| Quote ID / provider ID | Pending |
| Vehicle model / year / trim / powertrain | Pending |
| Damage scope and photos shared with consent | Pending |
| Repair or replacement / OEM or aftermarket part | Pending |
| Labour / parts / taxes, separately in UZS | Pending |
| Quote date and expiry | Pending |
| Written quote or consented call record | Pending |
| Reviewer and provider confirmation | Pending |

Leave `cost_estimate` and `price_ranges` null until supporting quotes exist. A parts list price is not a complete repair quote.
