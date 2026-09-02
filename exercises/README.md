# Exercises

Reference scripts. Nothing in the course *requires* them — every stage can be completed by hand in
the Sketch tab — but they are useful for two things: rebuilding a stage baseline quickly, and
proving that your written decisions actually reproduce the model.

All of them model the **Edith Farnsworth House** (Mies van der Rohe, Plano, Illinois, 1945–51).

The building is out of copyright — the US Architectural Works Copyright Protection Act does not
reach works constructed before 1 December 1990 — and the whole of its survey record,
[HABS IL-1105](https://www.loc.gov/resource/hhh.il0323.sheet), is public domain, photographs
included.

**Mies's own drawings are a different matter and are still protected**, separately from the
building, as pictorial works. These scripts reproduce no drawing: they are built from published
dimensions, which are facts. Take dimensions off the HABS sheets; do not trace anything. The
[reference model page](https://integration-innovation.github.io/bonsaiupskilling/reference-model/)
sets out all three positions.

## `reference-model/build_farnsworth.py`

Builds the complete Stage 04 model as IFC4: eight W8×48 columns, floor and roof planes at 15"
structural depth, four curtain walls aggregating 19 glass plates and 24 mullions, a six-partition
primavera core, the travertine as a covering carrying its 2'-9" × 2'-0" module, the two hopper
windows that are the house's only operable openings, the flue, two travertine flights, nine spaces,
and two grids — the column lines and the paving module they follow.

```bash
python exercises/reference-model/build_farnsworth.py
```

Writes `exercises/reference-model/FARN-A-DD-P01.ifc`. Requires IfcOpenShell 0.8.x — the same
library Bonsai ships — and NumPy.

Every dimension lives in one `DIMS` table at the top of the script, each figure carrying its source
and an A/B/C confidence grade, and every element carries that grade into the IFC file as a
`Farnsworth_Provenance` property set. Correcting a figure against the HABS drawings is a one-line
edit and a re-run.

## `reference-model/check_farnsworth.py`

The gate. 286 checks, exits non-zero on any failure, so it works in CI.

```bash
python exercises/reference-model/check_farnsworth.py            # the reference model
python exercises/reference-model/check_farnsworth.py mine.ifc   # your own
```

Three groups matter more than the rest:

- **CLOSURE** — the plan and section close exactly in feet. 3 × 22'-0" plus two 5'-6" cantilevers is
  77'-0"; 5'-3" + 9'-6" + 1'-3" is 16'-0". If yours does not close, you rounded something.
- **FRAME** — eight columns, on the right lines, outboard of the slab edge. The moment a column
  passes through a slab, the building stops being the building.
- **SOURCE** — every element with geometry declares where its dimensions came from.

CLOSURE now includes the paving: the travertine module is derived from the 220 pieces documented on
the terrace, and the gate tests that all six principal dimensions are whole numbers of pavers.

## `reference-model/build_gcb_house.py`

Builds the **Pinwheel House** — a Good Class Bungalow on a 1,600 m² plot, at **three stages from one
script**, because a model gains information across stages rather than being replaced.

```bash
python exercises/reference-model/build_gcb_house.py --all
python exercises/reference-model/check_gcb_house.py
```

| Stage | Output | What exists |
| --- | --- | --- |
| `concept` | `GCB-A-CON-P02.ifc` | Masses, shelter volume, spaces. No openings, no glazing |
| `dd` | `GCB-A-DD-P04.ifc` | Steel frame, glazed envelope, openings, quantities |
| `asbuilt` | `GCB-A-AB-AB01.ifc` | Plus `verified` / `assumed` on every element |

The parti takes Wright's pinwheel from the public-domain Wasmuth Portfolio and Mies's elevated steel
frame from public-domain HABS IL-1105 — as **concept only**, no drawing traced or reproduced. The
household shelter stands where Wright would have put the hearth, and because everything else is on
steel, it is the only part of the house that touches the ground.

**1,581 checks** across the three models. The ones worth stealing: setbacks and coverage are
measured *from the geometry*, the shelter's declared internal size must multiply out to its own
NetFloorArea, the shelter's walls must start at z=0, and a Concept model containing doors **fails**.

## `reference-model/build_servant_house.py`

Builds the course's own building — the **Servant and Served House** — as IFC4 at Stage 03: two
reinforced-concrete servant towers, a glazed served volume between them, a full-height light well,
and a household shelter sized to SCDF's 2023 requirements at 1500 × 3200 internal, 4.800 m², inside
250mm walls that run to roof level.

```bash
python exercises/reference-model/build_servant_house.py
python exercises/reference-model/check_servant_house.py
```

The parti is Louis Kahn's servant-and-served distinction, which is a *concept* and therefore free
under 17 U.S.C. §102(b) — no drawing by anyone was consulted or traced. The building is an original
design and the course owns it outright.

**322 checks.** Four groups matter: **SHELTER** (within SCDF's limits, carrying its data, and the
declared internal dimensions multiply out to the space's own NetFloorArea), **TOWER** (every tower
wall exists on every storey), **CORENET** (level naming, one site, SVY21, SHD, True North) and
**VAF** (every element names the component it serves).

## `01-massing/build_massing.py`

Builds a reference massing for [Stage 02](https://integration-innovation.github.io/bonsaiupskilling/stages/concept-design/):
the whole building as five moves — two horizontal planes, eight columns, a glass line 22'-0" in from
the west end, and a terrace one step down. Each object is tagged with `project_stage`,
`design_status`, `role` and `confidence` in line with the
[model standard](https://integration-innovation.github.io/bonsaiupskilling/standards/).

Run it headless:

```text
blender -b --python exercises/01-massing/build_massing.py
```

It writes `exercises/01-massing/farnsworth_massing.blend`. It is plain Blender mesh — deliberately
not IFC, because Stage 02 classifies nothing.

Use it to check your own massing against a known-good one, or as a starting point if you would
rather spend the session on the option comparison than on the geometry. Building it yourself with
`R` and `P` takes about twenty minutes and teaches more.

Licensed GPL-3.0-or-later, matching Bonsai.
