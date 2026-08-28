---
layout: default
title: Glossary
strap: The terms this course uses, in the sense it uses them.
permalink: /glossary/
---

## Software

**Blender** — the 3D application everything runs inside. Versions 5.0 and 5.2 LTS are supported here.

**Bonsai** — the open-source add-on that turns Blender into a native IFC authoring platform.
Formerly BlenderBIM. [bonsaibim.org](https://bonsaibim.org/)

**Bonsai Sketch Mode** — the direct-modelling interaction layer on top of Bonsai: single-key tools,
inference snapping and a measurement box. Produces plain meshes; Bonsai assigns them meaning.

**Sketch geometry** — plain Blender mesh produced by Line, Rectangle or Push/Pull. Not an
`IfcProduct`, and deliberately so.

**Describe** — the Sketch panel that builds geometry from a typed sentence, using the same verbs a
person would. Requires an Anthropic API key. Edits the live model with no proposal step.

**Text to Model** — a local loopback command channel that lets a script or agent drive Blender.
Token-authenticated, off by default, no undo.

## IFC and information

**IFC** — Industry Foundation Classes: the open, vendor-neutral data model for buildings. The
durable artefact of this course. An IFC file will open in ten years; a `.blend` may need an old
Blender.

**IfcProject / IfcSite / IfcBuilding / IfcBuildingStorey** — the spatial structure. Every element
belongs to exactly one storey; an element with no container is invisible to half of every downstream
tool.

**Type and occurrence** — an `IfcWallType` is the specification (layers, materials, thickness); each
`IfcWall` placed from it is an occurrence. One type used forty times is a schedule; forty
individually drawn walls are a drawing.

**IfcOpeningElement** — a real void related to its host wall. Not a mesh hole. Doors and windows are
placed into openings, which is what makes a door schedule possible.

**IfcSpace** — a room, named, numbered and measurable. Area read from the model beats area typed
into a drawing.

**LOIN** — Level of Information Need. What the model must contain at a given stage — no more. The
stage-by-stage table on the [SIA mapping]({{ '/sia-mapping/' | relative_url }}) page is this project's version.

**IDS** — Information Delivery Specification: a machine-checkable statement of what a model must
contain. Written once at Stage 04, run at every gate afterwards.

**BCF** — BIM Collaboration Format: an issue with a viewpoint attached, so a comment arrives with the
camera already pointing at the problem. Travels between applications; a CSV does not.

**IFC+SG** — the Singapore IFC data structure used for regulatory submission: IFC4 plus **SGPsets**
and standardised properties and values, with validation checks. Elements declare their class through
an `IfcExportAs` parameter and carry required parameter sets, staged across seven model content
stages. Captured on [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}); the authority is
[info.corenet.gov.sg](https://info.corenet.gov.sg/) at the time you submit.

**SGPset** — a Singapore property set: the container for the parameters IFC+SG requires on an
element, such as a door's clear width or a space's purpose group.

**CORENET X** — the Singapore regulatory submission process that reads IFC+SG models, organised
around gateways (pre-submission consultation, design, piling, construction, completion).

**General Modelling Practices** — CORENET X's twelve modelling rules in four groups: model setup and
structure, element modelling and data, coordinates and alignment, and model quality. Each one, and
what it means in Bonsai, is on the [IFC+SG page]({{ '/ifc-sg/' | relative_url }}).

**Block mechanism** — how a development is decomposed into blocks for IFC+SG submission, and how the
architectural, structural and MEP models align across them.

**SVY21** — Singapore's projected coordinate system, and the basis for geo-referencing a model that
will be federated or submitted.

**Predefined type / USERDEFINED** — every IFC type carries a predefined type from a standard
enumeration. Where IFC+SG needs a subtype the enumeration does not offer, the predefined type
becomes `USERDEFINED` and the object type carries the required name. A `USERDEFINED` with no name
passes visual inspection and fails a data check.

**GUID / GlobalId** — the unique identifier on every IFC element. Duplicating a file to make a
second "block" duplicates every GUID in it, which is a submission-level defect.

**BEP** — BIM Execution Plan. In the VAF it appears as a named component at the Pre-Submission
gateway, alongside constructing the model and coordinating it for clash detection and compliance
checks.

**CDE** — Common Data Environment. On this project it is a folder with a naming convention. On a
real one it is a system, and the convention still matters more than the system.

## Stages and appointment

**SIA** — Singapore Institute of Architects.

**Scope of Service Matrix** — SIA's reference setting out what an architect is normally responsible
for across eight stages and four roles, split into Basic and Additional Service. Not mandatory; your
scope is your consultancy agreement.

**VAF / SIA BluePrint** — the Value Articulation Framework: the same practice decomposed into
tasks, stages and components, with the staff grades each consumes. Used here for vocabulary and for
locating BIM work.

**Basic Service / Additional Service** — the split that decides whether work is inside the fee.
An as-built BIM model, post-occupancy evaluation, VR walk-throughs and any documentation arising
from a design change are Additional.

**Design change** — under the SIA definition, a change arising from a change to the brief, from the
client's request after accepting the design, from a new authority requirement, **or from site
conditions or construction method**. The last two surprise people.

**Qualified Person (QP)** — the person accountable for regulatory compliance and submissions.
One of the four roles in the matrix, and often the same human being as the Designer.

**Protraction** — the construction period running longer than contracted. Contract administration
work scales with it; a percentage fee on an unchanged contract sum does not.

## Submission and completion (Singapore)

**DC** — Development Control. **WP** — Written Permission, from URA, at Schematic Design.
**BP** — Building Plan, from BCA, at Design Development. **DP** — Detailed Plan.

**TOP** — Temporary Occupation Permit. **CSC** — Certificate of Statutory Completion, at Post
Completion. **FSC** — Fire Safety Certificate, from SCDF.

**DLP** — Defects Liability Period, running from substantial completion through Stage 08.

**Authorities you will meet in this course** — URA (planning), BCA (building), PUB (drainage and
sewerage), NParks (greenery and trees), SCDF (fire safety), LTA (roads, parking, rail), NEA
(environmental health and pollution), SLA (survey, strata, land betterment charge).

## Contract administration

**RFI / RFA** — Request for Information / Approval, from the contractor. Every one gets a dated
written answer and a note of whether it changed the documents.

**Variation / VO** — a change to the contracted works, instructed and priced. The model's job is to
make the quantity difference specific.

**EOT** — Extension of Time. **LD** — Liquidated Damages. **PC sum** — prime cost.
**Provisional sum** — an allowance for work not yet fully defined; it needs a different level of
drawing than a fully specified item.

**Transmittal** — the record of what was issued, at what revision, when, and to whom. A tender issue
with no transmittal cannot be defended, and later is when it will be questioned.

## This course's own vocabulary

**Gate** — the checklist at the end of each stage. Passing it means the model, the deliverable and
the registers agree.

**`A-` / `X-` / `Z-`** — issued architectural geometry / working geometry never issued / superseded
geometry kept for the record. Detail on the [model standard]({{ '/standards/' | relative_url }}) page.

**`design_status`** — `provisional`, `approved` or `superseded`. Three values, no more.

**Verified / assumed / unchanged** — the as-built provenance marks introduced at Stage 07. A model
that cannot distinguish them will be trusted completely and be wrong in places.
