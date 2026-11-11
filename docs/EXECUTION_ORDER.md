# Execution order (derived from file reads/writes in the code)

The project has **two independent workflows** and **one isolated experiment chain**:

- **Workflow A1 (detector):** 01 → 03 → 04. Connected only through the `best.pt` file, which the user downloads and uploads manually.
- **Workflow A2 (inventory):** [missing notebook] → `detections.json` → 06 and 07 → `shelves.json` → 08 → `gaps.json` → 09. Connected through JSON files that the user uploads manually.
- **Workflow B (dashboard):** a self-contained notebook that needs only `best.pt`, the classifier and a video.

The workflow suggested in the brief ("footage → detection → tracking → classification → inventory analysis") is **only partly true**. Detection → tracking → classification are chained **inside the dashboard**. The shelf/gap inventory analysis (06–09) runs on a **single still image's detections** and never uses tracking or classification. The dashboard's "Missing Products" page is a *different* method: class-level presence or absence in a video compared with a reference.

---

### 01_Setup.ipynb (`notebooks/detection/`)
- **Purpose:** check the GPU and Ultralytics installation; run pretrained YOLOv8n on a demo image.
- **Prerequisites:** Colab GPU runtime, internet.
- **Reads:** downloads `yolov8n.pt`, `https://ultralytics.com/images/bus.jpg`.
- **Outputs:** displayed demo image only (Ultralytics 8.4.138; T4, CUDA 13.0 driver).
- **Run before:** nothing required.

### 03_Dataset_Exploration.ipynb
- **Purpose:** obtain and explore SKU-110K; define the dataset YAML; train YOLOv8n.
- **Prerequisites:** GPU, ~12 GB+ free disk, ~20 min download, ~4.3 h training on T4. **Google Drive must be mounted** (the notebook writes to `/content/drive/MyDrive/...` but has no mount cell).
- **Reads:** SKU-110K (auto-download), `yolov8n.pt`.
- **Writes:** `/content/sku110k.yaml`; `/content/drive/MyDrive/SKU110K_results/yolov8n_baseline/` (weights `best.pt`, `last.pt`, `epoch*.pt` because `save_period=1`, plus Ultralytics plots/CSV, none of which were uploaded).
- **Run before:** 01 (optional).

### 04_TestingAndResults.ipynb
- **Purpose:** qualitative test of a trained detector on 5 new shelf images; effect of confidence threshold on counts.
- **Prerequisites:** a trained `best.pt` uploaded to `/content`; `img1.jpg`–`img5.jpg`.
- **Reads:** `/content/best.pt`, `/content/img{1..5}.jpg`.
- **Writes:** `/content/runs/detect/predict*/` annotated images, `/content/result.jpg` (not uploaded).
- **Run before:** 03.

### [missing] notebook that produces `detections.json`
- Inferred from 06/07 inputs: runs the detector on `self1.jpg` and saves boxes with `confidence ≥ 0.50` (the minimum confidence in the file is 0.5000), in the schema documented in README §14. **⚠ Not provided.** Numbering suggests `05_*.ipynb` (also `02_*` is missing).

### 06_Count.ipynb (`notebooks/inventory/`)
- **Purpose:** total count, count per class, confidence-threshold sweep, shelf grouping (assign to the first shelf whose running mean y is within 50 px), per-shelf counts, overlay.
- **Reads:** `detections.json` (upload), `self1.jpg` (upload).
- **Writes:** nothing (printed results and figures only).
- **Run before:** the detections notebook. Independent of 07.

### 07_Shelves.ipynb
- **Purpose:** automatic shelf-row detection from gaps in the sorted y-centres (threshold `max(5 × median gap, 30)`), left-to-right ordering.
- **Reads:** `detections.json`, `self1.jpg`.
- **Writes:** `/content/shelves.json` → downloaded (`results/inventory/shelves.json`).
- **Run before:** the detections notebook.

### 08_Gaps.ipynb
- **Purpose:** horizontal edge-to-edge gaps between neighbouring boxes; candidate gaps > `max(2.5 × median non-negative gap, 20 px)`; estimated missing-product positions (gap midpoint).
- **Reads:** `shelves.json`, `self1.jpg`.
- **Writes:** `/content/gaps.json` → `results/inventory/gaps.json`.
- **Run before:** 07.

### 09_Missing.ipynb
- **Purpose:** estimated number of missing products per gap = gap / median product width of that shelf; status "Potential Missing Product" if ≥ 0.75, else "Small Gap"; final summary.
- **Reads:** `shelves.json`, `gaps.json`, `self1.jpg`.
- **Writes:** `/content/missing_products.json` → `results/inventory/missing_products.json`.
- **Run before:** 07 and 08.

### Supermarket_AI_Studio_Dashboard_v3_MissingProducts.ipynb (`notebooks/dashboard/`)
- **Purpose:** interactive video analysis with detection, ByteTrack, classification, KPIs and charts, CSV export, Missing Products comparison.
- **Prerequisites:** run cells top to bottom; cell 1 installs pinned packages (restart the session if prompted). The final cell launches Gradio and blocks.
- **Reads:** `best.pt`, `grocery_classifier_1143.zip`, optional `class_names.json`, user video, optional reference image or expected list.
- **Writes:** `supermarket_ai_outputs/` (annotated MP4, CSV, per-confidence ByteTrack YAML, evidence crops).
- **Run before:** needs only the two model files; independent of notebooks 01–09.
