---
layout: default
title: IFC+SG and CORENET X
strap: What Singapore's regulatory submission expects of your model, practice by practice, and how to satisfy each one in Bonsai.
permalink: /ifc-sg/
---

The [SIA scope]({{ '/sia-mapping/' | relative_url }}) says what you deliver. The [VAF]({{ '/vaf/' | relative_url }})
says what it costs. **IFC+SG says what the model itself must contain**, and CORENET X is the process
that reads it. This is the page that turns all of that into things you do in Bonsai.

<div class="warn" markdown="1">
**Read the source; this is a teaching summary.** Regulatory requirements change and this page will
go stale. The authority is [info.corenet.gov.sg](https://info.corenet.gov.sg/) — in particular
[What is IFC+SG](https://info.corenet.gov.sg/ifc-sg/start-here/WhatIsIFCSG),
the [IFC+SG Excel Mapping File](https://info.corenet.gov.sg/ifc-sg/requirements---submission/ifc-sg-excel-mapping-file),
the [Glossary of Identified Components](https://info.corenet.gov.sg/ifc-sg/glossary-of-identified-components),
and the [General Modelling Practices](https://info.corenet.gov.sg/ifc-sg/modelling---authoring/GeneralModellingPractices),
each of which links to an illustrated guide worth reading in full. Summarised here as at
**August 2026**. Check the current version before any real submission.
</div>

## What IFC+SG is

IFC+SG is the data structure for BIM models submitted through CORENET X, so that regulatory agencies
can read, review and check model data directly rather than reading drawings of it. It is built on
**IFC4**, extended with **SGPsets** — Singapore property sets — and standardised properties and
values, plus validation checks the submission runs against.

Two consequences for how you model:

- **The class is the interface.** An agency's check finds a household shelter because it is classified and propertied as one, not because a drawing labels it. Geometry that looks right and classifies wrong fails silently.
- **Data is required by stage, not all at once.** IFC+SG states which parameters are needed at which stage, so a conceptual model is not expected to carry as-built detail. That staging is why this can be a course rather than one enormous checklist.

## The IFC+SG stages

IFC+SG defines seven model content stages of its own. They are not the SIA stages and not the VAF
stages — a third vocabulary, and the one your *model* is measured against.

| IFC+SG stage | SIA Scope of Service | This course |
| --- | --- | --- |
| Conceptual Design | Concept Design | [Stage 02]({{ '/stages/concept-design/' | relative_url }}) |
| Schematic / Preliminary Design | Schematic Design | [Stage 03]({{ '/stages/schematic-design/' | relative_url }}) |
| Detailed Design / Final Design | Design Development | [Stage 04]({{ '/stages/design-development/' | relative_url }}) |
| Tender | Documentation | [Stage 05]({{ '/stages/documentation/' | relative_url }}) |
| Construction & Fabrication | Construction | [Stage 06]({{ '/stages/construction/' | relative_url }}) |
| As-Built | Completion | [Stage 07]({{ '/stages/completion/' | relative_url }}) |
| O&M / Asset Information | Post Completion | [Stage 08]({{ '/stages/post-completion/' | relative_url }}) |

Note the shape: **Pre-Design has no IFC+SG stage**, because there is no model yet, and **O&M / Asset
Information does** — the data outlives the project. Most practices resource the first five and are
surprised by the last two.

Alongside these sit the submission **gateways**, which is where modelling effort is actually
governed: **Design Gateway (DG)**, **Piling Gateway (PG)** where applicable, and **Construction
Gateway (CG)**, then Completion.

---

# The twelve General Modelling Practices

CORENET X publishes twelve modelling practices in four groups. Each one below gives what CORENET X
requires, **what it means in Bonsai**, and where this course exercises it.

## 01 · Model setup and structure

### Applying consistent level naming

<div class="sia" markdown="1">
**CORENET X.** Different physical levels must use different names, and **names and Z values must
remain consistent across all disciplines**. Where the structural floor level sits at a different
elevation from the architectural one, structural levels may use a suffix — `_SFL` — to say so.

Their worked example: architectural and MEP both call it `1st Storey` at Z = 3.000; structural calls
it `1st Storey_SFL` at Z = 2.950, because the structural slab underside is 50 mm lower. Same
physical level, deliberately different name, because the elevation genuinely differs.
</div>

The naming conventions are specific enough to be worth learning once:

| Storey type | Valid | Invalid |
| --- | --- | --- |
| Above-ground floors | `Storey 1` · `Level 20` · `1st Storey` · `20th Level` | `Storey 1st Level MPL` · `20 Level` · `Loft Storey` · `2nd Story` · `1st Floor` · `Level one` |
| Mezzanine | `Storey 1 Mezzanine 2` · `1st Storey Mezzanine 2` · `20th Level Mezzanine` | `Mezzanine Level 1` · `4th Storey Mezzanine A` |
| Split floor, multi-storey car park | `2nd Storey 2A` | `2nd Storey 3A` · `2nd Storey A` |
| Below ground | `Basement 1` | `Upper basement` · `Basement A` · `1st Basement` · `B1` · `Basement mezzanine` · `Basement carpark` |
| Attic | `Attic` · `Attic Storey` | `Attic A` · `Attic 1` · `1st Storey Attic` · `Lower Attic` |
| Roof | `Roof` · `Upper Roof` · `Lower Roof Storey` | `Upper Roof 1` · `Roof Lower` |
| Distinguishing blocks or datum | `1st Storey_club house` · `4th Storey_Tower A` · `1st Storey_SFL` · `1st Storey_MPL` | `Block 1 - 2nd Storey` · `2nd Storey Block A&C` |

**In Bonsai.** Storeys live in `Properties → Project Overview → Spatial Decomposition`. Name and
elevate them there. For this house that means **`1st Storey`** at your finished floor level,
**`1st Storey_Terrace`** for the lower terrace datum and **`Roof`** — not `Ground`, not `Level 1`,
not `Main Floor`, and never `1st Floor`.

**Good practice, per CORENET X:** agree naming and Z values at project start; use consistent names
across disciplines; use suffixes only where elevations genuinely differ; coordinate and verify levels
against the same reference model. **Common issues:** different names for the same physical level;
different Z values for the same level; missing suffix where structural sits lower; changing names or
Z values without telling anybody.

**In this course.** [Stage 03]({{ '/stages/schematic-design/' | relative_url }}), and the spatial structure
in the [model standard]({{ '/standards/' | relative_url }}).

### Block mechanism

<div class="sia" markdown="1">
**CORENET X.** Architectural models are **split by block, one file per block**. A development with
two towers, a podium and a basement produces four architectural IFC files, plus a separate file for
site elements — roads, landscape, external works.

And the rule that catches people: **each IFC file has only one `IfcSite`, and the block name appears
under that `IfcSite`'s Name.** The block identity is not a property you invent; it is where the site
is named.
</div>

**In Bonsai.** One `IfcProject → IfcSite` per file, with the site named for the block. The house
is a single block with one submitting discipline, so this is the practice the course exercises least
— but the *habit* it teaches, one site per file and the site named deliberately, costs nothing to
adopt now and is a resubmission to learn later.

## 02 · Element modelling and data

### Use the correct IFC entities

<div class="sia" markdown="1">
**CORENET X.** Three things have to be right on every element, using COP Section 4 and the IFC+SG
Excel Mapping File to identify them:

1. **IFC Entity** — what the object *is*
2. **IFC SubType** — if applicable
3. **Property Sets** (SGPsets / Psets) — what data it must carry

Their examples across disciplines: a louvred window is `IfcWindow` · subtype `LOUVER` ·
`SGPset_Material`. A column is `IfcColumn` · subtype N.A. · `SGPset_ColumnReinforcement`. A flexible
pipe is `IfcPipeSegment` · subtype `FLEXIBLESEGMENT` · `PipeSegmentDimension`.

The workflow is six steps: **identify the component → check COP Section 4, the Mapping File and the
Glossary → assign the IFC entity → apply the subtype if applicable → apply the property sets and
populate them → validate the IFC.**
</div>

**In Bonsai.** `Properties → Object Information → Products` dropdown → choose the class → **Assign
IFC Class**. From the Sketch tab, the `IFC` panel in the sidebar does the same for a finished sketch.
A wall drawn as a mesh and left unclassified is, to a checker, nothing at all.

Note that steps four and five have no shortcut: assigning the class is a third of the job.

### IFC SubType — predefined vs USERDEFINED

<div class="sia" markdown="1">
**CORENET X.** The Mapping File drives this, and there are four cases.

**N.A.** — no subtype required. You may fill in `N.A.` or leave it blank. Examples: `IfcWall`,
`IfcColumn`, `IfcPile`, `IfcBeam`.

**Predefined type** — use one of the values listed in the Mapping File, marked without an asterisk.
For example `IfcSpace` → `SPACE`; `IfcDoor` → `DOOR`, `GATE`; `IfcAirTerminal` → `GRILLE`.

**USERDEFINED** — indicated by an asterisk (`*`) in the Mapping File. Set the subtype to
`USERDEFINED` **and provide the actual value**. For example `IfcSpace` → `AREA_GFA`; `IfcDoor` →
`BLASTDOOR`; `IfcAlarm` → `FIREALAMPANEL`; `IfcCivilElement` → `GUTTER`; `IfcPipeFitting` →
`DRAINCHANNELBEND`.

**Mixed** — some components allow both. `IfcDoor` lists `DOOR, GATE, BLASTDOOR, ROLLERSHUTTER`:
predefined for the standard types (`DOOR`, `GATE`), `USERDEFINED` for the specific ones (`BLASTDOOR`,
`ROLLERSHUTTER`).

**Common issues:** misspelling a predefined or USERDEFINED value; putting spaces in the value;
**inventing a USERDEFINED value that is not in the mapping guidance**.
</div>

**In Bonsai.** Every type carries a predefined type. Use the standard enumeration where one fits, and
where IFC+SG asks for a value the enumeration does not offer, set `USERDEFINED` and carry the
required name on the object type. A `USERDEFINED` with no name passes visual inspection and fails a
data check.

`AREA_GFA` is the one to notice: the GFA areas your planning submission depends on are `IfcSpace`
elements with a USERDEFINED subtype, carrying the `AGF_` properties listed further down this page.

### COP, Excel Mapping File and Glossary — which to use when

<div class="sia" markdown="1">
**CORENET X.** Three documents, three distinct jobs:

| Document | Answers | Used for |
| --- | --- | --- |
| **Industry Mapping File** (.xlsx) | **HOW** IFC+SG data should be structured and populated | Mapping between components, IFC entities, property sets, property names and data types. Model authoring, data population, QA |
| **Code of Practice (COP)** | **WHAT** is required for submission, per gateway and agency | Submission requirements, modelling expectations, required information and documents |
| **Glossary of Identified Components** | Finding a component and understanding it | Definitions, IFC representation, required properties, examples. Learning and quick look-up |

Their worked example of the three together: the COP confirms that *Beam Depth* is required for the
relevant gateway and agency → the Glossary locates the component and shows its IFC entity, property
set, property name, description and example → the Mapping File gives the exact mapping (`IfcBeam`,
Pset `OSPref_BeamDimension`, property `Depth`, data type Length, unit mm) → populate the model with
that value in that property in that unit → validate against the COP before submission.
</div>

**In practice.** The Mapping File is the one you keep open while modelling. All three are versioned;
check them, do not remember them.

### Can I use a different element representation?

<div class="sia" markdown="1">
**CORENET X: yes, you can.** The Mapping File and COP give *suggested* element representations per
element type. A different element may be used when appropriate, provided **two requirements** are
met:

1. **Assign the correct IFC entity and IFC SubType before IFC export.**
2. **Add and populate all required IFC+SG properties** as defined in the COP for that entity.

Their example: the Mapping File suggests modelling a ramp with a Ramp element, but you would rather
use a floor slab. That is allowed — model it as a slab, then export it as `IfcRamp` with subtype
`STRAIGHT_RUN_RAMP`, and supply everything `IfcRamp` requires: Gradient (text, e.g. `1:16`), Width
(length, mm, e.g. `1200`), BarrierFreeAccessibility, TransitionRamp, Accessway, Egress, Ingress,
Vehicular (booleans), Material (text).

Their warning is the important part: because the authored element was a slab and not a ramp, **some
IFC+SG properties will not be populated automatically.** You have to add the missing ones yourself.
</div>

**In Bonsai.** This is the permission that makes [Stage 02]({{ '/stages/concept-design/' | relative_url }})
legitimate: sketch geometry, study masses and `X-` cutters are fine while the intent is preserved.
It is *not* permission to submit a mesh box called a wall — the two conditions are the price, and the
second one is real work.

## 03 · Project coordinates and alignment

### Project coordinates and geo-referencing

<div class="sia" markdown="1">
**CORENET X.** All models must align to **SVY21** for Easting (X) and Northing (Y), **SHD — Singapore
Height Datum** for elevation (Z), and **real-world orientation (True North)**.

The sequence is: take the survey reference from the licensed land surveyor → establish one shared
coordinate reference for the project from it, with a consistent origin and orientation → make every
discipline model use that same reference, so they align in 3D when federated.

**Good practice:** establish coordinates from survey data at project start; same reference in every
model; keep it consistent when linking or federating; verify coordinates and orientation before
export and submission. **Common issues:** models not aligned to SVY21; elevation not referenced to
SHD; misalignment between disciplines at federation; orientation not aligned to True North; late
coordinate changes causing rework.
</div>

**In Bonsai.** Set the projected CRS and map conversion in the project's georeferencing settings
rather than dragging geometry to real-world coordinates — IFC's map conversion is exactly the
mechanism that lets you author near the origin while the file still declares its true position and
rotation. What must be true is that the file *states* its SVY21 easting and northing, its SHD
elevation and its True North rotation. What must not be true is a model floating 30 km from its own
origin, losing precision and patience.

**In this course.** [Stage 01]({{ '/stages/pre-design/' | relative_url }}) sets datum and north; record the
coordinate basis in the same decision-log entry, and note that the brief's `5'-3"` is a
site-relative assumption until it is tied to a published vertical datum — which on this project is
NAVD88 and a FEMA base flood elevation rather than SHD. The requirement CORENET X is really making
is that the file *states* its datum; which datum follows the site.

### Ensure models align correctly in federation

<div class="sia" markdown="1">
**CORENET X.** **Federation means multiple models aligned, not merged** — the models stay separate
IFC files and are combined for review and coordination.

For that to work, two things must match across every discipline:

- **Coordinate system** — same origin (0,0,0), same orientation, same True North, same survey reference.
- **Spatial structure** — same site, same building structure, **same storey names and elevations**.

The alignment check runs three times: **pre-check in the native software** (coordinates, origin,
spatial structure) → **after export in an IFC viewer** (overlay the models, verify orientation and
scale, check storey alignment, confirm no unexpected offsets) → **during submission in the portal
viewer**, before confirming.
</div>

**In Bonsai.** Export, then open the result somewhere that is not Blender, before you believe it.
Worth forming as a habit on a project with no other disciplines, because it is unforgiving on one
that has them.

## 04 · Model quality and coordination

### Maintain unique GUIDs across models

<div class="sia" markdown="1">
**CORENET X.** Every IFC element must have a unique GUID so it can be identified, tracked and
compared across models and submissions.

The clarification matters: **repeated or similar elements are perfectly acceptable** — forty
identical windows are forty distinct GUIDs. Duplicate GUIDs arise when *files or elements are reused
incorrectly*: duplicating a completed model file and using it as a new project or block file gives
every element in the copy the same GUID as its twin.

**Good practice:** do not duplicate completed model files to create new projects or blocks; follow
the recommended workflow for preset elements and templates; **check for duplicate GUIDs before
submission**.
</div>

**In Bonsai.** Bonsai assigns `GlobalId`s. The [model standard's]({{ '/standards/' | relative_url }}) rule of
branching *revisions* rather than duplicating *blocks* is what keeps you out of this.

### Manage file size for performance

<div class="sia" markdown="1">
**CORENET X.** Keep each IFC file within **800 MB** (recommended). Split models by block, zone or
discipline where appropriate, and avoid merging multiple buildings into a single file.

The reason this practice is really about *modelling*, not compression:

> **Over-modelling increases file size without improving submission outcome.** Always model
> proportionately to the requirements of each gateway.

And the gateway guidance is the clearest level-of-detail statement in the whole of IFC+SG:

| Gateway | Model |
| --- | --- |
| **DG · Design Gateway** | Design intent only. Simplified geometry. Include the elements required for submission. Avoid detailed modelling |
| **PG · Piling Gateway** (if applicable) | Foundation and piling elements only. Keep geometry simple and focused on scope. Exclude unrelated elements |
| **CG · Construction Gateway** | Buildable elements required for submission. Add detail only where required. Avoid fabrication-level or as-built detail |

</div>

**In Bonsai.** Parametric elements driven by types are small; tessellated meshes and imported
high-poly content are not. Every time Push/Pull refuses an IFC element it is protecting both the
parametric definition and the file size.

**In this course.** This is the regulator saying, in its own words, what the stage gates say: build
what the stage needs and no more. A one-room pavilion will never approach 800 MB — but the habit of
asking *which gateway is this detail for?* is the transferable part.

### Model coordination and clash detection

<div class="sia" markdown="1">
**CORENET X.** Clash detection here is **rule-based, not merely geometry-based**, and it is governed
by a coordination matrix of element type against element type.

> **Clash ≠ always fail.** Determine the action: **Resolve / Accept / Alert.**

Some clashes are simply not allowed — an architectural **door intersecting a structural beam** is a
design clash and should not occur. Others are conditional, judged on size. Their MEP example, a pipe
clashing with a structural beam:

| Pipe diameter / width | Result |
| --- | --- |
| ≤ 100 mm | **Pass** |
| > 100 mm and ≤ 200 mm | **Alert** |
| ≥ 200 mm | **Fail** |

**How to apply:** run clash detection on the coordinated IFC models → review results against the
coordination matrix → resolve, accept or escalate according to the rules and requirements of the
submission.
</div>

**In Bonsai.** Clash tooling is built in. Run it at
[Stage 04]({{ '/stages/design-development/' | relative_url }}) and after every substantial change — the
[VAF]({{ '/vaf/' | relative_url }}) prices coordination as a separate component at each of four gateways for
exactly this reason.

The transferable lesson is the triage. A clash list is not a defect list: every entry needs a
decision, and "accepted" is a legitimate answer that has to be recorded.

### Export gridlines to all storeys

<div class="sia" markdown="1">
**CORENET X.** Four steps: create gridlines in the authoring tool → **associate them to storeys**,
exporting them to *every* required storey → export the IFC with gridlines enabled → **check the
gridlines in an IFC viewer** across multiple levels before submission.

**Common mistakes:** gridlines exported at only one level; hidden in the export view; missing storey
association; incorrect export settings; **visible in the BIM tool but missing from the IFC**.
</div>

**In Bonsai.** Grids are model objects, not drawing decoration. This house can be built without one
and should still have one — setting out, coordination and every later dimension check hang off it.
The last common mistake is the one to internalise: grids that look right in the authoring tool prove
nothing about the exported file.

---

## What the data actually looks like

The IFC+SG model content requirements list, per element, which parameters are needed at which stage
and which discipline owns them. Below is the extract relevant to this project.

Legend: **C** conceptual · **S** schematic · **D** detailed · **T** tender · **X** construction ·
**A** as-built.

### Doors — Architectural

| Parameter | C | S | D | T | X | A |
| --- | :-: | :-: | :-: | :-: | :-: | :-: |
| Main Entrance | | ● | ● | ● | ● | ● |
| Clear Height · Clear Width | | | ● | ● | ● | ● |
| Fire Rating · Fire Exit · Fire Access Opening | | | ● | ● | ● | ● |
| Material · Hardware · Operation Type | | | ● | ● | ● | ● |
| Overall Width · Overall Height | | | ● | ● | ● | ● |
| One Way Locking Device | | | ● | ● | ● | ● |

Twenty-six parameters in total across doors and their sub-elements, blast doors included. Note what
is required from **schematic**: whether a door is the main entrance. That is a data decision made at
[Stage 03]({{ '/stages/schematic-design/' | relative_url }}), which is why the course asks you to mark doors
then rather than at documentation.

### Windows — Architectural

| Parameter | C | S | D | T | X | A |
| --- | :-: | :-: | :-: | :-: | :-: | :-: |
| Ventilation Sleeve: Inner / Outer Diameter | ● | ● | ● | ● | ● | ● |
| Bay Window: Operation Type · Window: Material | | ● | ● | ● | ● | ● |
| Percentage of Opening | | | ● | ● | ● | ● |
| Safety Barrier Height | | | ● | ● | ● | ● |
| Structural Height · Structural Width | | | ● | ● | ● | ● |
| Fire Access Opening | | | ● | ● | ● | ● |

**Percentage of opening** is the ventilation requirement expressed as model data. The brief's "cool
without machines" success criterion stops being rhetoric and becomes a number a checker reads.

### Spaces and spatial allocation — Architectural

| Parameter group | From stage |
| --- | --- |
| **Household Shelter** — construction method, internal length, internal width | **Conceptual** |
| **Area GFA** (`AGF_`) — name, development use, use quantum, bonus GFA type, unit number, note | Schematic |
| **Area Landscape** (`ALS_`) — landscape type, greenery features | Schematic |
| **Area Connectivity** (`ACN_`) — connectivity type, opening hours, paving specification | Schematic |
| **Area Strata** (`AST_`) — area type, legal area, strata lot numbers | Schematic |
| Space: occupancy type, parking type, C value, refuse output, unit number | Schematic |
| Space: name, area, height, volume, occupancy load, purpose group | Detailed |
| Space: barrier-free accessibility, ambulant disabled, larger accessible, step ramp access | Detailed |
| Space: elderly friendly, children friendly, hearing enhancement | Detailed |
| Space: ventilation mode and type, smoke control, fire detection and suppression | Detailed |
| Accessible Route: barrier-free accessibility | Detailed |

Remember from the subtype guidance above: a GFA area is an `IfcSpace` with subtype `USERDEFINED` and
the value `AREA_GFA`. The `AGF_` properties hang off that.

<div class="warn" markdown="1">
#### The household shelter is a conceptual-stage requirement

Its construction method and internal dimensions are expected in the model from the **conceptual**
stage — earlier than almost anything else in the list. A Singapore landed house has one, and if it
appears at Design Development you have already planned around a room that was not there.

It is the clearest example in the whole of IFC+SG of a data requirement that is really a design
requirement wearing a data costume.

The course project is an Illinois house and has no household shelter, so this one is reference
rather than exercise. The transferable habit is the point: find the requirements your jurisdiction
expects at **conceptual** stage, and put them in the massing — because the ones demanded earliest
are almost always the ones that cannot be fitted in later.
</div>

### Walls

Wall carries twenty-four parameters — and all but one are **C&S discipline**: rebar, stirrups,
material grade, load bearing, working loads, precaster accreditation, prefinished and double-bay
façade, shelter usage. The architect's own is **construction method**.

That single fact is worth more than it looks. It says plainly that a wall in an IFC+SG submission is
a shared object with divided ownership, and that "the architect models the walls" is a sentence about
geometry, not about data. Under the [VAF]({{ '/vaf/' | relative_url }}), coordinating that division is a
priced component at every gateway.

### Building and storey

| Parameter | Element | From stage |
| --- | --- | --- |
| Project development type · owner built / owner stay | Building | Detailed |
| Attic level | Building Storey | Schematic |

**Attic level** matters here: if the design has an attic, the storey has to say so from
schematic onwards — and per the level-naming practice, that storey is called `Attic`, not `Attic 1`.

## How the course uses all of this

You are not submitting anything. What you are building are the habits that make a submission
survivable:

{: .steps}
1. **Name storeys to the convention from day one** ([Stage 03]({{ '/stages/schematic-design/' | relative_url }})) — `1st Storey`, `Attic`, `Roof`. Renaming later breaks every drawing reference.
2. **Classify deliberately, then subtype, then propertise** ([Stage 03]({{ '/stages/schematic-design/' | relative_url }})) — the entity is only the first of three.
3. **Mark data at the stage it is required** — main entrance at schematic, clear widths at detailed, as-built provenance at as-built.
4. **Model to the gateway, not to your enthusiasm** ([Stage 04]({{ '/stages/design-development/' | relative_url }})) — design intent at DG, buildable at CG, and over-modelling helps nobody.
5. **Write the IDS** ([Stage 04]({{ '/stages/design-development/' | relative_url }})) — an IDS makes an IFC+SG-shaped requirement machine-checkable on your own model, before anyone else checks it.
6. **Triage clashes rather than counting them** — resolve, accept or alert, and record which.
7. **Verify after export, every time** — in a viewer, not in Blender. Three of the twelve practices end with this instruction.
8. **Keep GUIDs and coordinates clean from the start** — both are cheap at Stage 01 and expensive at Stage 07.

<div class="note" markdown="1">
#### Where the material on this page came from

The twelve practices are summarised from the illustrated guides published under
[CORENET X → IFC+SG → Modelling & Authoring → General Modelling Practices](https://info.corenet.gov.sg/ifc-sg/modelling---authoring/GeneralModellingPractices),
read in August 2026. Each guide is worth opening in full; the diagrams carry more than a summary can.

The parameter tables are extracted from **IFC+SG Model Content Requirements V2.0 (20 March 2026)**,
as shipped in [Bonsai Sketch Mode's](https://github.com/integrations-space/BonsaiSketch)
`data/ifc_sg.json`. That extract covers 21 element groups; this page shows only those a small landed
house touches.

The standard's own mechanism for recording an element's class is a parameter named `IfcExportAs` —
that is, the modeller declares it. Any mapping from an IFC+SG element name to an IFC class is
therefore a judgement, which is why the add-on keeps it as editable data rather than code, and why
unmapped elements attach nothing rather than attaching requirements that might be wrong.

CORENET X also publishes a [BIM Authoring Tools](https://info.corenet.gov.sg/ifc-sg/modelling---authoring/bim-authoring-tools)
guide with tool-specific steps, and a [Plug-in & 3rd Party Tools](https://info.corenet.gov.sg/ifc-sg/modelling---authoring/3rdpartytools)
page listing IFC viewers and checkers. Bonsai is not among the tools they document; the translations
on this site are ours.
</div>
