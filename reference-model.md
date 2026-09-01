---
layout: default
title: The reference model
strap: Mies van der Rohe's Farnsworth House as IFC4 — every dimension carrying its source, and a 286-check gate you can run.
permalink: /reference-model/
---

The course rebuilds one documented masterwork through eight stages. This is that building,
modelled: a valid IFC4 file with a real steel frame, four curtain walls, a primavera core and
nine spaces, at the state the model should be in at the end of
[Stage 04 · Design Development]({{ '/stages/design-development/' | relative_url }}).

<div class="big-note" markdown="1">

### Download

**[FARN-A-DD-P01.ifc]({{ '/exercises/reference-model/FARN-A-DD-P01.ifc' | relative_url }})** — 117 KB, IFC4

Built by **[build_farnsworth.py](https://github.com/integration-innovation/bonsaiupskilling/blob/main/exercises/reference-model/build_farnsworth.py)**,
checked by **[check_farnsworth.py](https://github.com/integration-innovation/bonsaiupskilling/blob/main/exercises/reference-model/check_farnsworth.py)**.
Both run on IfcOpenShell 0.8.x, the same library Bonsai ships.

</div>

## The building

**Ludwig Mies van der Rohe, Edith Farnsworth House.** 14520 River Road, Plano, Kendall County,
Illinois. Designed 1945–47, built 1949–51. One room, eight columns, two horizontal planes and a
glass skin, standing 5'-3" clear of the Fox River floodplain.

It is here because it is the clearest teaching object in modern architecture. Nothing is buried in
a cavity. Every element you can see is a structural or spatial decision, and the whole building is
governed by one module — which means a modelling mistake shows up immediately as a dimension that
will not close.

## Why we can ship it

<div class="big-note" markdown="1">

This has **three different answers**, and collapsing them into one is how people get it wrong.

**1 · The building — free.** The US
[Architectural Works Copyright Protection Act](https://www.copyright.gov/circs/circ41.pdf) took
effect on **1 December 1990** and does not reach works constructed before that date. The house was
completed in 1951, so as *architecture* it carries no US copyright that a model of it could
infringe.

**2 · The HABS record — free, all of it.** The Historic American Buildings Survey documented the
house as **HABS IL-1105**: **8 measured drawings**, **32 photographs**, 54 data pages. Everything
transmitted to HABS is placed in the public domain as a condition of the transfer, and the Library
of Congress rights advisory reads *"no known restrictions on publication"*. That includes the
photographs — this is the one photographic source of the house you can use freely.

- [Survey record](https://www.loc.gov/pictures/item/il0323/)
- [The eight measured drawings](https://www.loc.gov/resource/hhh.il0323.sheet)

**3 · Mies's own drawings — not free, and the 1990 rule does not help.** Architectural drawings are
protected as *pictorial and graphic works* under
[17 U.S.C. §102(a)(5)](https://copyright.uslegal.com/enumerated-categories-of-copyrightable-works/architectural-plans-drawings-and-models/),
**separately from the building they describe**, and the AWCPA never removed that — the Second
Circuit has held that pre-1990 plans remain protected as pictorial works. The Farnsworth drawings
are in the [Mies van der Rohe Archive at MoMA](https://www.moma.org/collection/works/784) and their
copyright is administered by Artists Rights Society (ARS), New York / VG Bild-Kunst, Bonn.

So: **the building is free, the survey of it is free, the architect's drawings of it are not.**

</div>

<div class="warn" markdown="1">
#### Why this model is clear of all three

**Dimensions are facts.** Recording that a bay is 22'-0" and putting `22'-0"` in a table is not
copying a drawing. This model reproduces no drawing of any kind: it is built from published
dimensions, and every one of them is attributed.

That is also the rule for your own work on this course. Read the HABS drawings, take the
*dimensions* off them, and model from those. Do not trace a Mies drawing, and do not paste one into
your submission — including the redrawn plans and sections that circulate on architecture websites,
which are derivative works of exactly the drawings you may not copy.

Nothing here is legal advice. If you are publishing commercially, check it yourself.
</div>

## What is in it

| | |
| --- | --- |
| Columns | 8 — W8×48 wide flange, welded to the slab edges, grade to 16'-0" |
| Slabs | 3 — floor and roof planes at 15" structural depth, plus the lower terrace |
| Beams | 4 — 15" edge channels, the white band you read as the edge of each plane |
| Curtain walls | 4 — one per elevation, aggregating **19 glass plates** and **24 mullions** |
| Walls | 6 — the primavera core, and nothing else in the building |
| Coverings | 2 — the travertine, floor and terrace, carrying its module and piece count |
| Windows | **2** — the only operable openings in the entire house |
| Chimney | 1 — the flue, the only element that punctures the roof plane |
| Stairs · Door · Furniture | 2 · 1 · 1 |
| Spaces | 9 — seven internal zones, the west porch and the terrace |
| Storeys | `1st Storey_Terrace` (+610), `1st Storey` (+1600), `Roof` (+4877) |
| Grids | 2 — 1–4 / A–B on the column lines, and the travertine paving module |
| Extent | −38 to 77 ft east, −22 to 29 ft north, 0 to 18 ft up |
| Enclosed area | **1,517 sq ft** (140.9 m²) against a published figure of about 1,500 |
| Glass | **1,544 sq ft** (143.4 m²) of single-glazed plate, 9'-6" floor to ceiling |

## The plan

A 77'-0" × 28'-0" slab. The eastern 55'-0" is glazed; the western 22'-0" is an open porch under the
same roof. The core sits asymmetrically inside the glass, leaving a 12'-0" living band to the south
and an 8'-0" kitchen run to the north. There are no internal doors except the core's.

```text
                                         N
   x -33                     0        22           38        58      77
    +------------------------+--------+------------+---------+-------+  y 28
    |                        |        |            | Kitchen |       |
    |                        |  WEST  |   Dining   +---------+ Sleep |  y 20
    |                        |  PORCH |            |  CORE   |  ing  |
    |     (terrace below,    |        |            | Bw|U|Be |       |  y 12
    |      2'-0" above       |        +------------+---------+-------+
    |      grade)            |        |         Living               |
    +------------------------+--------+------------------------------+  y 0
    |                                 |
    |            TERRACE              |   55'-0" x 22'-0", one step down
    +---------------------------------+  y -22
                              x 22

    Bw  Bathroom W    U  Utility    Be  Bathroom E
```

## The travertine module, which turns out to be the building's module

The lower terrace is documented as 55'-0" × 22'-0" carrying **220 pieces** of travertine. Laid as a
regular grid, 220 factors into only four candidates — and three of them are absurd shapes
(11'-0" × 6", 5'-6" × 1'-0", 1'-0" × 5'-6"). The fourth is **20 × 11 pieces of 2'-9" × 2'-0"**.

Take that module back to the building and every principal dimension is a whole number of pavers:

| | |
| --- | --- |
| 77'-0" slab length | **28** pavers |
| 55'-0" glazed enclosure | **20** pavers |
| 22'-0" structural bay | **8** pavers |
| 5'-6" cantilever | **2** pavers |
| 28'-0" slab width | **14** pavers |
| 22'-0" terrace width | **11** pavers |

Six exact closures on a figure derived from a piece count is not proof, and the module is graded
**B** accordingly — but it is a great deal more than a guess, and the gate tests all six. The main
slab lays up in **392** pavers and the terrace in **220**, which is where the derivation started.

This is what "the whole building is governed by one module" means in practice. It is not a stylistic
observation; it is a stone size, and the steel was set out from it.

## The section, which is the point

Three dimensions from three different sources, and they close exactly:

```text
    5'-3"   floor slab above grade
  + 9'-6"   floor to ceiling  (the height of every pane of glass)
  + 1'-3"   15" edge channel at roof
  ---------
   16'-0"   top of roof
```

And the plan closes too: three bays of **22'-0"** with a **5'-6"** cantilever at each end is
**77'-0"**. Two independent closures on figures taken from unrelated sources is good evidence the
numbers are right — and it is the check the gate script runs first.

## Two windows, and why they matter

The house has exactly **two operable windows** — small bottom-hung hoppers in the east wall at the
sleeping end. With the west entrance doors open, they are the entire cross-ventilation strategy of a
fully-glazed, uninsulated, un-airconditioned building in an Illinois summer. There was also an
electric exhaust fan set into the kitchen floor.

Contemporaries reported that it was not enough, and Dr Farnsworth said so at the time.

They are modelled as real `IfcWindow` elements carrying a `Farnsworth_Ventilation` property set, and
the gate checks that there are exactly two and that both record their operation. That is deliberate:
it is very easy to model this house as an elegant glass box and never notice that you have modelled
a building nobody can open. **Habitable** is one of the [brief's]({{ '/brief/' | relative_url }})
four success criteria for exactly this reason.

## Every dimension carries its source

This is the model standard's *record the source and the date* rule applied to the model itself
rather than to a spreadsheet. Open any element in Bonsai and there is a `Farnsworth_Provenance`
property set on it:

| Property | Example |
| --- | --- |
| `dimension_source` | `Columbia GSAPP; Britannica; ArchEyes` |
| `confidence` | `A` |
| `note` | `77'-0" x 28'-0", 15" structural depth` |

Confidence is one of three grades, and nothing else:

| | | In the model |
| --- | --- | --- |
| **A** | Cross-checked, arithmetically self-consistent, agreed by most sources | 18 elements |
| **B** | Widely published, but sources differ; the alternatives are recorded | 7 elements |
| **C** | Derived by the author from A-grade figures and proportional logic — plausible, unverified | 15 elements |

<div class="warn" markdown="1">
#### This model is not a survey, and says so

The HABS measured drawings were **not reachable** from the machine that built this file, so every
dimension came from published secondary sources — and those sources contradict each other. The
build script records the contradictions in full. The headlines:

| | Used | Also published |
| --- | --- | --- |
| Slab width | 28'-0" | 29'-0" |
| Bay spacing | 22'-0" | 20'-0" — cannot close to 77'-0" with a credible cantilever |
| Terrace width | 22'-0" | 23'-0" |
| Core size | 20'-0" × 8'-0" | 10'-0" × 28'-0"; 32'-0" × 8'-0" |

Everything about the terrace's position relative to the house is **grade C**: it comes from
photographs and description, not from a plan. HABS sheet 3 settles it.

**This is an exercise, not a defect.** Correcting a grade-C figure against a measured drawing, and
watching the change propagate through the model and the schedules, is
[Stage 04]({{ '/stages/design-development/' | relative_url }}) doing exactly what Design Development
is for. The build script is parametric: every dimension lives in one `DIMS` table at the top, so a
correction is a one-line edit and a re-run.
</div>

## Running the gate

```bash
python exercises/reference-model/build_farnsworth.py
python exercises/reference-model/check_farnsworth.py
```

286 checks, in three groups that matter more than the rest, because they are the ones a
hand-modelled copy of this house usually fails:

| Group | What it proves |
| --- | --- |
| **CLOSURE** | The plan and section close exactly in feet. If yours does not, you rounded something. |
| **FRAME** | Eight columns, on the right lines, *outboard of the slab edge*. The moment a column passes through a slab, the building stops being the building. |
| **SOURCE** | Every element with geometry carries a source and a valid confidence grade. A dimension without a source is not a dimension. |

Point it at your own model to check your work:

```bash
python exercises/reference-model/check_farnsworth.py my-model.ifc
```

## The conventions it demonstrates

| Convention | In the file |
| --- | --- |
| CORENET X level naming | `1st Storey`, `1st Storey_Terrace`, `Roof` — never `Main Floor`, never `Level 1`. The building is in Illinois and would never be submitted through CORENET X, but a reference model that breaks the convention the course teaches teaches the opposite |
| Georeferenced to its own locale | EPSG:26916 (NAD83 / UTM 16N), not SVY21. What CORENET X actually requires is that the file *states* its CRS, datum and rotation — the specific system follows the site |
| Author in the building's own units | Feet and inches throughout the script, stored as millimetres. Metric-first authoring invents precision the building never had |
| Correct entity, correct subtype | `IfcCurtainWall` aggregating `IfcPlate` and `IfcMember` — not a wall with a glass material |
| Types before instances | Every slab, column, beam, plate, mullion and wall comes from a type carrying its material or layer set |
| Structure told the truth | Columns stop at 16'-0" and stand outboard of the slabs, because that is how they were welded |
| One thing punctures the roof | The flue is an `IfcChimney` and it is the only element above 16'-0" |
| Quantities, not guesses | Every space carries `Qto_SpaceBaseQuantities`, so "how much glass" is a query rather than a measurement |
| Provenance on the element | `Farnsworth_Provenance` travels with the geometry, not in a side document that will be lost |

## Known simplifications

Honest ones, at Design Development level of detail:

- **Pane rhythm is derived, not measured.** Five 11'-0" panes on the long elevations, four 7'-0"
  panes on the ends. The overall glass area is right; the joint positions are grade C.
- **Travertine is one covering per plane, not 612 pavers.** The module and the piece count are
  carried as data. Cutting the stone is a Stage 05 question, not a Design Development one.
- **The porch screens are not modelled.** Dr Farnsworth had the west porch screened *after*
  completion, so it does not belong in a Design Development model. It belongs in
  [Stage 07]({{ '/stages/completion/' | relative_url }}) as an as-built variation — which is
  precisely the kind of change the course asks you to record rather than absorb.
- **The curtain track is not modelled.** MoMA's drawings show a ceiling detail for a track that
  would have divided the space into three rooms. The drapery was never installed.
- **No mechanical services.** The house has a plenum and radiant floor heating; neither is modelled.
- **No furniture beyond the wardrobe.** The Mies-designed pieces are separately protected as designs.
- **True North is left at zero.** The building's real bearing is on HABS sheet 1, and this script has
  not seen it. Rather than invent a rotation, the model declares none — and the gate does not test
  for one.
- **Georeferencing is approximate.** EPSG:26916 (NAD83 / UTM 16N) puts the model on the real site,
  read off a map. Do not quote those coordinates as survey data.
