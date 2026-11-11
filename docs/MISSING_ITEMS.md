# Missing dependencies, models, datasets and configuration (deliverable F)

| # | Item | Needed for | Impact if absent | How to obtain |
|---|---|---|---|---|
| 1 | Notebook that generates `detections.json` (probably `05_*.ipynb`) | Re-creating inventory input | Inventory chain starts from a saved file and cannot be re-derived from an image | Author |
| 2 | `02_*.ipynb` | Unknown (numbering gap) | Unknown; may be an abandoned step | Author to confirm whether it exists |
| 3 | 30-epoch `best.pt` / `last.pt` (6.2 MB each) from `MyDrive/SKU110K_results/yolov8n_baseline/weights/` | Matching the reported mAP 0.901 / 0.547 | Shipped weights correspond to 0.867 / 0.511 | Author's Google Drive |
| 4 | Ultralytics run folder (`results.csv`, `results.png`, PR/F1 curves, confusion matrix, `args.yaml`) of the 30-epoch run | Standard detection evaluation plots | Only text log available | Same Drive folder |
| 5 | `self1.jpg` (1024×1024) | Overlays in 06–09; regenerating `detections.json` | Numbers still reproducible from JSON; figures already saved | Author (+ source/licence) |
| 6 | `img1.jpg`–`img5.jpg` | Re-running 04 | 04 results not reproducible | Author (+ source/licence) |
| 7 | Classifier training notebook, dataset, split, preprocessing, metrics | Any claim about classification accuracy | Classifier only demonstrable, not evaluated | Author |
| 8 | `class_names.json` (25 names in training order) | Human-readable classifier labels; typed-name matching on the Missing Products page | Labels show `class_0`–`class_24` | Author (from the classifier's training `ImageFolder.classes` or equivalent) |
| 9 | Input video for `annotated_20261029_085622.mp4` | Reproducing the dashboard output | Output is qualitative only | Author |
| 10 | Ground-truth annotations for shelf counts, empty slots and tracks | Any quantitative evaluation of counting, missing-product or tracking | No accuracy claims possible for these tasks | Would need to be created |
| 11 | SKU-110K dataset | Training/validation | — | Ultralytics autodownload (see `data/README.md`) |
| 12 | Exact versions of torch/torchvision/numpy/matplotlib/pandas/Pillow used in Colab | Exact environment replication | Minor numerical differences possible | Run `pip freeze` in the original Colab session if still available |
| 13 | Google Drive mount cell for 03 | Running 03 unmodified | Training output path fails | Add `drive.mount('/content/drive')` before training |

Dependencies that must be installed separately: `ffmpeg` (system package, optional), a CUDA-matched PyTorch build (from pytorch.org), and `google.colab`, which exists only inside Colab.
