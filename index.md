---
layout: default
title: Bonsai Upskilling
permalink: /
---

<div class="hero" markdown="1">

# Build a bungalow, stage by stage

One house. One IFC model. Eight stages of the SIA Architect's Scope of Service, from the
first site question to the last defect — modelled in **Blender**, **Bonsai** and
**Bonsai Sketch Mode**, and free to work through at your own pace.

</div>

This is not a tour of buttons. It is a project you carry: a small detached house that starts as a
massing block and finishes as an as-built record with an asset register attached. Each stage adds
information rather than replacing the model, which is the habit that separates a BIM model from a
3D drawing.

<ul class="cards">
{% for s in site.data.stages %}
  <li style="--c:{{ s.colour }}">
    <a href="{{ '/stages/' | append: s.slug | append: '/' | relative_url }}">
      <span class="n">STAGE {{ s.num }}</span>
      <span class="t">{{ s.title }}</span>
      <span class="d">{{ s.strap }}</span>
      <span class="m">{{ s.weeks }} · {{ s.hours }} hours</span>
    </a>
  </li>
{% endfor %}
</ul>

<div class="big-note" markdown="1">

### Start here

1. **[Set up]({{ '/setup/' | relative_url }})** — Blender 5.0 or 5.2, Bonsai 0.8.4 or 0.8.5, Bonsai Sketch Mode. About fifteen minutes.
2. **[Read the brief]({{ '/brief/' | relative_url }})** — the client, the site, the money, and what you are not told.
3. **[Kickstart]({{ '/kickstart/' | relative_url }})** — one hour, from an empty Blender to a saved IFC with real walls, a door, a window and a named room.
4. **[Adopt the model standard]({{ '/standards/' | relative_url }})** — naming, status, decision log, issue register. Ten minutes now saves the whole of Stage 05.
5. **[Stage 01 · Pre-Design]({{ '/stages/pre-design/' | relative_url }})** — begin.

Want to see where this ends up first? The
**[reference model]({{ '/reference-model/' | relative_url }})** is the finished Stage 03 bungalow as a
downloadable IFC4 file — real types, real openings, SVY21 georeferencing, and a 158-check script
you can run against your own model at every gate.

</div>

## Who this is for

Architects, architectural executives, technologists and students who can read a plan and want to
work natively in IFC without first becoming Blender users. It suits three people in particular:

- someone moving from a direct modeller (SketchUp, Rhino, FormIt) who wants the same interaction with real building data underneath;
- a practice deciding what its BIM deliverable per stage should actually be, and what that costs in hours;
- anyone who has produced a beautiful model that could not answer a single contractual question, and would rather not do it twice.

No prior Blender knowledge is assumed. Some architectural practice experience is, because the
stages are described in the language of a real appointment, not a software tutorial.

## Why the SIA stages

