"""Build the Courtyard Bungalow reference model as IFC4, to Singapore conventions.

This is the model the Bonsai Upskilling course describes, built with IfcOpenShell's
API -- the same API Bonsai's own operators drive -- so that the result opens in
Bonsai, in any IFC viewer, and can be checked by anything that reads IFC4.

    python exercises/reference-model/build_bungalow.py

It writes BUNG-A-SCH-P03.ifc beside this script: the model at the end of Stage 03,
Schematic Design. That is deliberate. IFC+SG's schematic stage, and CORENET X's
Design Gateway, both ask for design intent and simplified geometry, not detail --
so doors are openings with leaves rather than ironmongery, and there is no
material take-off pretending to be a specification.

Conventions applied, and why:

  Storey names        "1st Storey", "Roof" -- CORENET X level naming. Not "Ground",
                      not "Level 1", never "1st Floor".
  One IfcSite         Named for the block, per the block mechanism.
  Georeferencing      EPSG:3414 (SVY21 / Singapore TM) with SHD elevation and a
                      True North rotation. The coordinates are an example, not a
                      real plot.
  Types before walls  Every wall, slab and opening comes from a type carrying a
                      material layer set.
  Real openings       IfcOpeningElement voiding its host, filled by the door or
                      window. Never a hole in a mesh.
  Household shelter   Modelled from the conceptual stage, in 300 mm reinforced
                      concrete, carrying its internal dimensions as data.

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

OUT = Path(__file__).resolve().parent / "BUNG-A-SCH-P03.ifc"

# ---------------------------------------------------------------- dimensions --
# Metres, origin at the south-west corner of the building, +Y is project north.

FFL = 0.150          # finished floor level above site datum
STOREY_H = 3.000     # floor to ceiling
ROOF_LEVEL = FFL + STOREY_H
EAVE = 0.600

T_EXT, T_INT, T_HS = 0.200, 0.100, 0.300

# The footprint is a 12 x 10 rectangle with a 4 x 4 courtyard notch at the
# south-east corner. Centrelines of the external walls:
PERIMETER = [(0, 0), (8, 0), (8, 4), (12, 4), (12, 10), (0, 10)]

# Outer face of the external walls, and the roof edge beyond it.
OUTER = [(-0.1, -0.1), (8.1, -0.1), (8.1, 3.9), (12.1, 3.9), (12.1, 10.1), (-0.1, 10.1)]
ROOF_EDGE = [(-0.6, -0.6), (8.6, -0.6), (8.6, 3.4), (12.6, 3.4), (12.6, 10.6), (-0.6, 10.6)]

# tag: (p1, p2, type key)
WALLS: dict[str, tuple[tuple[float, float], tuple[float, float], str]] = {
    # external, anticlockwise around the L
    "A-Walls-Ext-South":     ((0, 0), (8, 0), "EXT"),
    "A-Walls-Ext-Court-W":   ((8, 0), (8, 4), "EXT"),
    "A-Walls-Ext-Court-N":   ((8, 4), (12, 4), "EXT"),
    "A-Walls-Ext-East":      ((12, 4), (12, 10), "EXT"),
    "A-Walls-Ext-North":     ((12, 10), (0, 10), "EXT"),
    "A-Walls-Ext-West":      ((0, 10), (0, 0), "EXT"),
    # internal partitions
    "A-Walls-Int-P01":       ((0, 4), (8, 4), "INT"),      # south band | circulation
    "A-Walls-Int-P02a":      ((0, 7), (2, 7), "INT"),      # utility | bedroom 1
    "A-Walls-Int-P02b":      ((4, 7), (12, 7), "INT"),     # wet band | bedrooms
    "A-Walls-Int-P03":       ((5, 0), (5, 4), "INT"),      # living | entry
    "A-Walls-Int-P04a":      ((0, 5.5), (2, 5.5), "INT"),  # circulation | utility
    "A-Walls-Int-P04b":      ((4, 5.5), (8, 5.5), "INT"),  # circulation | bathrooms
    "A-Walls-Int-P06":       ((6, 5.5), (6, 7), "INT"),    # bathroom 2 | bathroom 1
    "A-Walls-Int-P08":       ((8, 4), (8, 7), "INT"),      # circulation | kitchen
    "A-Walls-Int-P09":       ((4, 7), (4, 10), "INT"),     # bedroom 1 | bedroom 2
    "A-Walls-Int-P10":       ((8, 7), (8, 10), "INT"),     # bedroom 2 | bedroom 3
    # household shelter, 300 reinforced concrete on all four sides
    "A-Walls-HS-South":      ((2, 5.5), (4, 5.5), "HS"),
    "A-Walls-HS-East":       ((4, 5.5), (4, 7), "HS"),
    "A-Walls-HS-North":      ((4, 7), (2, 7), "HS"),
    "A-Walls-HS-West":       ((2, 7), (2, 5.5), "HS"),
}

THICKNESS = {"EXT": T_EXT, "INT": T_INT, "HS": T_HS}

# number, name, long name, rectangle, per-edge wall thickness (W, S, E, N), external?
SPACES = [
    ("01", "Living/Dining", "Living and dining",  (0, 0, 5, 4),      (T_EXT, T_EXT, T_INT, T_INT), False),
    ("02", "Entry Foyer",   "Entrance foyer",     (5, 0, 8, 4),      (T_INT, T_EXT, T_EXT, T_INT), False),
    ("03", "Kitchen",       "Kitchen",            (8, 4, 12, 7),     (T_INT, T_EXT, T_EXT, T_INT), False),
    ("04", "Circulation",   "Circulation",        (0, 4, 8, 5.5),    (T_EXT, T_INT, T_INT, T_INT), False),
    ("05", "Utility",       "Utility",            (0, 5.5, 2, 7),    (T_EXT, T_INT, T_HS, T_INT), False),
    ("06", "Household Shelter", "Household shelter", (2, 5.5, 4, 7), (T_HS, T_HS, T_HS, T_HS), False),
    ("07", "Bathroom 2",    "Bathroom 2",         (4, 5.5, 6, 7),    (T_HS, T_INT, T_INT, T_INT), False),
    ("08", "Bathroom 1",    "Bathroom 1",         (6, 5.5, 8, 7),    (T_INT, T_INT, T_EXT, T_INT), False),
    ("09", "Bedroom 1",     "Master bedroom",     (0, 7, 4, 10),     (T_EXT, T_INT, T_INT, T_EXT), False),
    ("10", "Bedroom 2",     "Bedroom 2",          (4, 7, 8, 10),     (T_INT, T_INT, T_INT, T_EXT), False),
    ("11", "Bedroom 3",     "Bedroom 3",          (8, 7, 12, 10),    (T_INT, T_INT, T_EXT, T_EXT), False),
    ("12", "Courtyard",     "Courtyard, open to sky", (8, 0, 12, 4), (T_EXT, 0.0, 0.0, T_EXT), True),
    ("13", "Covered Entry", "Covered entry porch", (5, -1.5, 8, 0),  (0.0, 0.0, 0.0, T_EXT), True),
]

# mark, host wall, distance along wall from p1, width, height, sill, main entrance
DOORS = [
    ("D01", "A-Walls-Ext-South",  6.5,  1.200, 2.400, 0.0, True),
    ("D02", "A-Walls-Int-P01",    6.5,  0.900, 2.100, 0.0, False),
    ("D03", "A-Walls-Int-P03",    2.0,  0.900, 2.100, 0.0, False),
    ("D04", "A-Walls-Int-P08",    1.0,  0.900, 2.100, 0.0, False),
    ("D05", "A-Walls-HS-South",   1.0,  0.850, 2.000, 0.0, False),
    ("D06", "A-Walls-Int-P04a",   1.0,  0.800, 2.100, 0.0, False),
    ("D07", "A-Walls-Int-P04b",   1.0,  0.800, 2.100, 0.0, False),
    ("D08", "A-Walls-Int-P04b",   3.0,  0.800, 2.100, 0.0, False),
    ("D09", "A-Walls-Int-P02a",   1.0,  0.900, 2.100, 0.0, False),
    ("D10", "A-Walls-Int-P02b",   1.5,  0.900, 2.100, 0.0, False),
    ("D11", "A-Walls-Int-P02b",   5.5,  0.900, 2.100, 0.0, False),
    ("D12", "A-Walls-Ext-Court-W", 2.0, 1.800, 2.400, 0.0, False),
]

# mark, host wall, distance along wall, width, height, sill
WINDOWS = [
    ("W01", "A-Walls-Ext-South",   2.5, 1.800, 1.500, 0.900),
    ("W02", "A-Walls-Ext-West",    8.0, 1.200, 1.500, 0.900),
    ("W03", "A-Walls-Ext-North",  10.0, 1.500, 1.500, 0.900),
    ("W04", "A-Walls-Ext-North",   6.0, 1.500, 1.500, 0.900),
    ("W05", "A-Walls-Ext-North",   2.0, 1.500, 1.500, 0.900),
    ("W06", "A-Walls-Ext-East",    4.5, 1.200, 1.500, 0.900),
    ("W07", "A-Walls-Ext-East",    1.5, 1.200, 1.500, 0.900),
    ("W08", "A-Walls-Ext-Court-N", 2.0, 1.200, 1.500, 0.900),
]

GRID_U = [("A", 0.0), ("B", 4.0), ("C", 8.0), ("D", 12.0)]
GRID_V = [("1", 0.0), ("2", 4.0), ("3", 7.0), ("4", 10.0)]


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
    return np.array(
        [
            [dx, -dy, 0.0, origin[0]],
            [dy, dx, 0.0, origin[1]],
            [0.0, 0.0, 1.0, origin[2]],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def box_polyline(width, depth):
    hw, hd = width / 2.0, depth / 2.0
    return [(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)]


def inset(rect, thicknesses):
    x0, y0, x1, y1 = rect
    tw, ts, te, tn = thicknesses
    return [
        (x0 + tw / 2, y0 + ts / 2),
        (x1 - te / 2, y0 + ts / 2),
        (x1 - te / 2, y1 - tn / 2),
        (x0 + tw / 2, y1 - tn / 2),
    ]


def area_of(polyline):
    a = 0.0
    for i in range(len(polyline)):
        x0, y0 = polyline[i]
        x1, y1 = polyline[(i + 1) % len(polyline)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2.0


# -------------------------------------------------------------------- build --

def build() -> ifcopenshell.file:
    f = api.project.create_file("IFC4")

    project = api.root.create_entity(f, "IfcProject", name="Courtyard Bungalow")
    api.unit.assign_unit(
        f,
        units=[
            api.unit.add_si_unit(f, unit_type="LENGTHUNIT", prefix="MILLI"),
            api.unit.add_si_unit(f, unit_type="AREAUNIT"),
            api.unit.add_si_unit(f, unit_type="VOLUMEUNIT"),
        ],
    )

    model = api.context.add_context(f, context_type="Model")
    body = api.context.add_context(
        f, context_type="Model", context_identifier="Body",
        target_view="MODEL_VIEW", parent=model,
    )

    # Georeferencing. SVY21 for easting and northing, SHD for height, and a
    # rotation to True North. These numbers are a plausible example, not a plot.
    api.georeference.add_georeferencing(f)
    bearing = math.radians(8.0)          # project +Y is 8 degrees east of true north
    api.georeference.edit_georeferencing(
        f,
        projected_crs={
            "Name": "EPSG:3414",
            "Description": "SVY21 / Singapore TM",
            "GeodeticDatum": "SVY21",
            "VerticalDatum": "SHD",
        },
        coordinate_operation={
            "Eastings": 33000.0,
            "Northings": 39000.0,
            "OrthogonalHeight": 15.400,
            "XAxisAbscissa": math.cos(bearing),
            "XAxisOrdinate": math.sin(bearing),
            "Scale": 1.0,
        },
    )

    # Spatial structure. One site, named for the block.
    site = api.root.create_entity(f, "IfcSite", name="Main Block")
    building = api.root.create_entity(f, "IfcBuilding", name="Courtyard Bungalow")
    storey = api.root.create_entity(f, "IfcBuildingStorey", name="1st Storey")
    roof_storey = api.root.create_entity(f, "IfcBuildingStorey", name="Roof")
    storey.Elevation = FFL * 1000.0
    roof_storey.Elevation = ROOF_LEVEL * 1000.0
    api.aggregate.assign_object(f, products=[site], relating_object=project)
    api.aggregate.assign_object(f, products=[building], relating_object=site)
    api.aggregate.assign_object(f, products=[storey, roof_storey], relating_object=building)

    stage_pset(f, building, extra={"Project Development Type": "Landed housing",
                                   "Owner Built Owner Stay": True})
    for s in (storey, roof_storey):
        stage_pset(f, s, extra={"Attic Level": False})

    materials = {
        name: api.material.add_material(f, name=name, category=cat)
        for name, cat in [
            ("Cement plaster", "plaster"),
            ("Clay brickwork", "brick"),
            ("Concrete blockwork", "block"),
            ("Reinforced concrete", "concrete"),
        ]
    }

    types = {}
    types["EXT"] = wall_type(f, "EXT-200-BRK", [
        ("Cement plaster", 0.015), ("Clay brickwork", 0.170), ("Cement plaster", 0.015)], materials)
    types["INT"] = wall_type(f, "INT-100-BLK", [
        ("Cement plaster", 0.010), ("Concrete blockwork", 0.080), ("Cement plaster", 0.010)], materials)
    types["HS"] = wall_type(f, "HS-300-RC", [
        ("Reinforced concrete", 0.300)], materials)

    slab_gf = api.root.create_entity(f, "IfcSlabType", predefined_type="FLOOR", name="SLAB-GF-150")
    slab_roof = api.root.create_entity(f, "IfcSlabType", predefined_type="ROOF", name="ROOF-125")
    for t, layers in ((slab_gf, [("Reinforced concrete", 0.150)]),
                      (slab_roof, [("Reinforced concrete", 0.125)])):
        attach_layers(f, t, layers, materials)

    door_types = {
        w: api.root.create_entity(f, "IfcDoorType", predefined_type="DOOR", name=f"DR-{int(w * 1000)}")
        for w in sorted({d[3] for d in DOORS})
    }
    window_types = {
        w: api.root.create_entity(f, "IfcWindowType", predefined_type="WINDOW", name=f"WN-{int(w * 1000)}")
        for w in sorted({x[3] for x in WINDOWS})
    }

    # ---- walls
    walls = {}
    for tag, (p1, p2, key) in WALLS.items():
        t = THICKNESS[key]
        wall = api.root.create_entity(f, "IfcWall", name=tag)
        a, b = centred(p1, p2, t)
        rep = api.geometry.create_2pt_wall(
            f, element=wall, context=body, p1=a, p2=b,
            elevation=FFL, height=STOREY_H, thickness=t, is_si=True,
        )
        api.geometry.assign_representation(f, product=wall, representation=rep)
        api.type.assign_type(f, related_objects=[wall], relating_type=types[key])
        api.spatial.assign_container(f, products=[wall], relating_structure=storey)
        external = key == "EXT"
        pset = api.pset.add_pset(f, product=wall, name="Pset_WallCommon")
        api.pset.edit_pset(f, pset=pset, properties={
            "IsExternal": external, "LoadBearing": key in ("EXT", "HS")})
        stage_pset(f, wall, extra={"Construction Method": "Cast in-situ" if key == "HS" else "Masonry"})
        walls[tag] = (wall, p1, p2, t)

    # ---- ground slab and roof
    ground = api.root.create_entity(f, "IfcSlab", predefined_type="FLOOR", name="A-Slabs-1st-Storey")
    rep = api.geometry.add_slab_representation(f, context=body, depth=0.150, polyline=OUTER)
    api.geometry.assign_representation(f, product=ground, representation=rep)
    api.geometry.edit_object_placement(f, product=ground, matrix=placement_matrix((0, 0, 0.0)), is_si=True)
    api.type.assign_type(f, related_objects=[ground], relating_type=slab_gf)
    api.spatial.assign_container(f, products=[ground], relating_structure=storey)
    stage_pset(f, ground)

    roof = api.root.create_entity(f, "IfcRoof", predefined_type="FLAT_ROOF", name="A-Roof-Main")
    api.spatial.assign_container(f, products=[roof], relating_structure=roof_storey)
    roof_slab = api.root.create_entity(f, "IfcSlab", predefined_type="ROOF", name="A-Roof-Slab")
    rep = api.geometry.add_slab_representation(f, context=body, depth=0.125, polyline=ROOF_EDGE)
    api.geometry.assign_representation(f, product=roof_slab, representation=rep)
    api.geometry.edit_object_placement(
        f, product=roof_slab, matrix=placement_matrix((0, 0, ROOF_LEVEL)), is_si=True)
    api.type.assign_type(f, related_objects=[roof_slab], relating_type=slab_roof)
    api.aggregate.assign_object(f, products=[roof_slab], relating_object=roof)
    stage_pset(f, roof_slab)

    # ---- porch columns
    for i, x in enumerate((5.3, 7.7), start=1):
        col = api.root.create_entity(f, "IfcColumn", predefined_type="COLUMN", name=f"A-Columns-P{i:02d}")
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=STOREY_H, polyline=box_polyline(0.200, 0.200))
        api.geometry.assign_representation(f, product=col, representation=rep)
        api.geometry.edit_object_placement(
            f, product=col, matrix=placement_matrix((x, -1.2, FFL)), is_si=True)
        api.spatial.assign_container(f, products=[col], relating_structure=storey)
        stage_pset(f, col)

    # ---- openings, doors and windows
    for mark, host, dist, width, height, sill, main in DOORS:
        make_opening(f, body, storey, walls, host, dist, width, height, sill,
                     element_class="IfcDoor", mark=mark,
                     relating_type=door_types[width],
                     extra={"Main Entrance": main,
                            "Clear Width": round(width * 1000),
                            "Clear Height": round(height * 1000)})

    for mark, host, dist, width, height, sill in WINDOWS:
        make_opening(f, body, storey, walls, host, dist, width, height, sill,
                     element_class="IfcWindow", mark=mark,
                     relating_type=window_types[width],
                     extra={"Percentage of Opening": 50.0,
                            "Safety Barrier Height": 1000})

    # ---- spaces
    for number, name, long_name, rect, thicknesses, external in SPACES:
        space = api.root.create_entity(
            f, "IfcSpace", predefined_type="EXTERNAL" if external else "INTERNAL", name=name)
        space.LongName = long_name
        space.CompositionType = "ELEMENT"
        poly = inset(rect, thicknesses)
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=STOREY_H if not external else 0.050, polyline=poly)
        api.geometry.assign_representation(f, product=space, representation=rep)
        api.geometry.edit_object_placement(
            f, product=space, matrix=placement_matrix((0, 0, FFL)), is_si=True)
        api.aggregate.assign_object(f, products=[space], relating_object=storey)

        pset = api.pset.add_pset(f, product=space, name="Pset_SpaceCommon")
        api.pset.edit_pset(f, pset=pset, properties={
            "IsExternal": external, "Reference": number})

        sg = {"Space Name": name, "Area": round(area_of(poly), 2)}
        if name == "Household Shelter":
            x0, y0, x1, y1 = rect
            sg.update({
                "Construction Method": "Cast in-situ reinforced concrete",
                "Internal Length": round((x1 - x0 - T_HS) * 1000),
                "Internal Width": round((y1 - y0 - T_HS) * 1000),
            })
        if name in ("Bedroom 1", "Bathroom 1", "Circulation", "Entry Foyer", "Covered Entry"):
            sg["Barrier Free Accessibility"] = True
        stage_pset(f, space, extra=sg)

    # ---- grid
    grid = api.root.create_entity(f, "IfcGrid", name="A-Grid")
    api.spatial.assign_container(f, products=[grid], relating_structure=storey)
    for tag, x in GRID_U:
        axis = api.grid.create_grid_axis(f, grid=grid, axis_tag=tag, uvw_axes="UAxes")
        api.grid.create_axis_curve(f, p1=np.array([x, -2.0, 0.0]), p2=np.array([x, 12.0, 0.0]),
                                   grid_axis=axis, is_si=True)
    for tag, y in GRID_V:
        axis = api.grid.create_grid_axis(f, grid=grid, axis_tag=tag, uvw_axes="VAxes")
        api.grid.create_axis_curve(f, p1=np.array([-2.0, y, 0.0]), p2=np.array([14.0, y, 0.0]),
                                   grid_axis=axis, is_si=True)

    return f


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


def make_opening(f, body, storey, walls, host, dist, width, height, sill,
                 element_class, mark, relating_type, extra):
    wall, p1, p2, thickness = walls[host]
    (dx, dy), _ = direction(p1, p2)
    origin = (p1[0] + dx * dist, p1[1] + dy * dist, FFL + sill)

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
    api.spatial.assign_container(f, products=[element], relating_structure=storey)
    api.feature.add_filling(f, opening=opening, element=element)

    common = api.pset.add_pset(f, product=element, name=f"Pset_{element_class[3:]}Common")
    api.pset.edit_pset(f, pset=common, properties={"Reference": mark})
    stage_pset(f, element, extra=extra)
    return element


def stage_pset(f, product, extra=None):
    """Two property sets on everything.

    Bonsai_Upskilling is the course's own change-control data. IFCSG_Demo carries
    IFC+SG *parameter names* so the workflow is visible -- it is deliberately not
    called SGPset_something, because the authoritative property set names come
    from the IFC+SG Excel Mapping File, which you must consult rather than
    inherit from a teaching model.
    """
    pset = api.pset.add_pset(f, product=product, name="Bonsai_Upskilling")
    api.pset.edit_pset(f, pset=pset, properties={
        "project_stage": "03 Schematic Design",
        "design_status": "approved",
    })
    if extra:
        sg = api.pset.add_pset(f, product=product, name="IFCSG_Demo")
        api.pset.edit_pset(f, pset=sg, properties=extra)


if __name__ == "__main__":
    model = build()
    model.write(str(OUT))
    print(f"wrote {OUT}")
    for cls in ("IfcWall", "IfcSlab", "IfcRoof", "IfcColumn", "IfcDoor", "IfcWindow",
                "IfcOpeningElement", "IfcSpace", "IfcBuildingStorey", "IfcGrid"):
        print(f"  {cls:20} {len(model.by_type(cls))}")
