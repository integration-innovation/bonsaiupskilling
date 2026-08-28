---
layout: default
title: The brief
strap: A courtyard bungalow for a family of four, on a fictional plot, with a real client's habits.
permalink: /brief/
---

Everything in this section is fictional and deliberately small. It is sized so that the *modelling*
never becomes the hard part — the hard part is keeping the information honest across eight stages.

## The client

Mr and Mrs Tan, both in their forties, two children aged 9 and 13, and one grandparent who visits
for weeks at a time and cannot manage stairs. They have owned the plot for two years. They have
never built anything before and have opinions about kitchens.

What they say they want, in their words:

> "Single storey if possible. Cross-ventilated — we don't want to live in air-conditioning. A place
> outside that is usable at 3pm. Somewhere the kids can be loud that isn't the living room. And we
> want to know what it costs before we're committed."

What they have not said, and you will have to establish in Stage 01: the budget, the programme,
who makes decisions when they disagree, and whether "single storey" is a requirement or a
preference.

## The site

A **20 m × 30 m (600 m²)** rectangular plot in a landed-housing estate, level to within 300 mm,
with a 6 m public road along one short edge. Neighbours on both long edges, an open drain reserve
along the rear boundary. Mature trees near the rear corner.

<div class="warn" markdown="1">
#### The site is fictional; the controls are not

This course does **not** hand you plot ratio, setbacks, height control, site coverage or greenery
provision, because inventing them would teach you to trust invented numbers. In Stage 01 you will
go and find the real ones — from [URA](https://www.ura.gov.sg/), [BCA](https://www1.bca.gov.sg/),
[PUB](https://www.pub.gov.sg/), [NParks](https://www.nparks.gov.sg/) and
[SCDF](https://www.scdf.gov.sg/) — for a landed-housing plot of your choosing, and record them in
your own control sheet.

If you are outside Singapore, do exactly the same with your own jurisdiction's controls. The
exercise is *finding and recording the binding constraints before designing*, which is what
Pre-Design is.
</div>

## The requirement

| | |
| --- | --- |
| Gross floor area target | approximately **120 m²** |
| Main footprint target | **12 m × 10 m** |
| Finished floor level | **+0.15 m** above site datum (revisit against flood/platform levels in Stage 01) |
| Storey height | **3.00 m** floor to ceiling |
| External wall | **200 mm** target thickness |
| Internal partition | **100 mm** target thickness |
| Roof | simple pitched, **25°–30°** |
| Orientation | main entrance faces the north arrow you set — record the assumption |

**Programme:** 3 bedrooms · 2 bathrooms · kitchen · living/dining · utility · covered entry · one
shaded outdoor room or small courtyard.

**Accessibility:** the grandparent's bedroom and one bathroom must be reachable without a step, from
the car to the bed.

## Success criteria

The client will judge the finished house on four things. Write them at the top of your decision log
and test every option against them.

1. **Cool without machines.** Cross-ventilation through every habitable room; the outdoor room is usable in the afternoon.
2. **Loud and quiet can coexist.** The children's zone and the living room are not the same acoustic space.
3. **No steps where they matter.** Car to bed, and bed to bathroom, are level.
4. **Priced before committed.** The tender at Stage 05 is within the budget agreed at Stage 01, or the variance is explained and was foreseen.

## What you will not be given

Real projects fail in the gaps, so this brief has some on purpose:

- **No budget figure.** You establish one in Stage 01 and carry it as a project constraint.
- **No survey.** You decide what survey information you would need, list it, and record what you assumed instead.
- **No consultant team.** In Stage 01 you decide which consultants this project actually needs — and, crucially, which services are *not* in an architect's basic scope and therefore have to be procured by someone.
- **No sample drawings.** The drawing set at Stage 05 is one you specify, not one you copy.

## Deliberate change events

The course is not a straight line. Three changes are scripted in, because a model that has never
been changed proves nothing:

| Stage | Event |
| --- | --- |
| **03 · Schematic** | The client asks for a study/home-office at the last minute. It has to fit without growing the footprint |
| **06 · Construction** | The contractor reports the rear drain reserve is wider on site than assumed. The rear setback moves |
| **07 · Completion** | Survey finds one opening built 150 mm off. You decide whether it is a defect or an as-built condition |

Each one has to land in the model, the register and the drawings *without* destroying what was
approved before it. That is the actual skill.

## Model rules

Full detail on the [model standard]({{ '/standards/' | relative_url }}) page. In short:

- Name objects by discipline and role: `A-Site`, `A-Massing`, `A-Walls`, `A-Slabs`, `A-Roof`, `A-Openings`, `A-Fixtures`, `A-Annotations`.
- Use plain Sketch geometry for exploration. Assign IFC classes only when a decision is stable.
- Once something is IFC, use Bonsai's native tools for it — walls, slabs, doors, windows, openings, types and spatial structure. Push/Pull will refuse it, correctly.
- Never delete a superseded option. Mark it superseded and move it out of the way.

## The decision log

Every stage adds rows. One row per decision, and a decision without a reason is not a decision:

| Date | Author | Decision | Reason | Affects | Status |
| --- | --- | --- | --- | --- | --- |
| 2026-08-28 | AT | North arrow set to +Y | Road frontage is south; entrance faces road | `A-Site`, all plans | approved |

Status is one of **provisional**, **approved** or **superseded**. Nothing else.
