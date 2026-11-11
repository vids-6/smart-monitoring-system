# Reproducibility checklist (deliverable H)

✅ done/available · ⚠ partial / needs author action · ❌ missing

## Code and environment
- ✅ All original notebooks included unchanged, outputs preserved (`notebooks/`)
- ✅ `requirements.txt` derived from actual imports; pins only where the project states them
- ⚠ Exact library versions of the original Colab sessions only partly known (Ultralytics 8.4.138/147/154; torch 2.11.0+cu128)
- ⚠ Notebooks rely on `google.colab` uploads; a local run needs path edits (documented, not applied)
- ✅ Hardware documented (Tesla T4, 15 GB; training ≈ 4.3 h for 30 epochs)
- ✅ Random seed recorded (`seed=0, deterministic=True` in train args)

## Data
- ✅ Dataset identified (SKU-110K), download method and URL documented
- ✅ Directory structure, label format and class mapping documented
- ✅ Dataset config included (`configs/sku110k.yaml`, verbatim)
- ⚠ Dataset licence terms must be checked by the author before redistribution
- ❌ Test images `img1–5.jpg`, shelf image `self1.jpg`, dashboard input video not included

## Models
- ✅ Detector and classifier weights included, checksummed, load verified
- ✅ Detector training configuration extracted (`configs/best_pt_train_args.yaml`)
- ❌ Final 30-epoch detector weights (those behind the headline metrics) not included
- ❌ Classifier training code, data, preprocessing, class names not included

## Results
- ✅ Every reported number traced to a source file (`docs/RESULTS_AND_METRICS.md`)
- ✅ Detection metrics on the SKU-110K val split from log and checkpoint
- ❌ Detection metrics on the test split never computed
- ✅ Inventory JSON results reproduced exactly from `detections.json`
- ❌ `detections.json` cannot be regenerated (missing notebook + image)
- ❌ No quantitative evaluation of counting, missing-product detection, tracking or classification
- ✅ Visual results separated from quantitative ones; no metric fabricated or combined across tasks

## Package hygiene
- ✅ README and requirements in package root
- ✅ No secrets, credentials, virtual environments or caches
- ✅ Unrelated files excluded with reasons (`docs/FILE_INVENTORY.md` §G)
- ✅ Original → new mapping with checksums, so originals stay recoverable
- ⚠ Third-party (Alamy-watermarked) image remains inside notebook 04's saved output, flagged for the author
- ⚠ AGPL-3.0 implications of Ultralytics to be considered when choosing a licence (no LICENSE file added; the author must choose)

## To make the project fully reproducible, the author should
1. Add the 30-epoch `best.pt` (or re-state metrics for the shipped 9-epoch weights).
2. Add the notebook that creates `detections.json`, and `self1.jpg` with its source.
3. Add classifier training code and `class_names.json`, and report classifier test accuracy.
4. Run `yolo val ... split=test` and report test-split metrics.
5. Annotate a small set of shelf images (true counts, empty slots) to evaluate notebooks 06–09.
