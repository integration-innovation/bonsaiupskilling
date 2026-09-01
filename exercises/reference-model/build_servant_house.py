"""Build the Servant and Served House as IFC4, to Singapore conventions.

    python exercises/reference-model/build_servant_house.py

Writes SERV-A-SCH-P03.ifc beside this script: the model at the end of Stage 03,
Schematic Design.

WHY THIS HOUSE EXISTS
---------------------
The course needs one worked example that actually exercises IFC+SG and the VAF.
A famous foreign building cannot: it has no household shelter, it is not on
SVY21, and it will never be put through CORENET X. The Farnsworth model in this
repository is an excellent study of measurement and provenance and a poor study
of Singapore delivery, which is why both exist.

So this building is designed for the course, and the course owns it outright.

THE IDEA, AND WHY IT IS FREE TO USE
-----------------------------------
The parti is Louis Kahn's distinction between SERVANT and SERVED space: the
solid, founded, immovable masses that carry stairs, water, waste and shelter,
and the light, open, changeable rooms that live between them.

That is a *concept*, and 17 U.S.C. 102(b) is explicit that copyright never
extends to "any idea, procedure, process, system, method of operation, concept,
principle, or discovery, regardless of the form in which it is described,
explained, illustrated, or embodied". Kahn's drawings are protected until
roughly 2044. Kahn's idea is not protected at all, and never was.

No drawing of Kahn's -- or anyone's -- was consulted, traced or adapted. The
house below is an original design, and its copyright belongs to this course.

WHY THE IDEA FITS SINGAPORE EXACTLY
-----------------------------------
SCDF's Technical Requirements for Household Shelters describe the shelter as an
"HS tower": 250mm reinforced concrete for landed housing, founded, structurally
continuous to ground, with a minimum internal width of 1200mm, a maximum
internal slab length of 4000mm and a maximum internal floor area of 4.8 square
metres, at a clear height between 2400 and 3900mm.

A founded, structurally continuous, immovable concrete tower is *precisely* a
Kahn servant space. So this design stops treating the shelter as a regulatory
nuisance to be hidden in a corner and makes it the thing the plan is organised
around -- which is also what the brief means when it says the shelter is one of
the few rooms whose walls you do not get to move.

The tropical logic is the same move. Solid servant towers close the east and
west ends, where the low sun is punishing; the served volume between them opens
north and south for cross-ventilation; and a full-height light well pulls
daylight down and lets hot air out at the top.

    W SERVANT TOWER          SERVED VOLUME           E SERVANT TOWER
    shelter, utility,   |  living, dining,      |   stair, bathrooms,
    store, light well   |  kitchen, bedrooms    |   WC
    solid, founded      |  open, glazed N/S     |   solid, founded

DIMENSIONS
----------
Everything is a whole number of a 1.2m module, which is not arbitrary: 1200mm is
SCDF's minimum internal width for a household shelter. The regulation sets the
grain of the building.

WHAT TO CHECK YOURSELF
----------------------
The shelter dimensions here satisfy the 2023 requirements as this script reads
them. They are a teaching example and not a compliance submission. The course's
own rule applies with full force: find the current requirement yourself, record
it with its source and the date you read it, and do not trust a number because a
model contained it.

Requires ifcopenshell 0.8.x.  Licensed GPL-3.0-or-later, matching Bonsai.
"""

from __future__ import annotations

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

OUT = Path(__file__).resolve().parent / "SERV-A-SCH-P03.ifc"

# ---------------------------------------------------------------- dimensions --
# Metres. Origin at the south-west corner of the building, +Y is project north.
# The road is to the south.

M = 1.2                      # the module: SCDF's minimum internal HS width
FFL = 0.150                  # 1st Storey finished floor level
STOREY_H = 3.600
L2 = FFL + STOREY_H          # 2nd Storey
ROOF = L2 + STOREY_H         # Roof
EAVE = 1.200                 # deep overhang, because this is the tropics

T_EXT, T_INT, T_TOWER, T_HS = 0.200, 0.100, 0.200, 0.250

