---
layout: default
title: The reference model
strap: Mies van der Rohe's Farnsworth House as IFC4 — every dimension carrying its source, and a 244-check gate you can run.
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

**The building is free to model, publish and teach from.** The US
[Architectural Works Copyright Protection Act](https://www.copyright.gov/circs/circ41.pdf) took
effect on **1 December 1990** and does not reach works constructed before that date. The Farnsworth
House was completed in 1951, so as *architecture* it carries no US copyright that a model of it
could infringe.

**The measured record is public domain.** The Historic American Buildings Survey documented the
house as **HABS IL-1105** — 32 photographs, **8 measured drawings**, 54 data pages — held by the
Library of Congress. HABS documentation is prepared by the US National Park Service and is a work of
the United States Government: no known restrictions on publication.

- [Survey record](https://www.loc.gov/pictures/item/il0323/)
- [The eight measured drawings](https://www.loc.gov/resource/hhh.il0323.sheet)

**Photographs are a different question.** Photographs of the house are usually still in copyright,
and being of a public-domain building does not change that. This course therefore ships *geometry
and drawings you generate yourself*, never photographs.

</div>

## What is in it

| | |
| --- | --- |
| Columns | 8 — W8×48 wide flange, welded to the slab edges, grade to 16'-0" |
| Slabs | 3 — floor and roof planes at 15" structural depth, plus the lower terrace |
| Beams | 4 — 15" edge channels, the white band you read as the edge of each plane |
| Curtain walls | 4 — one per elevation, aggregating **19 glass plates** and **24 mullions** |
| Walls | 6 — the primavera core, and nothing else in the building |
| Chimney | 1 — the flue, the only element that punctures the roof plane |
| Stairs · Door · Furniture | 2 · 1 · 1 |
| Spaces | 9 — seven internal zones, the west porch and the terrace |
| Storeys | `Terrace` (+610), `Main Floor` (+1600), `Roof` (+4877) |
| Grid | 1–4 on the column lines, A–B on the column rows |
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

244 checks, in three groups that matter more than the rest, because they are the ones a
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
- **No mechanical services.** The house has a plenum and radiant floor heating; neither is modelled.
- **No furniture beyond the wardrobe.** The Mies-designed pieces are separately protected as designs.
- **True North is left at zero.** The building's real bearing is on HABS sheet 1, and this script has
  not seen it. Rather than invent a rotation, the model declares none — and the gate does not test
  for one.
- **Georeferencing is approximate.** EPSG:26916 (NAD83 / UTM 16N) puts the model on the real site,
  read off a map. Do not quote those coordinates as survey data.
