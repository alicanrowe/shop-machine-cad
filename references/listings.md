# Reading listings

## Which listing
- The exact product page (`/dp/<ASIN>` on Amazon), never a search URL. If the buy list only has a search, pick
  the listing: best match to the spec, real photos, a dimension drawing, decent reviews. Record the pick and why.
- Packs and kits: model one piece, note the pack size.
- Listings drift (same ASIN, new photos or a different variant). Save what you read with the date.

## How to read it
Amazon refuses cloud machines. Read it in a real browser, one tab at a time, closed when done:
1. Open the listing in a new tab.
2. Run `scripts/extract_listing.js` in that tab (it reads only that page: title, spec rows, bullets, photo URLs).
3. `save_listing.py '<json>'` saves it and downloads the photos (photos load fine from anywhere).
4. `listing_sheet.py <ASIN>` to see all photos at once. Close the tab.
Don't script a crawl through the person's logged-in browser; one listing per visit.
Other shops (maker sites, StepperOnline, Mean Well, Misumi) usually load from the cloud directly.

## What to take from it
- **Drawing** (usually photo 2 to 6): every dimension it gives. These beat the spec table.
- **Spec table:** "Product/Item dimensions" is often the package or rounded inches; use it only as a sanity check.
- **Title and bullets:** model numbers (look up the maker's datasheet), sizes in the title.
- **Photos:** colours and finishes per region, connector type and side, labels, what's black vs aluminium.
  The photo is the look reference for `look_sheet.py`.

## Lessons
- 2026-11-18: the "40 mm" NEMA17 on five bots is a 17HE15-1504S, **38 mm** body, black with a silver face
  plate only. The old model was 40 mm with silver caps at both ends. Both errors showed up on the first
  listing read.
- 2026-11-18: buy-list names drift from the product: a "V-wheel kit" listing was the mini V-wheel, a "2020 V-slot"
  was a T-slot, an "LRS-250-24" row pointed at an LRS-350-24 (Mean Well makes no LRS-250). Model from the
  listing's title and drawing, and tell every machine that uses the part when a fitting number changes.
- 2026-11-18 (Sandra Paper): check the listing title against the buy-list row first; the "BO5031K" link was a BO5041. When a listing has no drawing, the maker's spec table plus its 360-degree photo set (scaled from a known size such as the pad) is the drawing.
- 2026-11-18: read the drawing for how a part joins, not only its size. The K11-80 chuck has no thread (3x M6 on a
  66 circle, 55 register), so the design's "thread the spindle" step was impossible; kit photos also show contents the
  title leaves out (a T8 set's coupler and nut block, a 775 kit's bracket), and a "tool" can be inserts only.
- 2026-11-18: the buy-list name isn't the part. "50 kg bar load cells, 4-pack + HX711" was four half-bridge body-scale cells in 41 x 42 mm brackets; mounts designed from the name would not have let a cell flex. Also read the filament listing: its colour is the printed parts' colour, and the print volume has to fit the spool.
- 2026-11-18: read the listing title against the buy-list row text first. Dusty Springfield had a single gate sold as a
  "3-pack", a hose row that was an adapter set, a bucket row that was the lid only, and a vac with a different hose size.
