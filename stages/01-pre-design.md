---
layout: default
stage_num: "01"
title: Pre-Design
strap: Before a line is drawn, establish what the client actually needs, what the site is, and which rules bind you.
exit_state: Site, datum, north and a recorded flood elevation — nothing designed yet
permalink: /stages/pre-design/
---

Pre-Design is the stage everyone skips and every project pays for. Nothing here is design. Everything
here is the set of constraints that will decide whether the design is any good, and the paper trail
that proves you established them before you started rather than after you were challenged.

<div class="sia" markdown="1">
#### What the SIA scope expects of you here

- **Designer** — assist the client in establishing the design brief; investigate the site to ascertain its conditions.
- **Qualified Person** — pre-design research on regulatory requirements; obtain previously approved drawings if they exist; consult authorities on general and site-specific requirements where necessary.
- **Contract Administrator** — advise on the appropriate procurement method.
- **Design Manager** — ascertain the client's budget and prepare a project budget; ascertain the timeline and prepare a project programme; advise which consultants are needed; establish communication protocols.

The VAF adds the components that consume real hours: brief preparation, consultant team
recommendations, consultant service agreements, communication protocol — and, under Compliance,
buying site information: topographical survey, site drawings, DIP, SIP, RLP and services plans.
</div>

## What you will learn

- Blender navigation and view control without touching Blender's own interface.
- Sketch Mode's Line and Tape tools, axis locks and typed dimensions.
- Regional Push/Pull, used to build a flood plane rather than a building.
- Creating an IFC project and an `IfcSite` in Bonsai, and why the site is the only thing classified at this stage.
- The habit that carries the rest of the course: record the constraint, then design inside it.

## Before you start

You need the [set-up]({{ '/setup/' | relative_url }}) working, the [brief]({{ '/brief/' | relative_url }}) read, the
[model standard]({{ '/standards/' | relative_url }}) adopted, and an empty project folder with three empty CSV registers
in it.

## Build it

*Step-by-step detail for every operation below is in the [modelling recipes]({{ '/modelling/' | relative_url }}); the data each one has to carry is in [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}).*

{: .steps}
1. **Open a new Blender file and go to the `Sketch` tab.** Delete the default cube if your startup file has one. Press <span class="k">N</span> to show the sidebar and confirm the `IFC` panel is there.

2. **Create the IFC project.** `IFC` panel → **New IFC Project**. Metric, millimetre precision. Name it `Edith Farnsworth House`. Everything else in the course is behind this gate — Bonsai's Wall, Slab, Door and Window tools all read `No IFC Project` until it exists.

3. **Draw the site boundary with Line.** Press <span class="k">L</span>, click the origin, then build a rectangle around the building footprint with axis locks and typed distances rather than by eye — say 60 × 40 m, generous enough to hold the house, the terrace and the approach. Press <span class="k">X</span>, type `60`, <span class="k">Enter</span>; <span class="k">Y</span>, `40`, <span class="k">Enter</span>; <span class="k">X</span>, `-60`, <span class="k">Enter</span>; then <span class="k">C</span> to close the loop back to the start. A closed coplanar loop becomes a face. Name it `A-Site-Boundary`.

   The real plot is larger and irregular. You are not surveying it; you are establishing a working extent you can put dimensions on.

4. **Set and record north.** Draw a single line from the site centre along +Y and name it `A-Site-North`. Then write the assumption into the decision log — *why* that direction: the road frontage, the sun path, the neighbour you are shading. An unrecorded north arrow invalidates every daylight and ventilation claim you make later.

