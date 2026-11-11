"""Execute the dashboard notebook WITHOUT launching the Gradio server, to check that it loads both models
and that its built-in self-tests pass. The original notebook file is not modified; an executed copy is
written to verification/output/.

Skipped cells: the %pip install cell (cell 2: install requirements.txt yourself) and the blocking
`demo.launch(...)` cell (cell 27).

Usage (from the project root):
    python verification/run_dashboard_headless.py                 # self-tests only
    python verification/run_dashboard_headless.py path/to/video.mp4   # also runs analyze_video() on a real video
Requires: requirements.txt installed, plus `pip install nbclient ipykernel`.
"""
import os, sys, copy, shutil
import nbformat
from nbclient import NotebookClient

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "dashboard", "Supermarket_AI_Studio_Dashboard_v3_MissingProducts.ipynb")
WORK = os.path.join(ROOT, "verification", "output")
os.makedirs(WORK, exist_ok=True)
# The notebook searches its working directory for the model files.
for src in ("models/detector/best.pt", "models/classifier/grocery_classifier_1143.zip"):
    dst = os.path.join(WORK, os.path.basename(src))
    if not os.path.exists(dst):
        shutil.copy(os.path.join(ROOT, src), dst)

nb = nbformat.read(NB, as_version=4)
run = copy.deepcopy(nb)
run.cells = [c for i, c in enumerate(nb.cells) if i not in (2, 27)]
if len(sys.argv) > 1:
    video = os.path.abspath(sys.argv[1])
    run.cells.append(nbformat.v4.new_code_cell(
        f'out_video, summary, df_t, csv_t, st = analyze_video({video!r}, 0.40, 3, use_classifier=True, max_processed_frames=100)\n'
        'print({k: st[k] for k in ("processed_frames", "detections", "unique_tracks")}); print("video:", out_video); print("csv:", csv_t)'))
NotebookClient(run, timeout=1800, kernel_name="python3", resources={"metadata": {"path": WORK}}).execute()
out = os.path.join(WORK, "dashboard_headless_executed.ipynb")
nbformat.write(run, out)
for c in run.cells:
    for o in c.get("outputs", []):
        if o.get("output_type") == "stream":
            print(o["text"].rstrip())
print("\nExecuted copy written to", out)
