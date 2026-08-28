---
layout: default
stage_num: "08"
title: Post Completion
strap: Latent defects, statutory completion, the final account — and the only stage that improves the next project.
exit_state: A closed contract, an archived model, and a written account of what the model could and could not answer
permalink: /stages/post-completion/
---

The shortest stage, the one most often unpaid, and the only one that changes how you work next time.
It is also where the model's real value is finally testable: over the defects liability period,
somebody asks the model a question it was never explicitly built to answer, and either it answers or
it does not.

<div class="sia" markdown="1">
#### What the SIA scope expects of you here

- **Designer** — no basic design service. The design work is done.
- **Qualified Person** — obtain the clearances required for statutory completion from the relevant authorities.
- **Contract Administrator** — address latent defects and minor outstanding works; work with the QS to conclude the final account and the building contract.
- **Design Manager** — no basic service.

The VAF's *Post Completion* gateway lists the clearances that end a project in Singapore: amendment
BP plans and CSC, Green Mark verification, the Fire Safety Certificate, completion of landscape and
roadside planting, road and parking clearances, drainage and environmental health clearances. Its
contract sheet closes with *Closure of Contract*: final accounts, variation orders, extensions of
time, dispute resolution, defects completion. And under Compliance & Liabilities, one line with no
end date — **Duty of Care (Lifetime)**: the architect's liability under common law.
</div>

## What you will learn

- Running a defects liability period against a model rather than a memory.
- Reconciling a final account with model quantities and the variation record.
- Archiving so the model is openable in ten years by someone who has never met you.
- Post-occupancy evaluation, and where the model's predictions were wrong.
- Extracting the lessons that change the *next* project's Stage 01.

## Before you start

Stage 07's gate is passed, the building is occupied, and the defects liability period has begun.

## Build it

*Step-by-step detail for every operation below is in the [modelling recipes]({{ '/modelling/' | relative_url }}); the data each one has to carry is in [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}).*

{: .steps}
1. **Open the defects register against the model.** Every reported defect gets an element reference, a date, a responsible party and a target. BCF viewpoints are worth their setup cost here: a defect reported by an occupant, located on an element, is findable a year later by someone who was not there.

2. **Track rectification in the model.** When a defect is fixed, update the element's status and date. Do not change geometry unless the rectification changed it — and if it did, that is another verified as-built update, with the same provenance rules as Stage 07.

3. **Complete the statutory clearances.** Work through the list that applies to your project: amendment plans where the as-built differs from the approved, record plans, the fire safety certificate, landscape completion, and the final completion certificate. Each one is a question about whether the record matches reality — which is exactly the question the last two stages have been preparing you to answer quickly.

4. **Reconcile the final account.** Contract sum, plus instructed variations, plus or minus remeasurement, less liquidated damages if any, less retention released. Check it against your own variation record and against model quantities. Where the contractor's figure and yours differ, the difference should be one you can name, element by element.

5. **Close the contract.** Final certificate, retention release, and a note of anything unresolved and how it is being handled. Then stop touching the model.

6. **Do a post-occupancy evaluation.** Go back after the first hot month. Does the courtyard work at 3pm? Is the cross-ventilation real or theoretical? Did the accessible route survive contact with furniture? Compare against the four success criteria from the [brief]({{ '/brief/' | relative_url }}), and write down which predictions were wrong and by how much.

   This is an **Additional Service** under the SIA matrix, along with building performance studies and gap analysis. It is also the only feedback loop the profession has.

7. **Archive properly.** One folder, self-describing, with:

   - every gate export from `P01` to `AB01`, unmodified;
   - the working `.blend`, and a note of the exact Blender, Bonsai and Sketch Mode versions it needs;
   - all three registers, plus the asset register, as CSV;
   - the drawing sets as PDF, per issue;
   - the IDS file;
   - a `README.md` explaining what everything is and in what order it happened;
   - a manifest with file names, dates, revisions and checksums.

   The version note is not bureaucracy: this model was authored in software that moves quickly, and in five years the `.blend` may need an older Blender to open cleanly. The IFC will not.

8. **Write the retrospective.** One page. Three questions, answered honestly:

   - **What did the model answer** that a set of drawings could not have?
   - **What could it not answer**, and what would it have cost — in hours, in the right stage — to make it able to?
   - **Which decision was hardest to reconstruct**, and what would have made it easy?

   Then carry the answers into Stage 01 of your next project, which is the only place they can be acted on.

## Deliverables

| Item | File |
| --- | --- |
| Defects register | closed out, with dates and responsible parties |
| Statutory completion record | clearances obtained, with dates |
| Final account reconciliation | contract sum to final sum, variation by variation |
| Post-occupancy evaluation | against the four success criteria |
| Archive | complete, manifested, checksummed |
| Retrospective | one page, three questions |

## The gate

<div class="gate" markdown="1">
{: .check}
- Every defect is closed, or open with a named owner and a date.
- The final account reconciles to the variation record, element by element where it differs.
- Statutory completion clearances are obtained and recorded.
- The archive opens on a clean machine, and the README explains it without you present.
- Every gate export from `P01` to `AB01` exists and is unmodified.
- The post-occupancy evaluation names at least one prediction that was wrong.
- The retrospective exists, and at least one lesson is written as a change to how you will run Stage 01 next time.
</div>

## Where this goes wrong

**Stopping at handover.** The clearances, the final account and the defects period are all after
handover, and all of them ask the model questions. A model abandoned at Completion answers none of
them.

**A final account reconciled at summary level.** "Roughly right" is how a five-figure difference
survives. The model exists precisely so that the comparison can be made element by element.

**An archive nobody can open.** No version note, no README, no manifest, and a `.blend` that needs
software nobody records. The IFC is the durable artefact; treat the rest as convenience copies.

**No retrospective.** Then the next project starts from the same Stage 01 as this one, and the whole
exercise was a modelling course rather than a practice change.

## You have finished

Eight stages, one house, one model, and a set of registers that can answer what was decided, when,
by whom, on what evidence, and what it cost.

The geometry was never the hard part. Look back at what actually took the time: naming, status,
provenance, revision control, and the discipline of not deleting the option you rejected. Those
transfer to every project you will ever run, in any software.

If something here was wrong, unclear, or is now out of date, the fix belongs in the open:
[integration-innovation/bonsaiupskilling](https://github.com/integration-innovation/bonsaiupskilling).
