# Exercises

Reference scripts. Nothing in the course *requires* them — every stage can be completed by hand in
the Sketch tab — but they are useful for two things: rebuilding a stage baseline quickly, and
proving that your written decisions actually reproduce the model.

## `01-massing/build_massing.py`

Builds a reference massing for [Stage 02](https://integration-innovation.github.io/bonsaiupskilling/stages/concept-design/):
a 12 × 10 block, a covered entry, a courtyard and a pitched-roof study, each tagged with
`project_stage`, `design_status` and `role` custom properties in line with the
[model standard](https://integration-innovation.github.io/bonsaiupskilling/standards/).

Run it headless:

```text
blender -b --python exercises/01-massing/build_massing.py
```

It writes `exercises/01-massing/bungalow_massing.blend`. It is plain Blender
mesh — deliberately not IFC, because Stage 02 classifies nothing.

Use it to check your own massing against a known-good one, or as a starting point if you would
rather spend the session on the option comparison than on the geometry. Building it yourself with
`R` and `P` takes about twenty minutes and teaches more.

Licensed GPL-3.0-or-later, matching Bonsai.
