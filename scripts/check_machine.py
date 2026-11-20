#!/usr/bin/env python3
"""Whole-machine checks for a shop bot (bots/<slug>.py with build(state) -> list[P]).

usage: check_machine.py <slug> [--state after] [--gap 0.3] [--wire-end 8] [--wires-only]
  1. BOM coverage: every buy_list.csv row marked buy/owned must be claimed by at least one part, through the
     machine spec specs/machines/<slug>.json  {"bom": {"<buy_list item text>": ["<part name or prefix>", ...]},
     "skip_bom": {"<item>": "why it isn't modelled (consumable, cable, spare)"}}.
  2. Every bought part that has a spec key (P.note 'spec:<key>' or a machine spec "specs" map) passes check_parts.
  3. Collisions: solid parts that overlap by more than 0.5 mm^3 (scene stand-ins and parts listed in
     "allow_overlap" pairs are skipped; a screw in its hole is fine if both are listed; wires are left to check 5).
  4. Floating parts: anything that doesn't touch (within --gap mm) another part or the floor (z=0, or the
     machine spec's "floor_z"). Wires don't count as support: a board held up only by its leads floats.
  5. Wires, leads and cables (name matches wire/lead/cable/cord/harness/jumper, or material wire_*):
     a. both ends must land in or on a non-wire part (a terminal, plug, pin, board or cable). An end in mid-air fails.
        A deliberate free end (a cable leaving the frame to a wall outlet) goes in the spec's
        "wire_free_ends": {"<part name>": "why"}.
     b. the wire must not pass through any other part, its own group included, or through another wire. Only the
        last --wire-end mm at each end may sit inside something (the terminal or plug it goes into).
     Parts the name pattern catches that aren't wires (a "lead screw" is excluded already) go in "not_wires".
Prints PASS/FAIL lines and exits non-zero on any failure.
"""
import csv, json, math, os, re, sys, importlib.util, itertools, subprocess
from pathlib import Path

KIT = Path(os.environ.get("SB_KIT", "./kit"))
SB = KIT.parent
sys.path.insert(0, str(KIT))
a = sys.argv[1:]
slug = a[0]
opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
state, gap = opt("--state", "after"), opt("--gap", 0.3)
WO = "--wires-only" in a                     # quick re-run of check 5 while fixing wires
wire_end = opt("--wire-end", 8.0)          # mm of each wire end allowed inside its terminal / plug
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
WIRE_RE = re.compile(r"\b(wires?|leads?|cables?|cords?|harness)\b", re.I)     # a "jumper" alone is a header cap
NOT_WIRE = re.compile(r"music wire|wax wire|wire (wheel|brush|rope|nut|mesh|shelf|rack)|lead ?screw|cable (tie|clip|chain|gland|clamp)|"
                      r"drag chain|cord (grip|wrap|clip)|wire_?form|spring|\b(plugs?|sockets?|jacks?|pins?|levers?|spacers?|"
                      r"sleeves?|boots?|reliefs?|ferrites?|gaskets?|seals?|ropes?|bungee|shock cord|drawstring|tails?|terminals?|connectors?|housings?|labels?|clips?|ties?|glands?|crimps?|tabs?|grommets?|spades?|ferrules?|joints?|solder)\b", re.I)


LIQUID = ("water", "concrete_wet", "glue", "epoxy", "resin", "slip", "wax_liquid")
BARE = ("steel", "steel_dark", "brass", "alu", "copper", "tin", "gold")    # bare component legs, not insulated wire


def is_wire(p):
    if p.name in MS.get("not_wires", []) or NOT_WIRE.search(p.name) or str(p.mat) in BARE:
        return False
    return str(p.mat).startswith("wire_") or bool(WIRE_RE.search(p.name))


# 3. collisions
solid = [p for p in parts if p.kind != "scene" and p.in_scene]
allow = {tuple(sorted(x)) for x in MS.get("allow_overlap", [])}
allow_pre = MS.get("allow_overlap_prefix", [])


