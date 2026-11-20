# Renders and the look check

- Part level: `look_sheet.py` beside the listing photo. Match colour, gloss, proportion and visible features.
  Turn the part (`--rx --ry --rz`) and camera (`--az --el`) to the photo's view, or the comparison lies.
- Machine level: the bots' studio look (white prints, soft key/fill/rim/top, shadow catcher, AgX). Render each
  state and an exploded view. Compare against the listing photos of the big parts (does the printer, laser or
  supply look like the photo?) and against the machine's neighbours on the site.
- Trace every wire in the render from one end to the other. It must leave a terminal, plug or pin and arrive at
  another, without vanishing into a block or stopping in mid-air. The check catches this in the CAD, but look anyway.
- Write down what's off, fix, re-render. Only renders that passed go to the site or to a person.
- Render on cloud machines. Split big batches one piece per machine.

## Lessons
- 2026-11-18: AgX lifts dark plastics to mid-grey under the studio lights. Motor bodies need a low-specular
  satin black (`satin_black`), and darker scenes may need exposure -0.5 to -0.8.
- 2026-11-18: saturated paints (orange) render salmon pink under AgX with the studio lights; use a darker, yellower base and low specular (`orange_paint`). Polished metal reflects the white studio and reads as white plastic; render polished stainless as satin grey (`steel_dark`). Try colours in a private kit copy (`SB_KIT`) first.
- 2026-11-18: large transmissive films (a vacuum bag pulled tight) render as an opaque grey sheet with the `bag`
  material and hide the work; `glass` lets the form read through. Keep `bag` for a loose, puffed bag.
- 2026-11-18: reds wash to salmon under AgX; use `red_deep` (S(140, 8, 10), coat 0.4) for red boards, rollers and buttons.
