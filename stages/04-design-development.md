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
1. **Turn each type into a real build-up.** The 200 mm external wall becomes its layers — finish, blockwork, cavity or insulation, internal finish — each with a material and a thickness that sums to the nominal. Do the same for the partition, the ground slab and the roof. The type is the specification; get it right once and forty walls inherit it.

2. **Reconcile the layers with the geometry.** A wall that was 200 mm nominal and is now 215 mm of real layers has moved a face. Decide which face is the setting-out reference and hold it — the wall centre line, or the structural face — and record the decision. Every junction downstream depends on this one sentence.

3. **Coordinate every opening properly.** For each door and window: check the head against the beam zone, the sill against the finished floor, the jamb against the wall junction and the reveal against the external finish. Use Bonsai's void workflow — an `IfcOpeningElement` related to its host — never a mesh subtraction. There is no auto-subtract in Sketch Mode, and this is the stage where that constraint is doing you a favour.

4. **Develop the roof as construction.** Thickness, eaves overhang, gutter line, fascia, the junction where the roof meets the wall head, and where water goes when it leaves the gutter. This is the junction that most bungalow models get wrong, because in the massing it was a single surface.

5. **Model the wet areas and the kitchen at coordination level.** Not catalogue fittings — zones with real dimensions: the shower tray, the WC clearance, the basin run, the kitchen counter with its appliance gaps. Enough to prove the room works and to hang a finish schedule on. Classify as `IfcSanitaryTerminal` and `IfcFurniture`.

6. **Prove the accessible route.** The brief requires level access from car to bed and bed to bathroom. Model the thresholds, the door clear widths and the turning space. Then check them against the current accessibility requirements, not against a memory of them.

7. **Keep studying in Sketch, still on `X-` geometry.** Push/Pull still works on plain meshes and this is exactly what it is for at this stage: a temporary cutter to visualise a proposed niche, a step tested at three depths, a construction sequence tried out. Study freely, then build the answer parametrically and delete or explain the study.

8. **Run a clash check.** Architecture against your assumed structure; the roof against the wall heads; sanitary fittings against door swings; the beam zone against every window head. Bonsai has clash tooling built in — use it rather than rotating the model and hoping.

9. **Write the IDS.** An Information Delivery Specification states, in a form software can test, what this model must contain: every `IfcWall` has a type; every `IfcDoor` has a host and a mark; every element has a storey; every `IfcSpace` has a name and a number. Write it once here, and every gate from now on is a button press instead of a checklist.

10. **Open the issue register properly.** Everything the clash check and the IDS run found becomes an issue with an owner and a date. From this stage keep it in **BCF** as well as CSV — a BCF issue carries the viewpoint, so "the window head clashes with the beam" arrives with the camera already pointing at it.

11. **Update the quantities and the cost.** Wall, slab, roof and finish quantities now come out of the model. Compare with the QS's estimate, and with Stage 02's order-of-magnitude figure. A three-way comparison finds errors that a two-way one hides.

12. **Freeze and export.** Fix the issues that are real, record the ones that are deferred with a reason, run the IDS again, and export `export/BUNG-A-DD-P04-<date>.ifc`.

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
| Coordinated DD model | `export/BUNG-A-DD-P04-<date>.ifc` |
| Type and element schedule | every type, its layers, its total thickness, its count |
| Junction studies | roof/wall head, sill, threshold, courtyard edge |
| Room finish assumptions | per space, aligned to the outline specification |
| Clash report | what was found, what was fixed, what was accepted |
| `bungalow.ids` | the ruleset, in the repository, versioned |
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
- The accessible route is modelled and checked against a current requirement.
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
