---
layout: default
title: Bonsai modelling recipes
strap: The operations this course uses, as reference — each one tagged with the stage it belongs to and the data it serves.
permalink: /modelling/
---

[Kickstart]({{ '/kickstart/' | relative_url }}) is an hour, start to finish. This page is the same material as fifteen
recipes you can open one at a time, each answering three questions: **when** you do it, **how** you
do it, and **what goes wrong**.

Every recipe carries its coordinates in the three frameworks the course runs on — the
[SIA stage]({{ '/sia-mapping/' | relative_url }}), the [VAF component]({{ '/vaf/' | relative_url }}), and the [IFC+SG]({{ '/ifc-sg/' | relative_url }}) data it produces.

<div class="note" markdown="1">
**Version and honesty note.** Written against **Bonsai 0.8.5** and **Bonsai Sketch Mode 0.4.x**,
from Bonsai's own documentation and the add-on's source. Bonsai is a rolling release with no stable
public API or UI contract. Several areas of the official documentation are explicitly marked
*work in progress* — spaces, drawings, spatial objects — and where that is true this page says so
rather than inventing click paths. Verify at
[docs.bonsaibim.org](https://docs.bonsaibim.org/) before relying on a detail.
</div>

## Contents

**Setting up** — [1 Project](#1--start-an-ifc-project) · [2 Storeys](#2--spatial-structure-and-storeys) · [3 Coordinates](#3--coordinates-and-geo-referencing) · [4 Grids](#4--grids)

**Building** — [5 Classify](#5--turn-sketch-geometry-into-an-ifc-element) · [6 Types](#6--wall-types-and-material-layers) · [7 Walls](#7--draw-and-join-walls) · [8 Slabs and roofs](#8--slabs-and-roofs) · [9 Openings](#9--doors-windows-and-openings) · [10 Spaces](#10--spaces)

**Informing** — [11 Properties](#11--properties-and-ifcsg-parameters) · [12 Quantities](#12--quantities-and-schedules) · [13 Drawings](#13--drawings-and-sheets)

**Checking and issuing** — [14 Quality](#14--ids-bcf-and-clash) · [15 Export](#15--export-revise-verify)

---

## 1 · Start an IFC project

<div class="sia" markdown="1">
**SIA** Pre-Design → Concept · **VAF** BIM: *construct the BIM model* · **IFC+SG** Setting up &
project information
</div>

**How.** Topbar → **`File` → `New IFC Project`** → choose `New Metric (mm) Project` for this course.
The other presets are `New Metric (m)`, `New Imperial (ft)`, `New Demo Project` and
`New Project Wizard`.

For control, use the wizard — **`File` → `New IFC Project` → `New Project Wizard`**, or
`Properties → Project Overview → Project Info`. Set:

| Field | For this course |
| --- | --- |
| IFC Schema | **IFC4** — IFC+SG is built on IFC4 |
| Unit system | Metric |
| Length / area / volume units | mm / m² / m³ |
| Template | Blank |

Press **Create Project**. From the Sketch tab, the sidebar's **`IFC`** panel offers the same thing as
one button: **New IFC Project**.

Then **`File` → `Save IFC Project`** (<span class="k">Ctrl</span>+<span class="k">S</span>) and choose
a `.ifc` name. The IFC is the deliverable; the `.blend` is your working copy.

**What goes wrong.** Working for twenty minutes before making the project, then discovering every
Bonsai tool reads `No IFC Project`. Choosing IFC2X3 out of habit. Never saving as `.ifc` at all, and
finding at Stage 05 that the only real artefact is a Blender file.

---

## 2 · Spatial structure and storeys

<div class="sia" markdown="1">
**SIA** Schematic Design · **VAF** BIM: *construct and coordinate* · **IFC+SG** Level naming and
organisation — general modelling practice 01
</div>

**How.** Creating the project generates the tree automatically:
`IfcProject → IfcSite → IfcBuilding → IfcStorey`. Inspect and edit it at
`Properties → Project Overview → Spatial Decomposition`.

For this house, five levels and no more:

```text
IfcProject          Edith Farnsworth House
  IfcSite           Fox River Floodplain   <- one IfcSite per file; its Name carries the block
    IfcBuilding     Edith Farnsworth House
      IfcBuildingStorey   1st Storey_Terrace  (+0.610)   <- 2'-0"
      IfcBuildingStorey   1st Storey          (+1.600)   <- 5'-3"
      IfcBuildingStorey   Roof                (+4.877)   <- 16'-0"
```

**Use the CORENET X names.** `1st Storey` and `Storey 1` are valid; `1st Floor`, `Level one` and
`2nd Story` are not. `Attic` is valid; `Attic 1` is not. Different physical levels get different
names, and names and Z values must stay consistent across every discipline — where the structural
floor level differs, structural adds a `_SFL` suffix rather than changing the number. Full table on
the [IFC+SG page]({{ '/ifc-sg/' | relative_url }}).

Check an element's container in `Properties → Object Information → Spatial Container`.

**What goes wrong.** Leaving `Level 1`, `Level 2` behind. Elements sitting loose at project level
with no storey. Inventing a fifth and sixth level for things that are not storeys. Renaming a storey
after other people have modelled against it.

*Bonsai's "Basic Spatial Objects" documentation page is marked incomplete; the panel above is the
reliable route.*

---

## 3 · Coordinates and geo-referencing

<div class="sia" markdown="1">
**SIA** Pre-Design · **VAF** Compliance: coordination between consultants · **IFC+SG** General
modelling practice 03
</div>

**What CORENET X requires.** Three things together: **SVY21** for Easting (X) and Northing (Y),
**SHD — Singapore Height Datum** for elevation (Z), and **real-world orientation to True North**.
One shared coordinate reference, taken from the licensed land surveyor's data, used by every
discipline model.

**How.** Set the projected CRS and map conversion in the project's georeferencing settings rather
than dragging geometry to real-world coordinates. IFC's map conversion is exactly the mechanism that
lets you author at a workable origin while the file still declares its true easting, northing,
height datum and rotation.

Record the coordinate basis, the datum and north in the same
[decision log]({{ '/standards/' | relative_url }}) entry at [Stage 01]({{ '/stages/pre-design/' | relative_url }}).

**What goes wrong.** Models not aligned to SVY21. Elevation referenced to a site datum rather than
SHD. Orientation not aligned to True North. No georeferencing at all, which makes federation
impossible. **Late coordinate changes causing rework** — CORENET X lists this explicitly, and it is
the expensive one.

---

## 4 · Grids

<div class="sia" markdown="1">
**SIA** Schematic Design · **VAF** Design: coordination · **IFC+SG** General modelling practice —
export gridlines to all storeys
</div>

**How.** Four steps, per CORENET X: create the gridlines → **associate them to storeys**, exporting
to *every* required storey → export the IFC with gridlines enabled → **check them in an IFC viewer**,
across multiple levels, before you rely on them.

Grids are model objects, not drawing decoration.

**What goes wrong.** Skipping the grid because one room looks too simple to need one — setting out, coordination and
every dimension check afterwards hang off it. Gridlines exported at only one level. Missing storey
association. And the one that catches everybody: **grids visible in the authoring tool but missing
from the IFC**, which is only ever discovered by opening the export.

---

## 5 · Turn sketch geometry into an IFC element

<div class="sia" markdown="1">
**SIA** Schematic Design onward · **VAF** BIM: *construct the model* · **IFC+SG** General modelling
practice — use correct IFC entities
</div>

**How.** Select the finished sketch, then either:

- **Sketch tab** — sidebar (<span class="k">N</span>) → **`IFC`** panel → pick a class → **Assign**.
- **BIM tab** — `Properties → Object Information` → **Products** dropdown → category, then class → **Assign IFC Class**.

Then confirm the spatial container in the same panel.

**Classification is three things.** CORENET X's workflow is: identify the component → check the COP,
Mapping File and Glossary → assign the **IFC entity** → apply the **IFC subtype** if applicable →
apply the **property sets** and populate them → validate the IFC. Assigning the class is the third
of six steps, not the finish line.

**Subtypes, in short.** Some entities need none (`IfcWall`, `IfcColumn`, `IfcBeam` — `N.A.` or
blank). Some take a predefined value from the Mapping File (`IfcDoor` gives `DOOR`, `GATE`). Some
take `USERDEFINED` plus an exact value, marked with an asterisk in the Mapping File (`IfcSpace` gives
`AREA_GFA`, `IfcDoor` gives `BLASTDOOR`). Never invent a `USERDEFINED` value that is not in the
guidance, and never put spaces in one.

**When to do it.** Only when the decision behind the geometry is stable. Massing at
[Stage 02]({{ '/stages/concept-design/' | relative_url }}) stays plain mesh on purpose; classification begins at
[Stage 03]({{ '/stages/schematic-design/' | relative_url }}).

**What goes wrong.** Classifying early, which makes you attached to geometry you should be
discarding — and makes Push/Pull refuse to help you discard it. Choosing the convenient class rather
than the correct one: to a checker, an element's class *is* what it is.

---

## 6 · Wall types and material layers

<div class="sia" markdown="1">
**SIA** Schematic Design (create) → Design Development (layer up) · **VAF** Design: detail design ·
**IFC+SG** Wall — construction method (Architectural); the rest is C&S
</div>

**How.** With the **Create Wall** tool active, the top bar reads
`[No IfcWallType Found] | Name [TYPEX] | + Add IfcWallType`. Replace `TYPEX` with a real name —
`EXT-200`, `INT-100` — and press **+ Add IfcWallType**.

At [Stage 04]({{ '/stages/design-development/' | relative_url }}), give each type its material layers: finish, structure,
cavity or insulation, internal finish, each with a material and thickness. The type is the
specification.

**Then reconcile the geometry.** A wall that was 200 mm nominal and is now 215 mm of real layers has
moved a face. Decide which face is the setting-out reference — centre line or structural face — hold
it, and write it in the decision log. Every junction downstream depends on that one sentence.

**What goes wrong.** Drawing forty individual walls instead of using one type forty times, which
throws away the schedule, the quantity and the specification simultaneously. Adding layers without
moving anything, which means the layers are decoration.

*Bonsai's wall guide covers type creation and drawing; the material-layer UI is not stepped through
in the documentation. Expect to explore the type's own properties.*

---

## 7 · Draw and join walls

<div class="sia" markdown="1">
**SIA** Schematic Design · **VAF** Design: design development up to sign-off
</div>

**How.**

{: .steps}
1. Activate **Create Wall** from the toolbar, or <span class="k">Shift</span>+<span class="k">Spacebar</span> then the tool's number.
2. Hold <span class="k">Shift</span> and left-click to set the 3D cursor at the start point.
3. <span class="k">Shift</span>+<span class="k">A</span> adds a wall segment.
4. Adjust length and height from the top-bar parameters, or by dragging.

Joining:

| | |
| --- | --- |
| <span class="k">Shift</span>+<span class="k">E</span> | Extend to intersect another face |
| <span class="k">Shift</span>+<span class="k">T</span> | Butt — end to end |
| <span class="k">Shift</span>+<span class="k">Y</span> | Mitre |
| <span class="k">Shift</span>+<span class="k">M</span> | Merge into a single wall |
| <span class="k">Shift</span>+<span class="k">R</span> | Rotate 90° |

**What goes wrong.** Reaching for <span class="k">P</span> to change a wall's height. Push/Pull
refuses IFC elements, deliberately — its shape comes from layers or a profile, and a tessellated mesh
would discard that. Use the parametric controls.

---

## 8 · Slabs and roofs

<div class="sia" markdown="1">
**SIA** Schematic Design (form) → Design Development (build-up) · **VAF** Design: detail design ·
**IFC+SG** Floor, Roof
</div>

**How.** **Create Slab** from the toolbar, driven by an `IfcSlabType` in the same way walls are driven
by an `IfcWallType`. A flat roof plane is an `IfcSlab` with `PredefinedType = ROOF`; where a roof has several coverings, an `IfcRoof` aggregates them.

At [Stage 04]({{ '/stages/design-development/' | relative_url }}) develop the real edge: the structural
depth, the channel at the perimeter, the soffit, and where water goes when there is no gutter,
no fascia and no overhang to take it.

**What goes wrong.** Leaving the roof as the single surface it was in the massing. It is the junction
most small-house models get wrong, and the one most likely to leak in reality.

---

## 9 · Doors, windows and openings

<div class="sia" markdown="1">
**SIA** Schematic Design (place and mark) → Design Development (coordinate) · **VAF** Design:
coordination · **IFC+SG** Door and Window parameter sets — *main entrance* from schematic, clear
widths and fire data from detailed
</div>

**How.**

{: .steps}
1. **Select the host wall first.** This is what causes the void relation between the opening and the wall to be created automatically.
2. Position the 3D cursor on the wall where the opening goes.
3. Choose **Create Door** (or **Create Window**) from the toolbar.
4. In the top bar, name the type — `D01`, `W01` — and press **+ Add IfcDoorType**.
5. <span class="k">Shift</span>+<span class="k">A</span> to place it.
6. Set width and height from the top-bar parameters.

| | |
| --- | --- |
| <span class="k">Shift</span>+<span class="k">O</span> | Apply void manually, if the wall was not pre-selected |
| <span class="k">Shift</span>+<span class="k">G</span> | Regenerate wall geometry after changing an opening |
| <span class="k">Shift</span>+<span class="k">F</span> | Flip the door 180°, changing the swing |

**Mark them now.** `D01`, `W01` must mean the same opening in the model, the schedule and the drawing
from the first day they exist. Stage 05's schedules are generated from these marks.

**Coordinate at Stage 04:** head against the beam zone, sill against finished floor, jamb against the
wall junction, reveal against the external finish.

**What goes wrong.** Cutting openings as mesh holes — they survive the viewport and die in the
schedule, with no mark, no host, no quantity and no lintel. There is no auto-subtract in Sketch Mode,
and at this stage that constraint is doing you a favour. Renaming marks later, which is how the model
and the drawings quietly diverge.

---

## 10 · Spaces

<div class="sia" markdown="1">
**SIA** Schematic Design · **VAF** Compliance: GFA and planning parameters · **IFC+SG** Spatial
allocation — `AGF_` GFA parameters from schematic; name, area, height, occupancy and accessibility
from detailed; **household shelter from conceptual**
</div>

**How.** The toolbar's **Spatial Tool** defines and manages spatial structures. Create an `IfcSpace`
per room, then name and number each one, and read the area out of the model.

**What goes wrong.** Adding spaces at the end, once the walls are frozen — they then get drawn to
match the walls rather than to test them. Letting a space report 5.8 m² and adjusting the number
instead of the design.

*Bonsai's "Defining Rooms and Spaces" documentation page is marked incomplete. The Spatial Tool is
the right place; expect to explore the workflow.*

---

## 11 · Properties and IFC+SG parameters

<div class="sia" markdown="1">
**SIA** Design Development onward · **VAF** BIM: *coordinate for compliance checks* · **IFC+SG** the
entire parameter set
</div>

**How.** With an element selected, its IFC properties are in `Properties → Object Information` and the
related panels. This is where an IFC+SG parameter lives — *main entrance* on a door, *percentage of
opening* on a window, *purpose group* and *barrier-free accessibility* on a space, *construction
method* on a wall.

Also set the course's own two properties on everything, from creation:

| Property | Values |
| --- | --- |
| `project_stage` | `01 Pre-Design` … `08 Post Completion` |
| `design_status` | `provisional` · `approved` · `superseded` |

**Predefined type vs USERDEFINED.** Use the standard enumeration where one fits. Where IFC+SG needs a
subtype the enumeration does not offer, set the predefined type to `USERDEFINED` **and give the
object type the required name**. A `USERDEFINED` with no name passes visual inspection and fails a
data check.

**What goes wrong.** Keeping the data in a spreadsheet beside the model; it will be separated within
a year. Adding parameters at the end, when [IFC+SG]({{ '/ifc-sg/' | relative_url }}) required several of them from
conceptual and schematic.

*Bonsai's documentation has no dedicated property-sets guide at present. This recipe is deliberately
short on click paths for that reason.*

---

## 12 · Quantities and schedules

<div class="sia" markdown="1">
**SIA** Design Development → Documentation · **VAF** Contract: drawings and BIM model; allocation of
contract sum
</div>

**How.** Quantities come out of the model — wall area by type, slab area, roof area, opening counts,
finish areas — and schedules come out of the types and marks. Bonsai's costing and scheduling tools
cover cost schedules and quantities; the payoff for naming discipline at Stages 03 and 04 is that
these generate rather than get typed.

**Always check independently.** By hand, on one wall and one room, at minimum. A model quantity you
have never sanity-checked is a number with unearned authority.

**What goes wrong.** A hand-typed door schedule: correct on the day it is typed and never again. A
mark that appears in a schedule and not in a drawing — which is a real error, and finding it is the
point.

---

## 13 · Drawings and sheets

<div class="sia" markdown="1">
**SIA** Documentation · **VAF** Contract: drawings and BIM model
</div>

**How.** Bonsai generates plans, sections and elevations from the model and places them on sheets,
under its drawings and documents tools. Set scales, title block and sheet numbers, then generate.

**The rule that matters more than the click path:** a drawing is a *view of the model*, not a document
beside it. If a view will not produce what you need, fix the model or the view — never the exported
drawing. The moment a dimension is corrected on a sheet, the set has two sources of truth and the
model has become decoration.

**What goes wrong.** Drawing over the model because it is faster today. It destroys the only thing
that makes Stages 06 to 08 tractable.

*Bonsai's drawings guide is marked work in progress. Treat the reference section as the current
authority and expect the UI to have moved.*

---

## 14 · IDS, BCF and clash

<div class="sia" markdown="1">
**SIA** Design Development onward · **VAF** BIM: *coordinate with all relevant parties for clash
detection, design resolution and compliance checks* — at four separate gateways
</div>

**How.**

- **Clash** — run Bonsai's clash tooling after every substantial change, not once at the end. Architecture against assumed structure; roof against wall heads; fittings against door swings; beam zone against every window head.

  Under CORENET X, clash detection is **rule-based, not merely geometric**: a coordination matrix decides whether a given pair is a Fail, an Alert or a Pass. An architectural door intersecting a structural beam is not allowed at all; an MEP pipe against a beam passes at 100 mm or under, alerts between 100 and 200 mm, and fails at 200 mm or over. **A clash is not always a failure** — every entry needs a decision: resolve, accept, or alert. Record which.
- **IDS** — an Information Delivery Specification states, in a form software can test, what the model must contain: every `IfcWall` has a type, every `IfcDoor` has a host and a mark, every element has a storey, every `IfcSpace` has a name and a number. Write it once at [Stage 04]({{ '/stages/design-development/' | relative_url }}); every gate afterwards is a button press.
- **BCF** — an issue with a viewpoint attached, so "the window head clashes with the beam" arrives with the camera already pointing at it. BCF travels between applications; a CSV does not. Keep both.

**What goes wrong.** A ruleset written and never run. A clash check run once, at the end, by which
time three weeks of work has been built on the clash.

*IDS, BCF and clash do not have dedicated pages in Bonsai's current documentation navigation, though
the tooling exists. Budget exploration time at Stage 04.*

---

## 15 · Export, revise, verify

<div class="sia" markdown="1">
**SIA** every gate · **VAF** BIM: *integrate the model for submission* · **IFC+SG** general modelling
practices 03 and 04 — federation alignment, unique GUIDs, file size
</div>

**How.** **`File` → `Save IFC Project`** writes the IFC. Export at every gate to `export/`, named to
the [model standard]({{ '/standards/' | relative_url }}):

```text
FARN-A-SCH-P03-2026-10-09.ifc     PROJECT-DISCIPLINE-STAGE-REVISION-DATE
```

Then **open the export in something that is not Blender.** CORENET X asks for exactly this check, and
it is the only way to know that the model you authored and the model someone else reads are the same
thing.

**Unique GUIDs.** Branch revisions; never duplicate a file and call the copy a different block. Every
element in the copy now shares a `GlobalId` with its twin, and that is a submission-level defect.

**File size.** Keep each IFC within **800 MB** (CORENET X's recommendation), split by block, zone or
discipline, and never merge multiple buildings into one file. Parametric elements driven by types are
small; tessellated meshes and imported high-poly content are not.

**Model to the gateway.** Over-modelling increases file size without improving the submission
outcome. The Design Gateway wants design intent and simplified geometry; the Piling Gateway wants
foundation and piling only; the Construction Gateway wants buildable elements, with detail added only
where required and nothing at fabrication or as-built level.

**What goes wrong.** Overwriting `T01` instead of issuing `T02`, which makes "what was priced" a
matter of opinion. Shipping an `X-` object in an issued model — an unexplained hole nobody can
account for. Believing an export you have never opened.

---

## The five rules underneath all of it

1. **Project first.** Everything is behind that gate.
2. **Sketch first, classify second.** Meaning follows a stable decision, not the other way round.
3. **Types before elements.** One type used forty times; never forty walls.
4. **Select the host before placing the opening.** The relationship is the point, not the hole.
5. **Push/Pull refusing an IFC element is the tool working.** Parametric definitions are worth more than convenience.