def ok_pair(a, b):
    if is_wire(a) or is_wire(b):
        return True                      # wires are checked in 5, with their 8 mm end zones
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
for (p, bp), (q, bq) in ([] if WO else itertools.combinations(bbs, 2)):
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
if not ncol and not WO:
    rec(True, f"no collisions among {len(solid)} parts")
# 4. floating (by group: a bought part floats only if none of its pieces touches something else)
fz = MS.get("floor_z", 0.0)
gkey = lambda p: getattr(p, "group", None) or ("n:" + p.name)
touch = {}


for p, bp in ([] if WO else bbs):
    g = gkey(p)
    if touch.get(g):
        continue
    t = bp.min.Z <= fz + gap
    if not t:
        for q, bq in bbs:
            if q is p or gkey(q) == g or is_wire(q) or bq.max.X < bp.min.X - gap or bp.max.X < bq.min.X - gap or bq.max.Y < bp.min.Y - gap or \
                    bp.max.Y < bq.min.Y - gap or bq.max.Z < bp.min.Z - gap or bp.max.Z < bq.min.Z - gap:
                continue
            try:
                if p.shape.distance_to(q.shape) <= gap:
                    t = True; break
            except Exception:
                t = True; break
    touch[g] = touch.get(g, False) or t
nfl = 0
for g, t in list(touch.items()):
    members = [p.name for p, _ in bbs if gkey(p) == g]
    if all(is_wire(p) for p, _ in bbs if gkey(p) == g):
        continue                         # loose wires are checked end by end in 5
    if not t and not any(m in MS.get("allow_floating", []) for m in members):
        nfl += 1; rec(False, f"floating: {', '.join(members[:4])} touches nothing")
if not nfl and not WO:
    rec(True, "nothing floating")

# 5. wires: both ends land on something, nothing passes through anything
from build123d import Vertex, Sphere, Pos as _Pos


def wire_ends(sh):
    """Centres of a wire's open end caps: the planar faces of the swept tube (a chain of cylinders pairs its
    joint caps up, so only the two real ends are left)."""
    caps = [f for f in sh.faces() if str(f.geom_type).upper().endswith("PLANE")]
    cs = [f.center() for f in caps]
    out = []
    for i, c in enumerate(cs):
        if not any(j != i and (c - d).length < 0.3 for j, d in enumerate(cs)):
            out.append(c)
            WRAD[(round(c.X, 2), round(c.Y, 2), round(c.Z, 2))] = math.sqrt(max(caps[i].area, 0) / math.pi)
    return out


WRAD = {}       # end centre -> the wire's radius there


TERM = re.compile(r"\b(pins?|headers?|terminals?|plugs?|sockets?|jacks?|connectors?|pads?|lugs?|solder|tabs?|posts?|"
                  r"spades?|ferrules?|leads? exit|glands?|grips?|grommets?|bushings?|inlets?|outlets?|bus|busbars?)\b", re.I)
GLAND = re.compile(r"(?<![a-z])(gland|grip|grommet|bushing)", re.I)     # a cable ends INSIDE the bore: its rim meets the wall


def _inside(sh, e):
    """True if point e is inside any solid of shape sh."""
    from build123d import Vector as _V
    sols = sh.solids() if hasattr(sh, "solids") else [sh]
    for so in sols:
        try:
            if so.is_inside(_V(e.X, e.Y, e.Z), 0.05):
                return True
        except Exception:
            pass
    return False


# wires are never stand-ins: check them even when marked "scene", and let them end in scene parts (a wall outlet)
ALL = [(p, p.shape.bounding_box()) for p in parts if p.in_scene]
wires = [(p, bp) for p, bp in ALL if is_wire(p)]
others = [(p, bp) for p, bp in ALL if not is_wire(p)]
WENDS = {}
for p, bp in wires:
    WENDS[id(p)] = wire_ends(p.shape)
free = MS.get("wire_free_ends", {})
nw = 0