# Plan zones, east-west. Solid at the ends, open in the middle.
W_TOWER = (0.0, 3.6)         # west servant tower
SERVED = (3.6, 9.6)          # served volume, glazed north and south
E_TOWER = (9.6, 13.2)        # east servant tower
DEPTH = 9.6                  # north-south

# The household shelter, sized to the 2023 requirements.
#   internal 1.5 x 3.2 = 4.80 m2   (max 4.8 m2, min width 1.2 m, max length 4.0 m)
#   walls 250mm  ->  gross 2.0 x 3.7
HS = (0.0, 0.0, 2.0, 3.7)
HS_CLEAR = 2.700             # between SCDF's 2.4 m and 3.9 m

# The light well: full height, open to the sky, at the north end of the west
# tower. Daylight down, hot air out.
WELL = (0.0, 6.0, 3.6, 9.6)

# tag: (p1, p2, type key, which storeys)
# The servant towers and the shelter run the full height of the building --
# that is what makes them towers, and it is what SCDF requires of the shelter.
WALLS: dict[str, tuple[tuple[float, float], tuple[float, float], str, str]] = {
    # --- external envelope, both storeys
    "A-Walls-Ext-South":      ((0.0, 0.0), (13.2, 0.0), "EXT", "12"),
    "A-Walls-Ext-East":       ((13.2, 0.0), (13.2, 9.6), "EXT", "12"),
    "A-Walls-Ext-North":      ((13.2, 9.6), (0.0, 9.6), "EXT", "12"),
    "A-Walls-Ext-West":       ((0.0, 9.6), (0.0, 0.0), "EXT", "12"),
    # --- the two servant towers, reinforced concrete, founded, full height
    "A-Walls-Tower-W-East":   ((3.6, 0.0), (3.6, 9.6), "TOWER", "12"),
    "A-Walls-Tower-E-West":   ((9.6, 0.0), (9.6, 9.6), "TOWER", "12"),
    # --- the household shelter tower, 250mm RC, founded, continuous to roof
    "A-Walls-HS-South":       ((0.0, 0.0), (2.0, 0.0), "HS", "12"),
    "A-Walls-HS-East":        ((2.0, 0.0), (2.0, 3.7), "HS", "12"),
    "A-Walls-HS-North":       ((2.0, 3.7), (0.0, 3.7), "HS", "12"),
    "A-Walls-HS-West":        ((0.0, 3.7), (0.0, 0.0), "HS", "12"),
    # --- partitions inside the towers
    "A-Walls-Int-W02":        ((0.0, 6.0), (3.6, 6.0), "INT", "12"),
    "A-Walls-Int-E01":        ((9.6, 2.4), (13.2, 2.4), "INT", "12"),
    "A-Walls-Int-E02":        ((9.6, 6.0), (13.2, 6.0), "INT", "12"),
    # --- the served volume: one partition below, two above
    "A-Walls-Int-S01":        ((3.6, 6.0), (9.6, 6.0), "INT", "1"),
    "A-Walls-Int-S02":        ((3.6, 4.0), (9.6, 4.0), "INT", "2"),
    "A-Walls-Int-S03":        ((3.6, 7.0), (9.6, 7.0), "INT", "2"),
}

THICKNESS = {"EXT": T_EXT, "INT": T_INT, "TOWER": T_TOWER, "HS": T_HS}

OUTER = [(-0.1, -0.1), (13.3, -0.1), (13.3, 9.7), (-0.1, 9.7)]
ROOF_EDGE = [(-EAVE, -EAVE), (13.2 + EAVE, -EAVE),
             (13.2 + EAVE, 9.6 + EAVE), (-EAVE, 9.6 + EAVE)]

GRID_U = [("A", 0.0), ("B", 3.6), ("C", 9.6), ("D", 13.2)]
GRID_V = [("1", 0.0), ("2", 6.0), ("3", 9.6)]

