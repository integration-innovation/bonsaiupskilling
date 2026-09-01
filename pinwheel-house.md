---
layout: default
title: The Pinwheel House
strap: A Good Class Bungalow on a real Singapore plot — Wright's pinwheel, Mies's elevated steel and glass, and the household shelter at the pivot. Built at three stages.
permalink: /pinwheel-house/
---

This is the course's fullest worked example: a **Good Class Bungalow** carried from Concept Design
through Design Development to Completion, on a real Singapore plot, under real controls, with the
household shelter as the thing the whole plan turns about.

<div class="big-note" markdown="1">

### Download — one building, three stages

| Stage | File | What exists |
| --- | --- | --- |
| **02 · Concept** | **[GCB-A-CON-P02.ifc]({{ '/exercises/reference-model/GCB-A-CON-P02.ifc' | relative_url }})** | Masses, the shelter as a volume, spaces. No openings, no glazing |
| **04 · Design Development** | **[GCB-A-DD-P04.ifc]({{ '/exercises/reference-model/GCB-A-DD-P04.ifc' | relative_url }})** | Steel frame, glazed envelope, openings, quantities |
| **07 · Completion** | **[GCB-A-AB-AB01.ifc]({{ '/exercises/reference-model/GCB-A-AB-AB01.ifc' | relative_url }})** | As-built, with every element marked **verified** or **assumed** |

