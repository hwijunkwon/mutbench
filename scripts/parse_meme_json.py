#!/usr/bin/env python3
"""Parse HyPhy MEME JSON output to CSV with per-site p-values."""
import json
import csv
import sys

def parse_meme_json(json_path, csv_path, threshold=0.1):
    with open(json_path) as f:
        data = json.load(f)

    # MEME results are in "MLE" -> "content" -> "0" (global results)
    # Each row: [alpha, beta-, p-(beta-), beta+, p-(beta+), p-value, ...]
    # The p-value for episodic selection is typically the last or 6th column

    content = data.get("MLE", {}).get("content", {})

    # Find the headers to identify p-value column
    headers_info = data.get("MLE", {}).get("headers", [])
    if headers_info:
        # headers is a list of lists: [[col_name, description], ...]
        col_names = [h[0] if isinstance(h, list) else h for h in headers_info]
        print(f"  MEME columns: {col_names}")
        # p-value column is typically "p-value"
        pval_idx = None
        for i, name in enumerate(col_names):
            if 'p-value' in str(name).lower() and 'beta' not in str(name).lower():
                pval_idx = i
                break
        if pval_idx is None:
            # Fallback: last column or index 5
            pval_idx = len(col_names) - 1
            for i, name in enumerate(col_names):
                if name == 'p-value':
                    pval_idx = i
                    break
        print(f"  Using p-value column index: {pval_idx} ({col_names[pval_idx] if pval_idx < len(col_names) else 'N/A'})")
    else:
        pval_idx = 5  # default MEME p-value position

    # Content "0" has the site-level results
    site_results = content.get("0", {})
    if not site_results:
        # Try getting from content directly if it's a list
        site_results = content

    rows = []
    if isinstance(site_results, dict):
        # Dict keyed by site index
        for site_key in sorted(site_results.keys(), key=lambda x: int(x)):
            site_data = site_results[site_key]
            pval = float(site_data[pval_idx]) if pval_idx < len(site_data) else 1.0
            pos = int(site_key) + 1  # 0-indexed to 1-indexed
            rows.append((pos, pval))
    elif isinstance(site_results, list):
        for i, site_data in enumerate(site_results):
            pval = float(site_data[pval_idx]) if pval_idx < len(site_data) else 1.0
            pos = i + 1
            rows.append((pos, pval))

    # Write CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['position', 'meme_pvalue', 'meme_significant'])
        for pos, pval in rows:
            sig = 1 if pval <= threshold else 0
            writer.writerow([pos, pval, sig])

    n_sig = sum(1 for _, p in rows if p <= threshold)
    print(f"  Total sites: {len(rows)}, Significant (p<={threshold}): {n_sig}")
    return len(rows), n_sig

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: parse_meme_json.py <input.json> <output.csv>")
        sys.exit(1)
    parse_meme_json(sys.argv[1], sys.argv[2])