# number, name, long name, (x0,y0,x1,y1), storey, per-edge thickness (W,S,E,N), external
SPACES = [
    # --- 1st Storey
    ("01", "Household Shelter", "Household shelter, 1st storey",
     HS, "1", (T_HS, T_HS, T_HS, T_HS), False),
    ("02", "Utility", "Utility and washing",
     (2.0, 0.0, 3.6, 3.7), "1", (T_HS, T_EXT, T_TOWER, T_INT), False),
    ("03", "Store", "Store, 1st storey",
     (0.0, 3.7, 3.6, 6.0), "1", (T_EXT, T_INT, T_TOWER, T_INT), False),
    ("04", "Light Well", "Light well, open to sky",
     WELL, "1", (T_EXT, T_INT, T_TOWER, T_EXT), True),
    ("05", "Living/Dining", "Living and dining",
     (3.6, 0.0, 9.6, 6.0), "1", (T_TOWER, T_EXT, T_TOWER, T_INT), False),
    ("06", "Kitchen", "Kitchen",
     (3.6, 6.0, 9.6, 9.6), "1", (T_TOWER, T_INT, T_TOWER, T_EXT), False),
    ("07", "WC", "Powder room",
     (9.6, 0.0, 13.2, 2.4), "1", (T_TOWER, T_EXT, T_EXT, T_INT), False),
    ("08", "Stair", "Stair, 1st storey",
     (9.6, 2.4, 13.2, 6.0), "1", (T_TOWER, T_INT, T_EXT, T_INT), False),
    ("09", "Bathroom 1", "Bathroom 1",
     (9.6, 6.0, 13.2, 9.6), "1", (T_TOWER, T_INT, T_EXT, T_EXT), False),
    # --- 2nd Storey. The shelter tower carries a bathroom above it: same walls,
    #     same foundations, which is exactly why the tower is worth having.
    ("10", "Bathroom 2", "Bathroom 2, over the shelter",
     HS, "2", (T_HS, T_HS, T_HS, T_HS), False),
    ("11", "Store 2", "Store, 2nd storey",
     (2.0, 0.0, 3.6, 3.7), "2", (T_HS, T_EXT, T_TOWER, T_INT), False),
    ("12", "Study", "Study",
     (0.0, 3.7, 3.6, 6.0), "2", (T_EXT, T_INT, T_TOWER, T_INT), False),
    ("13", "Bedroom 1", "Master bedroom",
     (3.6, 0.0, 9.6, 4.0), "2", (T_TOWER, T_EXT, T_TOWER, T_INT), False),
    ("14", "Bedroom 2", "Bedroom 2",
     (3.6, 4.0, 9.6, 7.0), "2", (T_TOWER, T_INT, T_TOWER, T_INT), False),
    ("15", "Bedroom 3", "Bedroom 3",
     (3.6, 7.0, 9.6, 9.6), "2", (T_TOWER, T_INT, T_TOWER, T_EXT), False),
    ("16", "Landing", "Landing, 2nd storey",
     (9.6, 0.0, 13.2, 2.4), "2", (T_TOWER, T_EXT, T_EXT, T_INT), False),
    ("17", "Stair 2", "Stair, 2nd storey",
     (9.6, 2.4, 13.2, 6.0), "2", (T_TOWER, T_INT, T_EXT, T_INT), False),
    ("18", "Bathroom 3", "Bathroom 3",
     (9.6, 6.0, 13.2, 9.6), "2", (T_TOWER, T_INT, T_EXT, T_EXT), False),
]

# mark, host wall, distance along wall from p1, width, height, sill, storey, main entrance
DOORS = [
    ("D01", "A-Walls-Ext-South",  6.0, 1.500, 2.400, 0.0, "1", True),   # entrance
    ("D02", "A-Walls-HS-East",    1.8, 0.850, 2.000, 0.0, "1", False),  # shelter door
    ("D03", "A-Walls-Int-S01",    1.5, 0.900, 2.100, 0.0, "1", False),
    ("D04", "A-Walls-Int-E01",    1.8, 0.900, 2.100, 0.0, "1", False),
    ("D05", "A-Walls-Int-E02",    1.8, 0.800, 2.100, 0.0, "1", False),
    ("D06", "A-Walls-Int-W02",    1.8, 0.900, 2.100, 0.0, "1", False),
    ("D07", "A-Walls-Tower-W-East", 1.8, 0.900, 2.100, 0.0, "1", False),
    ("D08", "A-Walls-Tower-E-West", 4.2, 0.900, 2.100, 0.0, "1", False),
    ("D09", "A-Walls-HS-East",    1.8, 0.850, 2.000, 0.0, "2", False),
    ("D10", "A-Walls-Int-S02",    1.5, 0.900, 2.100, 0.0, "2", False),
    ("D11", "A-Walls-Int-S03",    1.5, 0.900, 2.100, 0.0, "2", False),
    ("D12", "A-Walls-Int-E02",    1.8, 0.800, 2.100, 0.0, "2", False),
    ("D13", "A-Walls-Tower-E-West", 1.2, 0.900, 2.100, 0.0, "2", False),
    ("D14", "A-Walls-Tower-W-East", 4.8, 0.900, 2.100, 0.0, "2", False),
]

