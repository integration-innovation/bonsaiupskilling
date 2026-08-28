---
layout: default
title: Kickstart
strap: One hour, from an empty Blender to a saved IFC with real walls, a door, a window and a named room.
permalink: /kickstart/
---

Do this once before [Stage 01]({{ '/stages/pre-design/' | relative_url }}). It is not the bungalow — it is a single room,
built the way every later stage will ask you to build. By the end you will have produced a valid
IFC4 file and know which half of the interface does what.

Sixty minutes, six blocks of ten. [Set up]({{ '/setup/' | relative_url }}) must already be done.

<div class="note" markdown="1">
**Two tabs, two jobs.** The **`Sketch`** tab is for drawing: single-key tools, inference, plain
meshes. The **`BIM`** tab is Bonsai proper: project, spatial structure, types, classification,
properties, drawings. This hour crosses between them four times, deliberately, so the boundary stops
being confusing.

Written against **Bonsai 0.8.5** and **Sketch Mode 0.4.x**. Bonsai is a rolling release; if a panel
has moved, its name is usually still the right thing to search for.
</div>

## 0–10 min · Make a project that is legal IFC

Everything in Bonsai is behind an IFC project. Without one, the wall, slab, door and window tools
all read `No IFC Project` and nothing you draw is a building.

{: .steps}
1. **Open Blender.** Delete the default cube if there is one — <span class="k">X</span> with it selected, or right-click → Delete.

2. **Create the project.** Topbar → **`File` → `New IFC Project` → `New Metric (mm) Project`**.

   Millimetres, because construction dimensions are millimetres and [IFC+SG]({{ '/ifc-sg/' | relative_url }}) submissions are
   metric. The other options are `New Metric (m)`, `New Imperial (ft)`, `New Demo Project`, and
   `New Project Wizard`.

   *From the Sketch tab instead:* press <span class="k">N</span> for the sidebar → **`IFC`** panel →
   **New IFC Project**. Same gate, fewer clicks, no schema choice.

3. **If you want control, use the wizard.** **`File` → `New IFC Project` → `New Project Wizard`**, or
   `Properties → Project Overview → Project Info`. Set the **IFC Schema** to **IFC4** — IFC+SG is built on
   IFC4, so IFC2X3 is the wrong answer here and IFC4X3 is ahead of it. Set the unit system and the
   length, area and volume units. Leave the template **Blank**. Press **Create Project**.

4. **Look at what you were given.** `Properties → Project Overview → Spatial Decomposition`. There is
   already a tree: `IfcProject → IfcSite → IfcBuilding → IfcStorey`. You did not have to build it, and
   every element you make from now on has to live somewhere in it.

