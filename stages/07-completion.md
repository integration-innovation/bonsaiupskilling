---
layout: default
stage_num: "07"
title: Completion
strap: Inspect, reconcile with what was actually built, submit the as-built record, and hand over something the client can use.
exit_state: A verified as-built model with asset data, and a handover package that survives the software
permalink: /stages/completion/
---

Completion is where a model either becomes an asset or becomes a folder nobody opens again. The
difference is not detail. It is whether every statement in it is marked as **verified** or
**assumed**, and whether the client can find a thing, know what it is, and find its document.

<div class="sia" markdown="1">
#### What the SIA scope expects of you here

- **Designer** — inspect the site to check the completed works against the design intent.
- **Qualified Person** — submit architectural as-built drawings; arrange the required authority inspections; obtain the clearances required for occupancy; report to IRAS.
- **Contract Administrator** — issue the certification the contract requires; review as-builts, defects and outstanding works; facilitate site handover from contractor to client.
- **Design Manager** — manage the handover process.

The VAF is blunter about the work involved: *prepare as-built drawings, OMM and material card
sheets; conduct site walks and verification.* Its completion gateway lists a long column of
clearances — planning amendments, BCA record plans, as-built buildability and Green Mark scores,
façade and glazing declarations, accessibility, fire safety, sewerage and drainage, environmental
health, electrical, height declarations — most of which resolve into: *does the record match what
was built?*
</div>

## What you will learn

- Reconciling a model against a survey, and the discipline of changing only what was verified.
- Marking the provenance of every as-built statement.
- Attaching asset information — type, manufacturer, warranty, maintenance reference — where it can be found again.
- Deciding, on evidence, whether a deviation is a defect or an as-built condition.
- Packaging a handover that outlives the authoring tool.

## Before you start

Stage 06's gate is passed and the works are substantially complete. Take a survey or a measured
check to site with you; without measurements this stage is fiction with confident geometry.

## Build it

*Step-by-step detail for every operation below is in the [modelling recipes]({{ '/modelling/' | relative_url }}); the data each one has to carry is in [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}).*

{: .steps}
1. **Record the porch screens as a variation.** Dr Farnsworth had the west porch screened after the
   house was finished — an addition nobody drew at Design Development, made because the building as
   designed was unusable at dusk in an Illinois summer. Model it, and be strict about what kind of
   change it is: not a defect, not a design development, but a client-instructed variation arising
   from a performance shortfall. Log it with that reasoning. Half the arguments at completion are
   about which of those three words applies.

2. **Branch the as-built model.** From the last approved construction revision, to `export/FARN-A-AB-AB01-<date>.ifc`. The construction revisions stay exactly as they were — they are the record of what was instructed, which is a different question from what was built.

3. **Walk the building and record deviations.** Measure. Every difference between model and reality gets a row: element, drawing dimension, measured dimension, difference, and — crucially — **how you know**. Tape, laser, survey report or contractor's statement are four different levels of confidence and the register should say which.

4. **Judge the scripted deviation.** *One opening is 150 mm off its drawn position.* Is that a defect to be rectified, or an as-built condition to be accepted? Decide on evidence — does it breach a requirement, affect a clearance, or change anything the client cares about? — record the reasoning, and only then update the model or raise the defect. Deciding by feel here is how a defects list becomes a negotiation.

5. **Update only what was verified.** This is the rule that makes an as-built model worth having. If it was measured, change it. If it was assumed, leave it and mark the assumption. A model where the verified and the assumed are indistinguishable is worth less than no model, because it will be trusted.

6. **Mark the provenance.** Every element gets a property saying whether its as-built state is `verified`, `assumed` or `unchanged`. Three values. The client's facility manager, in four years, will care about nothing else.

7. **Attach the asset information.** For every maintainable item — sanitary fittings, kitchen appliances, the roof covering, the external doors and windows, any equipment — record type, manufacturer, model, installation date, warranty period and expiry, and a reference to the O&M document. Put it on the element as properties, not in a spreadsheet next to it.

8. **Check the spatial structure one last time.** Every element in a storey; every space named, numbered and measured against the as-built condition; every type still used; every opening still hosted. Run the IDS from Stage 04, plus any as-built rules you have added.

9. **Produce the as-built drawings and schedules.** Generated from the as-built model, marked as as-built, with a revision. Final space schedule with measured areas, final door and window schedules, final finish schedule.

10. **Assemble the handover package.** Not just the IFC:

   - the as-built IFC, and the drawing set as PDF;
   - the asset register as CSV, readable without any BIM software;
   - the O&M and warranty documents, indexed to the asset marks;
   - the deviation and verification record;
   - a **model information summary**: what the model contains, what it does not, what is verified, what is assumed, and what the client should not infer from it;
   - an archive manifest listing every file, its date, its revision and its checksum.

11. **Hand over and record it.** Date, recipient, contents, and the client's acknowledgement. A handover with no record is a handover that will happen again, from memory, in a worse mood.

<div class="warn" markdown="1">
#### As-built BIM is an Additional Service

Under the SIA matrix an **As-Built BIM model** is an *Additional Service* at Completion. Architectural
as-built *drawings* are a basic Qualified Person service; a maintained, data-carrying as-built
**model** is not.

If a client wants the model you are about to produce, it belongs in the agreement and in the fee.
This course builds one so that you know exactly what it costs in hours — and so you can say so with
a number.
</div>

## Deliverables

| Item | File |
| --- | --- |
| As-built model | `export/FARN-A-AB-AB01-<date>.ifc` |
| As-built drawings | `07-completion/FARN-AB-AB01.pdf` |
| Asset register | `registers/assets.csv` — mark, type, manufacturer, warranty, O&M reference |
| Deviation and verification record | measured against drawn, with the method of measurement |
| Final schedules | spaces, doors, windows, finishes |
| Model information summary | what is verified, what is assumed, what is absent |
| Handover checklist and archive manifest | with dates, revisions and checksums |
| Defects and outstanding works list | with responsibility and target dates |

## The gate

<div class="gate" markdown="1">
{: .check}
- Every as-built change traces to a measurement, with the measurement method recorded.
- Every element carries a verification status, and the three values mean what they say.
- Every maintainable asset has type, identity, warranty and an O&M reference on the element.
- The tender and construction revisions still exist, unmodified.
- The IDS runs clean on the as-built model.
- The client can locate an asset, identify it, and find its document, without opening Blender.
- The model information summary states plainly what should *not* be inferred from the model.
- The handover is recorded, with contents and acknowledgement.
</div>

## Where this goes wrong

**Editing the handover file directly.** Work on a copy, verify, then transfer. Exploratory edits in
the deliverable are how a hole appears with no explanation and no author.

**Tidying geometry that was not measured.** Nudging a wall to look right converts a record into a
drawing, silently.

**Asset data in a parallel spreadsheet.** It will be separated from the model within a year. If it is
not on the element, it is not handed over.

**Silent assumptions.** An as-built model that does not distinguish verified from assumed will be
trusted completely and be wrong in places, which is worse than a model that admits its gaps.

**Handing over only the IFC.** The client has no IFC viewer, no context and no index. CSV, PDF and a
one-page summary are what make the package usable on the day someone actually needs it.
