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
`farnsworth.blend` and hide nothing — the envelope must be visible while you work, or it is not
constraining anything.

## Build it

*Step-by-step detail for every operation below is in the [modelling recipes]({{ '/modelling/' | relative_url }}); the data each one has to carry is in [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}).*

{: .steps}
1. **Make a working collection per option.** `A-Massing-OptionA`, `A-Massing-OptionB`. Two options minimum. The brief has one binding requirement — a one-room house lifted clear of a floodplain — and at least two honest answers to it: a single pavilion held above grade on a frame, and a house on a raised podium or berm. Build both. You know which one Mies chose; you do not yet know why it was better, and Concept Design is where you earn that.

2. **Option A — the pavilion, in five moves.** Press <span class="k">R</span>, draw the 77'-0" × 28'-0" footprint. Press <span class="k">P</span>, hover the face, drag up and type the 15" structural depth. Duplicate it to 16'-0" for the roof plane. Add eight columns as 8" squares on the bay lines. Push the glazed enclosure up between the planes, stopping 22'-0" short of the west end. That is the house in about five minutes, which is the correct amount of time to spend on a first idea.

   `exercises/01-massing/build_massing.py` builds exactly this if you would rather spend the session on the comparison than on the geometry.

3. **Add the terrace by stacking.** Hover the face where the terrace belongs, hold <span class="k">Ctrl</span> as the push begins, and drag. A new solid grows on the face and the original stays put as the join between them. Type `2'-0"` as its height above grade. Double-click another face to repeat the same distance — useful for the two flights that connect grade, terrace and porch.

4. **Cut the porch with a regional push.** Draw the glass line across the floor plane with <span class="k">L</span> at 22'-0" from the west end, which divides that face into regions. Press <span class="k">P</span>, hover the enclosed region and push *up* to 9'-6". Only that region moves; the western region stays open under the same roof. The porch is now a line and a drag — and moving that one line is the whole argument about how much of this building is inside.

5. **Place the core in both options.** Not as a detail — as a fixed volume, 20'-0" × 8'-0", carrying the kitchen, two bathrooms, the mechanical space and the fireplace. It is the only thing in the building that touches both planes and is not glass, and everything else in the plan is defined by where it sits. Put it asymmetrically and say why.

   An option that has not decided where its services go has not decided anything: it is the one volume whose position you cannot revise later without redesigning the house around it.

6. **Option B — the raised podium.** Build it independently, in its own collection, from the same enclosed area and the same flood clearance. Resist copying Option A and nudging it: two options that differ by 300 mm are one option and a distraction. Option B will cost less and look heavier; the comparison is the point.

7. **Use inference rather than arithmetic.** When you push the roof plane, drag until the header reads `(aligned)` against the column tops instead of typing a number. Sketch Mode reads every visible mesh once as the push begins and offers the distances that bring the face level with something. Typing a value overrides it; use the type-in when the dimension is a decision and the inference when it is a relationship.

   On this building the distinction is unusually sharp. `22'-0"` is a decision. The roof meeting the top of the columns at 16'-0" is a relationship, and if you type it you will eventually type it wrong.

8. **Study the planes as mass, not as construction.** The roof at this stage is a solid 15" thick, pushed to 16'-0". It is a shape being tested for a shadow, a soffit and a silhouette. Do not build joists or channels. There is no `IfcSlab` in this stage, and that is deliberate.

9. **Measure what you made.** Press <span class="k">T</span> and check the dimensions you believe are true — starting with whether the plan closes: three bays of 22'-0" plus two 5'-6" cantilevers must be 77'-0" exactly. Then write down, per option: enclosed area, covered external area, terrace area, glazed area, and the clearance from finished floor to the flood elevation you recorded at Stage 01. Numbers you measured, not numbers you intended.

10. **Test each option against the flood plane and the four success criteria.** Priced before committed; dry; habitable; the module holds. Score each option out of the four in one line each. If both options score the same, one of them is not a real alternative.

11. **Get an order-of-magnitude cost.** Area × a rate you can defend, or the QS's preliminary estimate if you have one. Compare it to Stage 01's budget. If it is 40% over, that is a Concept Design finding and the brief needs refining — which the SIA scope explicitly makes part of this stage.

   Note what the frame does to the rate. An exposed, welded, ground-and-filled steel structure with no tolerance for a bad weld is not a normal residential rate, and pretending otherwise at Stage 02 is how a project arrives at Stage 05 thirty per cent over.

12. **Decide, and supersede.** Adopt one option. Rename the loser `Z-Massing-OptionA`, set `design_status = superseded`, move it to a hidden collection, and log both the decision and the reason. Deleting it destroys the only evidence that the choice was considered.

13. **Export the concept baseline.** `export/FARN-A-CON-P02-<date>.ifc`, one comparison sheet with both options side by side and the numbers under them, and the decision log rows.

<div class="note" markdown="1">
#### Optional · let Describe make the variant

If you have configured [Describe]({{ '/setup/' | relative_url }}), a sentence like *"a single-storey
glazed pavilion 23.5 by 8.5 metres, 2.9 metres floor to ceiling, raised 1.6 metres on eight
columns"* generates a starting point in seconds — real parametric elements, not a mesh box called a
wall. Useful for a third option you would not otherwise have had time to draw.

Note that you have just had to translate the building into metric to ask for it, and that the
numbers stopped closing when you did. That is worth noticing rather than working around.

It edits the live model with no proposal step. Know what you asked for, check what you got, and
remember <span class="k">Ctrl</span>+<span class="k">Z</span>. From Stage 04 the course asks you to
stop using it.
</div>

## Deliverables

| Item | File |
| --- | --- |
| Massing model with both options | `farnsworth.blend`, `export/FARN-A-CON-P02-<date>.ifc` |
| Option comparison | `02-concept/options.pdf` — plan, 3D and numbers per option |
| Area summary | enclosed, covered external, terrace, glazed, per option |
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
- The entrance, the porch, the terrace and the approach from grade are identifiable in the adopted mass.
- The core is placed in every option, at 20'-0" × 8'-0", with its position argued rather than centred by default.
- The plan closes: 3 × 22'-0" plus two 5'-6" cantilevers is 77'-0" exactly, measured in the model and not assumed.
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