Modelling exercises usually fail for the same reason: nothing forces the model to be *useful* at a
particular moment. A stage framework does. The [SIA Scope of Service
Matrix](https://sia.org.sg/architects-scope-of-service/) sets out what an architect in Singapore is
normally expected to deliver at each of eight stages, in four distinct roles — **Designer**,
**Qualified Person**, **Contract Administrator** and **Design Manager / Project Administrator**.
The [SIA Value Articulation Framework](https://sia.org.sg/sia-value-articulation-framework-vaf/)
goes further and breaks those services into individual components with the resources each needs.

Every stage here borrows that structure: what the profession expects of you, then what the model
has to contain for you to deliver it. See [SIA mapping]({{ '/sia-mapping/' | relative_url }}) for the full picture and the
attribution.

Three frameworks run underneath the course, and they use three different sets of stage names, which
is confusing exactly once and then stops being:

| | Answers | Captured here |
| --- | --- | --- |
| **SIA Scope of Service** | What is the architect responsible for? | [SIA mapping]({{ '/sia-mapping/' | relative_url }}) |
| **SIA VAF / BluePrint** | What does doing it take — components, grades, hours? | [The VAF, captured]({{ '/vaf/' | relative_url }}) |
| **IFC+SG · CORENET X** | What must the *model itself* contain? | [IFC+SG and CORENET X]({{ '/ifc-sg/' | relative_url }}) |

The third is the Singapore-specific one and the one most modelling courses skip: IFC+SG is built on
IFC4 with Singapore property sets, states which parameters are required at which stage, and comes
with twelve **General Modelling Practices** — level naming, coordinates, GUIDs, federation, clash,
file size — that this course folds into the exercises rather than listing at the end.

<div class="note" markdown="1">
#### Singapore-shaped, not Singapore-only

The stage names, the authorities and the submission gateways are Singaporean. The modelling is not.
If you work under RIBA Plan of Work, AIA phases or ISO 19650, the stage titles change and almost
nothing else does — the mapping table on the [SIA mapping]({{ '/sia-mapping/' | relative_url }}) page gives the
equivalents.
</div>

## The one-model rule

You will finish with **one** `.ifc` project and a folder of dated revisions of it. Not eight models.
Not a "presentation model" and a separate "real model".

| Stage | Course project | What the model becomes |
| --- | --- | --- |
{% for s in site.data.stages %}| {{ s.num }} · {{ s.title }} | {{ s.project }} | {{ s.strap }} |
{% endfor %}

That table is also the answer to a question the framework asks and most tutorials dodge: *what,
precisely, is the deliverable at the end of this stage?* Each stage page states it, and states the
gate you must pass before starting the next one.

## How a stage page works

Every one of the eight is laid out the same way, so you can find your place in it quickly.

- **Why this stage exists** — the SIA services being performed, in all four roles.
- **What you will learn** — the modelling and information skills, named.
- **Before you start** — the inputs that must already exist.
- **Build it** — numbered steps against a real keyboard, in Sketch Mode and in Bonsai.
- **Deliverables** — the files you produce, named to the standard.
- **The gate** — a checklist. Do not start the next stage until every line is true.
- **Where this goes wrong** — the failures that recur, and how to see them early.

The click-by-click detail sits beside the stages rather than inside them, so it stays findable:
[Kickstart]({{ '/kickstart/' | relative_url }}) for your first hour, and
[modelling recipes]({{ '/modelling/' | relative_url }}) for fifteen operations you can open one at a
time — each tagged with the SIA stage, the VAF component and the IFC+SG data it serves.

## Rhythm and total time

Three sessions a week of 45 to 60 minutes: one to read and plan, one to model, one to check and
record. That puts the whole programme at **11 to 12 weeks and roughly 35 to 45 focused hours**.

Going faster is possible and usually a mistake. The point of the exercise is not the geometry — a
120 m² bungalow is an afternoon's modelling — it is the discipline of making each decision findable
afterwards.

## What you need

| | |
| --- | --- |
| **Blender** | 5.0 or 5.2 LTS. Newer releases are refused on purpose |
| **Bonsai** | 0.8.4 or 0.8.5, installed from Blender's *Get Extensions* |
| **Bonsai Sketch Mode** | The [latest release zip](https://github.com/integrations-space/BonsaiSketch/releases/latest) |
| **Hardware** | Anything that runs Blender comfortably. This model is tiny |
| **Optional** | An Anthropic API key, if you want to try the `Describe` panel |

Full instructions, and what to do when a step misbehaves, are on [Set up]({{ '/setup/' | relative_url }}).

## Honest limits

<div class="warn" markdown="1">
#### Read this before Stage 01

**Bonsai Sketch Mode is early software.** Line, Rectangle, Push/Pull and Tape Measure work. Offset,
Follow Me, Eraser and Paint do not exist yet, and <span class="k">F</span>, <span class="k">B</span>
and <span class="k">E</span> are deliberately unbound rather than pointed at an approximation.

**Push/Pull refuses to touch an IFC element**, on purpose — an `IfcWall` gets its shape from
material layers or a profile, and overwriting that with a mesh would silently throw the parametric
definition away. Once something is IFC, depth belongs to Bonsai's own controls. This shapes the
whole course: sketch freely early, and stop pushing faces once the design is classified.

**Auto-subtract does not exist.** From Stage 04 onward, openings are made with Bonsai's own
void/opening workflow, never by leaving an unexplained hole in a mesh.

**Nothing here is legal or contractual advice.** The stages summarise a published SIA reference for
teaching. Your actual scope is whatever your consultancy agreement says, and authority requirements
change — check the source, every time.
</div>

## Contributing

Corrections, better exercises and translations are welcome. The site is plain Markdown in a public
repository: [integration-innovation/bonsaiupskilling](https://github.com/integration-innovation/bonsaiupskilling).
Bugs in the add-on itself belong in the
[BonsaiSketch issue tracker](https://github.com/integrations-space/BonsaiSketch/issues) — include
your Blender and Bonsai versions.
