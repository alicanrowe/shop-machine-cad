# Part specs (`specs/<key>.json`)

```json
{
 "key": "nema17",
 "name": "NEMA17 stepper, 38 mm body (STEPPERONLINE 17HE15-1504S)",
 "maker": "nema17",                       // function in parts/<key>.py or real.py
 "args": {"length": 38, "shaft": 23.5},   // the variant this listing is
 "listing": {"vendor": "Amazon", "asin": "B0B38GHRH8", "url": "https://www.amazon.com/dp/B0B38GHRH8",
             "title": "...", "photo": "_listings/B0B38GHRH8/01.jpg", "drawing": "_listings/B0B38GHRH8/04.jpg"},
 "sources": [{"what": "42.3 square, 38 body, 23.5 shaft ...", "from": "listing drawing (photo 04)"}],
 "tol_mm": 0.5,
 "overall_mm": [42.3, 42.3, 61.5],        // any order; compared sorted
 "overall_items": ["stepper face", "..."], // which items count (default: all but leads/wires/cables)
 "items": {"stepper shaft": {"bbox_mm": [23.5, 5, 5]}, "stepper boss": {"bbox_mm": [22, 22, 2], "tol_mm": 0.2},
           "servo body": {"axis_mm": {"z": 27.0}}},
 "look": "One or two sentences: colours and finishes by region, what you see first.",
 "used_by": ["sandra_paper", "..."]
}
```

- One spec per listing variant. Two listings for "the same" part (two NEMA17s) get two keys or args.
- Every number has a source. A number measured off a photo says what it was scaled from.
- Tolerance: 0.2 to 0.5 mm for machined parts and boards, 1 to 2 mm for moulded housings and supplies.
- Materials must exist in the renderer palette (`blrender.py`); add one there if a real finish needs it
  (`satin_black` was added for motor bodies: the old `black` rendered mid-grey).
