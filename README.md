# Shop machine CAD

A Claude skill for modelling small machines, robots and jigs built from bought parts (motors, rails,
extrusions, boards, power supplies) plus printed and laser-cut parts, so that every bought part matches its
real listing.

The loop, per machine: read each part's listing, write a spec with where every number came from, model the
part to the listing's drawing and photos, check it (`scripts/check_parts.py`, then a look sheet turned to
match the listing photo), build the machine from those parts, and check the whole thing
(`scripts/check_machine.py`: every buy-list row modelled, no collisions, nothing floating, every wire running
terminal to terminal). Passing renders are flattened onto white and handed to a website.

| Path | What |
|---|---|
| `SKILL.md` | The steps. |
| `references/` | Listings, specs, modelling, renders, and lessons learned. |
| `scripts/` | Part and machine checks, look sheets, listing capture, background check. |
