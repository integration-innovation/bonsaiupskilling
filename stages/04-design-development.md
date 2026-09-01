---
layout: default
stage_num: "04"
title: Design Development
strap: Real construction — assemblies, junctions, coordinated openings, fittings, and the first machine-checkable ruleset.
exit_state: A coordinated, typed, clash-checked model that a Building Plan submission could rest on
permalink: /stages/design-development/
---

Schematic Design proved the building works. Design Development proves it can be *built*: layers with
thicknesses, junctions that meet, openings with lintels above them, and a model whose quantities are
close enough to price. It is the longest stage here and the one that repays care most obviously.

<div class="sia" markdown="1">
#### What the SIA scope expects of you here

- **Designer** — develop the schematic design to the level of detail required for Building Plan submissions.
- **Qualified Person** — ensure continued regulatory compliance; prepare and submit plans for BP/DP clearances; prepare and submit to BCA for Building Plan approval.
- **Contract Administrator** — check the client's requirements for the pricing exercise; pre-qualify suitable tenderers; formulate tender evaluation criteria.
- **Design Manager** — continue tracking design, budget and programme; review the QS's estimate against the project budget.

The VAF calls this *Detail Design*: develop the design far enough to go into tender preparation, up
to design sign-off; coordinate and de-conflict across the client's departments, the other
consultants, stakeholders and the public; update the cost estimate; and produce a more detailed
construction timeline.
</div>

## What you will learn

- Material layers that add up to a real wall, and slab and roof build-ups that meet them.
- Coordinating an opening with its host: lintel, sill, jamb, reveal.
- Clash detection between architecture and the structure and services you have assumed.
- Writing an **IDS** — a machine-checkable statement of what this model must contain — and running it.
- Using **BCF** so an issue travels with a viewpoint instead of a sentence.

## Before you start

Stage 03's gate is passed and the model has a clean spatial structure. Bring a structural assumption
with you: this house has a slab, a beam zone and a roof structure whether or not an engineer has told
you their sizes yet. Assume, model, label the assumption, and check it later.

## Build it

*Step-by-step detail for every operation below is in the [modelling recipes]({{ '/modelling/' | relative_url }}); the data each one has to carry is in [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}).*

{: .steps}
1. **Turn each type into a real build-up.** The floor plane becomes its layers — travertine, precast plank, steel joist zone — each with a material and a thickness summing to the 15" structural depth. Do the same for the roof plane, the terrace and the core partition. The type is the specification; get it right once and every occurrence inherits it.

