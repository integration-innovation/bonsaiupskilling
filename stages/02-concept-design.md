---
layout: default
stage_num: "02"
title: Concept Design
strap: Two or three massings that answer the brief in genuinely different ways, compared honestly and decided once.
exit_state: One approved massing, one superseded option kept, areas and an order-of-magnitude cost
permalink: /stages/concept-design/
---

Concept Design is where Sketch Mode earns its existence. Everything you make here is plain mesh, made
fast, and most of it will be thrown away — which is only possible if none of it is IFC yet.

<div class="sia" markdown="1">
#### What the SIA scope expects of you here

- **Designer** — provide an initial design meeting the design brief in general; assist the client to refine the brief.
- **Qualified Person** — ensure the design complies with regulatory requirements; consult authorities on specific requirements where necessary; obtain land or building owner's consent if needed.
- **Contract Administrator** — advise on the selection of the form of building contract.
- **Design Manager** — track the design process; assist the client in appointing the consultant team; prepare project plans, responsibility matrices and execution plans; assist the QS to develop a preliminary cost estimate; update the project programme.

The VAF calls this the *Concept–Schematic* band, and lists the components plainly: budget estimation
with the QS, timeline estimation including what counts as a delay, site analysis for feasibility,
design development up to **design sign-off**, and coordination across the client's own departments,
the other consultants, the stakeholders and the public.
</div>

## What you will learn

- Rectangle and Push/Pull as a design instrument: massing at the speed of thinking.
- <span class="k">Ctrl</span>-stacking to add volumes, and double-click to repeat a distance.
- Push/Pull inference — landing a face level with something that already exists, rather than typing a number you guessed.
- Keeping options as objects, comparing them with numbers, and superseding rather than deleting.
- Reading area out of geometry, and why an area you measured beats an area you intended.

## Before you start

Stage 01's gate is passed: site, north, datum, envelope, controls, budget, brief. Open
`bungalow.blend` and hide nothing — the envelope must be visible while you work, or it is not
constraining anything.

## Build it

*Step-by-step detail for every operation below is in the [modelling recipes]({{ '/modelling/' | relative_url }}); the data each one has to carry is in [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}).*

{: .steps}
1. **Make a working collection per option.** `A-Massing-OptionA`, `A-Massing-OptionB`. Two options minimum; three if the brief pulls in genuinely different directions, which this one does — a courtyard, a linear plan and an L both answer it.

2. **Option A — the compact block.** Press <span class="k">R</span>, draw the 12 × 10 footprint inside the envelope. Press <span class="k">P</span>, hover the face, drag up and type `3` <span class="k">Enter</span>. That is the house in twenty seconds, which is the correct amount of time to spend on a first idea.

3. **Add the covered entry by stacking.** Hover the face where the porch belongs, hold <span class="k">Ctrl</span> as the push begins, and drag. A new solid grows on the face and the original stays put as the join between them. Type the projection you want. Double-click another face to repeat the same distance — useful for a symmetrical pair.

4. **Cut the courtyard with a regional push.** Draw the courtyard outline on the roof face with <span class="k">L</span>, which divides that face into regions. Press <span class="k">P</span>, hover the courtyard region and push *down*. Only that region moves; walls form along the lines dividing it from the rest. A courtyard is now a line and a drag.

5. **Option B — the L around a court.** Build it independently, in its own collection, from the same footprint area. Resist copying Option A and nudging it: two options that differ by 300 mm are one option and a distraction.

6. **Use inference rather than arithmetic.** When you push the porch roof, drag until the header reads `(aligned)` against the main roof line instead of typing a number. Sketch Mode reads every visible mesh once as the push begins and offers the distances that bring the face level with something. Typing a value overrides it; use the type-in when the dimension is a decision and the inference when it is a relationship.

7. **Study the roof as mass, not as construction.** A pitched roof at this stage is a stacked solid pushed to the ridge height, or a sheet pushed along its normal. It is a shape being tested for a shadow and a silhouette. Do not build rafters. There is no `IfcRoof` in this stage, and that is deliberate.

