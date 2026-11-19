#!/usr/bin/env python3
"""Check bought-part models against their listing specs.

usage: check_parts.py [key ...] [--kit DIR] [--all]
  Builds each part's maker (real.py or parts/<key>.py), measures it, and compares with specs/<key>.json:
  - overall bounding box (orientation-free: sorted extents) of the items the spec counts
  - per-item bounding boxes (sorted extents), and optional per-item axis extents
  - material names: every item's material must exist in the renderer's palette
Prints one line per check and exits non-zero if anything fails. Writes specs/_report/<key>.json.
"""
import json, os, re, sys, glob
from pathlib import Path

KIT = Path(os.environ.get("SB_KIT", "./kit"))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if "--kit" in sys.argv:
    KIT = Path(sys.argv[sys.argv.index("--kit") + 1]); args = [a for a in args if a != str(KIT)]
sys.path.insert(0, str(KIT))
import real as R  # noqa: E402
from build123d import Compound  # noqa: E402

PALETTE = set(re.findall(r'^(?:[\w, ]+=\s*)?(?:pbsdf|noisy|wood|grid)\("([a-z_0-9]+)"', open(KIT / "blrender.py").read(), re.M))
SKIP = re.compile(r"lead|wire|cable|cord(?!less)", re.I)


def ext(shape):
    b = shape.bounding_box()
    return [b.size.X, b.size.Y, b.size.Z], b


def srt(v):
    return sorted([float(x) for x in v], reverse=True)


def cmp(meas, want, tol):
    m, w = srt(meas), srt(want)
    bad = [(a, b) for a, b in zip(m, w) if b is not None and abs(a - b) > tol]
    return not bad, m, w


def check(key):
    sp = json.load(open(KIT / "specs" / f"{key}.json"))
    fn = getattr(R, sp.get("maker", key), None)
    out = {"key": key, "checks": [], "ok": True}

    def rec(name, ok, detail):
        out["checks"].append({"check": name, "ok": ok, "detail": detail}); out["ok"] &= ok
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")

    print(f"{key}  ({sp.get('name', '')})")
    if fn is None:
        rec("maker", False, f"no maker '{sp.get('maker', key)}' in real.py or parts/"); return out
    items = fn(**sp.get("args", {}))
    names = [n for (n, s, m) in items]
    tol = float(sp.get("tol_mm", 0.6))
    # overall
    if sp.get("overall_mm"):
        inc = sp.get("overall_items")
        use = [s for (n, s, m) in items if (n in inc if inc else not SKIP.search(n))]
        e, _ = ext(Compound(use))
        ok, m, w = cmp(e, sp["overall_mm"], tol)
        rec("overall", ok, f"model {[round(x, 1) for x in m]} vs listing {w} (±{tol})")
    # per item
    for iname, want in sp.get("items", {}).items():
        hit = [s for (n, s, m) in items if n == iname]
        if not hit:
            rec(f"item '{iname}'", False, f"not in model (has: {', '.join(names)})"); continue
        e, b = ext(Compound(hit))
        t = float(want.get("tol_mm", tol))
        if "bbox_mm" in want:
            ok, m, w = cmp(e, want["bbox_mm"], t)
            rec(f"item '{iname}'", ok, f"model {[round(x, 1) for x in m]} vs {w} (±{t})")
        for ax, val in want.get("axis_mm", {}).items():   # orientation-specific, e.g. {"z": 22.7}
            i = "xyz".index(ax); got = e[i]
            rec(f"item '{iname}' {ax}", abs(got - val) <= t, f"model {got:.1f} vs {val} (±{t})")
    # materials
    badm = sorted({m for (n, s, m) in items if m not in PALETTE})
    rec("materials", not badm, "all in the render palette" if not badm else f"not in blrender palette: {badm}")
    # listing record
    L = sp.get("listing", {})
    rec("listing", bool(L.get("url")) and bool(sp.get("sources")),
        f"{L.get('url', 'no url')} · {len(sp.get('sources', []))} source(s) for the numbers")
    return out


if __name__ == "__main__":
    keys = args or sorted(Path(p).stem for p in glob.glob(str(KIT / "specs" / "*.json")) if not Path(p).stem.startswith("_"))
    rep = [check(k) for k in keys]
    nfail = sum(not r["ok"] for r in rep)
    # One report file per part, written atomically, so parallel runs never clobber each other.
    rdir = KIT / "specs" / "_report"
    rdir.mkdir(exist_ok=True)
    for r in rep:
        tmp = rdir / f".{r['key']}.{os.getpid()}.tmp"
        json.dump(r, open(tmp, "w"), indent=1)
        os.replace(tmp, rdir / f"{r['key']}.json")
    print(f"\n{len(rep) - nfail}/{len(rep)} parts pass")
    sys.exit(1 if nfail else 0)