5. **Find the real flood data.** Leave Blender. This site has one control that dominates every other: the Fox River. Find and write down the **base flood elevation** at or near 14520 River Road, Plano, Illinois, and the recorded flood history. Sources: the [FEMA Flood Map Service Center](https://msc.fema.gov/portal/home) for the effective flood map and BFE, and the [USGS National Water Information System](https://waterdata.usgs.gov/) for the Fox River gauge record. Record each with its source and the date you read it — flood maps are revised, and a parameter without a date is a rumour.

   Then write down the design's answer: **finished floor at 5'-3" above grade**. The gap between those two numbers is the single most important thing Pre-Design produces on this project, and it is a number, not an opinion.

   If you would rather work in your own jurisdiction, do exactly the same with your own flood authority's data and your own local controls. The exercise is finding and recording the binding constraint before designing.

6. **Build the flood envelope.** Draw a second rectangle *inside* the site face with <span class="k">L</span> and typed offsets. The site face is now divided into two regions. Press <span class="k">P</span>, hover the inner region and drag upward — only that region rises, walls appear along the dividing lines, and the outer strip stays flat. Type the **base flood elevation** you found in step 5 as an exact value. Name the result `X-FloodLevel`.

   This is the single most useful thing Pre-Design produces on this project: a horizontal plane the building has to clear. Every later stage tests against it — and at Stage 06 the river is forecast above it, which is a much more useful conversation when the plane is already in the model.

7. **Set the datum.** Establish the finished floor level relative to your site datum and check it against the flood elevation from step 5 — do not simply accept the brief's `5'-3"`, which is the answer the building gives and therefore the thing under test. If the flood data says 5'-3" is not enough, that is a Pre-Design finding, and it is much cheaper here than at Stage 04. Record it either way, with the margin in feet and inches.

8. **Classify the site — and only the site.** Select `A-Site-Boundary`, and in the `IFC` panel assign it as `IfcSite`. Leave `X-FloodLevel` as plain mesh: it is a constraint, not a thing being built. This is the first application of the rule that classification follows decision.

9. **Decide the team.** List the consultants this project needs and the ones it does not — C&S certainly, because the entire building is an exposed welded steel frame; M&E for the radiant floor and the core; QS if the client wants cost certainty, which on this project she very much does; a surveyor for the flood levels; an arborist for the black sugar maple. For each, note whether the service is inside an architect's basic scope or has to be separately procured. This is a five-minute exercise that clients routinely discover too late.

10. **Set the budget and the programme.** A single figure and a single bar chart. Both will be wrong; both must exist, because Stage 02's cost estimate and Stage 05's tender are measured against them — and on this project the budget is not a formality. The real one was agreed at about **$58,400** and the building came in near **$74,000**, which is where the relationship ended. Write your figure down now so that Stage 03 can challenge it.

11. **Export the baseline.** IFC out to `export/FARN-A-PRE-P01-<date>.ifc`, one screenshot of the site with the flood plane, and the decision log rows for north, datum, flood elevation and team.

## Deliverables

| Item | File |
| --- | --- |
| Site and flood-plane model | `farnsworth.blend`, `export/FARN-A-PRE-P01-<date>.ifc` |
| Control sheet | `00-brief/controls.md` — every parameter, its source, its date |
| Design brief | `00-brief/brief.md` — agreed with the client, including the four success criteria |
| Project budget and programme | `00-brief/budget.md`, `00-brief/programme.md` |
| Consultant and procurement note | `00-brief/team.md` |
| Decision log | first five to eight rows |

## The gate

<div class="gate" markdown="1">
Do not start Stage 02 until every line is true.

{: .check}
- One `IfcProject` and exactly one `IfcSite` exist, at the right size.
- North is set, drawn, and justified in writing.
- The flood plane is modelled from a recorded base flood elevation, with its source and the date you read it, and the margin to the proposed finished floor level is written down in feet and inches.
- The finished floor level has been tested against a platform or flood level, not assumed.
- The budget exists as a number and the programme as dates.
- The consultant list distinguishes basic scope from separately procured services.
- Nothing in the file is classified except the site.
</div>

## Where this goes wrong

**Designing during Pre-Design.** The moment a footprint appears, the constraints stop being
questions and start being justifications. If you have drawn a house by the end of this stage, you
have skipped the stage.

**Parameters without provenance.** "Setback is 3 m" is worthless. "Setback 3 m, URA landed housing
handbook, read 4 Sep 2026" can be re-checked by someone else — including you, in November, when
somebody disputes it.

**Classifying too early.** An `IfcBuilding` full of `IfcWall`s at Pre-Design feels productive and
guarantees you will be reluctant to throw it away at Stage 02, which is exactly when you should be
throwing things away.

**Treating the flood plane as settled.** It is a constraint the building must clear, and this
building clears it by a margin that has proved insufficient six times in sixty years. Recording the
number is Pre-Design; deciding what to do about it is not, and it is not your call alone.

<div class="note" markdown="1">
#### Additional Service, if this were real

Converting existing drawings to CAD/BIM, measured surveys of existing buildings, user or community
engagement, checking an existing building for compliance, and special or protracted negotiations
with authorities are all **Additional Services** at Pre-Design under the SIA matrix. If the client
asks for any of them, they belong in the fee, not in goodwill.
</div>
