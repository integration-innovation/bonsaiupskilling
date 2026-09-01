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
