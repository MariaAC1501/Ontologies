#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

"""Generate a small HTML handoff page for manual PDF downloads."""

from __future__ import annotations

import argparse
import html
import json
import webbrowser
from pathlib import Path


def load_items(items_json: str | None) -> list[dict]:
    if not items_json:
        return []
    data = json.loads(items_json)
    if not isinstance(data, list):
        raise ValueError("--items-json must decode to a list")
    normalized: list[dict] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        normalized.append({
            "title": str(item.get("title", "Untitled paper")),
            "url": str(item.get("url", "")),
            "tier": str(item.get("tier", "supporting")),
            "note": str(item.get("note", "")),
        })
    return normalized


def build_html(drop_folder: Path, review_dir: Path | None, items: list[dict]) -> str:
    abs_drop = drop_folder.expanduser().resolve()
    review_dir_text = str(review_dir.expanduser().resolve()) if review_dir else ""

    rows = []
    for item in items:
        title = html.escape(item["title"])
        tier = html.escape(item["tier"])
        note = html.escape(item["note"])
        url = item["url"].strip()
        if url:
            link = f'<a href="{html.escape(url, quote=True)}">open link</a>'
        else:
            link = "no link available"
        note_html = f" — {note}" if note else ""
        rows.append(f"<li><strong>[{tier}]</strong> {title} ({link}){note_html}</li>")

    items_html = "\n".join(rows) if rows else "<li>No missing papers listed yet.</li>"

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>Manual PDF Drop</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }}
    code, pre {{ background: #f4f4f4; padding: 0.15rem 0.35rem; border-radius: 4px; }}
    .path {{ font-size: 1.05rem; }}
  </style>
</head>
<body>
  <h1>Manual PDF Drop</h1>
  <p>Download any obtainable PDFs into this folder <strong>without renaming them</strong>:</p>
  <p class=\"path\"><code>{html.escape(str(abs_drop))}</code></p>
  <p>The pipeline will normalize filenames later. Any missing paper that is still not present in this folder after your pass will be treated as inaccessible for this review run.</p>
  <ul>
    <li>Preferred browsers on macOS: Safari, then Chrome, then Firefox.</li>
    <li>Use institutional proxies / normal browser login / CAPTCHA handling as needed.</li>
    <li>Keep the original downloaded filenames.</li>
  </ul>
  {f'<p>Review directory: <code>{html.escape(review_dir_text)}</code></p>' if review_dir_text else ''}
  <h2>Still-missing papers</h2>
  <ol>
    {items_html}
  </ol>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an HTML handoff page for manual PDF downloads.")
    parser.add_argument("--output-path", required=True, help="Path to write README.html")
    parser.add_argument("--drop-folder", required=True, help="Manual PDF drop folder path shown to the user")
    parser.add_argument("--review-dir", help="Optional review directory path")
    parser.add_argument("--items-json", help="JSON list of missing-paper objects: [{title,url,tier,note}, ...]")
    parser.add_argument("--open", action="store_true", help="Open the generated HTML in the system browser")
    args = parser.parse_args()

    output_path = Path(args.output_path).expanduser()
    drop_folder = Path(args.drop_folder).expanduser()
    review_dir = Path(args.review_dir).expanduser() if args.review_dir else None
    items = load_items(args.items_json)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(drop_folder=drop_folder, review_dir=review_dir, items=items), encoding="utf-8")

    if args.open:
        webbrowser.open(output_path.resolve().as_uri())


if __name__ == "__main__":
    main()