2. **Absorb the change event: the measured drawings arrive.** Download [HABS IL-1105](https://www.loc.gov/resource/hhh.il0323.sheet) — eight measured drawings, public domain — and check your model against them. At least one dimension you have carried since Stage 02 is wrong.

   Your worklist is already written: every element carrying `confidence = C` in its `Farnsworth_Provenance` set is a figure you derived rather than measured. Work through them, correct each against the drawing, update the property set to name the sheet you took it from, and re-grade it **A**. Then re-run the gate and see what else moved.

   This is the whole argument for recording provenance at Stage 02. Without it you would now be re-checking every dimension in the model; with it you are checking fifteen.

3. **Coordinate every opening properly.** For each door and window: check the head against the beam zone, the sill against the finished floor, the jamb against the wall junction and the reveal against the external finish. Use Bonsai's void workflow — an `IfcOpeningElement` related to its host — never a mesh subtraction. There is no auto-subtract in Sketch Mode, and this is the stage where that constraint is doing you a favour.

4. **Develop the two planes as construction.** The 15" channel at the edge, the joists behind it, the precast plank, the travertine over it, and the soffit you see from underneath — this building has no ceiling void to hide anything in. Then answer the question the massing let you avoid: **where does the water go?** There is no gutter, no fascia and no overhang; the roof drains internally, through the core, in the one place the plane is allowed to be punctured. That is the junction most models of this house get wrong, because in the massing it was a single surface.

5. **Model the core at coordination level.** Everything wet or mechanical in this house is in one 20'-0" × 8'-0" box, so this step is where the building either works or does not. Not catalogue fittings — zones with real dimensions: the two bathrooms back to back, the mechanical space between them, the galley counter on the north face, the fireplace on the south, and the flue and vents that run up through the roof. Enough to prove the core works and to hang a finish schedule on. Classify as `IfcSanitaryTerminal` and `IfcFurniture`.

6. **Prove the approach.** Grade to terrace to porch to floor, in two flights and a threshold. Model the risers, the goings and the landings at their real dimensions and check they are consistent — the flights are broad and low on purpose, and getting them wrong reads immediately in every photograph of this building. Then check them against current accessibility requirements, not against a memory of them, and record what a 1951 house fails and what you would do about it today.

7. **Keep studying in Sketch, still on `X-` geometry.** Push/Pull still works on plain meshes and this is exactly what it is for at this stage: a temporary cutter to visualise a mullion junction, a stair riser tested at three heights, a welded corner tried out. Study freely, then build the answer parametrically and delete or explain the study.

8. **Run a clash check.** Architecture against structure — which on this building is the same thing seen twice, and therefore worth checking properly: the columns against the slab edges, the mullions against the columns, the flue against the roof plane, the core partitions against both slabs. Bonsai has clash tooling built in — use it rather than rotating the model and hoping.

9. **Write the IDS.** An Information Delivery Specification states, in a form software can test, what this model must contain: every `IfcColumn` has a type; every `IfcPlate` belongs to a curtain wall; every element has a storey; every `IfcSpace` has a name and a number; **every element with geometry carries a `Farnsworth_Provenance` set with a valid confidence grade**. Write it once here, and every gate from now on is a button press instead of a checklist.

10. **Open the issue register properly.** Everything the clash check and the IDS run found becomes an issue with an owner and a date. From this stage keep it in **BCF** as well as CSV — a BCF issue carries the viewpoint, so "the window head clashes with the beam" arrives with the camera already pointing at it.

11. **Update the quantities and the cost.** Steel tonnage, glass area, travertine area and core linings now come out of the model — and because the glass is a curtain wall aggregating plates, "how much glass" is a query rather than a measurement. Compare with the QS's estimate, and with Stage 02's order-of-magnitude figure. A three-way comparison finds errors that a two-way one hides, and this is the project where the cost got away.

12. **Freeze and export.** Fix the issues that are real, record the ones that are deferred with a reason, run the IDS again, and export `export/FARN-A-DD-P04-<date>.ifc`.

<div class="warn" markdown="1">
#### Turn Describe off now

From this stage on, the model is a record other people rely on. An unreviewed edit — from any
source, including a natural-language one — is exactly what a documentation model cannot absorb. If
you have been using [Describe]({{ '/setup/' | relative_url }}), stop here. Every change from now on should be one you can
name, justify and point at in a register.
</div>

## Deliverables

| Item | File |
| --- | --- |
| Coordinated DD model | `export/FARN-A-DD-P04-<date>.ifc` |
| Type and element schedule | every type, its layers, its total thickness, its count |
| Junction studies | column/slab weld, mullion/column, roof drainage through the core, stair threshold |
| Room finish assumptions | per space, aligned to the outline specification |
| Clash report | what was found, what was fixed, what was accepted |
| `farnsworth.ids` | the ruleset, in the repository, versioned |
| Issue register | CSV and BCF, every item owned and dated |
| Quantity and cost update | model quantities against the QS estimate against the budget |

## The gate

<div class="gate" markdown="1">
{: .check}
- Every wall, slab and roof is typed, and every type has material layers that sum correctly.
- The setting-out reference face is decided, recorded, and consistently applied.
- Every opening is coordinated at head, sill, jamb and reveal, and hosted properly.
- The roof has a real edge condition and a drainage route.
- Wet areas and kitchen are modelled to coordination level.
- The approach from grade to floor is modelled at real riser and going dimensions, and checked against a current accessibility requirement.
- Every grade-C dimension has been corrected against the HABS drawings, or is recorded as still outstanding with a reason.
- A clash check has been run; every clash is fixed, or accepted in writing.
- The IDS runs clean, or every failure is a logged and accepted exception.
- Quantities agree with an independent estimate within a stated tolerance.
- No element floats, overlaps unintentionally, or depends on an unnamed placeholder.
</div>

## Where this goes wrong

**Layers added without moving anything.** Turning 200 mm nominal into 215 mm of real layers changes
the plan. If nothing moved, the layers are decoration.

**Openings cut as mesh holes.** They survive the viewport and die in the schedule: no mark, no host,
no quantity, no lintel. Bonsai's opening workflow exists for this reason.

**A clash check run once, at the end.** Run it after each substantial change. A clash found in the
same session that caused it costs minutes; the same clash found three weeks later has been built on.

**An IDS nobody runs.** A ruleset written and never executed is a document. Run it at every gate from
here to Stage 08.

**Fittings modelled as furniture catalogue.** You need clearances and connections, not a beautiful
tap. Detail spent here is detail not spent on the roof junction that will actually leak.

<div class="note" markdown="1">
#### Additional Service, if this were real

Providing architectural content for the client's marketing, interior design beyond the basic, Green
Mark scoring and submission, and — as always — **documentation arising from a design change** are
Additional Services here. The VAF also files *Integrated Digital Delivery (IDD, including VDC and
BIM)*, Design for Maintainability, Design for Safety and Design for Buildability under **beyond
compliance**: services a practice offers, not services a basic fee assumes.
</div>
