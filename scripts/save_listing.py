#!/usr/bin/env python3
"""Save one listing read (JSON from extract_listing.js) and download its photos.
usage: save_listing.py '<json>' [requested_asin]   or   echo '<json>' | save_listing.py - [requested_asin]
Writes specs/_listings/<asin>.json and specs/_listings/<asin>/NN.jpg; prints the photo paths."""
import json, os, sys, urllib.request
from pathlib import Path
KIT = Path(os.environ.get("SB_KIT", "./kit"))
raw = sys.stdin.read() if sys.argv[1] == "-" else sys.argv[1]
d = json.loads(raw)
d["imgs"] = [(u if u.startswith("http") else "https://m.media-amazon.com/images/I/" + u).replace("/images/images/", "/images/")
             for u in d.get("imgs", [])]
if len(sys.argv) > 2 and sys.argv[2] != d.get("asin"):     # the page redirected to another variant
    d["redirected_from"] = sys.argv[2]; d["asin_page"] = d.get("asin"); d["asin"] = sys.argv[2]
import datetime; d["read"] = datetime.date.today().isoformat()
out = KIT / "specs" / "_listings"; (out / d["asin"]).mkdir(parents=True, exist_ok=True)
json.dump(d, open(out / f"{d['asin']}.json", "w"), indent=1)
for i, u in enumerate(d["imgs"]):
    f = out / d["asin"] / f"{i:02d}.jpg"
    if not f.exists():
        try:
            urllib.request.urlretrieve(u, f)
        except Exception as e:
            print("fail", u, e); continue
    print(f)
