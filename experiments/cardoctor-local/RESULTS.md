# CarDoctor local prototype: measured results

Recorded on **11 October 2026, Asia/Tashkent**, for the separate local experiment in `experiments/cardoctor-local/`. These results describe the prototype and its engineering checks. They are not competition metrics or automotive-model accuracy claims.

## Delivered

- Local browser interface for photo upload, manually selected regions, capture feedback, neural reference retrieval and sourced-note retrieval.
- Reviewable reference metadata: visible label, vehicle/incident group, source and permission basis.
- Vehicle and component filters for reviewed source notes.
- Three primary-source research summaries; no real vehicle-damage reference photos bundled.
- Markdown export written by the server to D:.
- A CPU linear-head training command with grouped development validation and saved reports.
- Full run, training, dataset and storage instructions in `README.md`.

The app has **zero real training/reference photos** at delivery and **three knowledge summaries**. No damage classifier is active. The ImageNet feature extractor is pretrained by its upstream provider; no automotive training occurred during this build.

## Hardware and disk check

| Item | Observed |
| --- | --- |
| Physical RAM | 15,919,865,856 bytes, about 14.8 GiB |
| PyTorch | `2.14.0+cpu` |
| Torchvision | `0.29.0+cpu` |
| CUDA available | No |
| Inference threads | 4 |
| C: free at first check | 3,601,231,872 bytes, about 3.4 GiB |
| D: free at first check | 58,083,028,992 bytes, about 54.1 GiB |
| D: free after model and browser checks | 57,988,218,880 bytes, about 54.0 GiB |

The difference in drive free space is a system-wide observation, not a precise allocation measurement for this experiment. Browser-test weight paths use hard links to the same model file; summing file lengths recursively counts that file more than once.

The single downloaded weight file is **46,830,571 bytes**. All model, temporary and browser-test storage paths were placed on D:. No dependencies or datasets were installed or downloaded. Existing Python, Node and Chrome installations were reused. The desktop app's own cache behavior was not modified.

## Backend verification

Final run: **12 tests passed**, with the unittest suite taking **1.593 seconds** after imports. Checks cover:

1. Component-specific source exclusion and inclusion.
2. Duplicate-reference rejection.
3. 512-dimensional normalized, repeatable image features.
4. Invalid image encoding and unsupported-format rejection.
5. Exact-image and incident-group exclusion.
6. Linear-head optimization, grouped splitting and saved-head loading.
7. HTTP health, static resources, token rejection, analysis and Markdown export.
8. Three-class group splitting with both train and validation coverage.
9. No automatic conversion of retrieved labels into knowledge queries.
10. Heuristic feedback for a dark, small, low-detail image.
11. Normalized region bounds, minimum region dimensions and invalid-coordinate rejection.
12. Exact vehicle applicability, valid source URLs and required source review.

Fixture storage:

```text
D:\hakathon_wiut\finals\mdb-vision-finals\experiments\cardoctor-local\.runtime\tests\b693f3b8dc624cbaae369bf4f984cfdd
```

Training smoke checks use **synthetic orthogonal vectors and toy labels**, not car images. Their optimization result verifies the training machinery only. Synthetic fixture reports remain inside the isolated test directory and were not activated or added to the review library.

## Browser verification

The app's browser-control helper could not initialize because its Windows sandbox helper failed. Verification used **preinstalled Chrome with bundled Playwright** instead. Its browser profile, cache, temporary files and screenshots were on D:.

Final browser run: **8 workflow checks passed**, approximately **7.518 seconds** including local server startup and browser launch:

- Empty library and loaded-model state render correctly.
- A reviewed source note can be submitted through the form.
- A local image can be uploaded and a region selected by dragging.
- The reference dialog saves the label, group, source, permission and selected region.
- Image-reference matches and source-text matches render after analysis.
- Export creates a Markdown file on D:.
- A 390-pixel viewport has no horizontal overflow.
- No page JavaScript or console errors were observed.

A long report path initially overflowed on mobile; wrapping was fixed and the final check passed. A missing favicon request was also resolved. The test uses explicitly synthetic geometric images and synthetic source notes, isolated from the actual starter knowledge library.

Screenshots and machine-readable browser results:

```text
D:\hakathon_wiut\finals\mdb-vision-finals\experiments\cardoctor-local\.runtime\ui-tests\1791670003491
```

## CPU latency check

A separate check analyzed the same **synthetic 640 × 480 geometric image** six times with the three starter source notes and no reference photos:

| Request | Measured analysis time |
| --- | ---: |
| First request, including model construction and weight loading | 273.4 ms |
| Warm request 1 | 71.1 ms |
| Warm request 2 | 64.4 ms |
| Warm request 3 | 65.2 ms |
| Warm request 4 | 68.7 ms |
| Warm request 5 | 63.8 ms |
| Warm median | **65.2 ms** |

Timing comes from `core.analyze()` and includes decoding, features, capture checks and note retrieval. It excludes Python imports, browser rendering and file upload transfer. This small test does not measure performance on a large reference library, high-resolution real inputs, concurrent users or another machine. Raw observations are in `.runtime/benchmark.json`.

## Next useful experiment

Collect a small set of permission-cleared vehicle photos with consistent visible labels, vehicle IDs and incident groups. Reserve independent vehicle groups for final testing before adding development references. Verify whether the pretrained features rank relevant defects above lookalikes; then compare a trained classification head or specialist detector against this baseline.

Do not add the synthetic UI fixtures to that dataset. No damage detection accuracy, segmentation IoU, specialist calibration, repair-cost accuracy or field safety result is available yet.

## Local review status

The local server listens at `http://127.0.0.1:8765`. Its PID and logs are under `.runtime/`; `stop.ps1` checks process identity before stopping the recorded background instance. No commit, push, pull request, cloud deployment or team message was made during this build. The shared source implementation and task assignments were left unchanged.
