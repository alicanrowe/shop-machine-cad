# Modelling bought parts and machines

## Bought parts
- One file per part key in `parts/`: `parts/<key>.py` defines `<key>(...)` returning `[(name, shape, mat), ...]`.
  A function with the same name as one in `real.py` replaces it, so parallel work never edits a shared file.
- Item names start with one shared word for the part ("stepper face", "stepper shaft"): the machine checker
  treats items sharing that first word, or made in one `R.bought()` call, as one part.
- Model what reads from a metre: silhouette, chamfers and fillets, holes, connectors, labels, heat sinks,
  fins, cable exits, the flat on a shaft, screw heads. Skip internal detail.
- Colours by region from the photos, not from memory. Black anodised, satin black, gloss black and grey
  plastics are different materials.
- Check the part's own pieces fit each other (a bearing inside a pulley's tooth band, a spacer through a wheel):
  a 625 bearing drawn inside a 20T idler cut the teeth away and nobody saw it until the render.
- Natural pose in the docstring (which face sits at z=0, which way the shaft points) and keep it.
- Cables: a short stub out of the real exit, so the part doesn't look unplugged. Full cable runs belong to the
  machine.

## Machines
- Build from part makers placed with `R.place()` and wrapped by `R.bought()`. No stand-in boxes for anything on
  the buy list.
- Printed and laser parts are designed around the real bought parts: pockets from the real body sizes plus
  clearance (0.2 to 0.4 mm printed), screw holes from the real hole pattern.
- Map every buy-list row to its parts in `specs/machines/<slug>.json` (`bom`), or say why not (`skip_bom`:
  consumables, spares, cables, tools). List deliberate overlaps (a screw in a heat-set insert) in
  `allow_overlap`.
- Trace every connection to a part on the buy list: power plug to a jack, hose to a barb of the right size, a
  gauge's mount type (lower vs back mount) to where it can go. Add the missing row rather than leave a gap.
- Fix collisions in the design. Moving a part 2 mm to make a check pass when the real one wouldn't fit is
  the thing this skill exists to stop.
- Tall tools beside an actuator: separate them in x, not just z (a posted pen is 162 mm tall). Mount the servo on its narrow side between the tools and run linkages in their own plane. Model the host machine's parts near the mount (motors, shafts above a swap plate) before sizing the head plate (Lady Liner, 2026-11-18).
- Enclosures: put every bought part that lives inside (motor hanging from the top, board stacks with drivers and
  heat sinks) into the scene before setting wall heights; a stacked Uno + CNC shield + A4988 is about 36 mm tall.
- Give each maker a name no other part file uses (prefix it with the product, e.g. `t8x2_screw`): parts load
  alphabetically and a later file's `t8_screw` silently replaces yours (2026-11-18, Handmaiden).
- Closed belts fix the pulley centres: use `gt2_center_distance(L, t1, t2)` and slot the motor holes +-1.5 mm along
  the belt for tension.
- Pose every moving part at both ends of its stroke and run the check in each (2026-11-18, Queen Bee: an on-axis
  lead screw met the plunger only at full load). Drive a syringe plunger from beside the barrel, through a yoke
  that also holds the thumb pad so it can retract.
- A syringe listing with no drawing: scale it from a straight side photo using its printed graduations. Px per
  5 mL and the barrel's px width, with a 1.0 mm wall, solve pi/4 * ID^2 * pitch = 5000 mm^3 for ID.

- Wires and leads: route them as straight segments with sphere joints, not splines; a spline bulges into neighbouring parts at tight bends (Drag Queen solenoid leads). Model every bought part from its listing before designing the printed parts around it: Drag Queen's old cradle was smaller than the real solenoid and its carriage ran off the rail at full stroke.
- 2026-11-18 (Sandra Paper): for each axis, check what holds it on both sides and trace the drive from motor to carriage. V-wheels sitting on top of a rail bolted flat to the base, with no belt modelled, rendered fine and could not work. Lift rails on end feet when wheels must wrap them.
- Give the workpiece (a seat frame, woven cord, a part being made) kind "work", not "scene", so check_machine tests it for collisions. Anything that turns must sit on the turning part; a rim-drive motor goes below the rim, with the rim in two layers so the pulley flanges clear (Cane-Dace, 2026-11-18).
- Woven or wrapped cord: one swept polyline solid per cord (Transition.ROUND), changing layer in gaps at least two cord diameters wide; it checks fast and cleanly.
- 2026-11-18: a maker defined in two part files resolves by file-name order with no warning. Grep `parts/*.py` for
  `def <name>` before adding one.
- Check what a made part has to fit into (an oven, a box, a door opening) as well as what it sits on, and that
  every part going into a heat source survives its temperature (printed plastics, magnets, adhesives).
- Ribbed hoses: build the wall as straight segments between the ribs, not one spline sweep (tight-bend sweeps can take
  minutes to tessellate and stall a render export; the ribs hide the joints).
