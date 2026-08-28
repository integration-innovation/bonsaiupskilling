---
layout: default
title: IFC+SG and CORENET X
strap: What Singapore's regulatory submission expects of your model, and how to satisfy it in Bonsai.
permalink: /ifc-sg/
---

The [SIA scope]({{ '/sia-mapping/' | relative_url }}) says what you deliver. The [VAF]({{ '/vaf/' | relative_url }}) says what it costs. **IFC+SG
says what the model itself must contain**, and CORENET X is the process that reads it. This page
captures both, and turns them into things you do in Bonsai.

<div class="warn" markdown="1">
**Read the source.** This is our summary for teaching, and regulatory requirements change. The
authority is [info.corenet.gov.sg](https://info.corenet.gov.sg/) — in particular
[What is IFC+SG](https://info.corenet.gov.sg/ifc-sg/start-here/WhatIsIFCSG),
the [IFC+SG Excel Mapping File](https://info.corenet.gov.sg/ifc-sg/requirements---submission/ifc-sg-excel-mapping-file),
and the [General Modelling Practices](https://info.corenet.gov.sg/ifc-sg/modelling---authoring/GeneralModellingPractices).
Check the current version before any real submission.
</div>

## What IFC+SG is

IFC+SG is the data structure for BIM models submitted through CORENET X, so that regulatory agencies
can read, review and check model data directly rather than reading drawings of it. It is built on
**IFC4**, extended with **SGPsets** — Singapore property sets — and standardised properties and
values, plus validation checks the submission runs against.

Two consequences for how you model:

- **The class is the interface.** An agency's check finds your household shelter because it is
  classified and propertied as one, not because a drawing labels it. Geometry that looks right and
  classifies wrong fails silently.
- **Data is required by stage, not all at once.** IFC+SG states which parameters are needed at
  which stage of the project, so a conceptual model is not expected to carry as-built detail. That
  staging is the reason this course can be a course rather than one enormous checklist.

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

Note the shape of it: **Pre-Design has no IFC+SG stage**, because there is no model yet, and
**O&M / Asset Information does** — the data outlives the project. Most practices resource the first
five and are surprised by the last two.

## CORENET X General Modelling Practices

CORENET X publishes twelve general modelling practices in four groups. They are illustrated guides,
best read at the source; what follows is each practice, why it bites, and **what it means in
Bonsai** for this project.

### 01 · Model setup and structure

<div class="sia" markdown="1">
#### Level naming and organisation
**CORENET X:** organise levels clearly so storeys can be understood and checked correctly after IFC
export.

**In Bonsai:** storeys live in `Properties → Project Overview → Spatial Decomposition`. Name them for
what they are and set real elevations — `Ground` at your FFL, `Roof` at FFL + 3.150, and `Attic` if
you have one. Do not leave `Level 1`, `Level 2`, `Level 3` behind: a checker reading your IFC has
only the name and the elevation to work with.

**In this course:** [Stage 03, step 1]({{ '/stages/schematic-design/' | relative_url }}), and the four-level structure in the
[model standard]({{ '/standards/' | relative_url }}).
</div>

<div class="sia" markdown="1">
#### Block mechanism
**CORENET X:** understand how architectural, structural and MEP models align with the IFC+SG block
mechanism.

**In Bonsai:** the bungalow is a single block with one submitting discipline, so this is the one
practice the course exercises least. Know it exists before your first multi-block project: blocks
are how a development is decomposed for submission, and getting them wrong is a resubmission, not a
correction.
</div>

### 02 · Element modelling and data

<div class="sia" markdown="1">
#### Use the correct IFC entities
**CORENET X:** select the correct IFC entity so each element is recognised and reviewed properly
after export.

**In Bonsai:** `Properties → Object Information → Products` dropdown → choose the class → **Assign
IFC Class**. Or, from the Sketch tab, the `IFC` panel in the sidebar does the same for a finished
sketch. A wall drawn as a mesh and left unclassified is, to a checker, nothing at all.

**In this course:** the whole reason classification is deferred until [Stage 03]({{ '/stages/schematic-design/' | relative_url }})
and then done deliberately — see [the recipes]({{ '/modelling/' | relative_url }}).
</div>

<div class="sia" markdown="1">
#### Predefined Type vs USERDEFINED
**CORENET X:** know when a standard predefined type is right and when `USERDEFINED` is needed for
IFC+SG subtype requirements.

**In Bonsai:** every type carries a predefined type. Use the standard enumeration where one fits —
an external wall is not a "custom" thing. Where IFC+SG needs a subtype the enumeration does not
offer, set the predefined type to `USERDEFINED` and give the object type the required name. A
`USERDEFINED` with no object type name is the most common way a model passes visual inspection and
fails a data check.
</div>

<div class="sia" markdown="1">
#### When to use the COP, the Excel Mapping File and the Glossary
**CORENET X:** three documents, three jobs — the Code of Practice for the submission process, the
IFC+SG Excel Mapping File for what data each element carries, and the Glossary of Identified
Components for what an element *is*.

**In practice:** the Mapping File is the one you keep open while modelling. It is the authority for
the parameter tables further down this page, and it is versioned — check it, do not remember it.
</div>

<div class="sia" markdown="1">
#### Can I use a different element representation?
**CORENET X:** an alternative representation may be used while modelling, provided it maintains the
intended IFC+SG submission requirements.

**In Bonsai:** this is the permission that makes [Stage 02]({{ '/stages/concept-design/' | relative_url }}) legitimate. Sketch
geometry, study masses and `X-` cutters are fine while the intent is preserved and the submitted
model carries the right entities and data. It is not permission to submit a mesh box called a wall.
</div>

### 03 · Project coordinates and alignment

<div class="sia" markdown="1">
#### Project coordinates and geo-referencing
**CORENET X:** coordinates and geo-referencing directly affect model placement, IFC export accuracy
and downstream review. Singapore's projected system is **SVY21**.

**In Bonsai:** set georeferencing in the project settings rather than dragging the model to real-world
coordinates. Model near the origin; record the map conversion. A model authored ten kilometres from
its own origin loses geometric precision and is miserable to work in, and one with no georeferencing
at all cannot be federated with anybody else's.

**In this course:** [Stage 01]({{ '/stages/pre-design/' | relative_url }}) sets the datum and north; record the coordinate
basis in the same decision-log entry.
</div>

<div class="sia" markdown="1">
#### Ensure models align correctly in federation
**CORENET X:** check that architectural, structural and MEP models align when federated in an IFC
viewer or coordination tool.

**In Bonsai:** export and open the result somewhere that is not Blender before you believe it. This is
a habit worth forming on a project with no other disciplines, because it is unforgiving on one that
has them.
</div>

### 04 · Model quality and coordination

<div class="sia" markdown="1">
#### Maintain unique GUIDs across models
**CORENET X:** prevent duplicated IFC GUIDs when creating multiple blocks, copying templates, or
managing linked discipline models.

**In Bonsai:** every IFC element has a `GlobalId`, and Bonsai assigns them. The way you break this is
copying a file and calling the copy a different block — every element in it now shares a GUID with
its twin. The [model standard's]({{ '/standards/' | relative_url }}) rule of branching *revisions* rather than duplicating
*blocks* keeps you out of this.
</div>

<div class="sia" markdown="1">
#### Manage file size for performance
**CORENET X:** reduce unnecessary complexity and optimise file size for export, loading, federation
and review.

**In Bonsai:** parametric elements driven by types are small; tessellated meshes are not. Every time
Push/Pull refuses an IFC element, it is protecting both the parametric definition and the file size.
Detailed manufacturers' furniture, imported blocks and high-poly vegetation are where a house-sized
model becomes a tower-sized file.
</div>

<div class="sia" markdown="1">
#### Clash detection and coordination
**CORENET X:** review clashes and coordination issues early, before IFC export and submission.

**In Bonsai:** clash tooling is built in. Run it at [Stage 04]({{ '/stages/design-development/' | relative_url }}) and after
every substantial change, not once at the end — the VAF prices coordination as a separate component
at each of four gateways for exactly this reason.
</div>

<div class="sia" markdown="1">
#### Export gridlines to all storeys
**CORENET X:** ensure gridlines export across all storeys to maintain spatial reference and support
coordination.

**In Bonsai:** grids are model objects, not drawing decoration. A bungalow can be built without a grid
and should still have one, because setting out, coordination and every later dimension check hang
off it.
</div>

## What the data actually looks like

The IFC+SG model content requirements list, per element, which parameters are needed at which stage
and which discipline owns them. The tables below are the bungalow-relevant extract, showing the
stages at which each parameter is expected.

Legend: **C** conceptual · **S** schematic · **D** detailed · **T** tender · **X** construction ·
**A** as-built · **O** operation.

### Doors — Architectural

| Parameter | C | S | D | T | X | A |
| --- | :-: | :-: | :-: | :-: | :-: | :-: |
| Main Entrance | | ● | ● | ● | ● | ● |
| Clear Height · Clear Width | | | ● | ● | ● | ● |
| Fire Rating · Fire Exit · Fire Access Opening | | | ● | ● | ● | ● |
| Material · Hardware · Operation Type | | | ● | ● | ● | ● |
| Overall Width · Overall Height | | | ● | ● | ● | ● |
| One Way Locking Device | | | ● | ● | ● | ● |

Twenty-six parameters in total for doors and their sub-elements, including blast doors. Note what
is required from **schematic**: whether a door is the main entrance. That is a data decision made at
[Stage 03]({{ '/stages/schematic-design/' | relative_url }}), which is why the course asks you to mark doors then rather
than at documentation.

### Windows — Architectural

| Parameter | C | S | D | T | X | A |
| --- | :-: | :-: | :-: | :-: | :-: | :-: |
| Ventilation Sleeve: Inner / Outer Diameter | ● | ● | ● | ● | ● | ● |
| Bay Window: Operation Type · Window: Material | | ● | ● | ● | ● | ● |
| Percentage of Opening | | | ● | ● | ● | ● |
| Safety Barrier Height | | | ● | ● | ● | ● |
| Structural Height · Structural Width | | | ● | ● | ● | ● |
| Fire Access Opening | | | ● | ● | ● | ● |

**Percentage of opening** is the ventilation requirement expressed as model data. The brief's
"cool without machines" success criterion stops being rhetoric and becomes a number a checker reads.

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

<div class="warn" markdown="1">
#### The household shelter is a conceptual-stage requirement

Its construction method and internal dimensions are expected in the model from the **conceptual**
stage — earlier than almost anything else in the list. A Singapore landed house has one, and if it
appears at Design Development you have already planned around a room that was not there.

Add it to the brief and to [Stage 02]({{ '/stages/concept-design/' | relative_url }}). It is the clearest example in the whole
of IFC+SG of a data requirement that is really a design requirement wearing a data costume.
</div>

### Walls

Wall carries twenty-four parameters — and all but one are **C&S discipline**: rebar, stirrups,
material grade, load bearing, working loads, precaster accreditation, prefinished and double-bay
façade, shelter usage. The architect's own is **construction method**.

That single fact is worth more than it looks. It says plainly that the wall in an IFC+SG submission
is a shared object with divided ownership, and that "the architect models the walls" is a sentence
about geometry, not about data. Under the [VAF]({{ '/vaf/' | relative_url }}), coordinating that division is a priced
component at every gateway.

### Building and storey

| Parameter | Element | From stage |
| --- | --- | --- |
| Project development type · owner built / owner stay | Building | Detailed |
| Attic level | Building Storey | Schematic |

**Attic level** matters for a bungalow: if the design has an attic, the storey has to say so from
schematic onwards.

## How the course uses this

You are not submitting anything. What you are doing is building the habits that make a submission
survivable:

{: .steps}
1. **Classify deliberately** ([Stage 03]({{ '/stages/schematic-design/' | relative_url }})) — the correct entity, not the convenient one.
2. **Name storeys and set elevations properly** ([Stage 03]({{ '/stages/schematic-design/' | relative_url }})) — level naming is practice number one for a reason.
3. **Mark data at the stage it is required, not later** — main entrance at schematic, clear widths at detailed, as-built provenance at as-built.
4. **Write the IDS** ([Stage 04]({{ '/stages/design-development/' | relative_url }})) — an IDS is how you make an IFC+SG-shaped requirement machine-checkable on your own model, before anyone else checks it.
5. **Coordinate four times, not once** ([Stages 03, 04, 06, 07]({{ '/vaf/' | relative_url }})) — matching the VAF's four BIM gateway components.
6. **Keep GUIDs and coordinates clean from the start** — both are cheap at Stage 01 and expensive at Stage 07.

<div class="note" markdown="1">
#### Where the data in this page came from

The parameter tables are extracted from **IFC+SG Model Content Requirements V2.0 (20 March 2026)**,
as shipped in [Bonsai Sketch Mode's](https://github.com/integrations-space/BonsaiSketch)
`data/ifc_sg.json`. The extract covers 21 element groups; this page shows only those a small landed
house touches.

The standard's own mechanism for recording an element's class is a parameter named `IfcExportAs` —
that is, the modeller declares it. Any mapping from an IFC+SG element name to an IFC class is
therefore a judgement, which is why the add-on keeps it as editable data rather than code, and why
unmapped elements attach nothing rather than attaching requirements that might be wrong.
</div>
