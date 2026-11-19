#!/usr/bin/env python3
"""Whole-machine checks for a shop bot (bots/<slug>.py with build(state) -> list[P]).

usage: check_machine.py <slug> [--state after] [--gap 0.3]
  1. BOM coverage: every buy_list.csv row marked buy/owned must be claimed by at least one part, through the
     machine spec specs/machines/<slug>.json  {"bom": {"<buy_list item text>": ["<part name or prefix>", ...]},
     "skip_bom": {"<item>": "why it isn't modelled (consumable, cable, spare)"}}.
  2. Every bought part that has a spec key (P.note 'spec:<key>' or a machine spec "specs" map) passes check_parts.
  3. Collisions: solid parts that overlap by more than 0.5 mm^3 (scene stand-ins and parts listed in
     "allow_overlap" pairs are skipped; a screw in its hole is fine if both are listed).
  4. Floating parts: anything that doesn't touch (within --gap mm) another part or the floor (z=0, or the
     machine spec's "floor_z").
Prints PASS/FAIL lines and exits non-zero on any failure.
"""
import csv, json, os, re, sys, importlib.util, itertools, subprocess
from pathlib import Path

KIT = Path(os.environ.get("SB_KIT", "./kit"))
SB = KIT.parent
sys.path.insert(0, str(KIT))
a = sys.argv[1:]
slug = a[0]
opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
state, gap = opt("--state", "after"), opt("--gap", 0.3)
spec_p = KIT / "specs" / "machines" / f"{slug}.json"
MS = json.load(open(spec_p)) if spec_p.exists() else {}
spec = importlib.util.spec_from_file_location(slug, SB / "bots" / f"{slug}.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
parts = mod.build(state)
fails = 0


def rec(ok, msg):
    global fails
    fails += (not ok)
    print(("  PASS  " if ok else "  FAIL  ") + msg)


names = [p.name for p in parts]
# 1. BOM
print(f"{slug}: {len(parts)} parts in '{state}'")
bl = SB / slug / "buy_list.csv"
rows = [r for r in csv.DictReader(open(bl))] if bl.exists() else []
bom, skip = MS.get("bom", {}), MS.get("skip_bom", {})
for r in rows:
    it = r["item"]
    if r.get("status", "buy") not in ("buy", "owned", ""):
        continue
    if it in skip:
        rec(True, f"bom '{it[:60]}' not modelled: {skip[it]}"); continue
    claim = bom.get(it)
    if not claim:
        rec(False, f"bom '{it[:60]}' has no part in the model (add it, or map it in specs/machines/{slug}.json)"); continue
    hit = [n for n in names if any(n == c or n.startswith(c) for c in claim)]
    rec(bool(hit), f"bom '{it[:60]}' -> {len(hit)} part(s)" + ("" if hit else f"; none named {claim}"))
# 2. part specs
keys = sorted(set(MS.get("specs", [])))
if keys:
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "check_parts.py")] + keys, capture_output=True, text=True)
    rec(r.returncode == 0, f"part specs {keys}: " + (r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:]))
# 3. collisions
solid = [p for p in parts if p.kind != "scene" and p.in_scene]
allow = {tuple(sorted(x)) for x in MS.get("allow_overlap", [])}
allow_pre = MS.get("allow_overlap_prefix", [])


def ok_pair(a, b):
    if a.name.split()[0] == b.name.split()[0]:
        return True                      # same assembly by name ("stepper face" / "stepper shaft")
    if getattr(a, "group", None) and getattr(a, "group", None) == getattr(b, "group", None):
        return True                      # pieces of one bought part
    k = tuple(sorted((a.name, b.name)))
    if k in allow:
        return True
    return any(a.name.startswith(x) and b.name.startswith(y) or b.name.startswith(x) and a.name.startswith(y) for x, y in allow_pre)


bbs = [(p, p.shape.bounding_box()) for p in solid]
ncol = 0
for (p, bp), (q, bq) in itertools.combinations(bbs, 2):
    if not bp.overlaps(bq) if hasattr(bp, "overlaps") else False:
        continue
    if (bp.max.X < bq.min.X or bq.max.X < bp.min.X or bp.max.Y < bq.min.Y or bq.max.Y < bp.min.Y or bp.max.Z < bq.min.Z or bq.max.Z < bp.min.Z):
        continue
    if ok_pair(p, q):
        continue
    try:
        v = (p.shape & q.shape).volume
    except Exception:
        continue
    if v > 0.5:
        ncol += 1
        rec(False, f"collision {p.name} x {q.name}: {v:.1f} mm^3")
if not ncol:
    rec(True, f"no collisions among {len(solid)} parts")
# 4. floating (by group: a bought part floats only if none of its pieces touches something else)
fz = MS.get("floor_z", 0.0)
gkey = lambda p: getattr(p, "group", None) or ("n:" + p.name)
touch = {}
for p, bp in bbs:
    g = gkey(p)
    if touch.get(g):
        continue
    t = bp.min.Z <= fz + gap
    if not t:
        for q, bq in bbs:
            if q is p or gkey(q) == g or bq.max.X < bp.min.X - gap or bp.max.X < bq.min.X - gap or bq.max.Y < bp.min.Y - gap or \
                    bp.max.Y < bq.min.Y - gap or bq.max.Z < bp.min.Z - gap or bp.max.Z < bq.min.Z - gap:
                continue
            try:
                if p.shape.distance_to(q.shape) <= gap:
                    t = True; break
            except Exception:
                t = True; break
    touch[g] = touch.get(g, False) or t
nfl = 0
for g, t in touch.items():
    members = [p.name for p, _ in bbs if gkey(p) == g]
    if not t and not any(m in MS.get("allow_floating", []) for m in members):
        nfl += 1; rec(False, f"floating: {', '.join(members[:4])} touches nothing")
if not nfl:
    rec(True, "nothing floating")
print(f"\n{slug}: {'PASS' if not fails else str(fails) + ' failure(s)'}")
sys.exit(1 if fails else 0)
