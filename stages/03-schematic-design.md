---
layout: default
stage_num: "03"
title: Schematic Design
strap: The mass becomes a building — walls, slab, roof, rooms and openings, resolved enough to submit for planning.
exit_state: Classified elements and named spaces, with areas that a submission could rest on
permalink: /stages/schematic-design/
---

This is the crossing. Up to now everything has been mesh you could push, pull and throw away. From
here the model carries meaning, and the tools change accordingly: Sketch Mode for study, Bonsai for
anything that will be scheduled, submitted or priced.

<div class="sia" markdown="1">
#### What the SIA scope expects of you here

- **Designer** — develop the initial design to the level of detail required for Development Control submissions; prepare outline specifications determining preferred materials, quality and construction method.
- **Qualified Person** — ensure regulatory compliance; prepare and submit plans to URA for Written Permission; prepare and submit to other authorities for DC clearances; apply for waivers; make amendment submissions.
- **Contract Administrator** — provide input on contractual matters in the outline specification; identify items requiring early procurement.
- **Design Manager** — coordinate and manage communication across the team; review the QS's cost estimate against the project budget; monitor progress against the programme.

Under the VAF's Compliance sheet this is the **Pre-Submission** and **Design Gateway** band, where
one component recurs across every authority: *create a BIM Execution Plan, construct the model,
coordinate it with all relevant parties for clash detection, design resolution and compliance checks,
and integrate it for submission.*
</div>

## What you will learn

- Creating storeys and putting every element in one.
- Wall and slab types with material layers, and why the type comes before the wall.
- Bonsai's own wall, slab, door and window tools — and why Push/Pull now refuses them.
- `IfcSpace`: naming, numbering, and getting area out of the model instead of a calculator.
- Absorbing a client change late in a stage without losing the approved state.

## Before you start

Stage 02's gate is passed. You have one adopted massing and at least one superseded option. The
adopted mass is about to become scaffolding: you will build over it, then hide it.

## Build it

*Step-by-step detail for every operation below is in the [modelling recipes]({{ '/modelling/' | relative_url }}); the data each one has to carry is in [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}).*

