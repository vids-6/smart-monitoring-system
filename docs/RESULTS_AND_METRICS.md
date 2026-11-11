# Results and metrics: provenance

Every number below is copied from a saved notebook output, a saved JSON file or the checkpoint metadata. Nothing was re-tuned or re-computed except where stated in the "Verified" column. Tasks are kept separate; **no metric from one task is combined with another.**

Legend: **Q** = quantitative metric with ground truth · **C** = raw count or estimate without ground truth · **V** = visual/qualitative example only.

## 1. Object detection

### 1.1 Validation metrics (Q): SKU-110K val split, 588 images, 90,968 instances, imgsz 640

| Run / weights | P | R | mAP50 | mAP50-95 | Source file | Verified |
|---|---|---|---|---|---|---|
| 30-epoch run, final best (epoch 29–30), weights **not in package** | 0.900 | 0.837 | 0.901 | 0.547 | `results/detection/training/03_training_log_30_epochs.txt` (last block) | copied from log |
| Included `best.pt` (9-epoch run, Ultralytics 8.4.138) | 0.87045 | 0.79829 | 0.86734 | 0.51126 | `results/detection/training/best_pt_checkpoint_metadata.json` | read from checkpoint |

Per-epoch curves: `03_training_log_per_epoch_val_metrics.csv` (30 rows parsed from the log) and `best_pt_embedded_train_results.csv` (9 rows from the checkpoint). Inference speed in the log: 0.3 ms preprocess, 9.4 ms inference, 7.9 ms postprocess per image on a T4.

**Not available:** test-split metrics; metrics on any non-SKU-110K image; class-wise metrics (single class).

### 1.2 Notebook 04: detections on uploaded images (C, V)

| Image | Input size (letterboxed) | Detections @ conf 0.25 | Notes |
|---|---|---|---|
| img1 | 384×640 | 221 | conf sweep: 0.25→221, 0.40→206, 0.50→190, 0.60→169, 0.70→111 |
| img2 | 640×480 | 126 | |
| img3 | 512×640 | 90 | 69 @ 0.50, 42 @ 0.60 |
| img4 | 480×640 | 220 | Alamy-watermarked stock image |
| img5 | 384×640 | 221 | ⚠ same size, same count and visually identical figure to img1, probably the same image |

These are **counts without ground truth**, so they say nothing about precision or recall. Prediction used Ultralytics' default `max_det=300`. The counts here stay below that cap, but denser shelves could be truncated (KNOWN_ISSUES I-6). The weights used are unconfirmed (I-1).

## 2. Inventory analysis on `self1.jpg` (C, V)

Input: `results/detection/detections.json`, 273 detections, all class 0, confidence 0.50–0.83+.

### 2.1 Counting: 06_Count and 07_Shelves (same result from two different grouping methods)

| Shelf | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Total |
|---|---|---|---|---|---|---|---|---|
| Products detected | 27 | 47 | 46 | 46 | 42 | 38 | 27 | **273** |
| Mean y (px), 07 | 151.6 | 294.9 | 424.1 | 531.5 | 645.4 | 752.1 | 874.7 | |

Confidence sweep (06): ≥0.50: 273 · ≥0.60: 258 · ≥0.70: 186 · ≥0.80: 12 · ≥0.90: 0.
These are **detected** counts, not true counts (no annotation of `self1.jpg` exists).

### 2.2 Gap detection: 08_Gaps (`gaps.json`)
Median non-negative gap 1.78 px (253 gaps; 13 overlapping pairs with negative gaps excluded), threshold 20 px.

| # | Shelf | Between products (1-based) | Gap (px) | Estimated position (x, y) |
|---|---|---|---|---|
| 1 | 1 | 13–14 | 218.5 | (612.6, 152.6) |
| 2 | 1 | 20–21 | 23.8 | (862.0, 151.7) |
| 3 | 5 | 14–15 | 54.9 | (339.4, 639.1) |
| 4 | 6 | 12–13 | 91.1 | (391.5, 737.5) |
| 5 | 6 | 18–19 | 35.0 | (531.9, 737.6) |
| 6 | 7 | 18–19 | 320.9 | (547.2, 869.2) |

### 2.3 Missing-product estimate: 09_Missing (`missing_products.json`)

| # | Shelf | Gap (px) | Median width (px) | Est. missing | Status |
|---|---|---|---|---|---|
| 1 | 1 | 218.5 | 20.6 | 10.59 | Potential Missing Product |
| 2 | 1 | 23.8 | 20.6 | 1.15 | Potential Missing Product |
| 3 | 5 | 54.9 | 22.1 | 2.49 | Potential Missing Product |
| 4 | 6 | 91.1 | 22.3 | 4.09 | Potential Missing Product |
| 5 | 6 | 35.0 | 22.3 | 1.57 | Potential Missing Product |
| 6 | 7 | 320.9 | 19.2 | 16.70 | Potential Missing Product |

Summary as saved: 7 shelves, 6 candidate gaps, `potential_missing_products: 6`. That value counts **gap regions**; the estimated product slots total 36.6 (I-8). There is no ground truth, so **no precision, recall or accuracy can be claimed** for missing-product identification.

**Verified during packaging:** `shelves.json`, `gaps.json` and `missing_products.json` are reproduced **exactly** (Python `==` on the parsed JSON) from `detections.json` by `verification/reproduce_inventory_json.py`, which contains code copied from notebooks 06–09. Notebook 06's shelf counts are also reproduced.

## 3. Tracking (ByteTrack) and classification (V only)
- `results/dashboard/annotated_20261029_085622.mp4`: 298 frames, 464×832, 30 fps, analysed every 3rd frame. Boxes are labelled `#<track id> class_<k>`. Track IDs above 300 appear by about frame 270.
- **No tracking metrics** (MOTA, IDF1, HOTA, ID switches) and **no classification metrics** (accuracy, confusion matrix) exist in the uploaded material. The classifier's class names are unknown.
- The input video for this output is not included, so the result cannot be reproduced.

## 4. Unrelated results (excluded)
`data.ipynb` reports 92–98 % accuracy for five scikit-learn models on the Breast Cancer Wisconsin dataset. **These figures have nothing to do with this project** and must not be cited for it.
