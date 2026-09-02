"""Build the Pinwheel House as IFC4 -- the course's Good Class Bungalow example.

    python exercises/reference-model/build_gcb_house.py [--stage concept|dd|asbuilt]

Writes GCB-A-<stage>.ifc beside this script. One script, three states of the same
building, because the course's central claim is that a model gains information
across stages rather than being replaced:

    concept   Stage 02.  Masses, the shelter as a volume, spaces. No openings,
                         no glazing, nothing classified that is not decided.
    dd        Stage 04.  The whole building: steel frame, glazed envelope,
                         openings, finishes, quantities.  [default]
    asbuilt   Stage 07.  Design Development plus verification: every element
                         says whether its as-built state was measured or assumed.

THE SITE
--------
A Good Class Bungalow plot. GCB status is the strictest residential control in
Singapore and it is what makes this a useful teaching site: the constraints are
real, published, and generous enough that the design question is architecture
rather than squeezing.

    Minimum plot area      1,400 m2         this plot: 1,600 m2 (40 x 40)
    Minimum plot width     18.5 m           this plot: 40 m
    Minimum plot depth     30 m             this plot: 40 m
    Maximum site coverage  40%              this design: 22.7%
    Height                 2 storeys + attic
    Setbacks               3 m              this design: 6.6 m all round
    Detached only, no subdivision, boundary walls to 1.8 m

There are 39 gazetted GCB Areas, in Districts 10, 11, 20, 21 and 23. This model
is georeferenced near Chatsworth Park, District 10. The coordinates are read off
a map and are a plausible example, not a survey, and the controls above are as
this course reads them in 2026 -- go and confirm both yourself, as Stage 01 asks.

THE CONCEPT, AND ITS TWO ROYALTY-FREE REFERENCES
------------------------------------------------
Two ideas, each taken from a master architect, each documented in a source that
is genuinely free to consult:

  Frank Lloyd Wright -- ORGANIC PLANNING, the pinwheel.
      Reference: the Wasmuth Portfolio, Berlin 1910-11, 100 lithographs of
      Wright's own drawings of work from 1893-1909. Published over 95 years ago
      and therefore public domain in the United States.
      What is taken: the Prairie plan's habit of pinwheeling wings about a
      solid central hearth, so the plan turns rather than lines up, and the
      horizontal is emphasised by deep overhangs and stepped massing.

  Mies van der Rohe -- STEEL, GLASS AND THE ELEVATED FLOOR PLANE.
      Reference: HABS IL-1105, the Farnsworth House, 8 measured drawings held
      by the Library of Congress. Historic American Buildings Survey
      documentation is a work of the US Government and is public domain.
      What is taken: the floor plane lifted clear of the ground on a light
      steel frame, and an envelope reduced to glass between structure.

Both are used as CONCEPT only. No drawing was traced, scanned, redrawn or
adapted, and none is reproduced here. What is borrowed is method -- and
17 U.S.C. 102(b) is explicit that copyright never extends to "any idea,
procedure, process, system, method of operation, concept, principle, or
discovery, regardless of the form in which it is described, explained,
illustrated, or embodied". The building below is an original design and this
course owns it outright.

WHY THE TWO IDEAS BELONG TOGETHER HERE
--------------------------------------
Wright pinwheels his plan about a hearth: a solid, founded masonry mass, the one
thing in the composition that cannot move. Singapore requires a household
shelter: 250mm reinforced concrete for landed housing, founded, structurally
continuous to ground -- SCDF calls it an "HS tower".

They are the same element. So the shelter takes the hearth's place at the pivot,
and the four wings turn about it.

Mies then supplies the answer to the tropics. Lifting the floor plane 1.8 m on a
steel frame puts an open, shaded, through-ventilated undercroft beneath the
house -- which is also, and not by coincidence, what a Malay kampong house does.
The glass envelope sits well back under a 1.8 m overhang, so the wall is shaded
by the roof rather than by the glass.

And the shelter is then the ONLY part of the building that touches the ground.
Everything else floats. A regulation that is usually hidden in a corner becomes
the thing the house is organised around and stands on.

Requires ifcopenshell 0.8.x.  Licensed GPL-3.0-or-later, matching Bonsai.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np

import ifcopenshell
import ifcopenshell.api as api
import ifcopenshell.api.aggregate
import ifcopenshell.api.context
import ifcopenshell.api.feature
import ifcopenshell.api.geometry
import ifcopenshell.api.georeference
import ifcopenshell.api.grid
import ifcopenshell.api.material
import ifcopenshell.api.project
import ifcopenshell.api.pset
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.api.type
import ifcopenshell.api.unit

HERE = Path(__file__).resolve().parent

STAGES = {
    "concept": ("02 Concept Design", "provisional", "GCB-A-CON-P02.ifc"),
    "dd":      ("04 Design Development", "approved", "GCB-A-DD-P04.ifc"),
    "asbuilt": ("07 Completion", "approved", "GCB-A-AB-AB01.ifc"),
}

# ------------------------------------------------------------- site controls --
PLOT = 40.0                  # square plot, 1,600 m2 against a 1,400 m2 minimum
SETBACK = 3.0                # GCB minimum, all sides
MAX_COVERAGE = 0.40          # GCB maximum site coverage

# ---------------------------------------------------------------- dimensions --
# Metres. Origin at the south-west corner of the PLOT. +Y is project north.

MOD = 3.6                    # structural module, three shelter-widths
UNDERCROFT = 1.800           # the floor plane lifted clear of the ground
STOREY_H = 3.600
L1 = UNDERCROFT              # 1st Storey finished floor level
L2 = L1 + STOREY_H           # 2nd Storey
ROOF = L2 + STOREY_H         # roof plane
EAVE = 1.800                 # deep overhang: the wall is shaded by the roof

T_HS, T_CORE, T_INT = 0.250, 0.200, 0.100
COL = 0.200                  # square hollow steel section

# The core, at the centre of the plot. The pinwheel turns about it.
CORE = (16.8, 16.8, 24.0, 24.0)

# The household shelter, sized to SCDF's 2023 requirements:
#   internal 1.5 x 3.2 = 4.80 m2   (max 4.8, min width 1.2, max length 4.0)
#   walls 250mm  ->  gross 2.0 x 3.7
HS = (16.8, 16.8, 18.8, 20.5)
HS_CLEAR = 2.700
HS_DOOR_FACE = "E"           # the door is in the east wall

# PROTECTION TO THE SHELTER, and why the first version of this design failed it.
#
# The shelter must be shielded by a minimum clear distance to the nearest
# enclosing external face: 2.0 m on the wall carrying the door, 2.7 m on the
# three walls without one.
#
# At 1st Storey the four wings wrap the core and the shelter clears those
# distances several times over. At GROUND level it did not clear them at all.
# Lifting the house on a steel frame -- the move the whole design rests on --
# leaves the shelter tower standing alone in an open undercroft with nothing
# around it on any side. Elegant, and non-compliant.
#
# The fix is a protective plinth: a low reinforced-concrete enclosure at ground
# level, wrapping the tower at the required distances and housing plant and
# store. The rest of the undercroft stays open, so the cross-ventilation and
# the floating reading survive. The house floats; it lands on one solid base;
# and that base is what protects the shelter.
HS_PROTECT_DOOR = 2.000
HS_PROTECT_OTHER = 2.700
PLINTH = (14.0, 14.0, 21.0, 23.4)   # clears 2.80 / 2.80 / 2.20 / 2.90
T_PLINTH = 0.200

# Four wings, each turned a quarter from the last. None aligns with another:
# that offset is the whole of the pinwheel, and it is what stops the plan
# reading as a cross.
# ------------------------------------------------------------------- context --
# A model with no context is a model that cannot be checked against its site.
PLOT_ORIGIN = (0.0, 0.0)
ROAD_DEPTH = 7.0             # the estate road, along the south boundary
BOUNDARY_WALL_H = 1.800      # GCB maximum
DRIVEWAY = (18.0, -0.2, 23.0, 14.0)

# Neighbouring GCB plots, as simplified context masses. Not our building, and
# the model says so: they are IfcBuildingElementProxy, never IfcBuilding.
#  name: (x0, y0, x1, y1, height)
NEIGHBOURS = [
    ("Context-Plot-W", -34.0, 4.0, -6.0, 32.0, 9.0),
    ("Context-Plot-E", 46.0, 6.0, 74.0, 34.0, 9.0),
    ("Context-Plot-N", 6.0, 50.0, 34.0, 78.0, 9.0),
]

# Mature trees, which on a GCB plot are often the reason a house is shaped as it
# is. Crown radius, trunk height. Kept clear of the building.
TREES = [(6.0, 6.0, 4.5), (34.0, 8.0, 3.5), (6.0, 34.0, 4.0),
         (34.0, 34.0, 5.0), (20.0, 36.5, 3.0)]

# The bungalow already standing on the plot. It exists at Concept, because the
# site plan has to show what is there; it is gone by Design Development, because
# by then it has been demolished. That is the whole point of modelling it.
EXISTING = (12.0, 12.0, 28.0, 26.0, 8.0)

#  name: (x0, y0, x1, y1, storeys)
WINGS = {
    "N": (16.8, 24.0, 27.6, 31.2, "12"),   # living, and bedrooms above
    "E": (24.0, 13.2, 31.2, 24.0, "12"),   # dining and kitchen, bedrooms above
    "S": (13.2,  9.6, 24.0, 16.8, "1"),    # guest and family, single storey
    "W": ( 9.6, 16.8, 16.8, 27.6, "1"),    # study and utility, single storey
}

# Which rectangles are occupied on each storey. The core is on both.
def footprint(storey: str) -> list[tuple[float, float, float, float]]:
    rects = [CORE]
    rects += [w[:4] for w in WINGS.values() if storey in w[4]]
    return rects


# number, name, long name, (x0,y0,x1,y1), storey, external
SPACES = [
    # --- 1st Storey: the public half of the house, turning about the shelter
    ("01", "Household Shelter", "Household shelter, 1st storey", HS, "1", False),
    ("02", "Stair", "Stair and hall, 1st storey", (18.8, 16.8, 24.0, 24.0), "1", False),
    ("03", "Living", "Living, north wing", (16.8, 24.0, 27.6, 31.2), "1", False),
    ("04", "Dining", "Dining, east wing", (24.0, 19.2, 31.2, 24.0), "1", False),
    ("05", "Kitchen", "Kitchen, east wing", (24.0, 13.2, 31.2, 19.2), "1", False),
    ("06", "Family", "Family room, south wing", (18.0, 9.6, 24.0, 16.8), "1", False),
    ("07", "Guest", "Guest bedroom, south wing", (13.2, 9.6, 18.0, 16.8), "1", False),
    ("08", "Study", "Study, west wing", (9.6, 22.8, 16.8, 27.6), "1", False),
    ("09", "Utility", "Utility, west wing", (9.6, 16.8, 16.8, 22.8), "1", False),
    # --- 2nd Storey: the private half, stepped back over two wings only
    ("10", "Bathroom 2", "Bathroom over the shelter", HS, "2", False),
    ("11", "Stair 2", "Stair and landing, 2nd storey", (18.8, 16.8, 24.0, 24.0), "2", False),
    ("12", "Bedroom 1", "Master bedroom, north wing", (16.8, 24.0, 27.6, 31.2), "2", False),
    ("13", "Bedroom 2", "Bedroom 2, east wing", (24.0, 19.2, 31.2, 24.0), "2", False),
    ("14", "Bedroom 3", "Bedroom 3, east wing", (24.0, 13.2, 31.2, 19.2), "2", False),
    # --- the roofs of the single-storey wings are terraces at 2nd Storey level
    ("15", "Terrace S", "Roof terrace over the south wing",
     (13.2, 9.6, 24.0, 16.8), "2", True),
    ("16", "Terrace W", "Roof terrace over the west wing",
     (9.6, 16.8, 16.8, 27.6), "2", True),
]

# The shelter tower, and the stair beside it. Everything else is glass.
# tag: (p1, p2, type key, storeys)
WALLS = {
    "A-Walls-HS-South": ((16.8, 16.8), (18.8, 16.8), "HS", "12"),
    "A-Walls-HS-East":  ((18.8, 16.8), (18.8, 20.5), "HS", "12"),
    "A-Walls-HS-North": ((18.8, 20.5), (16.8, 20.5), "HS", "12"),
    "A-Walls-HS-West":  ((16.8, 20.5), (16.8, 16.8), "HS", "12"),
    "A-Walls-Core-N":   ((18.8, 24.0), (24.0, 24.0), "CORE", "12"),
    "A-Walls-Int-E01":  ((24.0, 19.2), (31.2, 19.2), "INT", "12"),
    "A-Walls-Int-S01":  ((18.0, 9.6), (18.0, 16.8), "INT", "1"),
    "A-Walls-Int-W01":  ((9.6, 22.8), (16.8, 22.8), "INT", "1"),
}
THICKNESS = {"HS": T_HS, "CORE": T_CORE, "INT": T_INT}

# mark, host wall, distance along, width, height, sill, storey, main entrance
DOORS = [
    ("D01", "A-Walls-HS-East",  1.85, 0.850, 2.000, 0.0, "1", False),
    ("D02", "A-Walls-HS-East",  1.85, 0.850, 2.000, 0.0, "2", False),
    ("D03", "A-Walls-Core-N",   2.60, 1.500, 2.400, 0.0, "1", True),
    ("D04", "A-Walls-Int-E01",  3.60, 0.900, 2.100, 0.0, "1", False),
    ("D05", "A-Walls-Int-E01",  3.60, 0.900, 2.100, 0.0, "2", False),
    ("D06", "A-Walls-Int-S01",  3.60, 0.900, 2.100, 0.0, "1", False),
    ("D07", "A-Walls-Int-W01",  3.60, 0.900, 2.100, 0.0, "1", False),
]

STOREY_Z = {"1": L1, "2": L2}
STOREY_NAME = {"1": "1st Storey", "2": "2nd Storey"}

GRID_TAGS = "ABCDEFG"
GRID_X = [9.6 + i * MOD for i in range(7)]     # 9.6 .. 31.2
GRID_Y = [9.6 + i * MOD for i in range(7)]


# ------------------------------------------------------------------ helpers --

def inside(rects, x, y, tol=1e-6):
    return any(x0 - tol < x < x1 + tol and y0 - tol < y < y1 + tol
               for x0, y0, x1, y1 in rects)


def external_faces(storey: str):
    """Every wall face on the outer boundary of this storey's footprint.

    The wings meet each other at their corners -- that is what a pinwheel does --
    so a face is only glazed where nothing lies immediately beyond it. Testing
    that beats listing the faces by hand and getting one wrong.
    """
    rects = footprint(storey)
    faces = []
    for x0, y0, x1, y1 in rects:
        edges = [((x0, y0), (x1, y0), (0.0, -1.0)),   # south
                 ((x1, y0), (x1, y1), (1.0, 0.0)),    # east
                 ((x1, y1), (x0, y1), (0.0, 1.0)),    # north
                 ((x0, y1), (x0, y0), (-1.0, 0.0))]   # west
        for (ax, ay), (bx, by), (nx, ny) in edges:
            span = math.hypot(bx - ax, by - ay)
            steps = max(1, int(round(span / MOD)))
            for i in range(steps):
                t0, t1 = i / steps, (i + 1) / steps
                sx, sy = ax + (bx - ax) * t0, ay + (by - ay) * t0
                ex, ey = ax + (bx - ax) * t1, ay + (by - ay) * t1
                mx, my = (sx + ex) / 2.0, (sy + ey) / 2.0
                if not inside(rects, mx + nx * 0.05, my + ny * 0.05):
                    faces.append(((sx, sy), (ex, ey)))
    return faces


def columns_for(storey: str):
    """Steel columns on the module, wherever the grid falls inside the plan."""
    rects = footprint(storey)
    out = []
    for x in GRID_X:
        for y in GRID_Y:
            on_edge = any(
                (abs(x - x0) < 1e-6 or abs(x - x1) < 1e-6 or abs(y - y0) < 1e-6
                 or abs(y - y1) < 1e-6)
                and x0 - 1e-6 <= x <= x1 + 1e-6 and y0 - 1e-6 <= y <= y1 + 1e-6
                for x0, y0, x1, y1 in rects)
            if on_edge:
                out.append((x, y))
    return out


def direction(p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = math.hypot(dx, dy)
    return (dx / length, dy / length), length


def centred(p1, p2, thickness):
    (dx, dy), _ = direction(p1, p2)
    nx, ny = -dy, dx
    off = thickness / 2.0
    return (p1[0] - nx * off, p1[1] - ny * off), (p2[0] - nx * off, p2[1] - ny * off)


def placement(origin, xdir=(1.0, 0.0)):
    dx, dy = xdir
    return np.array([[dx, -dy, 0.0, origin[0]], [dy, dx, 0.0, origin[1]],
                     [0.0, 0.0, 1.0, origin[2]], [0.0, 0.0, 0.0, 1.0]], dtype=float)


def box(width, depth):
    hw, hd = width / 2.0, depth / 2.0
    return [(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)]


def inset_rect(rect, t):
    x0, y0, x1, y1 = rect
    return [(x0 + t, y0 + t), (x1 - t, y0 + t), (x1 - t, y1 - t), (x0 + t, y1 - t)]


def area_of(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2.0


def rect_poly(rect, grow=0.0):
    x0, y0, x1, y1 = rect
    return [(x0 - grow, y0 - grow), (x1 + grow, y0 - grow),
            (x1 + grow, y1 + grow), (x0 - grow, y1 + grow)]


def attach_layers(f, element_type, layers, materials):
    ls = api.material.add_material_set(
        f, name=element_type.Name, set_type="IfcMaterialLayerSet")
    for name, thickness in layers:
        layer = api.material.add_layer(
            f, layer_set=ls, material=materials[name], name=name)
        layer.LayerThickness = thickness * 1000.0
    api.material.assign_material(
        f, products=[element_type], type="IfcMaterialLayerSet", material=ls)


def psets_for(f, product, stage, status, sg=None, vaf=None, verified=None):
    p = api.pset.add_pset(f, product=product, name="Bonsai_Upskilling")
    api.pset.edit_pset(f, pset=p, properties={
        "project_stage": stage, "design_status": status})
    if sg:
        s = api.pset.add_pset(f, product=product, name="IFCSG_Demo")
        api.pset.edit_pset(f, pset=s, properties=sg)
    if vaf:
        v = api.pset.add_pset(f, product=product, name="VAF_Demo")
        api.pset.edit_pset(f, pset=v, properties=vaf)
    if verified is not None:
        a = api.pset.add_pset(f, product=product, name="AsBuilt")
        api.pset.edit_pset(f, pset=a, properties={"verification": verified})


# -------------------------------------------------------------------- build --

def build(stage_key: str) -> ifcopenshell.file:
    stage, status, _ = STAGES[stage_key]
    detailed = stage_key in ("dd", "asbuilt")
    asbuilt = stage_key == "asbuilt"
    # At Stage 07 most of the building was measured; the shelter and the frame
    # were surveyed, the finishes were taken on the contractor's word.
    verified = (lambda name: "verified" if ("HS" in name or "Column" in name
                                            or "Slab" in name) else "assumed") \
        if asbuilt else (lambda name: None)

    f = api.project.create_file("IFC4")
    project = api.root.create_entity(f, "IfcProject", name="Pinwheel House")
    api.unit.assign_unit(f, units=[
        api.unit.add_si_unit(f, unit_type="LENGTHUNIT", prefix="MILLI"),
        api.unit.add_si_unit(f, unit_type="AREAUNIT"),
        api.unit.add_si_unit(f, unit_type="VOLUMEUNIT")])
    model = api.context.add_context(f, context_type="Model")
    body = api.context.add_context(
        f, context_type="Model", context_identifier="Body",
        target_view="MODEL_VIEW", parent=model)

    # SVY21 for easting and northing, SHD for height, rotated to True North.
    # Near Chatsworth Park, District 10. Read off a map, not surveyed.
    api.georeference.add_georeferencing(f)
    bearing = math.radians(12.0)
    api.georeference.edit_georeferencing(
        f,
        projected_crs={"Name": "EPSG:3414", "Description": "SVY21 / Singapore TM",
                       "GeodeticDatum": "SVY21", "VerticalDatum": "SHD"},
        coordinate_operation={"Eastings": 26240.0, "Northings": 31590.0,
                              "OrthogonalHeight": 32.500,
                              "XAxisAbscissa": math.cos(bearing),
                              "XAxisOrdinate": math.sin(bearing), "Scale": 1.0})

    site = api.root.create_entity(f, "IfcSite", name="Main Block")
    site.RefElevation = 32.500
    building = api.root.create_entity(f, "IfcBuilding", name="Pinwheel House")
    storeys = {k: api.root.create_entity(f, "IfcBuildingStorey", name=v)
               for k, v in STOREY_NAME.items()}
    roof_storey = api.root.create_entity(f, "IfcBuildingStorey", name="Roof")
    storeys["1"].Elevation = L1 * 1000.0
    storeys["2"].Elevation = L2 * 1000.0
    roof_storey.Elevation = ROOF * 1000.0
    api.aggregate.assign_object(f, products=[site], relating_object=project)
    api.aggregate.assign_object(f, products=[building], relating_object=site)
    api.aggregate.assign_object(
        f, products=[storeys["1"], storeys["2"], roof_storey], relating_object=building)

    coverage = sum((x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in footprint("1"))
    psets_for(f, site, stage, status,
              sg={"Site Area": PLOT * PLOT,
                  "Site Coverage": round(coverage / (PLOT * PLOT) * 100.0, 2),
                  "Landed Housing Type": "Good Class Bungalow"},
              vaf={"component": "Regulatory", "resource_grade": "Architect"})
    psets_for(f, building, stage, status,
              sg={"Project Development Type": "Landed housing",
                  "Owner Built Owner Stay": True},
              vaf={"component": "Design", "resource_grade": "Architect"})
    for s in list(storeys.values()) + [roof_storey]:
        psets_for(f, s, stage, status, sg={"Attic Level": False})

    materials = {n: api.material.add_material(f, name=n, category=c) for n, c in [
        ("Reinforced concrete", "concrete"), ("Structural steel", "steel"),
        ("Glass", "glass"), ("Concrete blockwork", "block"),
        ("Cement plaster", "plaster"), ("Timber decking", "wood"),
        ("Fair-faced concrete", "concrete"), ("Anodised aluminium", "aluminium"),
        ("Granite paving", "stone"), ("Asphalt", "bitumen"),
        ("Topsoil and turf", "soil"), ("Planting", "vegetation")]}

    types = {}
    types["HS"] = api.root.create_entity(f, "IfcWallType", predefined_type="SOLIDWALL",
                                         name="HS-250-RC")
    types["CORE"] = api.root.create_entity(f, "IfcWallType", predefined_type="SOLIDWALL",
                                           name="CORE-200-RC")
    types["INT"] = api.root.create_entity(f, "IfcWallType", predefined_type="SOLIDWALL",
                                          name="INT-100-BLK")
    attach_layers(f, types["HS"], [("Reinforced concrete", 0.250)], materials)
    attach_layers(f, types["CORE"], [("Reinforced concrete", 0.200)], materials)
    attach_layers(f, types["INT"], [("Cement plaster", 0.010),
                                    ("Concrete blockwork", 0.080),
                                    ("Cement plaster", 0.010)], materials)
    slab_t = api.root.create_entity(f, "IfcSlabType", predefined_type="FLOOR",
                                    name="SLAB-RC-250")
    roof_t = api.root.create_entity(f, "IfcSlabType", predefined_type="ROOF",
                                    name="ROOF-RC-200")
    attach_layers(f, slab_t, [("Reinforced concrete", 0.250)], materials)
    attach_layers(f, roof_t, [("Reinforced concrete", 0.200)], materials)
    col_t = api.root.create_entity(f, "IfcColumnType", predefined_type="COLUMN",
                                   name="COL-SHS-200")
    api.material.assign_material(f, products=[col_t], type="IfcMaterial",
                                 material=materials["Structural steel"])
    cw_t = api.root.create_entity(f, "IfcCurtainWallType", predefined_type="NOTDEFINED",
                                  name="CW-GLAZED")
    plate_t = api.root.create_entity(f, "IfcPlateType", predefined_type="CURTAIN_PANEL",
                                      name="GL-PLATE")
    api.material.assign_material(f, products=[plate_t], type="IfcMaterial",
                                 material=materials["Glass"])
    door_t = {}
    for w in sorted({d[3] for d in DOORS}):
        dt = api.root.create_entity(f, "IfcDoorType", predefined_type="DOOR",
                                    name=f"DR-{int(w * 1000)}")
        # A door with no material cannot be scheduled, priced or specified.
        api.material.assign_material(
            f, products=[dt], type="IfcMaterial",
            material=materials["Timber decking" if w < 1.2 else "Glass"])
        door_t[w] = dt

    # ---- the shelter tower and what little else is solid
    walls = {}
    for tag, (p1, p2, key, on) in WALLS.items():
        for sk in on:
            t = THICKNESS[key]
            # The shelter is founded: its walls start at ground, not at the
            # floor plane the rest of the house stands on.
            base = 0.0 if (key == "HS" and sk == "1") else STOREY_Z[sk]
            height = (STOREY_Z["1"] + STOREY_H - base) if (key == "HS" and sk == "1") \
                else STOREY_H
            wall = api.root.create_entity(f, "IfcWall", name=f"{tag}-L{sk}")
            a, b = centred(p1, p2, t)
            rep = api.geometry.create_2pt_wall(
                f, element=wall, context=body, p1=a, p2=b, elevation=base,
                height=height, thickness=t, is_si=True)
            api.geometry.assign_representation(f, product=wall, representation=rep)
            api.type.assign_type(f, related_objects=[wall], relating_type=types[key])
            api.spatial.assign_container(f, products=[wall], relating_structure=storeys[sk])
            pc = api.pset.add_pset(f, product=wall, name="Pset_WallCommon")
            api.pset.edit_pset(f, pset=pc, properties={
                "IsExternal": False, "LoadBearing": key in ("HS", "CORE")})
            psets_for(f, wall, stage, status,
                      sg={"Construction Method": "Cast in-situ"
                          if key in ("HS", "CORE") else "Masonry"},
                      vaf={"component": "Structure" if key in ("HS", "CORE")
                           else "Space Planning", "resource_grade": "Architect"},
                      verified=verified(wall.Name))
            walls[(tag, sk)] = (wall, p1, p2, t)

    # ---- floor plates and the roof, each stepping back from the one below
    for sk, host in (("1", storeys["1"]), ("2", storeys["2"])):
        for i, r in enumerate(footprint(sk), start=1):
            slab = api.root.create_entity(f, "IfcSlab", predefined_type="FLOOR",
                                          name=f"A-Slabs-L{sk}-{i:02d}")
            rep = api.geometry.add_slab_representation(
                f, context=body, depth=0.250, polyline=rect_poly(r))
            api.geometry.assign_representation(f, product=slab, representation=rep)
            api.geometry.edit_object_placement(
                f, product=slab, matrix=placement((0, 0, STOREY_Z[sk] - 0.250)), is_si=True)
            api.type.assign_type(f, related_objects=[slab], relating_type=slab_t)
            api.spatial.assign_container(f, products=[slab], relating_structure=host)
            psets_for(f, slab, stage, status,
                      vaf={"component": "Structure", "resource_grade": "Architect"},
                      verified=verified(slab.Name))

    roof = api.root.create_entity(f, "IfcRoof", predefined_type="FLAT_ROOF",
                                  name="A-Roof-Main")
    api.spatial.assign_container(f, products=[roof], relating_structure=roof_storey)
    for i, r in enumerate(footprint("2"), start=1):
        rs = api.root.create_entity(f, "IfcSlab", predefined_type="ROOF",
                                    name=f"A-Roof-Slab-{i:02d}")
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=0.200, polyline=rect_poly(r, grow=EAVE))
        api.geometry.assign_representation(f, product=rs, representation=rep)
        api.geometry.edit_object_placement(
            f, product=rs, matrix=placement((0, 0, ROOF)), is_si=True)
        api.type.assign_type(f, related_objects=[rs], relating_type=roof_t)
        api.aggregate.assign_object(f, products=[rs], relating_object=roof)
        psets_for(f, rs, stage, status,
                  vaf={"component": "Envelope", "resource_grade": "Architect"},
                  verified=verified(rs.Name))

    # ---- the steel frame that lifts the house off the ground
    n_col = 0
    for sk in ("1", "2"):
        base = 0.0 if sk == "1" else STOREY_Z["2"]
        top = STOREY_Z["1"] if sk == "1" else ROOF
        for (x, y) in columns_for(sk):
            n_col += 1
            c = api.root.create_entity(f, "IfcColumn", predefined_type="COLUMN",
                                       name=f"A-Columns-L{sk}-{n_col:03d}")
            rep = api.geometry.add_slab_representation(
                f, context=body, depth=top - base, polyline=box(COL, COL))
            api.geometry.assign_representation(f, product=c, representation=rep)
            api.geometry.edit_object_placement(
                f, product=c, matrix=placement((x, y, base)), is_si=True)
            api.type.assign_type(f, related_objects=[c], relating_type=col_t)
            api.spatial.assign_container(f, products=[c], relating_structure=storeys[sk])
            pc = api.pset.add_pset(f, product=c, name="Pset_ColumnCommon")
            api.pset.edit_pset(f, pset=pc, properties={"IsExternal": sk == "1",
                                                        "LoadBearing": True})
            psets_for(f, c, stage, status,
                      vaf={"component": "Structure", "resource_grade": "Architect"},
                      verified=verified(c.Name))
    # ---- the protective plinth: what makes the shelter compliant at ground
    # Four 200mm RC walls at the required clear distances, enclosing plant and
    # store. Everything outside them stays open undercroft.
    px0, py0, px1, py1 = PLINTH
    plinth_lines = [("S", (px0, py0), (px1, py0)), ("E", (px1, py0), (px1, py1)),
                    ("N", (px1, py1), (px0, py1)), ("W", (px0, py1), (px0, py0))]
    for tag, a, b in plinth_lines:
        w = api.root.create_entity(f, "IfcWall", predefined_type="SOLIDWALL",
                                   name=f"A-Walls-Plinth-{tag}")
        ca, cb = centred(a, b, T_PLINTH)
        rep = api.geometry.create_2pt_wall(
            f, element=w, context=body, p1=ca, p2=cb, elevation=0.0,
            height=UNDERCROFT, thickness=T_PLINTH, is_si=True)
        api.geometry.assign_representation(f, product=w, representation=rep)
        api.type.assign_type(f, related_objects=[w], relating_type=types["CORE"])
        api.spatial.assign_container(f, products=[w], relating_structure=storeys["1"])
        pc = api.pset.add_pset(f, product=w, name="Pset_WallCommon")
        api.pset.edit_pset(f, pset=pc, properties={"IsExternal": True,
                                                    "LoadBearing": True})
        psets_for(f, w, stage, status,
                  sg={"Construction Method": "Cast in-situ"},
                  vaf={"component": "Structure", "resource_grade": "Architect"},
                  verified=verified("HS"))

    plinth_slab = api.root.create_entity(f, "IfcSlab", predefined_type="BASESLAB",
                                         name="A-Slabs-Plinth")
    rep = api.geometry.add_slab_representation(
        f, context=body, depth=0.300, polyline=rect_poly(PLINTH))
    api.geometry.assign_representation(f, product=plinth_slab, representation=rep)
    api.geometry.edit_object_placement(
        f, product=plinth_slab, matrix=placement((0, 0, -0.300)), is_si=True)
    api.type.assign_type(f, related_objects=[plinth_slab], relating_type=slab_t)
    api.spatial.assign_container(f, products=[plinth_slab],
                                 relating_structure=storeys["1"])
    psets_for(f, plinth_slab, stage, status,
              vaf={"component": "Structure", "resource_grade": "Architect"},
              verified="verified" if asbuilt else None)

    plant = api.root.create_entity(f, "IfcSpace", predefined_type="INTERNAL",
                                   name="Plant and Store")
    plant.LongName = "Plant and store, within the shelter's protective plinth"
    plant.CompositionType = "ELEMENT"
    poly = inset_rect(PLINTH, T_PLINTH)
    rep = api.geometry.add_slab_representation(
        f, context=body, depth=UNDERCROFT - 0.1, polyline=poly)
    api.geometry.assign_representation(f, product=plant, representation=rep)
    api.geometry.edit_object_placement(f, product=plant, matrix=placement((0, 0, 0.0)),
                                       is_si=True)
    api.aggregate.assign_object(f, products=[plant], relating_object=storeys["1"])
    pc = api.pset.add_pset(f, product=plant, name="Pset_SpaceCommon")
    api.pset.edit_pset(f, pset=pc, properties={"IsExternal": False, "Reference": "00"})
    q = api.pset.add_qto(f, product=plant, name="Qto_SpaceBaseQuantities")
    api.pset.edit_qto(f, qto=q, properties={"NetFloorArea": round(area_of(poly), 3),
                                             "FinishCeilingHeight": UNDERCROFT - 0.1})
    psets_for(f, plant, stage, status,
              sg={"Space Name": "Plant and Store", "Area": round(area_of(poly), 2),
                  "HS Protection Door Side": HS_PROTECT_DOOR,
                  "HS Protection Other Sides": HS_PROTECT_OTHER},
              vaf={"component": "Space Planning", "resource_grade": "Architect"})

    # ---- the glazed envelope: glass between structure, set back under the eaves
    plates = 0
    if detailed:
        for sk in ("1", "2"):
            for j, ((ax, ay), (bx, by)) in enumerate(external_faces(sk), start=1):
                cw = api.root.create_entity(
                    f, "IfcCurtainWall", predefined_type="NOTDEFINED",
                    name=f"A-Glazing-L{sk}-{j:02d}")
                api.type.assign_type(f, related_objects=[cw], relating_type=cw_t)
                api.spatial.assign_container(
                    f, products=[cw], relating_structure=storeys[sk])
                pc = api.pset.add_pset(f, product=cw, name="Pset_CurtainWallCommon")
                api.pset.edit_pset(f, pset=pc, properties={"IsExternal": True})
                psets_for(f, cw, stage, status,
                          vaf={"component": "Envelope", "resource_grade": "Architect"},
                          verified=verified(cw.Name))

                plates += 1
                plate = api.root.create_entity(
                    f, "IfcPlate", predefined_type="CURTAIN_PANEL",
                    name=f"A-Glazing-L{sk}-{j:02d}-P")
                (dx, dy), span = direction((ax, ay), (bx, by))
                rep = api.geometry.add_slab_representation(
                    f, context=body, depth=STOREY_H - 0.250,
                    polyline=box(span, 0.024))
                api.geometry.assign_representation(f, product=plate, representation=rep)
                api.geometry.edit_object_placement(
                    f, product=plate,
                    matrix=placement(((ax + bx) / 2.0, (ay + by) / 2.0, STOREY_Z[sk]),
                                     (dx, dy)), is_si=True)
                api.type.assign_type(f, related_objects=[plate], relating_type=plate_t)
                api.aggregate.assign_object(f, products=[plate], relating_object=cw)
                psets_for(f, plate, stage, status,
                          vaf={"component": "Envelope", "resource_grade": "Architect"})

    # ---- openings
    if detailed:
        for mark, host, dist, width, height, sill, sk, main in DOORS:
            wall, p1, p2, thickness = walls[(host, sk)]
            (dx, dy), _ = direction(p1, p2)
            origin = (p1[0] + dx * dist, p1[1] + dy * dist, STOREY_Z[sk] + sill)
            op = api.root.create_entity(f, "IfcOpeningElement", predefined_type="OPENING",
                                        name=f"A-Openings-{mark}")
            rep = api.geometry.add_slab_representation(
                f, context=body, depth=height, polyline=box(width, thickness + 0.100))
            api.geometry.assign_representation(f, product=op, representation=rep)
            api.geometry.edit_object_placement(
                f, product=op, matrix=placement(origin, (dx, dy)), is_si=True)
            api.feature.add_feature(f, feature=op, element=wall)

            d = api.root.create_entity(f, "IfcDoor", predefined_type="DOOR",
                                       name=f"A-Doors-{mark}")
            d.OverallWidth, d.OverallHeight, d.Tag = width * 1000.0, height * 1000.0, mark
            rep = api.geometry.add_slab_representation(
                f, context=body, depth=height, polyline=box(width, thickness * 0.5))
            api.geometry.assign_representation(f, product=d, representation=rep)
            api.geometry.edit_object_placement(
                f, product=d, matrix=placement(origin, (dx, dy)), is_si=True)
            api.type.assign_type(f, related_objects=[d], relating_type=door_t[width])
            api.spatial.assign_container(f, products=[d], relating_structure=storeys[sk])
            api.feature.add_filling(f, opening=op, element=d)
            pc = api.pset.add_pset(f, product=d, name="Pset_DoorCommon")
            api.pset.edit_pset(f, pset=pc, properties={"Reference": mark})
            psets_for(f, d, stage, status,
                      sg={"Main Entrance": main,
                          "Clear Width": round(width * 1000),
                          "Clear Height": round(height * 1000)},
                      vaf={"component": "Envelope" if main else "Space Planning",
                           "resource_grade": "Architect"})

    # ---- spaces
    for number, name, long_name, rect, sk, external in SPACES:
        sp = api.root.create_entity(
            f, "IfcSpace", predefined_type="EXTERNAL" if external else "INTERNAL",
            name=name)
        sp.LongName = long_name
        sp.CompositionType = "ELEMENT"
        t = T_HS if name in ("Household Shelter", "Bathroom 2") else T_INT
        poly = inset_rect(rect, t)
        height = HS_CLEAR if name in ("Household Shelter", "Bathroom 2") \
            else (0.050 if external else STOREY_H - 0.250)
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=height, polyline=poly)
        api.geometry.assign_representation(f, product=sp, representation=rep)
        api.geometry.edit_object_placement(
            f, product=sp, matrix=placement((0, 0, STOREY_Z[sk])), is_si=True)
        api.aggregate.assign_object(f, products=[sp], relating_object=storeys[sk])

        pc = api.pset.add_pset(f, product=sp, name="Pset_SpaceCommon")
        api.pset.edit_pset(f, pset=pc, properties={
            "IsExternal": external, "Reference": number})
        qto = api.pset.add_qto(f, product=sp, name="Qto_SpaceBaseQuantities")
        api.pset.edit_qto(f, qto=qto, properties={
            "NetFloorArea": round(area_of(poly), 3),
            "FinishCeilingHeight": round(height, 3)})

        sg = {"Space Name": name, "Area": round(area_of(poly), 2)}
        if name == "Household Shelter":
            x0, y0, x1, y1 = rect
            sg.update({"Construction Method": "Cast in-situ reinforced concrete",
                       "Internal Length": round((y1 - y0 - 2 * T_HS) * 1000),
                       "Internal Width": round((x1 - x0 - 2 * T_HS) * 1000),
                       "Clear Height": round(HS_CLEAR * 1000)})
        if name in ("Living", "Dining", "Kitchen", "Stair", "Household Shelter", "Guest"):
            sg["Barrier Free Accessibility"] = True
        psets_for(f, sp, stage, status, sg=sg,
                  vaf={"component": "Space Planning", "resource_grade": "Architect"},
                  verified=verified(sp.Name))

    # ---- gross floor area, as IFC+SG asks for it: a space, not a spreadsheet cell
    for sk in ("1", "2"):
        gfa = api.root.create_entity(f, "IfcSpace", predefined_type="USERDEFINED",
                                     name=f"GFA {STOREY_NAME[sk]}")
        gfa.ObjectType = "AREA_GFA"
        gfa.LongName = f"Gross floor area, {STOREY_NAME[sk]}"
        gfa.CompositionType = "ELEMENT"
        area = 0.0
        for i, r in enumerate(footprint(sk), start=1):
            area += (r[2] - r[0]) * (r[3] - r[1])
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=0.050, polyline=rect_poly(footprint(sk)[0]))
        api.geometry.assign_representation(f, product=gfa, representation=rep)
        api.geometry.edit_object_placement(
            f, product=gfa, matrix=placement((0, 0, STOREY_Z[sk])), is_si=True)
        api.aggregate.assign_object(f, products=[gfa], relating_object=storeys[sk])
        psets_for(f, gfa, stage, status,
                  sg={"AGF_Name": f"GFA {STOREY_NAME[sk]}",
                      "AGF_Development Use": "Landed housing",
                      "AGF_Use Quantum": round(area, 2)},
                  vaf={"component": "Regulatory", "resource_grade": "Architect"})

    # ---- detail: mullions, balustrades, the stair and the shading fins
    # A model with no detail cannot be read as a design. These decide how the
    # building looks, and they belong in Design Development, not in a rendering.
    if detailed:
        mull_t = api.root.create_entity(f, "IfcMemberType", predefined_type="MULLION",
                                        name="MULL-ALU-50X150")
        api.material.assign_material(f, products=[mull_t], type="IfcMaterial",
                                     material=materials["Anodised aluminium"])
        rail_t = api.root.create_entity(f, "IfcRailingType", predefined_type="BALUSTRADE",
                                        name="BAL-STEEL-1000")
        api.material.assign_material(f, products=[rail_t], type="IfcMaterial",
                                     material=materials["Structural steel"])
        fin_t = api.root.create_entity(f, "IfcShadingDeviceType",
                                       predefined_type="USERDEFINED",
                                       name="FIN-ALU-VERTICAL")
        fin_t.ElementType = "Vertical shading fin"
        api.material.assign_material(f, products=[fin_t], type="IfcMaterial",
                                     material=materials["Anodised aluminium"])

        n_m = n_f = 0
        for sk in ("1", "2"):
            for ((ax, ay), (bx, by)) in external_faces(sk):
                (dx, dy), span = direction((ax, ay), (bx, by))
                for tpos in (0.0, 1.0):
                    n_m += 1
                    mx, my = ax + (bx - ax) * tpos, ay + (by - ay) * tpos
                    m = api.root.create_entity(f, "IfcMember", predefined_type="MULLION",
                                               name=f"A-Mullions-L{sk}-{n_m:03d}")
                    rep = api.geometry.add_slab_representation(
                        f, context=body, depth=STOREY_H - 0.250,
                        polyline=box(0.050, 0.150))
                    api.geometry.assign_representation(f, product=m, representation=rep)
                    api.geometry.edit_object_placement(
                        f, product=m,
                        matrix=placement((mx, my, STOREY_Z[sk]), (dx, dy)), is_si=True)
                    api.type.assign_type(f, related_objects=[m], relating_type=mull_t)
                    api.spatial.assign_container(f, products=[m],
                                                 relating_structure=storeys[sk])
                    psets_for(f, m, stage, status,
                              vaf={"component": "Envelope",
                                   "resource_grade": "Architect"})
                # vertical fins where the sun comes in low: the east and west faces
                if abs(dy) > 0.5:
                    for k in (1, 2):
                        n_f += 1
                        fx = ax + (bx - ax) * (k / 3.0)
                        fy = ay + (by - ay) * (k / 3.0)
                        fin = api.root.create_entity(
                            f, "IfcShadingDevice", predefined_type="USERDEFINED",
                            name=f"A-Shading-L{sk}-{n_f:03d}")
                        rep = api.geometry.add_slab_representation(
                            f, context=body, depth=STOREY_H - 0.250,
                            polyline=box(0.040, 0.450))
                        api.geometry.assign_representation(f, product=fin,
                                                           representation=rep)
                        api.geometry.edit_object_placement(
                            f, product=fin,
                            matrix=placement((fx, fy, STOREY_Z[sk]), (dx, dy)),
                            is_si=True)
                        api.type.assign_type(f, related_objects=[fin],
                                             relating_type=fin_t)
                        api.spatial.assign_container(f, products=[fin],
                                                     relating_structure=storeys[sk])
                        psets_for(f, fin, stage, status,
                                  vaf={"component": "Envelope",
                                       "resource_grade": "Architect"})

        for name, rect in (("Terrace-S", WINGS["S"][:4]), ("Terrace-W", WINGS["W"][:4])):
            x0, y0, x1, y1 = rect
            for tag, a, b in (("S", (x0, y0), (x1, y0)), ("E", (x1, y0), (x1, y1)),
                              ("N", (x1, y1), (x0, y1)), ("W", (x0, y1), (x0, y0))):
                r = api.root.create_entity(f, "IfcRailing", predefined_type="BALUSTRADE",
                                           name=f"A-Railings-{name}-{tag}")
                (dx, dy), span = direction(a, b)
                rep = api.geometry.add_slab_representation(
                    f, context=body, depth=1.000, polyline=box(span, 0.050))
                api.geometry.assign_representation(f, product=r, representation=rep)
                api.geometry.edit_object_placement(
                    f, product=r,
                    matrix=placement(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, L2), (dx, dy)),
                    is_si=True)
                api.type.assign_type(f, related_objects=[r], relating_type=rail_t)
                api.spatial.assign_container(f, products=[r],
                                             relating_structure=storeys["2"])
                psets_for(f, r, stage, status,
                          vaf={"component": "Envelope", "resource_grade": "Architect"})

        for sk, base, top in (("1", 0.0, L1), ("2", L1, L2)):
            st = api.root.create_entity(f, "IfcStair",
                                        predefined_type="STRAIGHT_RUN_STAIR",
                                        name=f"A-Stairs-L{sk}")
            rep = api.geometry.add_slab_representation(
                f, context=body, depth=top - base,
                polyline=[(19.2, 21.0), (23.4, 21.0), (23.4, 23.4), (19.2, 23.4)])
            api.geometry.assign_representation(f, product=st, representation=rep)
            api.geometry.edit_object_placement(
                f, product=st, matrix=placement((0, 0, base)), is_si=True)
            api.spatial.assign_container(f, products=[st], relating_structure=storeys[sk])
            api.material.assign_material(f, products=[st], type="IfcMaterial",
                                         material=materials["Fair-faced concrete"])
            pc = api.pset.add_pset(f, product=st, name="Pset_StairCommon")
            api.pset.edit_pset(f, pset=pc, properties={"NumberOfRiser": 10,
                                                        "IsExternal": sk == "1"})
            psets_for(f, st, stage, status,
                      vaf={"component": "Space Planning", "resource_grade": "Architect"},
                      verified=verified("Slab"))

        cov_t = api.root.create_entity(f, "IfcCoveringType", predefined_type="FLOORING",
                                       name="FIN-GRANITE-20")
        api.material.assign_material(f, products=[cov_t], type="IfcMaterial",
                                     material=materials["Granite paving"])
        for sk in ("1", "2"):
            for i, r in enumerate(footprint(sk), start=1):
                c = api.root.create_entity(f, "IfcCovering", predefined_type="FLOORING",
                                           name=f"A-Finishes-L{sk}-{i:02d}")
                rep = api.geometry.add_slab_representation(
                    f, context=body, depth=0.020, polyline=rect_poly(r))
                api.geometry.assign_representation(f, product=c, representation=rep)
                api.geometry.edit_object_placement(
                    f, product=c, matrix=placement((0, 0, STOREY_Z[sk])), is_si=True)
                api.type.assign_type(f, related_objects=[c], relating_type=cov_t)
                api.spatial.assign_container(f, products=[c],
                                             relating_structure=storeys[sk])
                psets_for(f, c, stage, status,
                          vaf={"component": "Envelope", "resource_grade": "Architect"},
                          verified="assumed" if asbuilt else None)

    # ---- the site: terrain, road, boundary, driveway, neighbours, trees
    def site_thing(cls, name, poly, base, depth, material, pdt=None):
        kw = {"predefined_type": pdt} if pdt else {}
        e = api.root.create_entity(f, cls, name=name, **kw)
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=depth, polyline=poly)
        api.geometry.assign_representation(f, product=e, representation=rep)
        api.geometry.edit_object_placement(
            f, product=e, matrix=placement((0, 0, base)), is_si=True)
        api.spatial.assign_container(f, products=[e], relating_structure=site)
        api.material.assign_material(f, products=[e], type="IfcMaterial",
                                     material=materials[material])
        psets_for(f, e, stage, status,
                  vaf={"component": "Site", "resource_grade": "Architect"})
        return e

    site_thing("IfcGeographicElement", "X-Site-Terrain",
               [(-40.0, -12.0), (80.0, -12.0), (80.0, 80.0), (-40.0, 80.0)],
               -0.300, 0.300, "Topsoil and turf", pdt="TERRAIN")
    site_thing("IfcGeographicElement", "X-Site-Road",
               [(-40.0, -ROAD_DEPTH), (80.0, -ROAD_DEPTH), (80.0, -0.5), (-40.0, -0.5)],
               -0.020, 0.100, "Asphalt", pdt="USERDEFINED")
    drive = site_thing("IfcSlab", "A-Site-Driveway", rect_poly(DRIVEWAY), 0.0, 0.120,
                       "Granite paving", pdt="BASESLAB")
    api.type.assign_type(f, related_objects=[drive], relating_type=slab_t)

    for tag, a, b in (("S1", (0.0, 0.0), (17.5, 0.0)), ("S2", (23.5, 0.0), (PLOT, 0.0)),
                      ("E", (PLOT, 0.0), (PLOT, PLOT)), ("N", (PLOT, PLOT), (0.0, PLOT)),
                      ("W", (0.0, PLOT), (0.0, 0.0))):
        w = api.root.create_entity(f, "IfcWall", predefined_type="SOLIDWALL",
                                   name=f"A-Walls-Boundary-{tag}")
        ca, cb = centred(a, b, 0.150)
        rep = api.geometry.create_2pt_wall(
            f, element=w, context=body, p1=ca, p2=cb, elevation=0.0,
            height=BOUNDARY_WALL_H, thickness=0.150, is_si=True)
        api.geometry.assign_representation(f, product=w, representation=rep)
        api.type.assign_type(f, related_objects=[w], relating_type=types["INT"])
        api.spatial.assign_container(f, products=[w], relating_structure=site)
        pc = api.pset.add_pset(f, product=w, name="Pset_WallCommon")
        api.pset.edit_pset(f, pset=pc, properties={"IsExternal": True,
                                                    "LoadBearing": False})
        psets_for(f, w, stage, status,
                  sg={"Boundary Wall Height": BOUNDARY_WALL_H * 1000},
                  vaf={"component": "Site", "resource_grade": "Architect"})

    for name, x0, y0, x1, y1, h in NEIGHBOURS:
        e = site_thing("IfcBuildingElementProxy", f"X-{name}",
                       [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 0.0, h,
                       "Concrete blockwork")
        api.pset.edit_pset(
            f, pset=api.pset.add_pset(f, product=e, name="Context"),
            properties={"role": "Neighbouring building, context only",
                        "in_scope": False})

    for i, (cx, cy, r) in enumerate(TREES, start=1):
        n = 12
        crown = [(cx + r * math.cos(2 * math.pi * k / n),
                  cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
        site_thing("IfcGeographicElement", f"X-Site-Tree-{i:02d}", crown, 3.0, 6.0,
                   "Planting", pdt="USERDEFINED")

    # ---- the bungalow already standing on the plot
    # It exists at Concept, because the site plan must show what is there. It is
    # gone by Design Development, because by then it has been demolished. A
    # demolition nobody modelled is a demolition nobody priced.
    if stage_key == "concept":
        x0, y0, x1, y1, h = EXISTING
        old_b = api.root.create_entity(f, "IfcBuildingElementProxy",
                                       name="Z-Existing-Bungalow")
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=h, polyline=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
        api.geometry.assign_representation(f, product=old_b, representation=rep)
        api.geometry.edit_object_placement(f, product=old_b,
                                           matrix=placement((0, 0, 0.0)), is_si=True)
        api.spatial.assign_container(f, products=[old_b], relating_structure=site)
        api.material.assign_material(f, products=[old_b], type="IfcMaterial",
                                     material=materials["Concrete blockwork"])
        api.pset.edit_pset(
            f, pset=api.pset.add_pset(f, product=old_b, name="Demolition"),
            properties={"status": "TO BE DEMOLISHED",
                        "note": "Existing bungalow. Demolished before Stage 04."})
        psets_for(f, old_b, stage, "superseded",
                  vaf={"component": "Site", "resource_grade": "Architect"})

    # ---- grid, on the module the whole plan turns about
    grid = api.root.create_entity(f, "IfcGrid", name="A-Grid")
    api.spatial.assign_container(f, products=[grid], relating_structure=storeys["1"])
    for tag, x in zip(GRID_TAGS, GRID_X):
        ax = api.grid.create_grid_axis(f, grid=grid, axis_tag=tag, uvw_axes="UAxes")
        api.grid.create_axis_curve(f, p1=np.array([x, 6.0, 0.0]),
                                   p2=np.array([x, 34.0, 0.0]), grid_axis=ax, is_si=True)
    for i, y in enumerate(GRID_Y, start=1):
        ax = api.grid.create_grid_axis(f, grid=grid, axis_tag=str(i), uvw_axes="VAxes")
        api.grid.create_axis_curve(f, p1=np.array([6.0, y, 0.0]),
                                   p2=np.array([34.0, y, 0.0]), grid_axis=ax, is_si=True)

    print(f"  {stage}: {n_col} columns, {plates} glazed panels, "
          f"coverage {coverage / (PLOT * PLOT) * 100:.1f}%")
    return f


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", choices=list(STAGES), default="dd")
    ap.add_argument("--all", action="store_true", help="build all three stages")
    args = ap.parse_args()

    for key in (list(STAGES) if args.all else [args.stage]):
        model = build(key)
        out = HERE / STAGES[key][2]
        model.write(str(out))
        print(f"wrote {out.name}")
        for cls in ("IfcColumn", "IfcSlab", "IfcRoof", "IfcWall", "IfcCurtainWall",
                    "IfcPlate", "IfcMember", "IfcShadingDevice", "IfcRailing",
                    "IfcStair", "IfcCovering", "IfcDoor", "IfcSpace",
                    "IfcGeographicElement", "IfcBuildingElementProxy",
                    "IfcBuildingStorey", "IfcGrid"):
            n = len(model.by_type(cls))
            if n:
                print(f"    {cls:20} {n}")