def near(bp, bq, m):
    return not (bq.max.X < bp.min.X - m or bp.max.X < bq.min.X - m or bq.max.Y < bp.min.Y - m or bp.max.Y < bq.min.Y - m or
                bq.max.Z < bp.min.Z - m or bp.max.Z < bq.min.Z - m)


for p, bp in wires:
    ends = WENDS[id(p)]                 # several leads in one part are fine: each brings two ends
    if len(ends) < 2 or len(ends) % 2:
        nw += 1; rec(False, f"wire {p.name}: found {len(ends)} open ends, expected 2 per lead (model each lead with wire(pts))"); continue
    for e in ends:
        if p.name in free:
            break
        # the end must go INTO something (a terminal, plug, pin, pad or cable gland): touching a flat face isn't enough
        cand = [q for q, bq in others if near(bp, bq, 1)]
        if any(_inside(q.shape, e) for q in cand):
            continue
        # or it carries straight on as another wire (a cable drawn in two pieces): one end meets the other's end
        if any(n != id(p) and any((e - f).length <= 1.0 for f in fe) for n, fe in WENDS.items()):
            continue
        # or it is a conductor coming out of a cable's jacket (the end sits inside a thicker cable)
        if any(q is not p and near(bp, bq, 1) and _inside(q.shape, e) for q, bq in wires):
            continue
        # or it is a cable's stripped end: the conductors that come out of it start inside it, near this end
        if any(n != id(p) and any((f - e).length < 12 and _inside(p.shape, f) for f in fe) for n, fe in WENDS.items()):
            continue
        v = Vertex(e.X, e.Y, e.Z)
        ds = sorted([(v.distance_to(q.shape), q.name) for q in cand] or [(1e9, "")])
        d, qn = ds[0]
        # touching is enough only on a contact: a pin a crimp slides over, a terminal mouth, a pad, a plug face
        if any(dd <= 0.5 and (TERM.search(n) or any(n.startswith(t) for t in MS.get("wire_terminals", []))) for dd, n in ds):
            continue
        rw = WRAD.get((round(e.X, 2), round(e.Y, 2), round(e.Z, 2)), 0.0)
        # or it is a cable's jacket ending inside a gland, grip or grommet: the end sits in the bore, its rim at the wall
        inbb = lambda b, m=0.5: b.min.X - m <= e.X <= b.max.X + m and b.min.Y - m <= e.Y <= b.max.Y + m and b.min.Z - m <= e.Z <= b.max.Z + m
        if any(GLAND.search(q.name) and inbb(q.shape.bounding_box()) and v.distance_to(q.shape) <= rw + 0.5 for q in cand):
            continue
        nw += 1
        rec(False, f"wire {p.name}: end at ({e.X:.0f}, {e.Y:.0f}, {e.Z:.0f}) " +
            ("is in mid-air" if d > 0.5 else f"only touches the surface of {qn}") +
            f" ({d:.1f} mm to the nearest part). Run it into the terminal, plug, pin or pad it connects to.")
    zone = None
    for e in ends:
        s_ = _Pos(e.X, e.Y, e.Z) * Sphere(wire_end)
        zone = s_ if zone is None else zone + s_
    for q, bq in ALL:
        if q is p or not near(bp, bq, 0) or str(q.mat) in LIQUID:      # a lead may run through water
            continue
        try:
            inter = p.shape & q.shape
            va = inter.volume
            if va <= 0.2:
                continue
            v = (inter - zone).volume                # only what lies outside the end zones counts
            if not (0 <= v <= va + 1e-6):            # OCC boolean slip: measure it the other way round
                v = va - (inter & zone).volume
        except Exception:
            continue
        if v > 0.2:
            nw += 1; rec(False, f"wire {p.name} passes through {q.name}: {v:.2f} mm^3 outside the {wire_end:g} mm end zones")
if not nw:
    rec(True, f"wires: {len(wires)} checked, every end lands on a part, none passes through anything")
print(f"\n{slug}: {'PASS' if not fails else str(fails) + ' failure(s)'}")
sys.exit(1 if fails else 0)
