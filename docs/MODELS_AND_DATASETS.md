# Models and datasets

## 1. Detector: `models/detector/best.pt`

| Field | Value | How verified |
|---|---|---|
| Purpose | Find product-like objects on shelves (class-agnostic) | notebooks 03, 04, dashboard |
| Architecture | Ultralytics **YOLOv8n** `DetectionModel` (`depth_multiple 0.33`, `width_multiple 0.25`), `nc = 1`, names `{0: 'object'}`, 3,011,043 parameters | loaded with `torch.load`, `verification/inspect_models.py` |
| Initialisation | `yolov8n.pt` (COCO-pretrained), 319/355 tensors transferred | `train_args.model`, training log |
| Training data | `/content/sku110k.yaml` → SKU-110K | `train_args.data` |
| Key settings | epochs 30 (planned), imgsz 640, batch 16, optimizer auto, lr0 0.01, seed 0, deterministic, AMP, close_mosaic 10, save_period 1 | `configs/best_pt_train_args.yaml` |
| Saved by | Ultralytics **8.4.138**, date **2026-09-03 16:09 UTC** | checkpoint `version`, `date` |
| Epochs completed when saved | **9** (`epoch` field = 8, `train_results` has 9 rows) | checkpoint |
| Optimizer state attached | **Yes** → 24.5 MB (a stripped YOLOv8n is ~6 MB) | checkpoint |
| Val metrics stored inside | P 0.870, R 0.798, mAP50 0.867, mAP50-95 0.511 (`best_fitness` 0.51126) | `train_metrics` |
| Loaded by | `04_TestingAndResults.ipynb` (`YOLO("/content/best.pt")`); dashboard (`find_newest(["best.pt", ...])` in cwd, `/content`, `/content/drive/MyDrive`, `/mnt/user-data/uploads`, `/mnt/data`, or `DETECTOR_PATH_OVERRIDE`) | source |
| Included in ZIP | ✅ | |
| Licence | AGPL-3.0 (string stored in the checkpoint by Ultralytics) | checkpoint |

### Relationship to notebook 03 (⚠ important)
Notebook 03 logs a **complete 30-epoch run** (Ultralytics **8.4.147**, torch 2.11.0+cu128, Python 3.13, T4, 4.31 h). Its final stripped `best.pt` (6.2 MB) was saved to `/content/drive/MyDrive/SKU110K_results/yolov8n_baseline/weights/` and validated at P 0.900 / R 0.837 / mAP50 0.901 / mAP50-95 0.547.

The uploaded `best.pt` differs from that run:
- the Ultralytics version is different (8.4.138 vs 8.4.147);
- it covers 9 epochs, not 30;
- its size is different (24.5 MB vs 6.2 MB);
- its per-epoch metrics differ, e.g. epoch-9 mAP50-95 0.511 in the checkpoint vs 0.508 in the log;
- `max_det` is 718 in the checkpoint vs 300 in the log.

It is therefore a checkpoint from a **separate, earlier or interrupted training session** with the same configuration and run name (`yolov8n_baseline`).

**⚠ Needs verification by the author:**
1. Which weights were used in notebook 04 (installs 8.4.154; uploads an unidentified `best.pt`).
2. Which weights produced `detections.json`.
3. Whether the 30-epoch weights should be added (recommended).

## 2. Classifier: `models/classifier/grocery_classifier_1143.zip`

| Field | Value | How verified |
|---|---|---|
| Purpose | Assign each detected crop to one of 25 grocery classes | dashboard §6 |
| Format | PyTorch zip serialisation of an `OrderedDict` state-dict (archive root `grocery_classifier/`), 122 tensors, no metadata entries | `torch.load(..., weights_only=True)` |
| Architecture | torchvision **ResNet18**, `conv1` 64×3×7×7, `fc` 25×512, 11,189,337 parameters; loads with `strict=True` | `verification/inspect_models.py` |
| Class names | **Not stored anywhere** → displayed as `class_0`…`class_24` | checkpoint + dashboard logic |
| Preprocessing | **Not stored.** Dashboard assumes RGB, 224×224, ImageNet mean/std (stated as an assumption in its config cell) | dashboard §3 |
| Training data / code / metrics | **Not provided** | — |
| Meaning of "1143" in file name | Unknown (⚠) | — |
| Loaded by | dashboard (`find_newest(["grocery_classifier*.zip", "*.pt", "*.pth"])` or `CLASSIFIER_PATH_OVERRIDE`) | source |
| Included in ZIP | ✅ | |

Note: 25 classes is also the class count of some public grocery datasets, e.g. the Freiburg Groceries Dataset. **Nothing in the uploaded files links this classifier to any dataset**, so this must not be cited without confirmation from the author.

## 3. Other weights referenced
- `yolov8n.pt` (COCO-pretrained, downloaded automatically by Ultralytics in 01 and 03). Not included; regenerated on demand.
- `yolo26n.pt`, downloaded by Ultralytics only for the AMP check during training ("not used for training", per log). Not included.

## 4. Dataset: SKU-110K

| Item | Value (from notebook 03 outputs) |
|---|---|
| Source | Ultralytics `SKU-110K.yaml` autodownload → `http://trax-geometry.s3.amazonaws.com/cvpr_challenge/SKU110K_fixed.tar.gz` (11.4 GB); also `git clone https://github.com/eg4000/SKU110K_CVPR19` (paper repo, not used for training) |
| Local path in Colab | `/content/datasets/SKU-110K` |
| Structure | `images/` (all splits in one folder, e.g. `train_3607.jpg`, `test_2871.jpg`), `labels/` (YOLO txt, same stem), `annotations/annotations_{train,val,test}.csv` + `readme.txt`, `train.txt`, `val.txt`, `test.txt`, `LICENSE.txt` |
| Splits | train 8,219 (8,216 used, 3 corrupt), val 588, test 2,936 |
| Labels | YOLO format `class x_center y_center width height` (normalised); all `class = 0` |
| Class mapping | `{0: 'object'}` |
| Path configuration | `configs/sku110k.yaml` (`path:` key; written to `/content/sku110k.yaml` by 03 cell 12) |
| Max objects per image | train 576, val 718 (training-log warning) |
| Included in ZIP | ❌ must be downloaded separately; check `LICENSE.txt` |

## 5. Inventory input image `self1.jpg`
1024×1024 shelf image used by 06–09 (visible in `results/inventory/figures/07_input_shelf_image_self1.png`). **Not included; source and licence unknown (⚠).** `detections.json` coordinates are in this image's pixel space (x ∈ [0, 1024], y ≤ 899).