# mark, host wall, distance along wall, width, height, sill, storey
# The served volume opens north and south. The towers are almost blind, which is
# the point: solid where the sun is low, open where the breeze runs.
WINDOWS = [
    ("W01", "A-Walls-Ext-South",   4.2, 2.400, 2.100, 0.900, "1"),
    ("W02", "A-Walls-Ext-South",   8.4, 2.400, 2.100, 0.900, "1"),
    ("W03", "A-Walls-Ext-North",   4.2, 2.400, 2.100, 0.900, "1"),
    ("W04", "A-Walls-Ext-North",   8.4, 2.400, 2.100, 0.900, "1"),
    ("W05", "A-Walls-Ext-South",   4.2, 2.400, 2.100, 0.900, "2"),
    ("W06", "A-Walls-Ext-South",   8.4, 2.400, 2.100, 0.900, "2"),
    ("W07", "A-Walls-Ext-North",   4.2, 2.400, 2.100, 0.900, "2"),
    ("W08", "A-Walls-Ext-North",   8.4, 2.400, 2.100, 0.900, "2"),
    ("W09", "A-Walls-Ext-East",    7.8, 0.900, 1.200, 1.500, "1"),
    ("W10", "A-Walls-Ext-East",    7.8, 0.900, 1.200, 1.500, "2"),
    ("W11", "A-Walls-Ext-West",    7.2, 0.900, 1.200, 1.500, "2"),
]

STOREY_Z = {"1": FFL, "2": L2}


# ------------------------------------------------------------------ helpers --

