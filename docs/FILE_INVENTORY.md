# File inventory, mapping and exclusions

Deliverables A (inventory), C (original → destination mapping) and G (excluded files).

Uploaded file names carried an 8-character upload prefix, e.g. `05d8a25a-01_Setup__1_.ipynb`. The prefix was removed. `01_Setup__1_.ipynb` was renamed to `01_Setup.ipynb` because the `__1_` suffix is a browser download-duplicate marker. No other renaming was done. **Every included file is byte-identical to the upload.** Verify with the SHA-256 prefixes below (`sha256sum <file> | cut -c1-16`).

## A + C. Inventory and mapping

| # | Original upload | Type | Purpose / main functionality | Key dependencies | Essential? | Destination in package | SHA-256 (first 16) | Missing associated files |
|---|---|---|---|---|---|---|---|---|
| 1 | `01_Setup__1_.ipynb` | Colab notebook, outputs saved | Environment check: `nvidia-smi`, install Ultralytics, load pretrained `yolov8n.pt`, run on Ultralytics `bus.jpg` demo | ultralytics | Useful (setup evidence) | `notebooks/detection/01_Setup.ipynb` | `2007947b62835826` | none (downloads pretrained weights) |
| 2 | `03_Dataset_Exploration.ipynb` | Colab notebook, outputs saved | Clone SKU110K repo; auto-download SKU-110K via Ultralytics; inspect labels; visualise GT boxes; write `sku110k.yaml`; **train YOLOv8n, 30 epochs, imgsz 640, batch 16** (full log saved) | ultralytics, PIL, matplotlib | **Essential** (training + metrics) | `notebooks/detection/03_Dataset_Exploration.ipynb` | `45e5c9eb51293e15` | Google Drive mount cell; resulting 30-epoch `best.pt`/`last.pt` |
| 3 | `04_TestingAndResults.ipynb` | Colab notebook, outputs saved | Load `best.pt`; predict on 5 uploaded images; counts at conf 0.25–0.70 | ultralytics, IPython, matplotlib, google.colab | **Essential** (qualitative test) | `notebooks/detection/04_TestingAndResults.ipynb` | `c2349df993a2a4da` | `img1.jpg`–`img5.jpg`; identity of the `best.pt` used |
| 4 | `06_Count.ipynb` | Colab notebook, outputs saved | Load `detections.json`; total/class counts; confidence sweep; shelf grouping by running-mean y (±50 px); per-shelf counts | numpy, cv2, matplotlib, google.colab | **Essential** | `notebooks/inventory/06_Count.ipynb` | `e2dac266e48f3fa5` | `self1.jpg` |
| 5 | `07_Shelves.ipynb` | Colab notebook, outputs saved | Shelf-row detection from vertical centre gaps (threshold `max(5×median, 30)`); writes `shelves.json` | numpy, cv2, matplotlib, google.colab | **Essential** | `notebooks/inventory/07_Shelves.ipynb` | `cc86f29835c46bf6` | `self1.jpg` |
| 6 | `08_Gaps.ipynb` | Colab notebook, outputs saved | Horizontal gaps between neighbours; candidate gaps > `max(2.5×median, 20)` px; estimated positions; writes `gaps.json` | numpy, cv2, matplotlib, google.colab | **Essential** | `notebooks/inventory/08_Gaps.ipynb` | `08ae04aef1bf90d8` | `self1.jpg` |
| 7 | `09_Missing.ipynb` | Colab notebook, outputs saved | gap ÷ median product width per shelf → estimated missing count; status ≥ 0.75; writes `missing_products.json` | numpy, cv2, matplotlib, google.colab | **Essential** | `notebooks/inventory/09_Missing.ipynb` | `a4ba0ea060210607` | `self1.jpg` |
| 8 | `Supermarket_AI_Studio_Dashboard_v3_MissingProducts.ipynb` | Colab notebook, **no saved outputs** | Gradio dashboard: OpenCV → YOLOv8 → ByteTrack → ResNet18 classifier → annotated MP4/CSV; Missing Products page; built-in self-tests | ultralytics 8.4.138, gradio 6.30.0, torch, torchvision, opencv-headless 4.10, pandas, PyYAML, lapx | **Essential** (only tracking + classification code) | `notebooks/dashboard/…v3_MissingProducts.ipynb` | `14b058974936cc59` | `class_names.json` (25 class names); input video |
| 9 | `best.pt` | Ultralytics checkpoint (24.5 MB) | YOLOv8n single-class detector | ultralytics | **Essential** | `models/detector/best.pt` | `cd2f5b638e099b2a` | 30-epoch final weights (see KNOWN_ISSUES I-1) |
| 10 | `grocery_classifier_1143.zip` | PyTorch zip-serialised `state_dict` (44.8 MB) | ResNet18, 25 output classes | torch, torchvision | **Essential** for dashboard | `models/classifier/grocery_classifier_1143.zip` | `cefe2867bcf29f62` | class names, training notebook, dataset, preprocessing, metrics |
| 11 | `detections.json` | JSON (273 boxes) | Detector output on `self1.jpg` (1024×1024); input to 06/07 | — | **Essential** | `results/detection/detections.json` | `2a0ebfcf2d4e362d` | the notebook that generated it; `self1.jpg` |
| 12 | `shelves.json` | JSON | Output of 07; input to 08/09 | — | **Essential** | `results/inventory/shelves.json` | `12d6cca57b9f06ce` | — |
| 13 | `gaps.json` | JSON | Output of 08; input to 09 | — | **Essential** | `results/inventory/gaps.json` | `b6abd857cda3d2f4` | — |
| 14 | `missing_products.json` | JSON | Output of 09 (final inventory result) | — | **Essential** | `results/inventory/missing_products.json` | `05d26d5f0475aed0` | — |
| 15 | `annotated_20261029_085622.mp4` | H.264 video 464×832, 298 frames, 9.9 s | Dashboard output: HUD `frame N \| analysed \| interval 3`, boxes labelled `#track_id class_N` | — | Recommended (only evidence of tracking/classification run) | `results/dashboard/annotated_20261029_085622.mp4` | `662fbf5ae5175d71` | the input video |
| 16 | `Recording_2026-10-23_104003.mp4` | H.264 + AAC, 1486×986, 43.7 s, 18.2 MB | Illustrated/animated "Supermarket AI" intro clip (cartoon store scene), not model output | — | No | **excluded** | `6e62e1acd7efbe25` | — |
| 17 | `data.ipynb` | Kaggle notebook | **Unrelated**: Breast Cancer Wisconsin tabular classification (RF, DT, KNN, LR, NB) | sklearn, seaborn | No | **excluded** | `e07a411c130ae0c4` | — |
| 18 | `attachment.txt` | text | The packaging instructions (prompt) | — | No | **excluded** | `e7826661d972e455` | — |

