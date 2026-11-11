# Known issues, inconsistencies and proposed improvements

**None of these were applied to the original notebooks.** They are documented so that reviewers and the author can decide. Severity: 🔴 affects claims or reproducibility · 🟠 affects correctness of a method · 🟡 minor or practical.

## Reproducibility and provenance

**I-1 🔴 The included `best.pt` is not the 30-epoch model reported in notebook 03.**
Evidence: the checkpoint stores Ultralytics 8.4.138, date 2026-09-03, 9 epochs, optimizer attached (24.5 MB), mAP50-95 0.511. The log in 03 shows 8.4.147, 30 epochs, a stripped 6.2 MB `best.pt`, mAP50-95 0.547. Epoch-1…9 metrics also differ between the two.
*Action:* upload `/content/drive/MyDrive/SKU110K_results/yolov8n_baseline/weights/best.pt` from the 30-epoch run, or report 0.511 as the metric of the shipped weights. Optional: strip the optimizer with `ultralytics.utils.torch_utils.strip_optimizer` on a **copy**. Do not overwrite the original.

**I-2 🔴 The notebook that creates `detections.json` is missing** (notebook numbers 02 and 05 are absent). The weights, confidence threshold (the data suggest 0.50) and the image `self1.jpg` used to create it are undocumented.

**I-3 🔴 Classifier provenance is missing.** There is no training code, dataset, class names, preprocessing, train/val split or accuracy. Classification therefore cannot be described as evaluated. The dashboard's preprocessing (224 px, ImageNet normalisation) is an assumption.

**I-4 🟠 Notebook 04 testing images are probably duplicated.** img5 has the same letterboxed size (384×640), the same 221 detections and a visually identical plot to img1. The summary lists 5 images, but there are likely 4 distinct ones.

**I-5 🟡 Versions drift across notebooks.** Ultralytics is 8.4.138 (01, dashboard, `best.pt`), 8.4.147 (03 run) and 8.4.154 (04). Nothing is pinned in 01/03/04 (`pip install ultralytics`).

**I-6 🟡 `max_det` differs between training and testing.** The 03 log uses `max_det=300`, while `best.pt` train_args has 718, because Ultralytics raises it when the data contain up to 718 objects. Prediction in 04 uses the default 300. SKU-110K-density shelves (up to 718 objects) could be truncated. The dashboard sets `MAX_DET = 500`.

**I-7 🟡 Notebook 03 writes to Google Drive without a `drive.mount()` cell.** It must have been mounted manually or in a deleted cell.

## Method correctness (inventory notebooks)

**I-8 🟠 `potential_missing_products` counts gaps, not products** (09, cell 14). The value 6 is the number of gap regions. The estimated product slots sum to 36.6.
*Proposal:* add `"estimated_missing_units": round(sum(...))` and rename the key in a new version.

**I-9 🟠 Shelf-end gaps are never checked** (08). Only gaps *between* neighbouring detections are measured. Empty space between the image or shelf edge and the first or last product cannot be flagged.

**I-10 🟠 Gap detection cannot separate "empty" from "not detected".** A missed detection creates a gap of exactly one product width and would be reported as missing. Gap 2 (23.8 px ≈ 1.15 product widths) is an example worth checking visually. The 20 px floor is in absolute pixels, so it changes meaning with image resolution and camera distance.
*Proposal:* normalise the threshold by the median product width, e.g. gap > 0.75 × width, and evaluate against a manually annotated set of empty slots.

**I-11 🟡 Status rule in 09 has little effect.** Every candidate gap is > 20 px and median widths are about 19–22 px, so `estimated ≥ 0.75` is satisfied by all candidates. "Small Gap" never occurs on this data.

**I-12 🟡 Gap lookup by floating-point size** (09, cell 13): `abs(gap["gap"] - candidate["gap"]) < 0.001`. This is fragile if two gaps on the same shelf have equal size.
*Proposal:* carry `left_product_index` through to `missing_candidates`.

**I-13 🟡 The two shelf-grouping methods (06 running mean ±50 px; 07 gap > max(5×median, 30)) are both tuned in absolute pixels.** They agree on this image (7 shelves, identical counts) but may not on tilted or perspective images. Neither handles shelves with a vertical step inside a row; shelf 1 contains products at y ≈ 145–159.

**I-14 🟡 Overlapping boxes** (13 negative gaps) are silently ignored in the median. They may indicate duplicate detections (NMS IoU 0.7).

## Dashboard

**I-15 🟡 Colab-only file handling.** Notebooks 04 and 06–09 use `google.colab.files.upload()`, so they cannot run locally without editing a cell. The dashboard already has local fallbacks.

**I-16 🟡 Pinned OpenCV 4.10.0.84 / Gradio 6.30.0.** During verification the pipeline ran with OpenCV 5.0.0 (the notebook printed a version warning only).

**I-17 🟡 Tracking quality is unmeasured.** Track IDs above 300 in a 10 s hand-held clip suggest identity fragmentation; no ground-truth tracks exist.

## Licensing and data

**I-18 🔴 A third-party image is embedded in notebook outputs.** The img4 output in 04 (cell 26) shows an Alamy watermark. Sources of `self1.jpg` and img1–5 are not recorded. Clear those outputs, or obtain permission, before public release.

**I-19 🟡 The AGPL-3.0 licence (Ultralytics) applies** to the trained weights and to code built on Ultralytics. Choose the repository licence accordingly.
