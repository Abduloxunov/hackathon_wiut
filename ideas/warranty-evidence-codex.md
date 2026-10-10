---
name: Warranty Evidence Review
added_by: Bexruz + codex, refining WarrantyProof and TrueClaim
date: Sat 10 Oct 2026
direction: dealer/service operations
mode: "Partner product: proposed Royal Motors warranty-review unit"
---

# Warranty Evidence Review

**One line:** Part photographs, requested item record and declared submission history → reused-image/identifier/coverage evidence → request more evidence or manual review.

## Problem and user

A warranty reviewer must check whether a submission contains adequate, consistent evidence. Pictures may be unclear, omit a required view, show a conflicting identifier or closely match an earlier submission. Local prevalence, workload and financial loss are unverified.

- User/owner: warranty-review officer.
- Proposed payer: Royal Motors warranty/aftersales department; no access agreement or real claims history.
- [Truepic's automotive-warranty article](https://www.truepic.com/blog/snapshot-impact-of-image-authenticity-for-the-auto-warranty-industry) describes image/object reuse and recapture as evidence issues. Its vendor savings/fraud figures are not our evidence.
- Credits: claude-1's WarrantyProof and ClaimProof, claude-2's TrueClaim. This narrows the output to evidence consistency, not a universal authenticity verdict.

## What the product does

1. Reviewer chooses the expected supported part and required views.
2. The app checks the submitted image quality and evidence coverage.
3. It searches a declared authorised image history for matching/near-matching submissions.
4. It reads a visible part identifier when supported and compares it with the record.
5. It shows matching images, conflicting text and missing views with review reasons.

- Input: photographs, a small structured expected-item record and a declared image index. Prototype records are explicitly synthetic/seeded, not real customer claims.
- Output: no inconsistency detected within supported checks, possible image reuse, identifier conflict, missing/unreadable evidence, retake or review required. Human review controls the real decision.
- Live jury test: new uploads, crop/resize/recompress an authorised reference, a genuinely different but similar image, a conflicting identifier and an unfamiliar item. Never preassign an upload's result.
- Boundary: repeated images may be legitimate; similarity is not proof of fraud or physical-object reuse. Missing EXIF is not manipulation evidence. No automated payment/rejection or universal real/fake-photo claim.

## Tech (why it is a system, not one API call)

Quality gate → part-region localisation → perceptual-hash candidate search + visual-embedding retrieval → local correspondence verification → OCR confidence/identifier comparison → view-completeness rules → evidence report. Similar-looking objects require uncertainty, not a match declaration. Show which reference/result supported each reason.

- Data needed: authorised reference images and correctly labelled match/nonmatch pairs; declared digital edits test transformation robustness, separately from real captures. Supported identifiers need trustworthy records. No real claims/data are available. Verify all image, model and weight licences; hashes/embeddings are not automatically anonymous.
- Proposed inference: server CPU for a bounded image index, subject to actual benchmark. Hardware/speed/cost are unmeasured.
- Local/night/rain: OCR and correspondence need tests on local parts/phones, low light, reflective/wet surfaces and unreadable codes. Retrieval stability under edits does not establish night capture quality. Conditions without examples remain not evaluated.
- Deployment: public browser upload → server retrieval/OCR/rules → matched evidence and retake/review page from submitted repo.

## Quality and validation

Hold out source images/physical items and capture devices/sessions. Measure false matching of different images first, retrieval recall for supported transformations, identifier transcription/conflict errors, unknown rejection, completeness/retake behaviour and reviewer time. Compare exact-hash-only and identifier-only baselines. Label seeded/history experiments openly; do not present them as customer fraud statistics.

## Why hard to copy

Potential advantage: authorised local histories, validated match thresholds and review integration. These do not exist yet. Prior art is substantial; adding an image search to a UI alone is easy to replicate. Any extra stage must demonstrate improved review quality.

## Business

- Proposed pricing: warranty-desk subscription or completed evidence review; amount unverified.
- Cost per review: compute/index maintenance, storage/network, retake and reviewer labour; use [shared cost model](cv-shortlist-codex.md#shared-pilot-cost-model).
- Validate completeness, review time and independently confirmed inconsistencies. Do not turn suspicious flags into assumed avoided payouts.
- Three-month pilot: authorised scope/history and baseline → shadow review with expert labels → supervised request-for-evidence workflow. Legal/process and buyer approvals remain unconfirmed.

## Can we build it in ~8 h?

Conditional MVP: small openly seeded index, image-quality and verified near-duplicate search, readable supported identifier check and evidence report. It can be explored with digital samples but requires licence-cleared inputs. Biggest risks are false matches and lack of representative automotive evidence. Exclude universal AI-generation/forgery detection from the MVP. No implementation selected.

## Comments
<!-- Other agents may append comments. -->
