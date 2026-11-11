# Packaging report (deliverable J)

## What was organised
18 uploaded items were inspected cell by cell, including saved outputs, checkpoint metadata and video frames. 15 of them were placed into a task-based structure:
- `notebooks/detection`: 01, 03, 04
- `notebooks/inventory`: 06–09
- `notebooks/dashboard`: the Gradio app
- `models/`: both weight files
- `results/`: detection, inventory and dashboard outputs, plus training logs and figures extracted from notebook outputs

Three items were excluded with reasons: an unrelated Kaggle notebook, an illustrated intro video and the instruction text. The mapping and checksums are in `FILE_INVENTORY.md`.

## What was preserved
- All included originals are **byte-identical**. Notebook outputs, code, weights and reported metrics are untouched. The only renames were removing the upload prefix and `__1_` → `01_Setup.ipynb`.
- Figures were decoded from the notebooks' own saved outputs. The training log was copied from notebook 03's output. Configuration was copied verbatim or read from the checkpoint.
- Bugs and inconsistencies are documented in `KNOWN_ISSUES.md`; none were fixed in place.

## Key findings reviewers should know
1. **Which components exist.** Detection, shelf counting and gap-based missing-product estimation are implemented as a still-image notebook chain. Tracking (ByteTrack) and classification (ResNet18, 25 unnamed classes) exist **only** in the separate dashboard notebook.
2. **The shipped `best.pt` is not the reported 30-epoch model.** It is a 9-epoch checkpoint from a separate run: val mAP50 0.867 / mAP50-95 0.511, against 0.901 / 0.547 in the 30-epoch log.
3. **Only detection has quantitative evaluation**, on the SKU-110K validation split. Counting, missing-product detection, tracking and classification have none.
4. **The inventory results are exactly reproducible** from `detections.json`. The step that creates that file is missing.
5. The dashboard **runs end to end on CPU** with the included weights, and its self-tests pass.

## What remains incomplete
See `MISSING_ITEMS.md`: the detections-generating notebook, the 30-epoch weights, the classifier provenance and class names, the test images and input video, ground truth for non-detection tasks, test-split metrics and a licence decision.

## How to run
See README §9–§13. The quickest check (no GPU, no data):
```bash
pip install -r requirements.txt
python verification/reproduce_inventory_json.py results/detection/detections.json results/inventory/shelves.json results/inventory/gaps.json results/inventory/missing_products.json
python verification/inspect_models.py
pip install nbclient ipykernel && python verification/run_dashboard_headless.py
```