8. **Measure what you made.** Press <span class="k">T</span> and check the dimensions you believe are true. Then write down, per option: footprint area, GFA, courtyard area, covered outdoor area, and the number of rooms that get cross-ventilation. Numbers you measured, not numbers you intended.

9. **Test each option against the envelope and the four success criteria.** Cool without machines; loud and quiet separated; no steps where they matter; priceable. Score each option out of the four in one line each. If both options score the same, one of them is not a real alternative.

10. **Get an order-of-magnitude cost.** Area × a rate you can defend, or the QS's preliminary estimate if you have one. Compare it to Stage 01's budget. If it is 40% over, that is a Concept Design finding and the brief needs refining — which the SIA scope explicitly makes part of this stage.

11. **Decide, and supersede.** Adopt one option. Rename the loser `Z-Massing-OptionA`, set `design_status = superseded`, move it to a hidden collection, and log both the decision and the reason. Deleting it destroys the only evidence that the choice was considered.

12. **Export the concept baseline.** `export/BUNG-A-CON-P02-<date>.ifc`, one comparison sheet with both options side by side and the numbers under them, and the decision log rows.

<div class="note" markdown="1">
#### Optional · let Describe make the variant

If you have configured [Describe]({{ '/setup/' | relative_url }}), a sentence like *"a 12 by 10 metre single-storey block,
3 metres high, with a 4 by 4 courtyard"* generates a starting point in seconds — real parametric
walls, not a mesh box called a wall. Useful for a third option you would not otherwise have had time
to draw.

It edits the live model with no proposal step. Know what you asked for, check what you got, and
remember <span class="k">Ctrl</span>+<span class="k">Z</span>. From Stage 04 the course asks you to
stop using it.
</div>

## Deliverables

| Item | File |
| --- | --- |
| Massing model with both options | `bungalow.blend`, `export/BUNG-A-CON-P02-<date>.ifc` |
| Option comparison | `02-concept/options.pdf` — plan, 3D and numbers per option |
| Area summary | footprint, GFA, courtyard, covered outdoor, per option |
| Preliminary cost check | `02-concept/cost-check.md`, against the Stage 01 budget |
| Refined brief | any change the client agreed as a result of seeing the options |
| Decision log | option adopted, option superseded, reasons, and any brief change |

## The gate

<div class="gate" markdown="1">
{: .check}
- Two or more genuinely different options exist, each buildable inside the envelope.
- Each option has measured areas, not estimated ones.
- Each option has been scored against the four success criteria in writing.
- One option is adopted; the others are `Z-` named, `superseded`, and still in the file.
- An order-of-magnitude cost has been compared to the Stage 01 budget, and the variance is explained.
- Nothing is classified as IFC except the site. Not one wall.
- The entrance, the outdoor room and the accessible route are identifiable in the adopted mass.
</div>

## Where this goes wrong

**One option, developed.** If you build one massing and refine it, you have not done Concept Design;
you have done Schematic Design badly. The comparison is the deliverable.

**Options that differ cosmetically.** Two boxes with different window positions are not options.
Options differ in organisation: where the court is, where the entrance is, what faces the sun.

**Classifying early to feel productive.** Assigning `IfcWall` here makes the model heavier, makes
Push/Pull refuse to work — correctly — and makes you attached to geometry you should be discarding.

**Deleting the loser.** Six weeks later the client asks "did we ever look at an L?" and the only
answer that helps is one you can show.

<div class="note" markdown="1">
#### Additional Service, if this were real

Artist's impressions, walk-throughs and VR, reviewing work by a previous designer, an Outline
Application to URA, consulting authorities not previously in scope, and **design change** — any
change following the client's acceptance of the design, or forced by a new authority requirement or
by site conditions — are **Additional Services** at Concept Design.

That last one is worth internalising early. The change events scripted into Stages 03, 06 and 07 of
this course are, in a real appointment, chargeable.
</div>