### Not uploaded but referenced by the code
`02_*.ipynb` and `05_*.ipynb` (numbering gaps; 05 probably produced `detections.json`, ⚠ unverified) · `self1.jpg` · `img1.jpg`–`img5.jpg` · the 30-epoch `best.pt`/`last.pt` in `/content/drive/MyDrive/SKU110K_results/yolov8n_baseline/weights/` · classifier training notebook · `class_names.json` · the dashboard input video. See `MISSING_ITEMS.md`.

## Files added during packaging (not original work)

| File | Origin |
|---|---|
| `README.md`, `requirements.txt`, `.gitignore`, `data/README.md`, `docs/*.md`, `models/SHA256SUMS` | written during packaging |
| `configs/sku110k.yaml` | text copied verbatim from notebook 03 cell 12 |
| `configs/best_pt_train_args.yaml` | `train_args` dumped from inside `best.pt` |
| `results/detection/training/03_training_log_30_epochs.txt` | stdout of notebook 03 cell 14, ANSI codes stripped |
| `results/detection/training/03_training_log_per_epoch_val_metrics.csv` | rows parsed from that log |
| `results/detection/training/best_pt_checkpoint_metadata.json`, `best_pt_embedded_train_results.csv` | read from `best.pt` |
| `results/*/figures/*` | images decoded from saved notebook outputs (pixel-identical to what the notebook displays) |
| `verification/*.py` | helper scripts for inspection and re-checking |

### Figure mapping (notebook cell → file)

| Notebook / cell | File |
|---|---|
| 01 / 5 | `results/detection/figures/01_Setup_pretrained_yolov8n_bus_demo.png` |
| 03 / 8 | `results/detection/figures/03_sku110k_sample_train_6898.png` |
| 03 / 9 | `results/detection/figures/03_sku110k_sample_train_6898_gt_boxes.png` |
| 04 / 5 (identical to 04 / 8) | `results/detection/figures/04_img1_predictions_conf0.25.jpg` |
| 04 / 27 | `results/detection/figures/04_img5_predictions_conf0.25.png` |
| 04 / 26 (img4) | **not extracted**: Alamy stock-photo watermark (still visible inside the notebook output) |
| 06 / 9, 16 | `results/inventory/figures/06_detected_product_centers.png`, `06_shelfwise_product_count.png` |
| 07 / 4, 5, 8, 14 | `07_input_shelf_image_self1.png`, `07_detected_product_centers.png`, `07_vertical_gaps_plot.png`, `07_detected_shelf_rows.png` |
| 08 / 12, 14 | `08_candidate_gaps.png`, `08_estimated_missing_positions.png` |
| 09 / 12, 13 | `09_original_shelf_image.png`, `09_potential_missing_products.png` |

Notebook 04 cells 13, 16, 19, 22–24 printed raw NumPy arrays (`display(results.plot())`) instead of images, so there is no figure to extract.

## G. Files excluded from the ZIP

| File | Reason |
|---|---|
| `data.ipynb` | Unrelated project (breast-cancer tabular classification on Kaggle data). Its outputs could mislead reviewers into associating these accuracy figures with this project. |
| `Recording_2026-10-23_104003.mp4` (18.2 MB) | Illustrated/animated intro clip, not output of any model and not needed to reproduce anything. Add it to `docs/media/` if you want it for a presentation. |
| `attachment.txt` | Packaging instructions, not project content. |
| Duplicate figure 04 / cell 8 | Byte-identical to 04 / cell 5. |
| SKU-110K dataset (11.4 GB) | Too large; downloadable via Ultralytics; redistribution terms must be checked. |
| Runtime caches (`runs/`, `supermarket_ai_outputs/`, `yolov8n.pt`, `yolo26n.pt`) | Regenerated automatically; listed in `.gitignore`. |

No virtual environments, `.ipynb_checkpoints`, credentials, API keys or tokens were found in the uploads. A scan for `api_key|token|password|secret|hf_|sk-` returned no matches (see `VERIFICATION_REPORT.md`).
