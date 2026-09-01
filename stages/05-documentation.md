---
layout: default
stage_num: "05"
title: Documentation
strap: Drawings, schedules, quantities and a specification that let a contractor price exactly what you intend to build.
exit_state: A frozen tender baseline, issued with a revision and a transmittal
permalink: /stages/documentation/
---

Everything before this was for you. Documentation is for someone else — a contractor who will read
your drawings adversarially, price them, and build precisely what is drawn rather than what you
meant. The test of this stage is not beauty. It is whether an unhelpful reader can find one
ambiguity to exploit.

<div class="sia" markdown="1">
#### What the SIA scope expects of you here

- **Designer** — prepare architectural tender drawings and specifications to a level of detail sufficient to enable pricing appropriate to the selected procurement method.
- **Qualified Person** — advise on the regulatory requirements to be included in the building contract.
- **Contract Administrator** — compile the tender documents; conduct the pricing/tender process; facilitate the award of the building contract; compile the contract documents.
- **Design Manager** — coordinate and communicate across the team.

The VAF's contract sheet is unusually specific about this stage's components: contractor qualifying
method (pre-qualification, invitation or open tender) and selection criteria (price first, quality
first, or PQM); contingency, provisional and prime cost sums; whether an advanced information
package is needed; the preliminaries; general and particular specifications; architectural
specifications; **drawings and the BIM model**; and the allocation of the contract sum — retention,
liquidated damages, performance bond.
</div>

## What you will learn

- Freezing a baseline, and what "frozen" has to mean to be worth anything.
- Generating plans, elevations, sections and details from the model rather than drawing them beside it.
- Door, window and finish schedules that are the model, not a spreadsheet that resembles it.
- Quantity take-off, and checking it against something independent.
- Revision control, transmittals, and recording an assumption instead of hiding it in geometry.

## Before you start

Stage 04's gate is passed, the IDS runs clean and the issue register has no open item that would
change a dimension. If anything is still moving, it is not ready to be priced.

## Build it

*Step-by-step detail for every operation below is in the [modelling recipes]({{ '/modelling/' | relative_url }}); the data each one has to carry is in [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}).*

{: .steps}
1. **Freeze the baseline.** Export `export/FARN-A-DD-P04-<date>.ifc` and treat it as immutable. Every change from now on is a change *to* the tender documents and gets a revision. This is a discipline, not a file permission — but a copy in `export/` makes it checkable.

2. **Decide the drawing list before drawing anything.** Site plan, floor plan, roof plan, four elevations, two sections, the column-to-slab weld detail, a mullion and glazing detail, the stair and threshold, and a core detail. Write the list, with a sheet number for each. A drawing set assembled by accident always has both gaps and duplicates.

3. **Set up sheets and drawings in Bonsai.** Bonsai generates plans, sections and elevations from the model and places them on sheets. Set your scales, title block and sheet numbers, then generate. Where the output is not what you want, fix the *model or the view*, not the exported drawing — a drawing edited after export is a drawing that will disagree with the model on its next issue.

4. **Dimension and annotate for construction, not for looks.** Setting-out dimensions from a stated datum and grid; levels at every floor, threshold and ridge; room names and numbers matching the space schedule; door and window marks matching the schedule; material tags matching the specification. Every annotation should be traceable to something in the model.

5. **Generate the schedules.** Door schedule, window schedule, room finish schedule, sanitary fittings. These come out of the types and marks you set in Stages 03 and 04 — which is the payoff for the naming discipline. If a mark appears in a schedule and not in a drawing, you have found a real error, and finding it now is the entire point.

6. **Take off the quantities.** Wall area by type, slab area, roof area, opening counts, finish areas. Then check them independently — by hand, on one wall and one room, at minimum. A model quantity you have never sanity-checked is a number with unearned authority.

7. **Write the specification.** Extend Stage 03's outline into a real specification: performance, materials, workmanship, standards, and what the contractor is responsible for designing. Cross-reference it to the drawings so that neither can be read alone.

8. **Record the assumptions.** Every place where you did not know something — the exact drain reserve width, the soil bearing capacity, the neighbour's boundary wall condition — gets an explicit note, in the drawings or the preliminaries. An assumption written down becomes a contractor's query; an assumption hidden in geometry becomes a variation.

9. **Decide what is priced how.** Which items are provisional sums, which are prime cost, what the contingency is, what is a nominated or designated sub-contract. This is Contract Administrator work and it changes the documents: a provisional sum item needs a different level of drawing than a fully specified one.

10. **Issue with a revision and a transmittal.** `export/FARN-A-TEN-T01-<date>.ifc`, the PDF set, the schedules, the specification. Record in `deliverables.csv` what was issued, when, at which revision, and to whom. A tender issue with no transmittal record cannot be defended later, and later is when it will be questioned.

11. **Run the tender process and record the answers.** Every tenderer's query and every answer goes in writing to every tenderer. Each answer that changes a document produces a new revision — `T02` — not an edited `T01`.

<div class="warn" markdown="1">
#### The rule that saves Stage 06

**A drawing is a view of the model, not a document beside it.** The moment a dimension is corrected
on a sheet rather than in the model, the set has two sources of truth and the model has quietly
become decoration. If a view will not produce what you need, that is a modelling problem wearing a
drawing costume.
</div>

## Deliverables

| Item | File |
| --- | --- |
| Tender model | `export/FARN-A-TEN-T01-<date>.ifc` |
| Drawing set | `05-documentation/FARN-TEN-T01.pdf`, every sheet numbered |
| Schedules | doors, windows, room finishes, sanitary |
| Quantity take-off | by element type, with the independent check shown |
| Specification | performance, materials, workmanship, standards |
| Assumption register | every unknown, stated explicitly |
| Revision and transmittal record | in `deliverables.csv` |
| Tender query log | queries, answers, and which revision each produced |

## The gate

<div class="gate" markdown="1">
{: .check}
- A contractor can identify **what** is being priced, **where** it occurs, **what type** it is, and **which revision** governs it.
- Every drawing was generated from the model; none was edited after export.
- Every schedule mark appears in at least one drawing, and every drawn mark appears in a schedule.
- Quantities have been checked independently on at least one element of each type.
- Every assumption is written somewhere a tenderer will read it.
- The IDS still runs clean on the tender model.
- The transmittal record shows what was issued, at what revision, when and to whom.
- Nothing in the issued model is named `X-`.
</div>

## Where this goes wrong

**Drawing over the model.** Faster today, and it destroys the only thing that makes the next three
stages tractable.

**Schedules typed by hand.** A hand-typed door schedule is correct on the day it is typed and never
again.

**Ambiguity left because it is obvious to you.** It is obvious to you because you designed it. The
contractor pricing it at 11pm has never seen the building.

**Revisions overwritten.** `T01` edited in place means nobody can say what was priced. The variance
arguments of Stage 06 are decided by whether `T01` still exists exactly as issued.

**Hidden cutters shipped.** Any `X-` object left in the issued model is an unexplained hole. Run the
name check before every issue.

<div class="note" markdown="1">
#### Additional Service, if this were real

Documentation resulting from a **design change**, artwork for site hoarding, and running the pricing
or tender process for nominated sub-contracts, the client's direct contracts, or early works
contracts are **Additional Services** at Documentation. On a project with several packages, the
last of those is not a small addition.
</div>
