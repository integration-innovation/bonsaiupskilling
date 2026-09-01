---
layout: default
title: Set up
strap: Blender, Bonsai and Bonsai Sketch Mode — about fifteen minutes, most of it downloading.
permalink: /setup/
---

Three pieces, each running inside the one below. You install all three; none of them replaces
another.

```text
Blender 5.0 / 5.2 LTS       the application you launch
  └─ Bonsai 0.8.4 / 0.8.5     add-on: makes Blender an IFC authoring tool
       └─ Bonsai Sketch Mode  add-on: gives Bonsai a direct-modelling interface
```

## 1 · Blender

Download **5.0 or 5.2 LTS** from [blender.org/download](https://www.blender.org/download/).

Newer releases are refused deliberately. Bonsai ships compiled Python components, so it only runs
where those match the host Python; a Blender nobody has tested against is a silent breakage
waiting to happen. Installing outside the supported range fails with a clear message instead:

```text
This Blender version (5.3.0) must be less than the maximum version (5.3.0)
```

## 2 · Bonsai

Inside Blender: **`Edit` → `Preferences` → `Get Extensions`**, search **`Bonsai`**, press
**Install**. It is a large download and takes a few minutes. When it finishes, a **`BIM`** tab
appears in the bar across the top of the window.

*Get Extensions* installs 0.8.5 today, which is what makes Blender 5.2 possible — 0.8.4's wheels
stopped at Python 3.11. If anything misbehaves later, your Bonsai version is the first thing to
write down.

## 3 · Bonsai Sketch Mode

Download **`bonsai_sketch_mode-<version>.zip`** from
[the latest release](https://github.com/integrations-space/BonsaiSketch/releases/latest). **Do not
unzip it.** Then, in Blender:

**`Edit` → `Preferences` → `Add-ons`** → the **`▾`** button, top right → **`Install from Disk…`**
→ choose the zip.

A **`Sketch`** tab appears in the top bar next to `BIM`, immediately — no restart.

<div class="note" markdown="1">
**Upgrading from 0.3.0 or earlier?** Remove the old add-on first. It was called *BonsaiBIM Sketch
Mode* up to 0.3.0, and Blender keys extensions by id — the new one installs *beside* the old one,
leaving two copies competing for the same single-key shortcuts. Being enabled is a saved preference
keyed by that same id, so the old entry stays ticked pointing at nothing and the new one arrives
switched off.
</div>

## 4 · Prove it works

Open the **`Sketch`** tab. One full-width viewport, tools down the left, nothing else. Then, in
order:

{: .steps}
1. **Press <span class="k">R</span>.** Click once, move the mouse, click again. A rectangle.
2. **Press <span class="k">P</span>.** Hover over the rectangle's face, drag upward, then type `3` and press <span class="k">Enter</span>. A 3-metre box.
3. **Press <span class="k">L</span>.** Click points to draw edges; <span class="k">C</span> closes the loop, <span class="k">Enter</span> finishes.
4. **Press <span class="k">T</span>** and click two points to measure between them.
5. **Press <span class="k">N</span>** to show the sidebar, and find the **`IFC`** panel. It should offer **New IFC Project**.

If all five behave, you are set up. Delete the test geometry — Stage 01 starts from an empty file.

## The toolset you will use for eleven weeks

| Key | Tool | Notes |
| --- | --- | --- |
| <span class="k">Space</span> | Select | Blender's box select |
| <span class="k">L</span> | Line | Connected edges; closed coplanar loops become faces |
| <span class="k">R</span> | Rectangle | Two opposite corners |
| <span class="k">P</span> | Push/Pull | Extrudes the face under the cursor along its normal |
| <span class="k">T</span> | Tape Measure | Bonsai's measure tool |
| <span class="k">M</span> <span class="k">Q</span> <span class="k">S</span> | Move / Rotate / Scale | Blender's transforms |
| <span class="k">O</span> <span class="k">H</span> <span class="k">Z</span> | Orbit / Pan / Zoom | <span class="k">Shift</span>+<span class="k">Z</span> zooms to extents |

While a tool is running:

| | |
| --- | --- |
| Type a number | An exact value — metric, imperial (`5' 6"`), or an expression (`=2*1.5`) |
| <span class="k">X</span> <span class="k">Y</span> <span class="k">Z</span> | Lock to one axis |
| <span class="k">Shift</span> + <span class="k">X</span> <span class="k">Y</span> <span class="k">Z</span> | Lock to one plane |
| <span class="k">Backspace</span> | Undo the last point |
| <span class="k">Esc</span> | Abandon the whole operation |

Three things about **Push/Pull** are worth knowing on day one, because the course leans on all
three:

- **It infers along its own axis.** As a face is dragged it stops where existing geometry already is — the top of the wall beside this one, the underside of the slab above — and the header reads `(aligned)` while it is held there. Typing a distance overrides the inference.
- **<span class="k">Ctrl</span> stacks.** Holding Ctrl as the push starts builds a *new* solid on the face and leaves the original in place. That is how the terrace mass and the roof plane get made in Stage 02.
- **Regions push separately.** A surface divided by drawn lines can be pushed one region at a time; walls appear along the dividing lines and the rest of the surface stays put. A step, a notch or a sill recess is a line and a drag.

<span class="k">F</span>, <span class="k">B</span> and <span class="k">E</span> do nothing **on
purpose**. Those tools are not built yet, and a key wired to an approximation teaches the wrong
habit.

## Sketch geometry is not IFC — and that is the point

Line, Rectangle and Push/Pull produce plain Blender meshes. Nothing about them is an `IfcProduct`.
A direct modeller's workflow is to sketch first and assign meaning second; making every stroke an
IFC element would invert it.

The **`IFC`** panel in the Sketch sidebar (<span class="k">N</span>) is where meaning gets
assigned. It shows one of two things:

- **No IFC project yet** — a **New IFC Project** button. Everything else is behind that gate; without a project, Bonsai's Wall, Slab, Door and Window tools all just read `No IFC Project`.
- **A project is open** — select a finished sketch, pick a class, press **Assign**. It becomes a real `IfcWall`, `IfcSlab`, or whatever you chose.

Anything past that — construction types, material layers, spatial structure, properties, drawings,
schedules — lives in Bonsai's **`BIM`** tab, which has the room for it.

<div class="warn" markdown="1">
**Push/Pull refuses IFC elements.** An `IfcWall` gets its shape from material layers or a profile.
Overwriting that with a tessellated mesh would silently discard the parametric definition, so the
tool declines. Use Bonsai's own depth controls instead. From Stage 04 onward this will be the
single most common thing that "doesn't work" — and it is working correctly.
</div>

## Optional · Describe

Type a sentence on the Sketch tab and let Claude build it with the same Sketch verbs:
**`IFC` sidebar → `Describe`**.

> a 6 by 4 metre room, 3 metres high

Four real parametric walls with material layers and thickness — not a mesh box called a wall.
Add an Anthropic API key in **`Preferences` → `Add-ons` → `Bonsai Sketch Mode` → `Describe`**, or
set `ANTHROPIC_API_KEY` in your environment. Requests go to Anthropic and are billed to that key.
Without a key the panel stays hidden.

It edits your live model with no proposal step, so treat it like any other edit: know what you
asked for, check what you got, and remember that <span class="k">Ctrl</span>+<span class="k">Z</span>
undoes a build.

This course never *requires* Describe. Stage 02 offers it as an option for generating study
variants quickly, and Stage 04 explicitly asks you to switch it off, because documentation is
exactly where an unreviewed edit becomes expensive.

## Optional · Text to Model

A local command channel, so something other than a person at a mouse can drive Blender — a script,
a CI job, an agent. Open it in **`Preferences` → `Add-ons` → `Bonsai Sketch Mode` → `Text to
Model`**. It listens on loopback only and every request carries a token generated for that session.

```text
python tools/textmodel_client.py ping
python tools/textmodel_client.py create_project
python tools/textmodel_client.py create_type '{"ifc_class": "IfcWallType"}'
python tools/textmodel_client.py add_walls '{"points": [[0,0],[6,0],[6,4],[0,4],[0,0]], "height": 3}'
```

Verbs available: `ping`, `describe`, `list_elements`, `create_project`, `create_type`, `add_walls`,
`sketch_polyline`, `push_pull`, `assign_class`.

Anything that reaches this socket can rewrite the model — there is no proposal step and no undo. It
is a local development channel, not a service. Useful here for one thing only: rebuilding a stage
baseline from a script, so you can prove your written decisions actually reproduce the model.

## Your project folder

Make this before Stage 01. The stage pages assume it.

```text
farnsworth/
  00-brief/          brief, site information, authority notes
  01-pre-design/
  02-concept/
  ...
  08-post-completion/
  registers/         decision-log.csv, issues.csv, deliverables.csv
  export/            IFC issued at each gate
  images/            screenshots you actually keep
```

Naming and revision conventions are on the [model standard]({{ '/standards/' | relative_url }}) page. Adopt them now — the
whole of Stage 06 depends on being able to say which revision a decision belongs to.

## When something does not work

| Symptom | Cause |
| --- | --- |
| Install fails, "must be less than the maximum version" | Your Blender is newer than 5.2. Use 5.0 or 5.2 |
| No `Sketch` tab after installing | Installed but not ticked in `Preferences → Add-ons` |
| `Sketch` tab present, letter keys do nothing | You are on a different tab. The keymap is only live on `Sketch` |
| Tools greyed out, or an error in their settings bar | Bonsai is missing or failed to load — check the `BIM` tab exists |
| Wall/Door/Window say `No IFC Project` | No project yet. `IFC` panel in the sidebar → **New IFC Project** |
| No `IFC` panel in the sidebar | The sidebar is closed — press <span class="k">N</span>, or re-tick **IFC sidebar** in preferences |
| Push/Pull says "no face under the cursor" | Hover directly over a face. It also declines objects that have modifiers |
| Push/Pull refuses an element you know is a wall | It is IFC now. Correct behaviour — use Bonsai's depth controls |

Still stuck: **`Window` → `Toggle System Console`** shows what Blender is complaining about, and
that output is the single most useful thing to put in an
[issue](https://github.com/integrations-space/BonsaiSketch/issues).
