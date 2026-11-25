---
name: shop-machine-cad
description: Use when modelling a small machine, robot or jig built from bought parts (motors, rails, extrusions, boards, power supplies) plus printed and laser-cut parts, and the model has to match the real parts. Covers reading each part's listing, modelling it to the listing's own drawing and photos, the part and whole-machine checks, the look check against the listing photo, and handing renders to a website.
metadata:
  author: Alican Rowe (@alicanrowe)
---

# Shop machine CAD, true to the parts you buy

A machine model is only as believable as its bought parts. A NEMA17 drawn as a silver box with the wrong
body length makes the whole machine look invented. This skill makes every bought part match its listing,
then checks the machine as a whole.

The loop, per machine:

1. **Read every listing** (references/listings.md). Exact product, not a search page. Save the title, spec
   table, bullets and all photos. Find the dimension drawing among the photos; most motor, rail, board and
   supply listings have one.
2. **Spec each part** in `specs/<key>.json` (references/specs.md): the numbers, where each came from, and a
   sentence on how it looks. Listing drawing first, then the maker's datasheet, then measuring off a photo
   against a known feature. Say which.
3. **Model each part** in its own file, `parts/<key>.py` (references/modelling.md). Real silhouette,
   real colours per region, the features you can see from 1 m away: holes, connectors, labels, chamfers,
   fins, the flat on a shaft. Natural pose documented in the docstring.
4. **Check the part:** `scripts/check_parts.py <key>` until every line passes, then
   `scripts/look_sheet.py <key> --rx .. --az ..` turned to match the listing photo. Look at the sheet, write
   down what's off (colour, gloss, proportion, a missing feature), fix, repeat until it holds up.
5. **Build the machine from real parts.** Replace stand-in boxes with the part makers. Map every buy-list row
   to its parts in `specs/machines/<slug>.json`.
6. **Check the machine:** `scripts/check_machine.py <slug>`: every buy-list row modelled (or a reason it
   isn't), every part spec passing, no collisions, nothing floating, and every wire, lead and cable going from a
   real terminal to a real terminal without passing through anything. Fix the design, not the checker: a pen
   running through a servo, or a lead that stops in mid-air, is a real design error. Model every connector a
   wire plugs into (a plug on a host machine's cable, a terminal block); "it connects off-model" isn't a reason.
7. **Render and look** (references/renders.md): studio renders of each state and an exploded view, checked
   against the listing photos and the machine's neighbours on the site. Only passing renders go out.
   Animations and big jobs go to GarageFarm through the `render-farm` skill (github.com/alicanrowe/render-farm), which uploads and submits without anyone clicking renderBeamer.
8. **Hand off** to the site (website-publishing skill): renders, the parts table with listing links and
   photos, and the numbers you checked. Renders come out transparent: anything made from them (site JPEGs,
   pairs, crops, teasers, sheets) is flattened onto white with `on_white()` (in `scripts/check_backgrounds.py`),
   never a plain `convert("RGB")`, which turns the background black. Then
   `scripts/check_backgrounds.py <every output dir>` must show 0 FAIL. White unless the owner asked otherwise.

## Naming and copy
A machine is "it" in every README, recipe, build guide and page: never "she" or "her", and never framed as a
person who serves (the owner, 25 Nov 2026, renaming the old group because it read as subservient robots made women).
The owner's set is Hivemind (formerly The Dancers): Queen Bee plus 23 bee and hive names with no gender (never "worker" or "drone").

## Scripts (in `scripts/`)
| Script | Does |
|---|---|
| `extract_listing.js` | Run in the listing's browser tab; returns title, spec rows, bullets, photo URLs as JSON |
| `save_listing.py` | Saves that JSON to `specs/_listings/<asin>.json` and downloads the photos |
| `listing_sheet.py` | Contact sheet of a listing's photos, to find the drawing |
| `check_parts.py` | Part vs spec: overall and per-item sizes, palette materials, sources recorded |
| `look_sheet.py` | Part render beside its listing photo, with the check results |
| `check_backgrounds.py` | Every exported image sits on white: fails black (or, with `--opaque`, transparent) backgrounds; `--changed <repo>` checks a site branch's new images; `on_white()` flattens a render safely |
| `check_machine.py` | Buy-list coverage, part specs, collisions, floating parts, wire ends and wire clashes (`--wires-only` for a quick re-run) |

The kit paths default to your shop-bot kit (`SB_KIT` overrides): makers in `real.py` and `parts/`,
scenes built with `sbkit.py`, rendered by `blrender.py`.

## Excuses that don't count
Each of these is a shortcut that ends in a broken result. If you catch yourself thinking the left column, do the right column.

| The excuse | What to do instead |
|---|---|
| "I know roughly how big that motor is" | Model each bought part to its listing's own drawing and photos. |
| "The parts fit in my head" | Run the interference/clipping check on the full assembly. |
| "The background will be fine" | Flatten onto white and run `scripts/check_backgrounds.py`. |
| "The fetched product page says it's 42 mm" | Web-fetch tools hand back a short summary and can drop spec-table rows. Read the full listing or datasheet as text (a Firecrawl scrape, e.g. Composio's `FIRECRAWL_SCRAPE`, public pages only), and model from the numbers as written there, with the URL noted. |
| "While I'm in here I'll also tidy/refactor this other bit" | Change only what the task needs. Smallest diff that works; no new options, helpers or files nobody asked for. Note other ideas for later instead. |

## Keep this skill improving
When a check misses something a person spots, add the lesson to `references/lessons.md` (dated) and, if a
script could have caught it, to the script. No private data: no names, emails, home paths, unpublished prices.

**Design taste.** How a page, render or piece looks is judged against the shared `design-taste` skill (`../design-taste/` next to this skill): read its principles and banned moves, and score visual work with its rubric before showing it. When the client critiques how anything looks, log the exact words in its `critique-log.md` in the same session, distil them into its principles or rubric, and publish it with `_publish/sync.sh design-taste`.
