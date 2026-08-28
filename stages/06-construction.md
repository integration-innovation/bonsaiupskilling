---
layout: default
stage_num: "06"
title: Construction
strap: Construction drawings, shop-drawing review, site inspection and contract administration — with the model as evidence.
exit_state: A controlled construction revision where every change has an instruction behind it
permalink: /stages/construction/
---

Two jobs run in parallel here and the SIA matrix keeps them apart on purpose: the **Designer** keeps
answering design questions, and the **Contract Administrator** runs the contract. The model serves
both, differently — and if it is not under change control by the end of the first week, it will be
serving neither by the end of the stage.

<div class="sia" markdown="1">
#### What the SIA scope expects of you here

- **Designer** — prepare architectural construction drawings; attend to construction issues relevant to the design; check the contractor's submissions against design intent; inspect the site against design intent.
- **Qualified Person** — ensure permits and clearances required before commencement are obtained; monitor the contractor's compliance with statutory requirements; inspect the site to check the works are carried out in accordance with the approved plans.
- **Contract Administrator** — administer the building contract, including issuing orders and certification; conduct site meetings; inspect that the works follow the building contract.
- **Design Manager** — monitor construction cost against the budget and progress against the programme.

The VAF splits this into *Contract Administration* (certification, assessment of variations, review
of project duration and EOT, directions and instructions) and *Site Inspection* (setting out, manpower
histogram, weekly and monthly reports, RFAs and RFIs, sub-contractors, mock-ups and factory visits,
regular inspections and meetings). Two different weeks of work, often on the same day.
</div>

## What you will learn

- Branching a construction revision from the tender baseline without losing either.
- Recording an approved change so that the original, the proposal and the approval all remain visible.
- Reviewing a shop drawing against design intent instead of against your own preference.
- Progress status held in the model, so that "what was built by 14 December" has an answer.
- Handling a site-driven change — the kind that arrives whether or not the design was finished.

## Before you start

Stage 05's gate is passed, `T01` exists exactly as issued, and the contract is awarded. From here,
**the tender baseline is never edited**. Everything happens on a construction revision.

## Build it

{: .steps}
1. **Branch the construction model.** Copy the tender baseline to `export/BUNG-A-CON-C01-<date>.ifc` and set `project_stage = 06 Construction` on the elements you touch. The tender model stays untouched forever: it is what was priced, and half of this stage's arguments are settled by pointing at it.

2. **Produce the construction drawings.** They differ from tender drawings in purpose — setting out, levels, junctions, sequences, and the details a builder needs at 7am — not in the model they come from. Same rule as Stage 05: generated from the model, never edited afterwards.

3. **Set up a status property for progress.** Foundation, envelope, roof, openings, finishes. Each element gets a state — `not started`, `in progress`, `complete` — and a date. Update it after each site visit. This is the difference between a model that shows the design and a model that answers *what existed on the day of the claim*.

4. **Review a shop drawing.** Take one element — the window assembly is the natural candidate — and review the contractor's submission against design intent. Not against how you would have detailed it: against what the contract documents require. Record the review, the comments and the outcome, and note where the shop drawing is *better* than your detail, because it usually is in at least one respect.

5. **Handle the site-driven change.** *The contractor reports the rear drain reserve is wider than assumed; the rear setback moves.* Work it in this order, and keep all three states:

   - **Original** — as issued in `T01`. Untouched.
   - **Proposed** — model it as `X-` study geometry first. Push/Pull still works on plain mesh, so test three positions in five minutes.
   - **Approved** — once instructed, apply it through Bonsai's parametric controls on the real elements, with an instruction reference, a date and a responsible party.

   Then ask the question that separates contract administration from modelling: *is this a variation?* It is a change necessitated by site conditions, which under the SIA definition is a design change. Assess it, price it, instruct it, record it.

6. **Answer RFIs against the model.** Every RFI gets a written answer, a date, and a note of whether it changed anything. An RFI that changed the design and did not produce a revision is a future dispute with a paper trail pointing at you.

7. **Certify against evidence, not impression.** When a payment claim arrives, compare the claimed quantity with the model quantity for the elements the claim covers, and with your recorded progress status. Where they differ, you now have a specific question to ask rather than a general unease.

8. **Keep the issue register alive.** Every site query, non-compliance, defect and deferred decision goes in with an owner and a date. BCF viewpoints make site issues far quicker to communicate than a paragraph and a photograph.

9. **Track cost and programme.** Every instructed variation adjusts the cost picture; every extension of time adjusts the programme. Update both after each instruction, not monthly — a monthly update is a reconstruction, and reconstructions are where errors live.

10. **Issue revisions properly.** `C02`, `C03` — each with a transmittal, each traceable to the instruction that caused it. Never edit `C01`.

<div class="warn" markdown="1">
#### The one rule of this stage

**No change without an instruction reference.** Not "the client asked on site", not "the contractor
suggested it and it was obviously right". Date, instruction, responsible party, affected elements —
in the register, before the model changes. A model that has drifted from the contract documents
cannot be used as evidence, and evidence is the only reason it is worth maintaining during
construction.
</div>

## Deliverables

| Item | File |
| --- | --- |
| Construction model revisions | `export/BUNG-A-CON-C01…Cn-<date>.ifc` |
| Construction drawing set | `06-construction/`, issued with transmittals |
| Shop-drawing review record | one worked example, with comments and outcome |
| Variation record | the approved change, with original / proposed / approved states |
| RFI log | query, answer, date, whether it changed anything |
| Progress record | element status and date, per site visit |
| Valuation check | claimed quantity against model quantity |
| Issue register | CSV and BCF, current |

## The gate

<div class="gate" markdown="1">
{: .check}
- The tender baseline is unmodified and still exports identically.
- Every difference between `T01` and the current construction revision traces to a numbered instruction.
- The site-driven change exists in three states, all still visible.
- At least one contractor submission has been reviewed against design intent, in writing.
- Progress status is current to the last site visit.
- One payment claim has been checked against model quantities.
- Every RFI has a dated answer and a note on whether it changed the documents.
- Cost and programme positions are current, not reconstructed.
</div>

## Where this goes wrong

**Editing the tender model.** Once it is gone, "what was priced" becomes a matter of opinion.

**Modelling the change before it is instructed.** The model then shows something nobody has approved,
and if the instruction never comes you have quietly built a discrepancy into the record.

**Progress tracked in a spreadsheet nobody reconciles.** If the status is not on the elements, the
model cannot answer questions about time, which is most of what construction disputes are about.

**Reviewing shop drawings as a design opportunity.** The question is whether the submission meets
the contract, not whether you would have done it differently. Redesigning at review is how a
programme slips and a variation arrives with your name on it.

**Letting the issue register lag.** An issue recorded a fortnight late has already been overtaken by
the works.

<div class="note" markdown="1">
#### Additional Service, if this were real

Revised or additional construction drawings resulting from a **design change**, protraction of the
construction period, providing architectural staff resident on site, coordinating the client's
direct contractors, administering non-standard contracts, and certification under the client's sale
and purchase agreement are **Additional Services** at Construction.

Protraction deserves a moment's thought: if the contract period doubles, contract administration
work roughly doubles, and a percentage fee on an unchanged contract sum does not.
</div>
