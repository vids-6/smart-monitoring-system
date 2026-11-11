# Data

No image data is distributed in this package. This folder documents what is needed and where it goes.

## 1. SKU-110K (detector training/validation: notebook 03)

**Automatic (what the notebook does):**
```python
from ultralytics.data.utils import check_det_dataset
check_det_dataset("SKU-110K.yaml", autodownload=True)   # downloads ~11.4 GB, converts CSV → YOLO labels
```
Ultralytics downloads `SKU110K_fixed.tar.gz` (URL in its `SKU-110K.yaml`, as shown in the notebook log) and builds:

```
datasets/SKU-110K/
├── images/            train_*.jpg, val_*.jpg, test_*.jpg   (11,743 images)
├── labels/            one .txt per image: "0 xc yc w h" (normalised)
├── annotations/       annotations_train.csv, annotations_val.csv, annotations_test.csv, readme.txt
├── train.txt  val.txt  test.txt
└── LICENSE.txt
```
Then edit `path:` in `configs/sku110k.yaml` to point at this folder (the original value is `/content/datasets/SKU-110K`).

Citation: Goldman et al., *Precise Detection in Densely Packed Scenes*, CVPR 2019. Read `LICENSE.txt` before sharing any images.

## 2. Images used in the notebooks (not included; ⚠ ask the author)

| File | Used in | Notes |
|---|---|---|
| `img1.jpg` … `img5.jpg` | 04_TestingAndResults | Uploaded via `files.upload()`. img4 shows an Alamy watermark; img5 appears identical to img1. |
| `self1.jpg` (1024×1024) | 06, 07, 08, 09 (+ the missing notebook that produced `detections.json`) | Only needed for drawing overlays; the numeric pipeline needs only `results/detection/detections.json`. |
| dashboard input video | dashboard | Produced `results/dashboard/annotated_20261029_085622.mp4`. |

If the author supplies these, place them in `data/sample/` and record their source and licence here.
