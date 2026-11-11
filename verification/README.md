# verification/ (added during packaging, NOT part of the original research code)

These helper scripts were written while organising the repository, so that reviewers can check the package
without a GPU or the dataset. They read the original files and never modify them.

| Script | What it does |
|---|---|
| `reproduce_inventory_json.py` | Re-runs the logic of notebooks 06–09 (code copied from the notebooks) on `results/detection/detections.json` and checks that `shelves.json`, `gaps.json` and `missing_products.json` are reproduced exactly. |
| `inspect_models.py` | Prints SHA-256, architecture and embedded metadata of `best.pt` and the classifier. `--write-metadata <dir>` regenerates the files in `results/detection/training/` and `configs/best_pt_train_args.yaml`. |
| `extract_training_log.py` | Extracts the training log from notebook 03 (cell 14) and parses per-epoch validation metrics to CSV. |
| `extract_figures.py` | Decodes the images saved in a notebook's outputs to files. |
| `run_dashboard_headless.py` | Executes the dashboard notebook without the install and launch cells, running its built-in self-tests; optionally analyses a video you provide. |

See `docs/VERIFICATION_REPORT.md` for the results obtained during packaging.
