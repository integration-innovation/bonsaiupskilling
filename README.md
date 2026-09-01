# Bonsai Upskilling

A free, project-based training programme: **rebuild one documented masterwork through the eight
stages of the SIA Architect's Scope of Service**, using Blender, [Bonsai](https://bonsaibim.org/)
and [Bonsai Sketch Mode](https://github.com/integrations-space/BonsaiSketch).

The building is Mies van der Rohe's **Edith Farnsworth House** (Plano, Illinois, 1945–51) — chosen
because it is measured, out of copyright, and governed by a module strict enough that a
modelling error shows up as a dimension that will not close.

**→ [integration-innovation.github.io/bonsaiupskilling](https://integration-innovation.github.io/bonsaiupskilling)**

One house. One IFC model. Eight stages — Pre-Design, Concept Design, Schematic Design, Design
Development, Documentation, Construction, Completion, Post Completion — each with a timebox, a
step-by-step exercise, a named deliverable and a gate you must pass before the next one.

Roughly 35–45 focused hours over 11–12 weeks.

## What is here

| | |
| --- | --- |
| `index.md` | Programme home: the eight stages, the one-model rule, time and prerequisites |
| `setup.md` | Installing Blender, Bonsai and Sketch Mode; the toolset; troubleshooting |
| `kickstart.md` | One hour, empty Blender to a saved IFC with walls, a door, a window and a room |
| `brief.md` | The client, the site, the requirement and the scripted change events |
| `modelling.md` | Fifteen Bonsai recipes, each tagged with its SIA stage, VAF component and IFC+SG data |
| `standards.md` | Naming, status, classification, spatial structure and the three registers |
| `sia-mapping.md` | The SIA Scope of Service Matrix, the four roles, and the eight stages |
| `vaf.md` | The SIA Value Articulation Framework captured — components, stages, resource grades |
| `ifc-sg.md` | IFC+SG data requirements and CORENET X's twelve General Modelling Practices |
| `sources.md` | Which master architects' drawings are royalty-free, which are not, and how to tell |
| `glossary.md` | Terms, in the sense this course uses them |
| `reference-model.md` | The Farnsworth House as downloadable IFC4, its 286-check gate, and why it is free to ship |
| `stages/` | The eight stage pages |
| `exercises/` | Reference scripts, including the model builder and its 286-check gate |
| `_layouts/`, `_data/`, `assets/` | The site itself — plain Jekyll, no theme gem, one stylesheet |

## Running it locally

The site is plain Markdown built by GitHub Pages. To preview it:

```bash
bundle exec jekyll serve
```

Or just read the Markdown — every page is written to be legible without the site around it.

## Contributing

Corrections, better exercises and translations are welcome. Two things to keep in mind:

- **Accuracy about the tools.** Bonsai Sketch Mode is early software. If a step describes behaviour the add-on does not have, that is a bug in this course, not an aspiration. Say so.
- **Accuracy about the profession.** The SIA summaries are paraphrases for teaching, prepared from the published documents. If one is wrong or out of date, please open an issue with the correction and the source.

Bugs in the add-on itself belong in the
[BonsaiSketch issue tracker](https://github.com/integrations-space/BonsaiSketch/issues) — include
your Blender and Bonsai versions.

## Licence and attribution

Text and course material: **CC BY 4.0**. Example scripts: **GPL-3.0-or-later**, matching Bonsai.
See [LICENSE.md](LICENSE.md).

The [SIA Scope of Service Matrix](https://sia.org.sg/architects-scope-of-service/) and the
[SIA Value Articulation Framework](https://sia.org.sg/sia-value-articulation-framework-vaf/) are
published by the Singapore Institute of Architects. **IFC+SG** and the **General Modelling
Practices** are published by [CORENET X](https://info.corenet.gov.sg/). Summaries here are our own
paraphrase for teaching, not reproductions. This project is not published by, endorsed by or
affiliated with SIA, BCA or the Government of Singapore, and is not a substitute for the source
documents, a consultancy agreement, or current authority requirements.

Not affiliated with the Bonsai project or the Blender Foundation.
