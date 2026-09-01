---
layout: default
title: Model standard
strap: Naming, classification, status and the three registers that make a model answerable.
permalink: /standards/
---

A project information standard is normally a fifty-page document nobody reads. This is the smallest
version that still works for one house, one modeller and eight stages. Adopt it before Stage 01;
retrofitting it at Stage 05 costs a full session.

## 1 · Files and revisions

One IFC project. One working `.blend`. A dated export at every gate, never overwritten.

```text
farnsworth/
  farnsworth.blend                      the working file
  export/
    FARN-A-PRE-P01-2026-09-04.ifc     Pre-Design baseline
    FARN-A-CON-P02-2026-09-18.ifc     Concept, option A approved
    FARN-A-SCH-P03-2026-10-09.ifc     Schematic, for planning
    FARN-A-DD-P04-2026-10-30.ifc      Design Development, coordinated
    FARN-A-TEN-T01-2026-11-20.ifc     Tender issue
    FARN-A-CON-C01-2026-12-11.ifc     Construction issue
    FARN-A-AB-AB01-2027-01-15.ifc     As-built
```

`PROJECT-DISCIPLINE-STAGE-REVISION-DATE`. Revision prefixes: **P** preliminary, **T** tender,
**C** construction, **AB** as-built. The prefix is the contractual status; the number is the
sequence within it. `P03` never becomes `P03a` — if it changed, it is `P04`.

<div class="note" markdown="1">
**Why export at gates rather than continuously.** A gate export is evidence: it is the model as it
was when a decision was made. Continuous exports are just backups, and backups answer no questions.
Keep both if you like, but only the gate exports go in `export/`.
</div>

## 2 · Object naming

Sketch geometry and IFC elements alike:

```text
A-Walls-Ext-North          discipline - system - subtype - location
A-Slabs-Ground
A-Roof-Main
A-Openings-W03            matches the window schedule mark
A-Massing-OptionB         study geometry
X-Cutter-W03              temporary, non-issued, to be deleted or explained
```

| Prefix | Meaning |
| --- | --- |
| `A-` | Architectural, intended to be issued |
| `X-` | Working geometry: studies, cutters, setting-out aids. Never issued, never left unexplained |
| `Z-` | Superseded. Kept for the record, moved to a hidden collection |

The rule that matters: **anything called `X-` must be gone or documented before a gate**. A stray
cutter that survives into a tender model is a hole nobody can account for.

## 3 · Status properties

Every element carries two custom properties from the moment it is created. Bonsai can hold these as
IFC property sets; while geometry is still plain Sketch mesh, Blender custom properties are fine.

| Property | Values |
| --- | --- |
| `project_stage` | `01 Pre-Design` … `08 Post Completion` — the stage the element was last touched in |
| `design_status` | `provisional` · `approved` · `superseded` |

Three values, not thirty. `provisional` means it may still change without anyone being told;
`approved` means changing it now requires a decision-log entry; `superseded` means it is history,
retained deliberately.

## 4 · Classification

Assign an IFC class only when the decision behind the geometry is stable. Early massing is
`X-Massing` mesh and nothing more.

| Element | Class | Typed? |
| --- | --- | --- |
| Floor and roof planes | `IfcSlab` | Yes — `IfcSlabType` with material layers |
| Steel columns | `IfcColumn` | Yes — `IfcColumnType`, one per section |
| Edge channels | `IfcBeam` | Yes — `IfcBeamType` |
| The glass skin | `IfcCurtainWall` aggregating `IfcPlate` and `IfcMember` | Yes — all three typed |
| Core partitions | `IfcWall` | Yes — `IfcWallType` with material layers |
| Doors | `IfcDoor` | Yes, with a mark that matches the schedule |
| Openings in walls | `IfcOpeningElement` via Bonsai's void workflow | n/a |
| Flue | `IfcChimney` | From Stage 04 |
| Rooms, the porch and the terrace | `IfcSpace` | Named and numbered |
| Site | `IfcSite` | One only |
| Stairs | `IfcStair` | From Stage 04 |
| Kitchen and sanitary fittings | `IfcFurniture`, `IfcSanitaryTerminal` | From Stage 04 |

The glass is a **curtain wall**, not a wall with a glass material on it. That is the single most
common classification error on this building, and it is the difference between being able to
schedule nineteen panes and not.

**Types before occurrences.** One `IfcPlateType` called `GL-PLATE-6MM` used nineteen times is a
schedule; nineteen individually-drawn panes are a drawing. Stage 04 is where this becomes
non-optional.

**Classification is three things, not one.** For a Singapore submission, IFC+SG expects every
element to carry the correct **IFC entity**, its **IFC subtype** where one applies, and the
**property sets** that entity requires — and the element declares its own class through an
`IfcExportAs` parameter. A GFA area, for instance, is an `IfcSpace` with subtype `USERDEFINED` and
the value `AREA_GFA`, carrying the `AGF_` properties.

