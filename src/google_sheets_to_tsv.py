#!/usr/bin/env python3
from pathlib import Path

import requests

SHEET_ID = "1yatMYkBVp7xac3DAJZ0r6jrtDBhyfjqAUcC1efDYLuc"
TAB_PREFIX = "BGCT"

# Map tab names -> gids for tabs exported into curation_tables/.
TABS = {
    "BGCT_annotation": "0",
}

OUTDIR = Path(__file__).resolve().parents[1] / "curation_tables"


def strip_prefix(name: str, prefix: str) -> str:
    pref = prefix + "_"
    return name[len(pref) :] if name.startswith(pref) else name


for tab_name, gid in TABS.items():
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=tsv&gid={gid}"
    )
    out_name = strip_prefix(tab_name, TAB_PREFIX) or "sheet"
    out_file = OUTDIR / f"{out_name}.tsv"

    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(out_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"Saved {out_file}")