Built by **[build_gcb_house.py](https://github.com/integration-innovation/bonsaiupskilling/blob/main/exercises/reference-model/build_gcb_house.py)**,
checked by **[check_gcb_house.py](https://github.com/integration-innovation/bonsaiupskilling/blob/main/exercises/reference-model/check_gcb_house.py)** —
**1,093 checks** across all three.

```bash
python exercises/reference-model/build_gcb_house.py --all
python exercises/reference-model/check_gcb_house.py
```

</div>

## One model, three stages — which is the whole argument

The three files come from **one script**. Nothing is remodelled between stages; information is
added. That is the course's central claim made testable:

- At **Concept** the building is masses and spaces. There are no doors, no glazing and no
  classification of anything not yet decided — and the gate *enforces* that. A concept model with
  door schedules in it has skipped a decision.
- At **Design Development** the frame, envelope and openings arrive.
- At **Completion** nothing new is built, but every element gains a **verification** value:
  `verified`, `assumed` or `unchanged`. In this model 72 elements were measured and 64 were taken on
  the contractor's word, and the model says which is which. A model where the verified and the
  assumed are indistinguishable is worth less than no model, because it will be trusted.

## The site: a Good Class Bungalow plot

GCB is the strictest residential control in Singapore, which makes it a good teaching site — the
constraints are real, published, and generous enough that the design question stays architectural
rather than becoming a squeeze.

| Control | Requirement | This design |
| --- | --- | --- |
| Plot area | ≥ 1,400 m² | **1,600 m²** (40 × 40) |
| Plot width | ≥ 18.5 m | 40 m |
| Plot depth | ≥ 30 m | 40 m |
| Site coverage | ≤ 40% | **22.7%** |
| Height | 2 storeys + attic | 2 storeys |
| Setbacks | ≥ 3 m all sides | **9.5 m** all sides |
| Form | Detached, no subdivision | Detached |

Georeferenced near **Chatsworth Park, District 10** — one of the 39 gazetted GCB Areas — on
**EPSG:3414 (SVY21)** with **SHD** elevation and a 12° rotation to True North.

<div class="warn" markdown="1">
The coordinates are read off a map, and the controls are as this course reads them in 2026. Both are
a plausible example, not a survey and not a compliance opinion. Go and confirm them yourself, which
is what [Stage 01]({{ '/stages/pre-design/' | relative_url }}) is for.
</div>

## The concept: two masters, two royalty-free sources

Each idea is taken from a different architect, and each from a source that is genuinely free to
consult — which is the point, and was not easy to arrange. See
[which drawings you can actually use]({{ '/sources/' | relative_url }}) for how these two survived
the filter when almost nothing else did.

### Frank Lloyd Wright — organic planning, the pinwheel

**Source: the [Wasmuth Portfolio](https://archive.org/details/Wasmuth1911), Berlin 1910–11.** One
hundred lithographs of Wright's own drawings of work from 1893–1909, published over 95 years ago and
therefore public domain in the United States.

**What is taken:** the Prairie plan's habit of pinwheeling its wings about a solid central hearth,
so the plan *turns* rather than lines up; the horizontal emphasised by deep overhangs; and massing
that steps rather than sitting in one block.

### Mies van der Rohe — steel, glass, and the elevated floor plane

**Source: [HABS IL-1105](https://www.loc.gov/pictures/item/il0323/), the Farnsworth House.** Eight
measured drawings at the Library of Congress. Historic American Buildings Survey documentation is a
US Government work and is public domain.

**What is taken:** the floor plane lifted clear of the ground on a light steel frame, and an
envelope reduced to glass between structure.

<div class="big-note" markdown="1">

### Concept only — and that is what makes it free

**No drawing was traced, scanned, redrawn or adapted, and none is reproduced here.** What is
borrowed is *method*.

[17 U.S.C. §102(b)](https://www.law.cornell.edu/uscode/text/17/102) puts that beyond doubt:
copyright never extends to *"any idea, procedure, process, system, method of operation, concept,
principle, or discovery — regardless of the form in which it is described, explained, illustrated,
or embodied."*

Wright's drawings from 1910 are free by age; his later ones are not. Mies's own drawings are
protected until roughly 2040. **Neither matters here**, because ideas were never protected at all.
The building is an original design and this course owns it outright.

</div>

## Why the two ideas belong together

Wright pinwheels his plan about a **hearth**: a solid, founded masonry mass, the one thing in the
composition that cannot move.

Singapore requires a **household shelter**: 250 mm reinforced concrete for landed housing, founded,
structurally continuous to ground. SCDF's own term for it is an **"HS tower"**.

They are the same element. So the shelter takes the hearth's place at the pivot, and the four wings
turn about it.

Mies then answers the tropics. Lifting the floor plane **1.8 m** on a steel frame puts an open,
shaded, through-ventilated undercroft beneath the house — which is also, and not by coincidence,
what a Malay kampong house does. The glass sits well back under a **1.8 m** overhang, so the wall is
shaded by the roof rather than by the glass.

And then the good part: **the shelter is the only part of the building that touches the ground.**
Everything else stands on steel. A regulation usually hidden in a corner becomes the thing the house
is organised around *and stands on*.

## The plan

```text
                                    N
        9.6      13.2  16.8      24.0      27.6  31.2
         +--------------+----------+----------+          31.2
         |              |   Living / Bedroom 1 |
         |    Study     |         N WING       |          27.6
         +-----+--------+----+-----+-----------+
         |     |             |     |                      24.0
         |  W  |    CORE     |  Dining          |
         | WING|  +-------+  |   E WING         |
         |     |  |  HS   |  |                  |         19.2
         | Util|  | 1.5 x |  |  Kitchen         |
         |     |  |  3.2  |  |                  |         16.8
         +-----+--+-------+--+------------------+
               |   Guest  |  Family  |                    13.2
               |        S WING       |
               +---------------------+                     9.6

    HS = household shelter, founded, the only thing touching the ground.
    Four wings, each turned a quarter from the last. None aligns with another.
```

Two wings rise to a second storey; two stay single and become **roof terraces** — which is where the
stepped, horizontal massing comes from.

## The shelter, against SCDF 2023

| | Model | Requirement | |
| --- | --- | --- | --- |
| Internal width | **1500 mm** | ≥ 1200 mm | ✅ |
| Internal length | **3200 mm** | ≤ 4000 mm | ✅ |
| Internal area | **4.800 m²** | ≤ 4.8 m² | ✅ |
| Clear height | **2700 mm** | 2400–3900 mm | ✅ |
| Walls | 250 mm cast in-situ RC | 250 mm for landed | ✅ |
| Founded | z = 0.00 → 9.00 m, through both storeys | "HS tower" | ✅ |

## What the gate checks that a checklist would not

| Group | The check worth stealing |
| --- | --- |
| **GCB** | Setbacks and coverage are **measured from the geometry**, not read from an asserted figure. A coverage number typed into a form is not a check |
| **SHELTER** | The declared internal size must **multiply out** to the space's own `NetFloorArea`. A shelter whose data and geometry disagree is worse than one with no data, because a checker will believe the data |
| **SHELTER** | The shelter's walls must start at **z = 0**. Not at the floor plane the rest of the house stands on. This is the check that catches a shelter drawn as a room instead of built as a tower |
| **PINWHEEL** | The wings must not share face lines. A pinwheel that has drifted into a cross has lost the idea it was built on |
| **STAGE** | A Concept model containing doors **fails**. You cannot detail your way past a decision you have not made |

## What is in it

| | |
| --- | --- |
| Columns | 53 — square hollow steel, on a 3.6 m module |
| Slabs · Roof | 11 · 1, stepping with the massing, under a 1.8 m eave |
| Walls | 14 — the shelter tower, the core, and four partitions. Everything else is glass |
| Curtain walls · Plates | 42 · 42 (Design Development onward) |
| Doors | 7 |
| Spaces | 18 — 16 rooms and terraces, plus **two GFA spaces** |
| Storeys | `1st Storey` (+1800), `2nd Storey` (+5400), `Roof` (+9000) |
| Grid | A–G × 1–7 on the 3.6 m module |
| GFA (modelled) | 362.88 + 207.36 = **570.24 m²** |

## Two partis, one brief

The course now carries **two** Singapore houses, and that is deliberate — they are the
[Stage 02]({{ '/stages/concept-design/' | relative_url }}) option comparison made real. Same brief,
same regulations, two genuinely different answers:

| | [Servant and Served House]({{ '/servant-house/' | relative_url }}) | The Pinwheel House |
| --- | --- | --- |
| Parti | Kahn — linear, solid towers at the ends | Wright + Mies — rotating, elevated |
| Ground | Sits on the ground | Floats on steel; only the shelter lands |
| The shelter is | The base of a servant tower | The hearth at the pivot |
| Site | Generic landed plot | Good Class Bungalow, 1,600 m² |
| Stages | One (Schematic) | **Three** (Concept, DD, As-built) |

Neither is the right answer. That is what makes them worth comparing.

And [Farnsworth]({{ '/reference-model/' | relative_url }}) remains the third example, doing the one
thing neither of these can: teaching *measurement and provenance* against a real, documented,
surveyed building.
