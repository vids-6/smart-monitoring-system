# Verification report (packaging, 31 Oct 2026)

**Environment used for checks:** Linux container, **CPU only** (no GPU), Python 3, torch 2.15.0, ultralytics 8.4.138, gradio 6.30.0, OpenCV 5.0.0, lapx. This environment is **not** identical to the original Colab/T4 setup.

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Included notebooks, models, JSON and video are byte-identical to the uploads | ✅ 15/15 files identical (`cmp`) | SHA-256 listed in `FILE_INVENTORY.md` |
| 2 | Notebooks are valid nbformat-4 files | ✅ 8/8 | |
| 3 | `best.pt` loads; architecture and metadata | ✅ YOLOv8n, 1 class, 3,011,043 params, Ultralytics 8.4.138, 9 epochs | `verification/inspect_models.py` |
| 4 | Classifier loads into torchvision ResNet18 with `strict=True`; forward pass | ✅ 25 outputs; random-input forward OK | |
| 5 | Inventory chain (06→07→08→09) reproduced from `detections.json` | ✅ exact match of all three JSON files; 06 counts reproduced | `verification/reproduce_inventory_json.py` |
| 6 | Dashboard notebook executes headlessly (all cells except pip-install and `launch`) | ✅ models found and loaded; ByteTrack threshold test and all three Missing-Products self-tests pass | `verification/run_dashboard_headless.py`; self-tests use synthetic fixtures defined in the notebook |
| 7 | Dashboard `analyze_video()` on a real shelf picture | ✅ runs end to end (detect → ByteTrack → classifier → MP4 + CSV) | Functional test only: a 30-frame panning clip cut from the `self1` figure in notebook 07's output gave 10 analysed frames, 1,314 detections, 246 track IDs. **Not an accuracy result; not included in results/.** |
| 8 | Training-log metrics extracted | ✅ 30 epoch rows parsed; final values match the log text | |
| 9 | Secrets / personal data | ✅ none found in notebook code, text outputs or metadata (pattern scan for keys, tokens, passwords, e-mail addresses) | Base64 image data excluded from the scan |
| 10 | README references resolve | ✅ all concrete paths exist (wildcards and the proposed `data/sample/`, `docs/media/` are intentional) | |

## Not tested (and why)
- **Training (notebook 03):** needs the 11.4 GB dataset, a GPU and about 4 hours.
- **Validation of `best.pt` on SKU-110K** (`yolo val`): dataset not available here, so reported metrics are copied, not re-measured.
- **Notebook 04:** test images missing.
- **Notebooks 06–09 as notebooks:** they need `google.colab` uploads and `self1.jpg`. Their logic was tested through the extracted-code script (row 5).
- **Generation of `detections.json`:** notebook missing.
- **Gradio UI interaction / public share link:** launch cell skipped; UI not clicked through.
- **GPU execution path** of the dashboard.
- **Accuracy of tracking, classification, counting or missing-product detection:** no ground truth exists.

**The complete pipeline was NOT tested as a single run**, because Parts A and B are separate and Part A has a missing step. The individual components were tested as listed above.
