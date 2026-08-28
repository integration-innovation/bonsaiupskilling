---
layout: default
title: The reference model
strap: A complete Courtyard Bungalow as IFC4, built to Singapore conventions — download it, open it, check it, argue with it.
permalink: /reference-model/
---

The course describes a bungalow. This is that bungalow, built: a valid IFC4 file with real
types, real openings, named spaces, a grid, and SVY21 georeferencing, at the state the model should
be in at the end of [Stage 03 · Schematic Design]({{ '/stages/schematic-design/' | relative_url }}).

<div class="big-note" markdown="1">

### Download

**[BUNG-A-SCH-P03.ifc]({{ '/exercises/reference-model/BUNG-A-SCH-P03.ifc' | relative_url }})** — 117 KB, IFC4

Built by **[build_bungalow.py](https://github.com/integration-innovation/bonsaiupskilling/blob/main/exercises/reference-model/build_bungalow.py)**,
checked by **[check_bungalow.py](https://github.com/integration-innovation/bonsaiupskilling/blob/main/exercises/reference-model/check_bungalow.py)**.
Both run on IfcOpenShell 0.8.x, the same library Bonsai ships.

</div>

## What is in it

| | |
| --- | --- |
| Walls | 20 — external, internal, and four in 300 mm reinforced concrete around the shelter |
| Slabs | 2 — ground slab and roof, each from a type with material layers |
| Doors · Windows | 12 · 8, every one filling a real `IfcOpeningElement` |
| Spaces | 13, named and numbered, including the courtyard and covered entry |
| Storeys | `1st Storey` (+150) and `Roof` (+3150) |
| Grid | A–D and 1–4 |
| Extent | −0.6 to 12.6 m east, −1.3 to 10.6 m north, 0 to 3.275 m up |
| GFA to outer face | **108.4 m²** — against a brief target of 120 m² |
| Net internal area | **94.2 m²** from the space data |

That GFA line is not an oversight. The [brief]({{ '/brief/' | relative_url }}) asks for approximately
120 m² and the plan that satisfies the room list comes out at 108.4. The course's own rule applies:
the model is right and the estimate was wrong. Write down by how much, and decide whether to grow
the footprint or revise the brief — which is exactly the conversation
[Stage 02]({{ '/stages/concept-design/' | relative_url }}) says belongs to Concept Design.

## The plan

A 12 × 10 m rectangle with a 4 × 4 m courtyard notch cut from the south-east corner, so the outdoor
room is formed by the building rather than carved out of the roof. Entry from the south, under a
covered porch on two columns.

```text
        N
  +---------------------------+
  | Bed 1   | Bed 2  | Bed 3  |   y 7.0 – 10.0
  +----+----+---+----+--------+
  |Util| HS |Ba2|Ba1 | Kitchen|   y 5.5 – 7.0
  +----+----+---+----+        |
  |   Circulation    |        |   y 4.0 – 5.5
  +--------+---------+--------+
  | Living | Entry   |Courtyard|  y 0.0 – 4.0
  | Dining |  ___    | (open) |
  +--------+-|   |---+--------+
             porch                y −1.5 – 0.0
  x 0                    8    12
```

Household shelter at 2.0 × 1.5 m gross, 1.7 × 1.2 m internal, in the middle of the service band
where its 300 mm walls do no harm.

## The Singapore conventions it demonstrates

Each of these is a decision the course argues for somewhere. The model is where you see them
together.

| Convention | In the file | Source |
| --- | --- | --- |
| Storey names | `1st Storey`, `Roof` — not `Ground`, not `Level 1` | [CORENET X level naming]({{ '/ifc-sg/' | relative_url }}) |
| One `IfcSite`, named for the block | `IfcSite` Name = `Main Block` | Block mechanism |
| Geo-referencing | `IfcProjectedCRS` EPSG:3414, SVY21 / Singapore TM, vertical datum SHD | Project coordinates |
| True North | `IfcMapConversion` rotated 8° | Project coordinates |
| Correct entity + subtype | Every element classified and given a predefined type | Correct IFC entities |
| Types before elements | 3 wall types, 2 slab types, door and window types, each with material layers | Model standard |
| Real openings | 20 `IfcOpeningElement`, each voiding one wall and filled by one door or window | Stage 03 gate |
| Household shelter data | Construction method, internal length, internal width — from **conceptual** stage | IFC+SG model content |
| Main entrance flagged | `D01` carries *Main Entrance* — required from **schematic** | IFC+SG model content |
| Grid exported | `IfcGrid` with U and V axes | Export gridlines to all storeys |
| Simplified geometry | Doors and windows are sized panels, not ironmongery | Design Gateway guidance |

## Open it in Bonsai

{: .steps}
1. **Download** the file above.
2. **Blender → `File` → `Open IFC Project`**, or drag the `.ifc` into the viewport.
3. **Look at `Properties → Project Overview → Spatial Decomposition`.** Two storeys with real names and elevations, everything contained.
4. **Select a wall** and check `Object Information` — it has a type, and the type has material layers that sum to its thickness.
5. **Select a door** and follow its opening to the host wall. That relationship is the thing to internalise; it is what makes a schedule possible.
6. **Try Push/Pull on a wall.** It refuses. Correctly.

Verified to load in **Blender 5.2 with Bonsai 0.8.5**: 65 mesh objects, both storeys, all
relationships intact.

## Check it yourself

`check_bungalow.py` runs **158 checks** and exits non-zero on any failure, so it works as a CI gate.
It is the [model standard's]({{ '/standards/' | relative_url }}) five-minute checking pass, written
down:

```text
python exercises/reference-model/check_bungalow.py
```

It tests, among others: one project, one site, millimetre units, EPSG:3414 with SHD, a True North
rotation, every storey name against the CORENET X naming pattern, every element contained in a
storey, every wall and slab typed with a summing material layer set, every opening voiding exactly
one host and filled exactly once, every door and window marked, every space named and numbered, the
household shelter's conceptual-stage data, exactly one main entrance, a grid with axes in both
directions, geometry that produces without error, nothing above roof level, and no `X-` working
geometry left in the file.

Point it at your own model when you reach the Stage 03 gate:

```text
python exercises/reference-model/check_bungalow.py my-bungalow.ifc
```

Most of it will fail on a first attempt. That is the point — each failure names a rule you have not
yet applied, and the rules are the course.

## What it deliberately does not do

Honesty about a reference model matters more than completeness, because the gaps are where a learner
would otherwise assume the model is authoritative.

- **The roof is flat.** The brief asks for a 25–30° pitch. Developing the roof — thickness, eaves, gutter, the wall-head junction — is [Stage 04]({{ '/stages/design-development/' | relative_url }}) work, and handing it over finished would remove the most instructive junction in the project. The eaves overhang is there; the pitch is yours.
- **Doors and windows are sized panels.** No ironmongery, no lining profiles, no glazing build-up. This is not laziness: CORENET X's file-size practice asks for *design intent and simplified geometry* at the Design Gateway, and says plainly that over-modelling increases file size without improving the submission outcome.
- **No structure, no services.** One discipline, one block. Coordination and clash triage need a second model, which is [Stage 04]({{ '/stages/design-development/' | relative_url }}).
- **`IFCSG_Demo` is not a real property set name.** IFC+SG parameter *names* are carried in a property set deliberately named as a demonstration, because the authoritative set names come from the [IFC+SG Excel Mapping File](https://info.corenet.gov.sg/ifc-sg/requirements---submission/ifc-sg-excel-mapping-file), which you must consult rather than inherit from a teaching model.
- **The coordinates are an example.** SVY21 easting 33000, northing 39000, SHD +15.400 — plausible, and not a real plot. Real georeferencing comes from a licensed land surveyor.
- **It is not a submission.** It demonstrates conventions. It has not been through a gateway, a checker, or a QP.

## Why it is not derived from a Revit sample export

The obvious shortcut would be to take a published sample IFC — Autodesk's Revit sample projects are
the usual candidate — and adapt it. That was considered and rejected, for a reason worth stating.

A Revit IFC export carries Revit's conventions into the file: storeys named `Level 1` and `Level 2`,
`IfcWallStandardCase` where IFC4 prefers `IfcWall`, and property sets shaped by the exporter's own
mapping. Those conventions are not wrong in their own context — but `Level 1` is on the *invalid*
side of CORENET X's level-naming table, and the whole point of this model is to show what the
Singapore conventions look like when they are applied from the first entity rather than corrected
afterwards.

Autodesk also publishes its samples as `.rvt`, not `.ifc`, so any comparison would be with an export
someone else configured. Starting from IfcOpenShell's API — the same API Bonsai's own operators call
— means every attribute in the file was set deliberately and can be traced to a line in a script you
can read.

If you want the comparison, make it yourself: export any Revit model to IFC, open both in the same
viewer, and look at the storey names first.

## Using it in the course

**Do not open it and copy.** Build your own; the difficulty is the lesson. Use this one three ways:

- **As a target.** Stuck on how an opening should relate to its host, or what a material layer set looks like in practice? Open the reference and inspect that one relationship.
- **As a checker.** Run `check_bungalow.py` against your model at each gate.
- **As an argument.** The plan is one answer to the brief, not the answer. It scores well on cross-ventilation and level access and badly on GFA against target. Find where it is wrong and do better — and record the reason, which is [Stage 02's]({{ '/stages/concept-design/' | relative_url }}) actual deliverable.

<div class="note" markdown="1">
#### Rebuilding it

```text
python exercises/reference-model/build_bungalow.py
python exercises/reference-model/check_bungalow.py
```

The script is about 500 lines with the plan held as data at the top — wall centrelines, space
rectangles, door and window schedules. Change a room dimension there and the whole model, including
its openings and space areas, rebuilds consistently. That is worth doing once, because it makes the
relationship between a schedule and a model concrete in a way that dragging geometry never does.

Licensed GPL-3.0-or-later, matching Bonsai.
</div>
