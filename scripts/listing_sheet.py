#!/usr/bin/env python3
"""Contact sheet of one listing's photos, to find the dimension drawing. usage: listing_sheet.py ASIN [out.jpg]"""
import sys, glob, os
from PIL import Image, ImageDraw
K = os.environ.get("SB_KIT", "./kit")
a = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/{a}_sheet.jpg"
fs = sorted(glob.glob(f"{K}/specs/_listings/{a}/*.jpg")); W = 600; cols = 3
c = Image.new("RGB", (cols * W, ((len(fs) + cols - 1) // cols) * (W + 20)), "white"); d = ImageDraw.Draw(c)
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB"); im.thumbnail((W - 8, W - 8)); x, y = (i % cols) * W, (i // cols) * (W + 20)
    c.paste(im, (x + 4, y + 4)); d.text((x + 6, y + W), os.path.basename(f), fill="black")
c.save(out, quality=85); print(out)
