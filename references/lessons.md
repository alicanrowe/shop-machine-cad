# Lessons

Dated, newest first. Each is also written into the reference it belongs to.

## 2026-11-18
- Dusty Springfield: four of ten picked listings didn't match their buy-list row (a single gate sold as a "3-pack", a
  "hose + fittings" row pointing at a vac adapter set, a "bucket with lid" row pointing at the lid only, a vac whose hose
  is 1-7/8 in in a 2-1/2 in system). Read the title against the row text before modelling anything (listings.md).
- Hoses swept along a spline with tight bends can take many minutes to tessellate and stall the render export. Build
  ribbed hose as straight segments between the ribs; the ribs hide the joints and it exports in 0.1 s (modelling.md).
- Slip Kitten: check that a sensor actually carries the load it measures. The old model's load cell sat on the base while the cradle stood on its own ears beside it, so fill-by-weight could never work; the fix put the whole tilt station on the cell (fixed end on a foot, free end under the platform). Same pass: a row named "motor + board" was a listing for the board only, so read the listing title before trusting a row's description; and a printed ring cut shorter than the ring leaves a hidden 1 mm membrane, which check_machine catches as a collision with whatever passes through.
- Moisture Madame: a buy-list name can hide a different part type ("50 kg bar load cells, 4-pack + HX711" was half-bridge body-scale cells in brackets, so the old saddles could never have let a cell flex), and the printed parts take the bought spool's colour and must fit its mass (black PETG; solid stickers alone needed 2.2 kg of a 1 kg spool). Read the listing before designing mounts, sum the print volume, and check every board's connector against the supply (a USB-C ESP32 on a USB-A charger needed a cable that wasn't on the list).
- Check every printed part against the shop printer (Ender-3 V3 Plus, 300 x 300 x 330) before rendering: Glow Diva's
  back plate came out 347 mm long and had to be split into two halves with a half-lap (modelling.md).
- Skin Tight: check every bought part a made part has to fit INTO, not just onto. The vacuum former's sheet frame
  (410 x 330) could never go in the toaster oven on its own buy list (310 x 150 door); the fix sized the frame from
  the oven cavity inward. Same pass: anything that goes into a heat source must survive it. Printed PETG/ASA/PC
  bushings and standard neodymium magnets (about 80 C) don't survive 150-190 C (modelling.md).
- Lathe Minnelli: a listing can contradict the design, not just a size. The K11-80 chuck's drawing showed no thread
  (3x M6 on a 66 circle into a 55 register), so "thread the spindle for the chuck" was impossible; a bought back
  plate replaced the machining. A "turning tool" row was loose inserts only, and a "T8 set" row hid a coupler and
  a nut block in its photos but not its title. Read the drawing and every photo for how parts join, not only
  their sizes (listings.md).
- A function defined in two part files is resolved by file-name order, silently: a `mks_ts24()` in this thread's
  file overrode the DLC32 owner's maker of the same name. Before adding a maker, grep `parts/*.py` for `def <name>`
  as well as for the file name.
- Check that the picked listing is the product on the row, not just a match on keywords: Glow Diva's "NEMA17 with
  integrated lead screw" link was a bare screw-and-nut 2-pack, and its "1:1 epoxy" link a 2:1 deep-pour that a 1:1
  cartridge can't meter. Read the title and the mix ratio or kit contents against the row before modelling (listings.md).
- Wires swept along a spline (`wire()`/`bent_tube`) overshoot tight corners into neighbouring parts; for leads on a
  machine use straight runs with round joints, and end each lead on the board it plugs into, or it counts as floating
  (modelling.md).
- Cane-Dace: mark the work-in-progress (a seat frame, the woven cord) as its own kind ("work"), not "scene": check_machine skips scene parts, and that hid a frame running clean through all four of its cups. Two layout checks the renders hid: anything that turns (cups on a turntable) must sit on the turning part, and a rim-drive pulley can't share the rim's height with its motor body, so hang the motor below and make the rim two layers (belt land plus a smaller top disc) so the pulley's flanges clear. Weaves pass the collision check when cords are swept polylines (one solid each) changing layer in gaps at least two cord diameters wide between warp groups; thousands of cylinders and spheres made the check take minutes. Reds wash to salmon under AgX like black goes grey: use `red_deep` for red boards and buttons (modelling.md, renders.md).
- Flex Appeal: read what a kit actually is before designing around its name. The "vacuum bag kit" was a 52 in polyurethane tube with its own brass fitting and closure, so the platen goes inside the bag (no feet) and the printed bag port was dropped; the "-80 kPa" pump was -75 kPa, which moved the control band. Also check that every connection has a part on the list: nothing took the power brick's plug (a panel jack was added), and a lower-mount gauge can't go through a wall. A large transmissive film (the pulled-down bag) renders as an opaque grey sheet in this studio; use `glass` for tight film so the work reads through it (modelling.md, renders.md).
- A gantry can pass every render and still be unbuildable: Sandra Paper's V-wheels sat on top of rails bolted flat to the base (nothing under them), and no belt, pulley, supply or relay was modelled. For each axis, check what holds it on both sides and trace the drive path from motor to carriage. Lift rails on end feet when wheels must wrap them (modelling.md).
- A buy-list link can point at the wrong model: the "BO5031K" link was a BO5041 with a front handle. Check the listing title against the row before modelling, and use the maker's own spec table and 360 photos as the drawing when a listing has none (listings.md).
- Drag Queen: the old kit was designed from part names, and the listings broke it three ways: the solenoid frame (25 x 26) was bigger than its cradle (24 x 20), the MGN9H carriage ran off the rail bottom at blade-down, and the "36 x 18 in" cutting area was really the Ray5 extension kit's 850 x 850 mm. Model the bought parts first and design the printed parts around them. Also, spline wires bulge into neighbouring parts at tight bends; route leads as straight segments with sphere joints (modelling.md).
- Pour Decisions: a kit listing can change the whole look, not just sizes (the vacuum kit was stainless, glass and orange, not aluminium, acrylic and blue). Saturated colours need tuning in this studio: under AgX a plain orange base renders salmon pink; a darker, yellower base with low specular (`orange_paint` S(180, 60, 0), specular 0.2) reads orange, and a polished metal reads white, so polished stainless is rendered satin grey (`steel_dark`). Test colours in a private copy of the kit with `SB_KIT` before asking for palette changes. A pot's shaft can run parallel to its board (the CCMAC speed board), which decides how the pod mounts it; check the photos before designing the enclosure (renders.md, modelling.md).
- Honey Glaze: check_machine skips scene parts, so a tool head can run into its host machine unseen. The syringe holder's top arm went through the Ray5's X motor (it stands on the head carriage) and only a separate intersection test of every made and bought part against the scene parts caught it; run one for any head that mounts on another machine. Also, the shared Ray5 maker grew an extension-kit option (1036 x 1033) that moved the frame under the bench: re-run the machines that use a shared part when that part changes (modelling.md).
- Queen Bee: run every moving part through its whole stroke in the model. The old WX-1 put the T8 lead screw on the
  syringe axis through the pusher, so loading a full syringe drove the screw's free end into the plunger; plunger
  drives go beside the barrel, on a yoke. A syringe listing with no sizes can still be measured: its printed
  graduations (px per 5 mL) plus an assumed wall solve the bore, which is the slicer's filament diameter
  (modelling.md).
- Handmaiden: read what a kit actually contains before designing around it. The GT2 "pulleys + belt" listing was a
  20T + 60T (8 mm bore) aluminium pair, which replaced two printed pulleys and set the joint ratio (3:1) and the
  closed-belt centres (gt2_center_distance). The cup listing's G1/4 female insert also changed the printed cup bar
  (the buy list said M10 male). And name every part maker uniquely (t8x2_*, flex_coupler_5x8): parts/*.py load in
  alphabetical order, so a same-named maker in another thread's file silently replaces yours (modelling.md).
- Vogue: size the enclosure from the real stack, not the old box. The 36 mm base could not hold a 38 mm NEMA17 hanging
  from the top (the old model ran it through the bottom plate) and had no room or model for the Uno + CNC shield +
  A4988 at all (36 mm stacked). Add every buy-list electronics row to the scene first, then set the wall height; and
  check board colours on the current listing photos (the Elegoo UNO R3 is now black, the CNC Shield V3 kit red) (modelling.md).
- Lady Liner: a tall tool (a posted pen is 162 mm) beside a servo only clears it if they are apart in x, not just in z. Stand the servo on its narrow side (12 mm wide) between the tools and keep the rocker in its own y plane in front of the pens; then the check passed with no clearance tricks. Also check the host machine's own parts above the swap plate (the Ray5 X motor shaft) before sizing a head plate (modelling.md).
- Shared motion parts: the buy-list names were wrong three times, and only the listing showed it. The "V-wheel
  kit" is the mini wheel (15.3 OD, not 23.9), which moves wheel centres from depth + 20 to depth + 12; the "2020
  V-slot" is a European T-slot; "LRS-250-24" doesn't exist (the listing is an LRS-350-24). Read the listing title
  and drawing before modelling from the name (listings.md).
- check_parts.py missed palette materials defined with an assignment (`_m, _b = pbsdf("satin_black", ...)`), so
  every part using satin_black failed; the regex now allows it.
- A toothed 20T GT2 idler can't hold 625 bearings (16 OD inside a 12.2 tooth band); check that a bought part's own
  pieces fit inside it before rendering (modelling.md).
- First listing read (NEMA17 17HE15-1504S) caught two errors in the old model: body 38 mm not 40, and black
  caps with a silver face plate, not silver caps at both ends (listings.md).
- First machine check (Lady Liner) found real design errors the renders hid: the pen cap running through the
  servo body, the scribe holder through the servo bracket. Checkers must treat one bought part's own pieces as
  one part, or the real errors drown in noise (modelling.md).
- AgX renders `black` as mid-grey: use `satin_black` for motor bodies (renders.md).
- Mother: read where the bought box actually sits before placing a heater. The 56 qt latching box stands on
  wheels, so a heat mat "under the tote" would heat a 6 mm air gap; the IP67 mat moved inside under a printed
  rack. Wheels, feet and lids change how a bought container meets the table (modelling.md).
- A clear base with a near-mirror finish (roughness under 0.1) throws a sharp reflection of what's inside onto
  its walls that reads as a second object; frosted storage plastics need roughness about 0.3 (renders.md).
- Shared `parts/__pycache__` can be half-written by a parallel thread ("marshal data too short"); set
  `PYTHONPYCACHEPREFIX` to your own scratch folder when several threads import the kit at once.
- Shared-parts batch (13 listings): a buy-list row's link can be a different product from its text (a "NEMA17 with
  integrated screw" row linked a bare screw and nut; a "17HS08 34 mm" ask is really a 20 mm pancake). Read the
  title against the row before modelling, and send the mismatch back to the machine (listings.md).
- AgX Punchy desaturates strong colours whatever the base value: a swatch test from S(6, 38, 120) down to
  S(0, 20, 80) all rendered periwinkle, and magenta labels render pink. Judge saturated parts by hue and layout on
  the look sheet, not by matching the photo's saturation (renders.md).
- The pin-header helper's "black" plastic renders mid-grey; boards read right only with headers, chips and black
  PCBs in `satin_black` (renders.md).
- Mortisha: read a kit's whole contents against the rest of the buy list. The DLC32 kit already held three
  endstops and three drivers (a separate endstop pack was dropped), and the "belt + pulleys" kit had no idlers
  that three omega drives need (a 5-pack row was added). Count pulleys, idlers and belt length per drive.
- Parts of kind "scene" are left out of the collision and floating checks, so a duplicate plate marked "scene" let
  an endstop screwed to it read as floating, and could hide a real clash. Give every modelled piece a real kind.
- Part file and spec keys share one folder across threads: a generic key (`coupler_5x8`, `t8_leadscrew`) was
  overwritten by another thread within the hour. Name a machine-only part after its listing or kit (`t8kit_rod`).
- Export file names come from the part name, so `P("mt_y_side_plate R", ..., laser=...)` wrote a DXF with a space
  in its name. Give the piece that carries the laser or STL the clean base name.
- Cher Bend: check the listing's ratings and stock sizes against how the machine uses them, not just the part's shape. Reflectix is rated to 180 F, so a lining inside a 100 C steam box fails (it moved outside); PETG softens near 80 C, so nothing printed may sit in the steam; and a 712 mm panel on a buy list of 12 x 24 in sheets can't be cut. A nesting check that places every laser part on the listed sheets (`check_layout()` in bots/cher_bend.py) catches the last one.
- Hot Flash: a listing's main photo can be an edited image that contradicts the product. The toaster oven's photo
  00 shows the door handle at the bottom; its four real photos all show it across the top. Model from the photos
  that agree, and use the dimension photo for proportions (listings.md).
- Hot Flash: check that every bought part is powered and mounted, not just listed. The buy list had a 12 V fan and
  nothing that made 12 V; a mains-to-12 V module (HLK-PM12) in the pod fixed it without a second cord.
- Hot Flash: a probe's real length decides where it can go. The kit's thermocouple is an M6 screw probe with a
  12 mm thread, too short to reach through an oven's skin, air gap and liner; it now nuts to the liner through a
  13 mm skin hole. Model wall thickness and the probe together before choosing the hole.
- Bog Witch: check every panel against the sheet you buy and every print against the bed before modelling the
  rest. The old cabinet's back (460 x 420) and door (454 x 420) fit no 12 x 24 in sheet, and its 460 mm tray and
  440 mm shelves fit no 300 mm bed; resizing to 580 x 290 panels and splitting the tray into two trays plus a
  reservoir fixed both. Clear panels read as fogged in "acrylic"; use "glass" with transparent glass on so the
  inside shows, and check a bpy attribute exists (sc.cycles.film_transparent_glass) before suggesting it.
- Lazarella: check that bought parts fit each other, not only that each one matches its listing. The buy list paired
  25 mm ID band heaters with a 26.7 mm OD pipe and a 15.9 mm auger with a 20.9 mm bore; the fix was the smaller
  pipe plus a shim sleeve. Also list what screws into what: the wax adapter was 1/8 NPT with no 1/8 NPT port, and
  M6 screw thermocouples (14 mm) would have reached the auger through a 2.8 mm pipe wall without a jam nut.
- Lazarella: build123d's project_to_viewport (hidden-line removal) stalls for 20+ min on a machine with helical
  flights, threads and knurls, and even a whole-scene run with those swapped out still stalled. What worked (14 s):
  project each part on its own, swap parts with more than ~40 faces for their bounding box or cylinder, and box any
  single part that still hangs (here the ground auger flutes). SIGALRM can't interrupt the OCC call, so find the
  hanging part by printing each name before it projects. Script: shop-bots/lazarella/site/make_dims.py.
- Sterling Silva: run check_machine on every storyboard pose (park, pick, tack), not only the finished one. The
  finished pose hid a servo hitting the lead screw at high X and a tray row out of reach. Then compare the dims
  bounding box with the base: a bought motor's flying leads 22 mm past the base edge made the overall width 422
  instead of 400; turning the motor so its leads ran over the base fixed it.