{: .steps}
1. **Create the storeys, and name them to the convention.** Creating the project already generated `IfcProject → IfcSite → IfcBuilding → IfcStorey`; adjust it in `Properties → Project Overview → Spatial Decomposition`. Two storeys — **`1st Storey`** at your FFL, **`Roof`** at FFL + 3.150, plus **`Attic`** if the design has one. Every element from now on belongs to one of them.

   Those names come from [CORENET X's level-naming practice]({{ '/ifc-sg/' | relative_url }}), which publishes valid and invalid examples: `1st Storey` valid, `1st Floor` invalid; `Attic` valid, `Attic 1` invalid. Names and Z values must stay consistent across every discipline, so agree them now rather than after someone else has modelled against them.

2. **Make the types before the elements.** Create an `IfcWallType` for the 200 mm external wall and one for the 100 mm partition, each with its material layers, and an `IfcSlabType` for the ground slab. Three types, made once. Forty individually drawn walls are a drawing; one type used forty times is a schedule, a quantity and a specification simultaneously.

3. **Trace the approved massing with Bonsai's wall tool.** Using the adopted mass as the reference, place external walls along its perimeter and partitions inside it. These are parametric `IfcWall`s driven by their type — not extruded meshes. Name them to the standard: `A-Walls-Ext-North` and so on.

4. **Discover that Push/Pull refuses them.** Try it. Hover an `IfcWall` face, press <span class="k">P</span>, and watch it decline. Its shape comes from material layers; overwriting that with a tessellated mesh would silently throw the parametric definition away. Height and thickness now belong to Bonsai's own controls. This is the moment the course's central rule stops being advice and becomes muscle memory.

5. **Place the ground slab and the roof.** Slab from its type, aligned to the wall centre lines you decided — record which face the slab edge follows, because Stage 04's junctions depend on it. The roof stays a simple pitched form; its construction is Stage 04's problem, but its shape must now be a real element rather than a stacked box.

6. **Zone the rooms as `IfcSpace`.** Three bedrooms, two bathrooms, kitchen, living/dining, utility, covered entry, household shelter, courtyard. Each gets a name and a number. Then read the areas out of the model. Compare them against the brief's 120 m² target and against your Stage 02 estimate. Where they differ, the model is right and your estimate was wrong — write down by how much.

   **GFA areas are spaces too.** Under [IFC+SG]({{ '/ifc-sg/' | relative_url }}) a gross floor area is an `IfcSpace` with subtype `USERDEFINED` and the value `AREA_GFA`, carrying its own `AGF_` properties — name, development use, use quantum. From schematic onward, the GFA you quote in a submission is a modelled object, not a number in a spreadsheet beside the model.

7. **Place the principal doors and windows.** Bonsai's door and window tools cut a real opening in a host wall — an `IfcOpeningElement` with a relationship, not a hole. Mark each one (`D01`, `W01`…) now, because Stage 05's schedules are generated from these marks and renaming later is how marks and drawings drift apart.

8. **Keep studying with Sketch, on separate geometry.** Sill recesses, the porch soffit, a step at the courtyard, a built-in niche — these are still questions, so they stay `X-` mesh where <span class="k">P</span> and regional pushes still work. Study freely, then rebuild the answer as a real element. Never leave a study object pretending to be a building element.

9. **Absorb the change event.** *The client asks for a study/home-office, and the footprint cannot grow.* Do not start over. Work out what gives — the utility room shrinks, the third bedroom becomes a shared zone, the courtyard narrows by 600 mm. Model the answer, log the decision with its reason, and mark what it superseded. This is what "develop the design up to design sign-off" means when the design will not sit still.

10. **Check compliance against your control sheet.** Setbacks, coverage, height, GFA, greenery — measured from the model, not from intent. Any breach found here is free; the same breach found at Stage 04 costs a resubmission.

11. **Write the outline specification.** One page: external wall, internal wall, floor, roof, windows, doors, finishes — preferred material, quality level, construction method. It is the first document a QS can price and the first the Contract Administrator can read for contractual implications.

12. **Run the first model check and export.** Every element in a storey; every opening with a host; every space named, numbered and measured; nothing left called `X-`. Then `export/BUNG-A-SCH-P03-<date>.ifc`, plus plan, elevations and a 3D view.

<div class="warn" markdown="1">
#### The submission mindset

A model prepared for a planning submission is not a prettier design model — it is a model whose
*numbers* will be read by someone who has never met you. Areas, setbacks, heights and coverage must
come out of the geometry. Anything typed into a drawing by hand and not derived from the model is a
number that will eventually disagree with the model, usually in front of an authority.
</div>

## Deliverables

| Item | File |
| --- | --- |
| Schematic model | `export/BUNG-A-SCH-P03-<date>.ifc` |
| Plan, elevations, section, 3D | `03-schematic/` |
| Space schedule | name, number, area, per room, out of the model |
| Compliance check | each control from Stage 01 with the measured value beside it |
| Outline specification | `03-schematic/outline-spec.md` |
| Cost estimate review | QS estimate or your own, against the Stage 01 budget |
| Decision log | classification decisions, the change event, what it superseded |

## The gate

<div class="gate" markdown="1">
{: .check}
- Spatial structure is complete and every element sits in a storey.
- Wall, slab and roof types exist, carry material layers, and are actually used.
- Every door and window has a host wall and a real opening relationship.
- Every space is named, numbered, and has an area read from the model.
- Total GFA is within a stated tolerance of the brief, and the difference is explained.
- The control sheet has a measured value beside every parameter.
- The change event is modelled, logged, and has not destroyed the pre-change state.
- No `X-` object is doing a building element's job.
- An outline specification exists and matches the model.
- `check_bungalow.py` runs clean against your export, or every failure is understood and logged.
</div>

Run the check from the [reference model]({{ '/reference-model/' | relative_url }}) against your own
file — `python exercises/reference-model/check_bungalow.py my-bungalow.ifc`. It tests 158 rules
drawn from this course's model standard and CORENET X's modelling practices, and most of them will
fail on a first attempt. Each failure names a rule you have not yet applied.

## Where this goes wrong

**Modelling walls as meshes because Push/Pull is faster.** It is faster, and it costs you types,
quantities, schedules, and every opening relationship in Stage 04. Sketch Mode's whole design is
built on drawing the line here.

**Spaces added at the end.** Spaces drawn after the walls are frozen tend to be drawn to match the
walls rather than to test them. Zone early, and let a space that comes out at 5.8 m² tell you
something.

**Marks assigned late.** `W01` must mean the same window in the model, the schedule and the drawing
from the first day it exists.

**Absorbing the change by starting again.** The point of the change event is that the approved state
survives it. A rebuilt model loses the history that makes a change defensible.

<div class="note" markdown="1">
#### Additional Service, if this were real

Performance-based design, providing architectural content for the client's marketing or a public
exhibition, basic interior design, signage design, physical models, re-computation of existing GFA,
Green Mark documentation, applications for house number, change of use, advertisement licence or
operating licence — and again, **design change** — are all **Additional Services** at Schematic
Design.
</div>