def direction(p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = math.hypot(dx, dy)
    return (dx / length, dy / length), length


def centred(p1, p2, thickness):
    """create_2pt_wall grows the wall to the left of p1->p2, so shift the line
    back by half its thickness to leave it centred on the line we meant."""
    (dx, dy), _ = direction(p1, p2)
    nx, ny = -dy, dx
    off = thickness / 2.0
    return (p1[0] - nx * off, p1[1] - ny * off), (p2[0] - nx * off, p2[1] - ny * off)


def placement_matrix(origin, xdir=(1.0, 0.0)):
    dx, dy = xdir
    return np.array([[dx, -dy, 0.0, origin[0]],
                     [dy, dx, 0.0, origin[1]],
                     [0.0, 0.0, 1.0, origin[2]],
                     [0.0, 0.0, 0.0, 1.0]], dtype=float)


def box_polyline(width, depth):
    hw, hd = width / 2.0, depth / 2.0
    return [(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)]


def inset(rect, thicknesses):
    """Inset a room rectangle by the FULL wall thickness on each edge.

    Half-thickness would give the centreline area, which is a reasonable
    convention for gross calculations and the wrong one here. IFC+SG asks the
    household shelter for its *internal* length and width, and a checker that
    compares those two numbers against the space's NetFloorArea has every right
    to expect them to multiply out. So the space is the clear internal volume,
    and it is the same figure the shelter reports.
    """
    x0, y0, x1, y1 = rect
    tw, ts, te, tn = thicknesses
    return [(x0 + tw, y0 + ts), (x1 - te, y0 + ts),
            (x1 - te, y1 - tn), (x0 + tw, y1 - tn)]


def area_of(polyline):
    a = 0.0
    for i in range(len(polyline)):
        x0, y0 = polyline[i]
        x1, y1 = polyline[(i + 1) % len(polyline)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2.0


def wall_type(f, name, layers, materials):
    t = api.root.create_entity(f, "IfcWallType", predefined_type="SOLIDWALL", name=name)
    attach_layers(f, t, layers, materials)
    return t


def attach_layers(f, element_type, layers, materials):
    layer_set = api.material.add_material_set(
        f, name=element_type.Name, set_type="IfcMaterialLayerSet")
    for material_name, thickness in layers:
        layer = api.material.add_layer(
            f, layer_set=layer_set, material=materials[material_name], name=material_name)
        layer.LayerThickness = thickness * 1000.0
    api.material.assign_material(
        f, products=[element_type], type="IfcMaterialLayerSet", material=layer_set)


def stage_pset(f, product, extra=None, vaf=None):
    """Three property sets, each answering a different question.

    Bonsai_Upskilling  the course's own change-control data
    IFCSG_Demo         IFC+SG *parameter names*, so the workflow is visible. It
                       is deliberately not called SGPset_something: the
                       authoritative names come from the IFC+SG Excel Mapping
                       File, which you must consult rather than inherit from a
                       teaching model.
    VAF_Demo           which Value Articulation Framework component this element
                       serves, so the model can be read against the fee.
    """
    pset = api.pset.add_pset(f, product=product, name="Bonsai_Upskilling")
    api.pset.edit_pset(f, pset=pset, properties={
        "project_stage": "03 Schematic Design",
        "design_status": "approved",
    })
    if extra:
        sg = api.pset.add_pset(f, product=product, name="IFCSG_Demo")
        api.pset.edit_pset(f, pset=sg, properties=extra)
    if vaf:
        v = api.pset.add_pset(f, product=product, name="VAF_Demo")
        api.pset.edit_pset(f, pset=v, properties=vaf)


def make_opening(f, body, storeys, walls, host, dist, width, height, sill,
                 storey_key, element_class, mark, relating_type, extra):
    wall, p1, p2, thickness = walls[(host, storey_key)]
    (dx, dy), _ = direction(p1, p2)
    origin = (p1[0] + dx * dist, p1[1] + dy * dist, STOREY_Z[storey_key] + sill)

    opening = api.root.create_entity(f, "IfcOpeningElement", predefined_type="OPENING",
                                     name=f"A-Openings-{mark}")
    rep = api.geometry.add_slab_representation(
        f, context=body, depth=height, polyline=box_polyline(width, thickness + 0.100))
    api.geometry.assign_representation(f, product=opening, representation=rep)
    api.geometry.edit_object_placement(
        f, product=opening, matrix=placement_matrix(origin, (dx, dy)), is_si=True)
    api.feature.add_feature(f, feature=opening, element=wall)

    element = api.root.create_entity(f, element_class, name=f"A-{element_class[3:]}s-{mark}")
    element.OverallWidth = width * 1000.0
    element.OverallHeight = height * 1000.0
    element.Tag = mark
    rep = api.geometry.add_slab_representation(
        f, context=body, depth=height, polyline=box_polyline(width, thickness * 0.5))
    api.geometry.assign_representation(f, product=element, representation=rep)
    api.geometry.edit_object_placement(
        f, product=element, matrix=placement_matrix(origin, (dx, dy)), is_si=True)
    api.type.assign_type(f, related_objects=[element], relating_type=relating_type)
    api.spatial.assign_container(f, products=[element], relating_structure=storeys[storey_key])
    api.feature.add_filling(f, opening=opening, element=element)

    common = api.pset.add_pset(f, product=element, name=f"Pset_{element_class[3:]}Common")
    api.pset.edit_pset(f, pset=common, properties={"Reference": mark})
    stage_pset(f, element, extra=extra)
    return element


# -------------------------------------------------------------------- build --

def build() -> ifcopenshell.file:
    f = api.project.create_file("IFC4")

    project = api.root.create_entity(f, "IfcProject", name="Servant and Served House")
    api.unit.assign_unit(f, units=[
        api.unit.add_si_unit(f, unit_type="LENGTHUNIT", prefix="MILLI"),
        api.unit.add_si_unit(f, unit_type="AREAUNIT"),
        api.unit.add_si_unit(f, unit_type="VOLUMEUNIT"),
    ])

    model = api.context.add_context(f, context_type="Model")
    body = api.context.add_context(
        f, context_type="Model", context_identifier="Body",
        target_view="MODEL_VIEW", parent=model)

    # Georeferencing. SVY21 for easting and northing, SHD for height, and a
    # rotation to True North. The coordinates are a plausible example, not a plot.
    api.georeference.add_georeferencing(f)
    bearing = math.radians(8.0)
    api.georeference.edit_georeferencing(
        f,
        projected_crs={"Name": "EPSG:3414", "Description": "SVY21 / Singapore TM",
                       "GeodeticDatum": "SVY21", "VerticalDatum": "SHD"},
        coordinate_operation={"Eastings": 33000.0, "Northings": 39000.0,
                              "OrthogonalHeight": 15.400,
                              "XAxisAbscissa": math.cos(bearing),
                              "XAxisOrdinate": math.sin(bearing), "Scale": 1.0})

    site = api.root.create_entity(f, "IfcSite", name="Main Block")
    building = api.root.create_entity(f, "IfcBuilding", name="Servant and Served House")
    storeys = {
        "1": api.root.create_entity(f, "IfcBuildingStorey", name="1st Storey"),
        "2": api.root.create_entity(f, "IfcBuildingStorey", name="2nd Storey"),
    }
    roof_storey = api.root.create_entity(f, "IfcBuildingStorey", name="Roof")
    storeys["1"].Elevation = FFL * 1000.0
    storeys["2"].Elevation = L2 * 1000.0
    roof_storey.Elevation = ROOF * 1000.0
    api.aggregate.assign_object(f, products=[site], relating_object=project)
    api.aggregate.assign_object(f, products=[building], relating_object=site)
    api.aggregate.assign_object(
        f, products=[storeys["1"], storeys["2"], roof_storey], relating_object=building)

    stage_pset(f, building,
               extra={"Project Development Type": "Landed housing",
                      "Owner Built Owner Stay": True},
               vaf={"component": "Design", "resource_grade": "Architect"})
    for s in list(storeys.values()) + [roof_storey]:
        stage_pset(f, s, extra={"Attic Level": False})

    materials = {name: api.material.add_material(f, name=name, category=cat)
                 for name, cat in [("Cement plaster", "plaster"),
                                   ("Clay brickwork", "brick"),
                                   ("Concrete blockwork", "block"),
                                   ("Reinforced concrete", "concrete")]}

    types = {}
    types["EXT"] = wall_type(f, "EXT-200-BRK", [
        ("Cement plaster", 0.015), ("Clay brickwork", 0.170),
        ("Cement plaster", 0.015)], materials)
    types["INT"] = wall_type(f, "INT-100-BLK", [
        ("Cement plaster", 0.010), ("Concrete blockwork", 0.080),
        ("Cement plaster", 0.010)], materials)
    types["TOWER"] = wall_type(f, "TWR-200-RC", [("Reinforced concrete", 0.200)], materials)
    types["HS"] = wall_type(f, "HS-250-RC", [("Reinforced concrete", 0.250)], materials)

    slab_type = api.root.create_entity(f, "IfcSlabType", predefined_type="FLOOR",
                                       name="SLAB-RC-200")
    roof_type = api.root.create_entity(f, "IfcSlabType", predefined_type="ROOF",
                                       name="ROOF-RC-150")
    attach_layers(f, slab_type, [("Reinforced concrete", 0.200)], materials)
    attach_layers(f, roof_type, [("Reinforced concrete", 0.150)], materials)

    door_types = {w: api.root.create_entity(f, "IfcDoorType", predefined_type="DOOR",
                                            name=f"DR-{int(w * 1000)}")
                  for w in sorted({d[3] for d in DOORS})}
    window_types = {w: api.root.create_entity(f, "IfcWindowType", predefined_type="WINDOW",
                                              name=f"WN-{int(w * 1000)}")
                    for w in sorted({x[3] for x in WINDOWS})}

    # ---- walls, per storey
    walls = {}
    for tag, (p1, p2, key, on) in WALLS.items():
        for sk in on:
            t = THICKNESS[key]
            wall = api.root.create_entity(f, "IfcWall", name=f"{tag}-L{sk}")
            a, b = centred(p1, p2, t)
            rep = api.geometry.create_2pt_wall(
                f, element=wall, context=body, p1=a, p2=b,
                elevation=STOREY_Z[sk], height=STOREY_H, thickness=t, is_si=True)
            api.geometry.assign_representation(f, product=wall, representation=rep)
            api.type.assign_type(f, related_objects=[wall], relating_type=types[key])
            api.spatial.assign_container(f, products=[wall], relating_structure=storeys[sk])
            pset = api.pset.add_pset(f, product=wall, name="Pset_WallCommon")
            api.pset.edit_pset(f, pset=pset, properties={
                "IsExternal": key == "EXT",
                "LoadBearing": key in ("EXT", "TOWER", "HS")})
            stage_pset(
                f, wall,
                extra={"Construction Method": "Cast in-situ"
                       if key in ("HS", "TOWER") else "Masonry"},
                vaf={"component": "Structure" if key in ("HS", "TOWER") else "Envelope",
                     "resource_grade": "Architect"})
            walls[(tag, sk)] = (wall, p1, p2, t)

    # ---- slabs and roof
    for name, z, st, host in (("A-Slabs-1st-Storey", 0.0, slab_type, storeys["1"]),
                              ("A-Slabs-2nd-Storey", L2 - 0.200, slab_type, storeys["2"])):
        slab = api.root.create_entity(f, "IfcSlab", predefined_type="FLOOR", name=name)
        rep = api.geometry.add_slab_representation(f, context=body, depth=0.200, polyline=OUTER)
        api.geometry.assign_representation(f, product=slab, representation=rep)
        api.geometry.edit_object_placement(
            f, product=slab, matrix=placement_matrix((0, 0, z)), is_si=True)
        api.type.assign_type(f, related_objects=[slab], relating_type=slab_type)
        api.spatial.assign_container(f, products=[slab], relating_structure=host)
        stage_pset(f, slab, vaf={"component": "Structure", "resource_grade": "Architect"})

    roof = api.root.create_entity(f, "IfcRoof", predefined_type="FLAT_ROOF", name="A-Roof-Main")
    api.spatial.assign_container(f, products=[roof], relating_structure=roof_storey)
    roof_slab = api.root.create_entity(f, "IfcSlab", predefined_type="ROOF", name="A-Roof-Slab")
    rep = api.geometry.add_slab_representation(f, context=body, depth=0.150, polyline=ROOF_EDGE)
    api.geometry.assign_representation(f, product=roof_slab, representation=rep)
    api.geometry.edit_object_placement(
        f, product=roof_slab, matrix=placement_matrix((0, 0, ROOF)), is_si=True)
    api.type.assign_type(f, related_objects=[roof_slab], relating_type=roof_type)
    api.aggregate.assign_object(f, products=[roof_slab], relating_object=roof)
    stage_pset(f, roof_slab, vaf={"component": "Envelope", "resource_grade": "Architect"})

    # ---- openings
    for mark, host, dist, width, height, sill, sk, main in DOORS:
        make_opening(f, body, storeys, walls, host, dist, width, height, sill, sk,
                     element_class="IfcDoor", mark=mark, relating_type=door_types[width],
                     extra={"Main Entrance": main,
                            "Clear Width": round(width * 1000),
                            "Clear Height": round(height * 1000)})
    for mark, host, dist, width, height, sill, sk in WINDOWS:
        make_opening(f, body, storeys, walls, host, dist, width, height, sill, sk,
                     element_class="IfcWindow", mark=mark, relating_type=window_types[width],
                     extra={"Percentage of Opening": 50.0, "Safety Barrier Height": 1000})

    # ---- spaces
    for number, name, long_name, rect, sk, thicknesses, external in SPACES:
        space = api.root.create_entity(
            f, "IfcSpace", predefined_type="EXTERNAL" if external else "INTERNAL", name=name)
        space.LongName = long_name
        space.CompositionType = "ELEMENT"
        poly = inset(rect, thicknesses)
        height = STOREY_H if name != "Light Well" else STOREY_H * 2
        rep = api.geometry.add_slab_representation(f, context=body, depth=height, polyline=poly)
        api.geometry.assign_representation(f, product=space, representation=rep)
        api.geometry.edit_object_placement(
            f, product=space, matrix=placement_matrix((0, 0, STOREY_Z[sk])), is_si=True)
        api.aggregate.assign_object(f, products=[space], relating_object=storeys[sk])

        pset = api.pset.add_pset(f, product=space, name="Pset_SpaceCommon")
        api.pset.edit_pset(f, pset=pset, properties={
            "IsExternal": external, "Reference": number})
        qto = api.pset.add_qto(f, product=space, name="Qto_SpaceBaseQuantities")
        api.pset.edit_qto(f, qto=qto, properties={
            "NetFloorArea": round(area_of(poly), 3),
            "FinishCeilingHeight": round(height, 3)})

        sg = {"Space Name": name, "Area": round(area_of(poly), 2)}
        if name == "Household Shelter":
            x0, y0, x1, y1 = rect
            sg.update({
                "Construction Method": "Cast in-situ reinforced concrete",
                "Internal Length": round((y1 - y0 - 2 * T_HS) * 1000),
                "Internal Width": round((x1 - x0 - 2 * T_HS) * 1000),
                "Clear Height": round(HS_CLEAR * 1000),
            })
        if name in ("Living/Dining", "Kitchen", "WC", "Stair", "Household Shelter"):
            sg["Barrier Free Accessibility"] = True
        stage_pset(f, space, extra=sg,
                   vaf={"component": "Space Planning", "resource_grade": "Architect"})

    # ---- gross floor area, as IFC+SG asks for it: a space, not a spreadsheet cell
    for sk, label in (("1", "1st Storey"), ("2", "2nd Storey")):
        gfa = api.root.create_entity(f, "IfcSpace", predefined_type="USERDEFINED",
                                     name=f"GFA {label}")
        gfa.ObjectType = "AREA_GFA"
        gfa.LongName = f"Gross floor area, {label}"
        gfa.CompositionType = "ELEMENT"
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=0.050, polyline=[(p[0], p[1]) for p in OUTER])
        api.geometry.assign_representation(f, product=gfa, representation=rep)
        api.geometry.edit_object_placement(
            f, product=gfa, matrix=placement_matrix((0, 0, STOREY_Z[sk])), is_si=True)
        api.aggregate.assign_object(f, products=[gfa], relating_object=storeys[sk])
        area = area_of([(p[0], p[1]) for p in OUTER])
        stage_pset(f, gfa,
                   extra={"AGF_Name": f"GFA {label}",
                          "AGF_Development Use": "Landed housing",
                          "AGF_Use Quantum": round(area, 2)},
                   vaf={"component": "Regulatory", "resource_grade": "Architect"})

    # ---- grid
    grid = api.root.create_entity(f, "IfcGrid", name="A-Grid")
    api.spatial.assign_container(f, products=[grid], relating_structure=storeys["1"])
    for tag, x in GRID_U:
        axis = api.grid.create_grid_axis(f, grid=grid, axis_tag=tag, uvw_axes="UAxes")
        api.grid.create_axis_curve(f, p1=np.array([x, -2.0, 0.0]),
                                   p2=np.array([x, 11.6, 0.0]), grid_axis=axis, is_si=True)
    for tag, y in GRID_V:
        axis = api.grid.create_grid_axis(f, grid=grid, axis_tag=tag, uvw_axes="VAxes")
        api.grid.create_axis_curve(f, p1=np.array([-2.0, y, 0.0]),
                                   p2=np.array([15.2, y, 0.0]), grid_axis=axis, is_si=True)

    return f


if __name__ == "__main__":
    model = build()
    model.write(str(OUT))
    print(f"wrote {OUT}")
    for cls in ("IfcWall", "IfcSlab", "IfcRoof", "IfcDoor", "IfcWindow",
                "IfcOpeningElement", "IfcSpace", "IfcBuildingStorey", "IfcGrid"):
        print(f"  {cls:20} {len(model.by_type(cls))}")
