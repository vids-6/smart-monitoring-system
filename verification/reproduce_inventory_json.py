"""Re-run the logic of 06_Count, 07_Shelves, 08_Gaps, 09_Missing headlessly (no image needed)
and compare against the JSON files saved by the original notebooks. Code copied from the notebooks."""
import json, sys, numpy as np
det_p, shelves_p, gaps_p, miss_p = sys.argv[1:5]
detections = json.load(open(det_p))
print("detections:", len(detections))
# --- 06_Count (cell 11) ---
def group_into_shelves(detections, y_threshold=50):
    detections_sorted = sorted(detections, key=lambda d: d["center_y"])
    shelves = []
    for detection in detections_sorted:
        placed = False
        for shelf in shelves:
            average_y = np.mean([d["center_y"] for d in shelf])
            if abs(detection["center_y"] - average_y) <= y_threshold:
                shelf.append(detection); placed = True; break
        if not placed: shelves.append([detection])
    for shelf in shelves: shelf.sort(key=lambda d: d["center_x"])
    return shelves
filtered = [d for d in detections if d["confidence"] >= 0.50]
c06 = [len(s) for s in group_into_shelves(filtered, 50)]
print("06 shelf counts:", c06, "total", sum(c06))
# --- 07_Shelves (cells 6-15) ---
y_positions = sorted(d["center_y"] for d in detections)
y_gaps = np.diff(y_positions)
threshold = max(np.median(y_gaps) * 5, 30)
sd = sorted(detections, key=lambda d: d["center_y"])
shelves, cur = [], []
for i, d in enumerate(sd):
    cur.append(d)
    if i < len(sd) - 1 and sd[i+1]["center_y"] - d["center_y"] > threshold:
        shelves.append(cur); cur = []
if cur: shelves.append(cur)
for s in shelves: s.sort(key=lambda d: d["center_x"])
shelf_data = [{"shelf_id": i, "product_count": len(s), "average_y": float(np.mean([d["center_y"] for d in s])), "products": s} for i, s in enumerate(shelves, 1)]
saved_shelves = json.load(open(shelves_p))
print("07 shelves.json identical:", shelf_data == saved_shelves)
# --- 08_Gaps ---
gap_data = []
for shelf in saved_shelves:
    p = sorted(shelf["products"], key=lambda d: d["center_x"])
    gap_data.append({"shelf_id": shelf["shelf_id"], "gaps": [{"left_product_index": i, "right_product_index": i+1, "gap": float(p[i+1]["x1"] - p[i]["x2"])} for i in range(len(p)-1)]})
all_gaps = [g["gap"] for s in gap_data for g in s["gaps"] if g["gap"] >= 0]
median_gap = np.median(all_gaps); gap_threshold = max(median_gap * 2.5, 20)
cand = [{"shelf_id": s["shelf_id"], **{k: g[k] for k in ("left_product_index","right_product_index","gap")}} for s in gap_data for g in s["gaps"] if g["gap"] > gap_threshold]
est = []
for c in cand:
    p = sorted(next(s for s in saved_shelves if s["shelf_id"] == c["shelf_id"])["products"], key=lambda d: d["center_x"])
    l, r = p[c["left_product_index"]], p[c["right_product_index"]]
    est.append({"shelf_id": c["shelf_id"], "gap": c["gap"], "estimated_x": float((l["x2"] + r["x1"]) / 2), "estimated_y": float((l["center_y"] + r["center_y"]) / 2)})
gaps_out = {"median_gap": float(median_gap), "gap_threshold": float(gap_threshold), "candidate_gaps": cand, "estimated_positions": est}
print("08 gaps.json identical:", gaps_out == json.load(open(gaps_p)), "| negative (overlapping) gaps excluded from median:", sum(1 for s in gap_data for g in s["gaps"] if g["gap"] < 0))
# --- 09_Missing ---
saved_gaps = json.load(open(gaps_p))
for s in saved_shelves: s["median_product_width"] = float(np.median([p["width"] for p in s["products"]]))
mc = []
for g in saved_gaps["candidate_gaps"]:
    w = next(s for s in saved_shelves if s["shelf_id"] == g["shelf_id"])["median_product_width"]
    e = g["gap"] / w
    mc.append({"shelf_id": g["shelf_id"], "gap": g["gap"], "typical_product_width": w, "estimated_products": float(e), "status": "Potential Missing Product" if e >= 0.75 else "Small Gap"})
pm = [c for c in mc if c["status"] == "Potential Missing Product"]
summary = {"total_shelves": len(saved_shelves), "total_candidate_gaps": len(saved_gaps["candidate_gaps"]), "potential_missing_products": len(pm), "details": pm}
print("09 missing_products.json identical:", summary == json.load(open(miss_p)))
print("sum of estimated_products over gaps:", round(sum(c["estimated_products"] for c in pm), 2))
