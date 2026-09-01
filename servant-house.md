---
layout: default
title: The Servant and Served House
strap: The course's own building — designed on Kahn's principle, owned outright, and built to exercise IFC+SG and the VAF properly.
permalink: /servant-house/
---

The course carries **two** worked examples, because one building cannot do both jobs.

| | |
| --- | --- |
| **[Farnsworth House]({{ '/reference-model/' | relative_url }})** | A study in *measurement and provenance*. A real, documented building where every dimension has a source and a confidence grade, and the Stage 04 exercise is correcting the model against a measured survey |
| **The Servant and Served House** *(this page)* | A study in *Singapore delivery*. A household shelter, SVY21, CORENET X level naming, GFA as a modelled space, and every element mapped to a VAF component |

Farnsworth cannot teach the second. It has no household shelter, it is not on SVY21, and it will
never go through CORENET X. That is not a flaw in the model — it is a flaw in using a famous foreign
building as a regulatory example, and the honest fix is a second building.

<div class="big-note" markdown="1">

### Download

**[SERV-A-SCH-P03.ifc]({{ '/exercises/reference-model/SERV-A-SCH-P03.ifc' | relative_url }})** — 173 KB, IFC4

Built by **[build_servant_house.py](https://github.com/integration-innovation/bonsaiupskilling/blob/main/exercises/reference-model/build_servant_house.py)**,
checked by **[check_servant_house.py](https://github.com/integration-innovation/bonsaiupskilling/blob/main/exercises/reference-model/check_servant_house.py)** —
**322 checks**, exits non-zero on failure.

</div>

## Who owns it

**This course does.** The building is an original design, drawn for teaching. No architect's estate,
no licensing desk, no expiry date, and nothing to clear before you use it.

That matters because the alternative was impossible. Working through
[which drawings you can actually use]({{ '/sources/' | relative_url }}) produced a hard result: you
can have **postmodern**, **royalty-free drawings**, or an **IFC+SG showcase** — any two, never all
three. Designing the building removes the constraint entirely.

## The idea, and why it is free

The parti is Louis Kahn's distinction between **servant** and **served** space: the solid, founded,
immovable masses that carry stairs, water, waste and shelter, and the light, open, changeable rooms
that live between them.

Kahn died in 1974, so his *drawings* are protected until roughly 2044. His *idea* is not protected
at all, and never was. [17 U.S.C. §102(b)](https://www.law.cornell.edu/uscode/text/17/102) is
explicit:

> In no case does copyright protection for an original work of authorship extend to any idea,
> procedure, process, system, method of operation, concept, principle, or discovery, **regardless of
> the form in which it is described, explained, illustrated, or embodied**.

Ideas are free. Expression is not. No drawing by Kahn — or anyone — was consulted, traced or adapted
in making this model.

## Why the idea fits the regulation exactly

This is the part worth pausing on. SCDF's
[Technical Requirements for Household Shelters](https://www.scdf.gov.sg/home/civil-defence-shelter/acts-and-requirements/technical-requirements-for-household-shelters-2023)
describe the shelter as an **"HS tower"** — reinforced concrete, founded, structurally continuous to
ground, immovable.

A founded, structurally continuous, immovable concrete tower **is** a Kahn servant space. The two
ideas are the same idea, arrived at from opposite directions: one from a theory of how buildings
should be organised, the other from civil defence.

So this design stops treating the shelter as a nuisance to be hidden in a corner, and makes it the
thing the plan is organised around. Which is exactly what the [brief]({{ '/brief/' | relative_url }})
has always meant by calling it *one of the few rooms whose walls you do not get to move*.

## The plan

```text
                              N
   x 0        3.6                        9.6        13.2
    +----------+--------------------------+----------+  y 9.6
    | LIGHT    |         Kitchen          | Bath 1   |
    | WELL     |                          |          |  y 6.0
    | (to sky) +--------------------------+----------+
    +----------+                          |  Stair   |
    | Store    |      Living / Dining     |          |  y 2.4
    +----------+                          +----------+
    | HS | Util|                          |    WC    |
    +----+-----+--------------------------+----------+  y 0
    W SERVANT TOWER    SERVED VOLUME    E SERVANT TOWER
      solid, founded    open, glazed      solid, founded
                          N and S
```

Solid where the low sun is punishing — east and west. Open where the breeze runs — north and south.
A light well at the north-west corner runs the full height, pulling daylight down and letting hot
air out at the top.

Upstairs the served volume divides into three bedrooms; the west tower carries a bathroom **directly
over the shelter**, on the same walls and the same foundations. That is the whole argument for a
tower: build it once, use it twice.

## The module is the regulation

Everything is a whole number of **1.2 m** — and that is not an arbitrary choice. **1200mm is SCDF's
minimum internal width for a household shelter.** The regulation sets the grain of the building,
which is a more honest way round than designing freely and then discovering the shelter will not fit.

## The shelter, against the 2023 requirements

| | Model | Requirement | |
| --- | --- | --- | --- |
| Internal width | **1500 mm** | ≥ 1200 mm | ✅ |
| Internal length | **3200 mm** | ≤ 4000 mm | ✅ |
| Internal area | **4.800 m²** | ≤ 4.8 m² | ✅ |
| Clear height | **2700 mm** | 2400–3900 mm | ✅ |
| Walls | 250 mm cast in-situ RC | 250 mm for landed | ✅ |
| Continuity | Founded, continuous to roof | "HS tower" | ✅ |

<div class="warn" markdown="1">
#### The check that matters most

The gate does not only test that the shelter is within the limits. It tests that the **declared
internal dimensions multiply out to the space's own `NetFloorArea`**:

`Internal Length × Internal Width = 3200 × 1500 = 4.800 m² = NetFloorArea`

A shelter whose data and geometry disagree is worse than one with no data, because a checker will
believe the data. Writing that test found a real defect in this model's first build: the space
inset used *half* the wall thickness, which gives centreline area — a fine convention for gross
calculations and the wrong one when IFC+SG asks a room for its **internal** size.

Both numbers now come from the same place.
</div>

## What is in it

| | |
| --- | --- |
| Walls | 29 — external, partitions, two RC servant towers, and the four 250mm shelter walls |
| Slabs · Roof | 3 · 1 — with a 1.2 m overhang, because this is the tropics |
| Doors · Windows | 14 · 11, every one filling a real `IfcOpeningElement` |
| Spaces | 20 — 18 rooms plus **two GFA spaces**, one per storey |
| Storeys | `1st Storey` (+150), `2nd Storey` (+3750), `Roof` (+7350) |
| Grid | A–D and 1–3 |
| Net internal area | **197.4 m²** — 104.5 below, 92.9 above |
| GFA (modelled) | 131.32 m² per storey |

## The IFC+SG conventions it demonstrates

| Convention | In the file |
| --- | --- |
| Level naming | `1st Storey`, `2nd Storey`, `Roof` — not `Ground`, not `Level 1`, never `1st Floor` |
| One `IfcSite`, named for the block | `IfcSite` Name = `Main Block` |
| Geo-referencing | `IfcProjectedCRS` EPSG:3414, SVY21 / Singapore TM, vertical datum SHD |
| True North | `IfcMapConversion` rotated 8° |
| **GFA is a space, not a cell** | `IfcSpace` with `USERDEFINED` / `AREA_GFA`, carrying `AGF_Name`, `AGF_Development Use`, `AGF_Use Quantum` |
| Shelter data from conceptual stage | Construction method, internal length, internal width, clear height — on the space itself |
| Types before elements | Every wall, slab, door and window comes from a type with a material layer set |
| Real openings | `IfcOpeningElement` voiding its host, filled by the door or window |

## The VAF layer

Every element carries a `VAF_Demo` property set naming the
[Value Articulation Framework]({{ '/vaf/' | relative_url }}) component it serves — `Structure`,
`Envelope`, `Space Planning`, `Regulatory` — and the resource grade that produced it.

That is a small thing that changes how a model can be read. Once components are on the elements, you
can ask *what did the regulatory work consist of* and get an answer out of the model, rather than
out of a memory of the project. The gate enforces it: an element with no component fails.

## Running it

```bash
python exercises/reference-model/build_servant_house.py
python exercises/reference-model/check_servant_house.py
```

Point the checker at your own model to test your work:

```bash
python exercises/reference-model/check_servant_house.py my-house.ifc
```

The four groups that matter:

| Group | What it proves |
| --- | --- |
| **SHELTER** | Within SCDF's limits, carrying its data, and its two numbers reconcile |
| **TOWER** | Every tower wall exists on every storey. A tower that stops halfway is not a tower |
| **CORENET** | Level naming, one site, SVY21, SHD, a True North rotation |
| **VAF** | Every element names the component it serves |

<div class="warn" markdown="1">
#### Do not trust these numbers because a model contained them

The shelter figures satisfy the 2023 requirements *as this course reads them*. They are a teaching
example, not a compliance submission, and requirements change.

The course's own rule applies with full force: find the current requirement yourself in
[Stage 01]({{ '/stages/pre-design/' | relative_url }}), record it with its source and the date you
read it, and check this model against what you find. If it is out of date, that is a bug in the
course — please open an issue with the correction and the source.
</div>