Bonsai Sketch Mode ships the IFC+SG element list as data, and the requirements are summarised on the
[IFC+SG page]({{ '/ifc-sg/' | relative_url }}). The authoritative source is
[info.corenet.gov.sg](https://info.corenet.gov.sg/) at the time you submit.

## 5 · Spatial structure

Five levels, no more:

```text
IfcProject          Edith Farnsworth House
  IfcSite           Fox River Floodplain   <- one IfcSite per file; its Name carries the block
    IfcBuilding     Edith Farnsworth House
      IfcBuildingStorey   1st Storey_Terrace  (+0.610)   <- 2'-0"
      IfcBuildingStorey   1st Storey          (+1.600)   <- 5'-3"
      IfcBuildingStorey   Roof                (+4.877)   <- 16'-0"
```

Every element belongs to exactly one storey. An element with no spatial container is invisible to
half of every downstream tool, and it is the single most common defect found when a model is
checked for the first time.

**Storey names follow the CORENET X convention, not your habits.** `1st Storey` and `Storey 1` are
valid; `1st Floor`, `Level one` and `2nd Story` are not. `Attic` is valid; `Attic 1` is not. `Roof`,
`Upper Roof` and `Lower Roof Storey` are valid; `Roof Lower` is not. Different physical levels get
different names, and names and Z values stay consistent across every discipline. The full table,
including basements, mezzanines and block suffixes, is on the
[IFC+SG page]({{ '/ifc-sg/' | relative_url }}).

**One `IfcSite` per file**, named for the block. This house has one block, so this costs nothing
here — and on a development with towers, a podium and a basement it is four separate architectural
files plus one for site works.

## 6 · The three registers

Plain CSV in `registers/`. Open them in anything. They are the deliverable that survives the
software.

### decision-log.csv

```csv
date,author,decision,reason,affects,status
2026-09-04,AT,North arrow set to +Y,True bearing unknown until HABS sheet 1,A-Site;all plans,provisional
2026-09-18,AT,Bay spacing 22'-0" not 20'-0",20'-0" cannot close to 77'-0",A-Columns;A-Grid,approved
2026-09-18,AT,Option A superseded,Not deleted; see Z-Massing-OptionA,Z-Massing-OptionA,superseded
```

### issues.csv

```csv
id,raised,stage,element,description,owner,due,status,closed
I-001,2026-10-09,03,A-Walls-Ext-North,Window W03 head clashes with roof beam zone,AT,2026-10-16,open,
I-002,2026-10-11,03,A-Slabs-Ground,Slab edge does not meet wall centre line,AT,2026-10-16,closed,2026-10-14
```

From Stage 04 onward, keep this in **BCF** as well, using Bonsai's own BCF tools. BCF travels
between applications; a CSV does not. The CSV stays because it is readable in ten years.

### deliverables.csv

```csv
stage,item,file,issued,revision,status
02,Concept option comparison,02-concept/options.pdf,2026-09-18,P02,issued
02,Concept IFC,export/FARN-A-CON-P02-2026-09-18.ifc,2026-09-18,P02,issued
```

## 7 · The gate rule

<div class="gate" markdown="1">
#### A stage is complete when three things agree

1. **The model** contains what the stage requires, classified and contained.
2. **The exported deliverable** was produced from that model, not assembled beside it.
3. **The registers** explain every difference from the previous gate.

If a screenshot, a schedule and the model disagree, the stage is not finished — whichever one is
wrong, you do not yet know which.
</div>

Two habits make this survivable:

- **Never promote an unverified sketch into an IFC element because it looks right in the viewport.** Look at it in plan, in section, and in the schedule it will appear in.
- **Never fix a problem by deleting the evidence.** Supersede, record, move on.

## 8 · A checking pass, in five minutes

Run this before every gate. It catches most of what a formal model check would.

{: .check}
- One `IfcProject`, one `IfcSite`, one `IfcBuilding`, storeys at the levels you intended.
- Every element has a storey. Nothing sits loose at project level.
- No object still named `X-…` except ones the decision log explains.
- Every `IfcDoor` and `IfcWindow` has a host wall and an opening — not a mesh hole.
- Types exist and are used; no one-off element that should have been a type.
- Every `IfcSpace` has a name, a number and an area that matches the schedule.
- Wall, slab and roof quantities are within a few percent of a hand check.
- Element count has changed only where the decision log says it should have.
- No duplicate `GlobalId`s — which means no revision was made by duplicating a file and renaming it.
- Storey names still match the convention, and their Z values have not drifted.
- The export opens in an IFC viewer that is not Blender, at the right size and orientation.

Most of that list is already automated. `check_farnsworth.py`, shipped with the
[reference model]({{ '/reference-model/' | relative_url }}), runs 286 checks over any IFC you point it
at and exits non-zero on failure — use it from Stage 03 onward.

From Stage 04, add Bonsai's own model-checking tools as well: an **IDS** file expresses these rules
in a form the software can test, and running it beats reading a checklist. Write the IDS once,
at Stage 04, and every later gate is a button press.