5. **Rename the storey and set its elevation.** Not `Level 1`. Call it **`1st Storey`** and give it a real elevation.

   The name is not arbitrary. [CORENET X's first general modelling practice]({{ '/ifc-sg/' | relative_url }}) is level naming, and it publishes valid and invalid examples: `1st Storey` and `Storey 1` are valid, `1st Floor`, `Level one` and `2nd Story` are not. After export a checker has only the name and the Z value to work with.

6. **Save immediately.** <span class="k">Ctrl</span>+<span class="k">S</span>, or **`File` → `Save IFC
   Project`**. You will be asked where to put the `.ifc`. Call it `kickstart.ifc`.

   Note what just happened: you saved an **IFC file**, not a `.blend`. That is the durable artefact.

## 10–20 min · Draw something that is not IFC yet

Now the other half. Go to the **`Sketch`** tab.

{: .steps}
1. **Rectangle.** Press <span class="k">R</span>, click once, move, click again.

2. **Push it up.** Press <span class="k">P</span>, hover over the face, drag upward, then type `3000` and press <span class="k">Enter</span>. Three metres, in a millimetre project.

3. **Try typing an expression.** Undo, push again, and type `=3000/2`. The measurement box parses expressions, and imperial input, because it is Bonsai's own polyline engine underneath.

4. **Lock an axis.** Press <span class="k">L</span> for Line and use <span class="k">X</span>, <span class="k">Y</span> or <span class="k">Z</span> to lock direction, then type a distance. <span class="k">C</span> closes a loop; a closed coplanar loop becomes a face. <span class="k">Backspace</span> undoes a point, <span class="k">Esc</span> abandons.

5. **Cut a notch with a regional push.** Draw a line across the top face of your box to divide it, then press <span class="k">P</span> and push one region down. Only that region moves; walls appear along the dividing line. This is how a courtyard, a step or a sill recess gets made in [Stage 02]({{ '/stages/concept-design/' | relative_url }}).

6. **Notice what you have.** Plain Blender mesh. Not an `IfcProduct`. Sketch first, decide what it *is* second — which is the next block.

## 20–30 min · Turn a sketch into an IFC element

{: .steps}
1. **Select the box.**

2. **From the Sketch tab:** sidebar → **`IFC`** panel → pick a class → **Assign**.

   **From the BIM tab:** `Properties → Object Information` → the **Products** dropdown → choose a category, then a class → **Assign IFC Class**.

3. **Check where it landed.** `Properties → Object Information → Spatial Container`. It should be inside your `1st Storey`. An element with no container is invisible to half of every downstream tool and is the most common defect in a first model.

4. **Now try to push it.** Press <span class="k">P</span> and hover a face of the element you just classified. **It refuses.**

   This is correct and it is the single most important thing in the hour. An IFC element's shape comes from its material layers or its profile; overwriting that with a tessellated mesh would silently throw the parametric definition away. From here, depth belongs to Bonsai's controls.

5. **Save again.** <span class="k">Ctrl</span>+<span class="k">S</span>.

## 30–45 min · Build the same room properly

Delete the sketch box. This time, build it the way Stage 03 onwards will.

{: .steps}
1. **Go to the BIM tab and pick the wall tool.** The Bonsai toolbar has **Create Wall**; the whole toolbar is also on <span class="k">Shift</span>+<span class="k">Spacebar</span> for a quick menu.

2. **Make a wall type first.** With the tool active, the top bar reads `[No IfcWallType Found] | Name [TYPEX] | + Add IfcWallType`. Replace `TYPEX` with something meaningful — `EXT-200` — and press **+ Add IfcWallType**.

   The type is the specification. One type used forty times is a schedule, a quantity and a spec at once; forty individually drawn walls are a drawing.

3. **Set the start point.** Hold <span class="k">Shift</span> and left-click to place the 3D cursor where the wall begins.

4. **Add the wall.** <span class="k">Shift</span>+<span class="k">A</span>. Adjust length and height from the parameters in the top bar, or by dragging.

5. **Build four walls into a room** — about 6 m × 4 m, 3 m high — and join them:

   | | |
   | --- | --- |
   | <span class="k">Shift</span>+<span class="k">E</span> | Extend to intersect another face |
   | <span class="k">Shift</span>+<span class="k">T</span> | Butt — join end to end |
   | <span class="k">Shift</span>+<span class="k">Y</span> | Mitre |
   | <span class="k">Shift</span>+<span class="k">M</span> | Merge segments into one wall |
   | <span class="k">Shift</span>+<span class="k">R</span> | Rotate 90° |

6. **Add a door — and select the wall first.** This matters: selecting the host wall is what makes the void relation between door and wall get created automatically. Position the 3D cursor on the wall, choose **Create Door**, name the type in the top bar and press **+ Add IfcDoorType**, then <span class="k">Shift</span>+<span class="k">A</span> to place it.

   | | |
   | --- | --- |
   | <span class="k">Shift</span>+<span class="k">O</span> | Apply void manually, if the wall was not pre-selected |
   | <span class="k">Shift</span>+<span class="k">G</span> | Regenerate the wall geometry after changing an opening |
   | <span class="k">Shift</span>+<span class="k">F</span> | Flip the door — 180°, changing the swing |

7. **Add a window** the same way with **Create Window**.

8. **Look at the opening you just made.** It is an `IfcOpeningElement` related to its host wall — not a hole in a mesh. That relationship is what makes a door schedule, a quantity and a lintel possible later.

<div class="note" markdown="1">
**Faster route, same result.** If you have configured [Describe]({{ '/setup/' | relative_url }}), type *"a 6 by 4 metre
room, 3 metres high"* in the `IFC` sidebar and it builds four real parametric walls with material
layers, driving the same verbs. Useful for a starting point; not a substitute for knowing which
verbs those are. The course asks you to stop using it from [Stage 04]({{ '/stages/design-development/' | relative_url }}).
</div>

## 45–55 min · Give the room meaning

{: .steps}
1. **Add a space.** The toolbar's **Spatial Tool** defines and manages spatial structures. Make an `IfcSpace` for your room, then name and number it.

   Bonsai's own documentation for spaces is still marked work-in-progress, so expect to explore here. The result is what matters: a named, numbered space with an area you can read out of the model rather than off a calculator.

2. **Name everything to a standard.** `A-Walls-Ext-North`, not `IfcWall.005`. The [model standard]({{ '/standards/' | relative_url }}) is three rules long and Stage 05 depends on all three.

3. **Look at the properties.** With an element selected, work through the panels in `Properties → Object Information`. This is where an [IFC+SG]({{ '/ifc-sg/' | relative_url }}) parameter would live — *main entrance* on a door, *percentage of opening* on a window, *purpose group* on a space.

4. **Save, and export.** <span class="k">Ctrl</span>+<span class="k">S</span> writes the IFC.

## 55–60 min · Prove it to something that is not Blender

{: .steps}
1. **Open `kickstart.ifc` in an IFC viewer.** Any of them. If it opens, is the right size, has a named storey, and shows a door in a wall rather than a hole in a mesh, the hour worked.

2. **This is the habit, not the formality.** [CORENET X asks you to verify alignment and content after export]({{ '/ifc-sg/' | relative_url }}), because the model you author and the model an agency reads are not guaranteed to be the same thing until you have looked.

## What you now know

- IFC project first, always. Everything else is behind that gate.
- Sketch tab draws; BIM tab means. Crossing between them is the workflow, not a failure.
- Types before elements.
- Select the wall before placing the door.
- Push/Pull refusing an IFC element is the tool working.
- The `.ifc` is the deliverable; the `.blend` is your working copy.

## Where to go next

**[Stage 01 · Pre-Design]({{ '/stages/pre-design/' | relative_url }})** — start the real project, beginning with the site
and the rules rather than the building.

**[Bonsai modelling recipes]({{ '/modelling/' | relative_url }})** — the same operations as reference, each tagged with the
SIA stage and the IFC+SG data it serves, for when you need one step rather than a whole hour.

**[The reference model]({{ '/reference-model/' | relative_url }})** — the finished Stage 03 bungalow as
IFC4. Open it beside your own work when a relationship is not obvious, and run its check script
against your model at each gate.
