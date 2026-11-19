#!/usr/bin/env python3
"""Render a bought part beside its listing photo, for the look check.

usage: look_sheet.py <key> [--az -35 --el 24 --rx 0 --ry 0 --rz 0 --res 700 --samples 48]
  Builds the part from its spec (specs/<key>.json), renders it with the bots' own studio renderer (blrender.py)
  at the angle given, and lays it next to the spec's listing photo with the measured-vs-listing numbers from
  the last check_parts run. Output: specs/_looks/<key>.jpg
Compare: colours and finishes per region, proportions, the features you can see (holes, connectors, labels,
chamfers). List what's off, fix the maker, rerun. Pick --az/--el to match the photo's view.
"""
import json, os, sys, tempfile
from pathlib import Path

KIT = Path(os.environ.get("SB_KIT", "./kit"))
sys.path.insert(0, str(KIT))
import sbkit as S  # noqa: E402
import real as R  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

a = sys.argv[1:]
key = a[0]
opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
az, el, res, samples = opt("--az", -35.0), opt("--el", 24.0), opt("--res", 700), opt("--samples", 48)
rx, ry, rz = opt("--rx", 0.0), opt("--ry", 0.0), opt("--rz", 0.0)   # turn the part to match the photo
sp = json.load(open(KIT / "specs" / f"{key}.json"))
items = getattr(R, sp.get("maker", key))(**sp.get("args", {}))
parts = R.bought(R.place(items, 0, 0, 0, rx, ry, rz))
tmp = Path(tempfile.mkdtemp(prefix=f"look_{key}_"))
man = S.scene_manifest(parts, tmp / "m")
out_r = tmp / "render.png"
S.render([man], [out_r], az=az, el=el, res=res, margin=1.15, ground=True, extra=dict(samples=samples))

BR = "./fonts/"
f_t = ImageFont.truetype(BR + "Newsreader-300-opsz21.ttf", 30)
f_m = ImageFont.truetype(BR + "IBMPlexMono-Regular.ttf", 15)
W = 760
rend = Image.open(out_r).convert("RGBA"); bg = Image.new("RGBA", rend.size, (255, 255, 255, 255)); bg.alpha_composite(rend)
rend = bg.convert("RGB"); rend.thumbnail((W - 20, W - 20))
ph = sp["listing"].get("photo")
photo = Image.open(KIT / "specs" / ph).convert("RGB") if ph else Image.new("RGB", (W, W), "white")
photo.thumbnail((W - 20, W - 20))
_rp = KIT / "specs" / "_report" / f"{key}.json"
rep = json.load(open(_rp)) if _rp.exists() else {}
lines = [("PASS " if c["ok"] else "FAIL ") + c["check"] + ": " + c["detail"] for c in rep.get("checks", [])]
H = 110 + W + 24 * (len(lines) + 2)
c = Image.new("RGB", (2 * W, H), "white"); d = ImageDraw.Draw(c)
d.text((24, 26), sp.get("name", key), font=f_t, fill=(20, 20, 20))
d.text((24, 70), "LISTING PHOTO", font=f_m, fill=(120, 120, 120)); d.text((W + 24, 70), "MODEL", font=f_m, fill=(120, 120, 120))
c.paste(photo, ((W - photo.width) // 2, 100 + (W - photo.height) // 2))
c.paste(rend, (W + (W - rend.width) // 2, 100 + (W - rend.height) // 2))
y = 110 + W
d.text((24, y), (sp["listing"].get("url", "") + "   " + sp.get("look", ""))[:190], font=f_m, fill=(90, 90, 90)); y += 26
for ln in lines:
    d.text((24, y), ln[:190], font=f_m, fill=(150, 40, 28) if ln.startswith("FAIL") else (40, 40, 40)); y += 24
o = KIT / "specs" / "_looks"; o.mkdir(exist_ok=True)
c.save(o / f"{key}.jpg", quality=88)
print(o / f"{key}.jpg")
