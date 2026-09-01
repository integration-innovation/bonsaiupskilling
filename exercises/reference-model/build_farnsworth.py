"""Build the Farnsworth House reference model as IFC4.

Ludwig Mies van der Rohe, Edith Farnsworth House, 14520 River Road, Plano,
Kendall County, Illinois. Designed 1945-1947, built 1949-1951.

    python exercises/reference-model/build_farnsworth.py

It writes FARN-A-DD-P01.ifc beside this script: the house at the end of Stage 04,
Design Development. That is deliberate. The building is a structural diagram --
eight columns, two slabs, a glass skin and one core -- so the interesting
information is the frame, the curtain wall and the materials, not a room list.
A schematic-stage model of this house would have almost nothing in it.

Built with IfcOpenShell's API, the same API Bonsai's own operators drive, so the
result opens in Bonsai, in any IFC viewer, and can be checked by anything that
reads IFC4.

WHY THIS BUILDING
-----------------
It is the clearest teaching object in modern architecture: every element is
visible, nothing is buried in a cavity, and the whole thing is governed by one
module. It is also legally safe to model, publish and hand to students -- see
LICENSING below.

LICENSING
---------
The building itself is not a copyright constraint. The Architectural Works
Copyright Protection Act took effect 1 December 1990 and does not reach works
constructed before that date, so the Farnsworth House as *architecture* carries
no US copyright that a model of it could infringe.

Photographs are a separate matter and are usually still in copyright -- this
course therefore ships geometry and drawings, not photographs.

The authoritative dimensional record is the Historic American Buildings Survey,
HABS IL-1105 (32 photographs, 8 measured drawings, 54 data pages), held by the
Library of Congress. HABS documentation is prepared by the US National Park
Service and is a work of the United States Government: public domain, no known
restrictions on publication. That is the source this model should ultimately be
corrected against.

    https://www.loc.gov/pictures/item/il0323/          survey record
    https://www.loc.gov/resource/hhh.il0323.sheet      the 8 measured drawings

DIMENSIONAL PROVENANCE -- READ THIS BEFORE TRUSTING A NUMBER
------------------------------------------------------------
The HABS sheets were not reachable from the machine that wrote this script, so
every dimension below comes from published secondary sources, and those sources
disagree with each other. Each figure in DIMS carries its source and a
confidence grade, and each element carries the same grade into the IFC file as a
Farnsworth_Provenance property set. Nothing here pretends to be a survey.

Confidence grades used:

    A   Cross-checked, arithmetically self-consistent, agreed by most sources.
    B   Widely published, but sources differ; the alternatives are recorded.
    C   Derived by the author from A-grade figures and proportional logic.
        Plausible, unverified, and the first thing to correct against HABS.

The strongest single check available without the drawings is that the vertical
dimensions close exactly in feet:

    5'-3"  floor slab above grade
  + 9'-6"  floor to ceiling
  + 1'-3"  15" edge channel at roof
  = 16'-0" top of roof

and the plan closes exactly too:

    3 bays @ 22'-0" = 66'-0", plus 5'-6" cantilever each end = 77'-0"

Two independent closures on figures taken from different sources is good
evidence that the A-grade set is right. It is not a survey, and does not
replace one.

KNOWN CONFLICTS IN THE SOURCES
------------------------------
    Slab width        28'-0" used. Some sources say 29'-0". 28'-0" is adopted
                      because it matches the repeatedly stated "two parallel
                      rows of columns 28 feet apart", and the columns are welded
                      to the slab edge.
    Bay spacing       22'-0" used. One source says 20'-0" intervals, which
                      cannot close to 77'-0" with a credible cantilever
                      (3 x 20 = 60, leaving 8'-6" cantilevers against a 20' bay).
    Terrace width     22'-0" used. Sources offer 22'-0" and 23'-0".
    Core size         20'-0" x 8'-0" used, the best-attested of three published
                      figures. The others are 10'-0" x 28'-0" and 32'-0" x 8'-0";
                      the second is implausible (it would span the full width)
                      and the third is probably measuring core plus kitchen run.
    Terrace position  Grade C throughout. The offset between terrace and house
                      is taken from photographs and general description, not
                      from a plan. HABS sheet 3 settles it.

Requires ifcopenshell 0.8.x.  Licensed GPL-3.0-or-later, matching Bonsai.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

import ifcopenshell
import ifcopenshell.api as api
import ifcopenshell.api.aggregate
import ifcopenshell.api.context
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
import ifcopenshell.util.unit

OUT = Path(__file__).resolve().parent / "FARN-A-DD-P01.ifc"


# ------------------------------------------------------------------- units --
# The house was designed in feet and inches. Author in feet and inches, store
# in millimetres. Doing it the other way round invents precision that the
# building never had.

def ft(feet: float, inches: float = 0.0) -> float:
    """Feet and inches to metres.

    The sign belongs to the whole dimension, not to the feet alone: -6'-6" is
    -6.5 feet, not -5.5. Adding the inches unsigned is the obvious way to write
    this and it is wrong for every measurement west or south of the origin.
    """
    sign = -1.0 if (feet < 0 or (feet == 0 and inches < 0)) else 1.0
    return sign * (abs(feet) + abs(inches) / 12.0) * 0.3048


# -------------------------------------------------------------- dimensions --
# name: (metres, source, confidence, note)
DIMS: dict[str, tuple[float, str, str, str]] = {
    "slab_length":   (ft(77),     "Columbia GSAPP; Britannica; ArchEyes", "A",
                      "77'-0\" main house slab, long axis"),
    "slab_width":    (ft(28),     "Columbia GSAPP 'rows 28 feet apart'",  "B",
                      "28'-0\"; some sources say 29'-0\""),
    "bay":           (ft(22),     "closure against 77'-0\" overall",      "A",
                      "3 bays at 22'-0\""),
    "cantilever":    (ft(5, 6),   "closure: (77 - 3*22)/2",               "A",
                      "5'-6\" each end"),
    "floor_level":   (ft(5, 3),   "Columbia GSAPP; Britannica",           "A",
                      "top of floor slab above grade"),
    "clear_height":  (ft(9, 6),   "glass height, widely published",       "A",
                      "floor to ceiling"),
    "edge_channel":  (ft(1, 3),   "15\" channel, Columbia GSAPP",         "A",
                      "structural depth of floor and roof planes"),
    "terrace_level": (ft(2),      "widely published 'about 2 feet'",      "B",
                      "top of terrace slab above grade"),
    "terrace_length":(ft(55),     "Columbia GSAPP 55' x 23' slab",        "B",
                      "55'-0\""),
    "terrace_width": (ft(22),     "Columbia GSAPP; others say 23'-0\"",   "B",
                      "22'-0\""),
    "porch_length":  (ft(22),     "derived: 77 - 55 enclosure",           "C",
                      "west porch, one bay deep"),
    "enclosure_len": (ft(55),     "derived: 1,540 sq ft matches ~1,500",  "C",
                      "glazed enclosure, 55'-0\" x 28'-0\""),
    "core_length":   (ft(20),     "best-attested of three figures",       "B",
                      "20'-0\" service core"),
    "core_width":    (ft(8),      "best-attested of three figures",       "B",
                      "8'-0\" service core"),
}


def D(key: str) -> float:
    return DIMS[key][0]


def grade(key: str) -> str:
    return DIMS[key][2]


# Convenience locals, all metres.
SLAB_L = D("slab_length")
SLAB_W = D("slab_width")
BAY = D("bay")
CANT = D("cantilever")
FFL = D("floor_level")
CLEAR_H = D("clear_height")
CHANNEL = D("edge_channel")
TERR_FFL = D("terrace_level")
TERR_L = D("terrace_length")
TERR_W = D("terrace_width")
PORCH_L = D("porch_length")
ENC_L = D("enclosure_len")
CORE_L = D("core_length")
CORE_W = D("core_width")

CEILING = FFL + CLEAR_H          # 4.4958 m = 14'-9"
ROOF_TOP = CEILING + CHANNEL     # 4.8768 m = 16'-0" exactly

# Origin: south-west corner of the main house slab, at existing grade.
# +X east along the 77' axis, +Y north across the 28' axis, +Z up.
ENC_X0, ENC_X1 = PORCH_L, SLAB_L          # glazed enclosure, 22'-0" to 77'-0"
ENC_Y0, ENC_Y1 = 0.0, SLAB_W

# W8x48 wide flange. Depth 8.5", flange 8.117", web 0.40", flange 0.685".
COL_D, COL_BF = ft(0, 8.5), ft(0, 8.117)
COL_TW, COL_TF = ft(0, 0.40), ft(0, 0.685)

# Column centres. Welded to the slab edge, so the section sits outboard of it.
COL_X = [CANT + i * BAY for i in range(4)]
COL_Y = [ENC_Y0 - COL_D / 2.0, ENC_Y1 + COL_D / 2.0]

# Service core, asymmetrically placed. West of centre, pushed north, leaving a
# 12'-0" living band to the south and an 8'-0" kitchen run to the north.
CORE_X0, CORE_X1 = ft(38), ft(58)
CORE_Y0, CORE_Y1 = ft(12), ft(20)
CORE_T = ft(0, 4)                          # primavera-faced partition

# Terrace: south-west of the house, abutting its south edge. GRADE C.
TERR_X0, TERR_X1 = ft(-33), ft(22)
TERR_Y0, TERR_Y1 = ft(-22), ft(0)

MULLION_W, MULLION_D = ft(0, 2), ft(0, 4)
GLASS_T = ft(0, 0.25)

# Curtain wall bays. South and north: five panes of 11'-0". East and west: four
# panes of 7'-0". The west wall carries the entrance, so its run is split.
LONG_DIVS = [ENC_X0 + i * ft(11) for i in range(6)]
END_DIVS = [ENC_Y0 + i * ft(7) for i in range(5)]
DOOR_Y0, DOOR_Y1 = ft(15, 9), ft(19, 3)    # 3'-6" leaf in the west wall

GRID_U = [("1", COL_X[0]), ("2", COL_X[1]), ("3", COL_X[2]), ("4", COL_X[3])]
GRID_V = [("A", ENC_Y0), ("B", ENC_Y1)]

# number, name, long name, (x0, y0, x1, y1), height, external
SPACES = [
    ("01", "Living",      "Living area, south of the core",
     (ENC_X0, ENC_Y0, ENC_X1, CORE_Y0), CLEAR_H, False),
    ("02", "Dining",      "Dining area, west of the core",
     (ENC_X0, CORE_Y0, CORE_X0, ENC_Y1), CLEAR_H, False),
    ("03", "Kitchen",     "Kitchen run, north of the core",
     (CORE_X0, CORE_Y1, CORE_X1, ENC_Y1), CLEAR_H, False),
    ("04", "Sleeping",    "Sleeping area, east of the core",
     (CORE_X1, CORE_Y0, ENC_X1, ENC_Y1), CLEAR_H, False),
    ("05", "Bathroom W",  "Guest bathroom, in the core",
     (ft(38) + CORE_T, CORE_Y0 + CORE_T, ft(45) - CORE_T / 2, CORE_Y1 - CORE_T), CLEAR_H, False),
    ("06", "Utility",     "Mechanical space, in the core",
     (ft(45) + CORE_T / 2, CORE_Y0 + CORE_T, ft(49) - CORE_T / 2, CORE_Y1 - CORE_T), CLEAR_H, False),
    ("07", "Bathroom E",  "Primary bathroom, in the core",
     (ft(49) + CORE_T / 2, CORE_Y0 + CORE_T, CORE_X1 - CORE_T, CORE_Y1 - CORE_T), CLEAR_H, False),
    ("08", "West Porch",  "Open porch under the roof plane",
     (0.0, ENC_Y0, PORCH_L, ENC_Y1), CLEAR_H, True),
    ("09", "Terrace",     "Lower travertine terrace",
     (TERR_X0, TERR_Y0, TERR_X1, TERR_Y1), 0.050, True),
]


# ------------------------------------------------------------------ helpers --

def matrix(origin, xdir=(1.0, 0.0, 0.0), zdir=(0.0, 0.0, 1.0)) -> np.ndarray:
    """A right-handed placement from an origin and two axes."""
    x = np.array(xdir, dtype=float)
    x /= np.linalg.norm(x)
    z = np.array(zdir, dtype=float)
    z /= np.linalg.norm(z)
    y = np.cross(z, x)
    m = np.eye(4)
    m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = x, y, z, origin
    return m


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def area_of(polyline):
    a = 0.0
    for i in range(len(polyline)):
        x0, y0 = polyline[i]
        x1, y1 = polyline[(i + 1) % len(polyline)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2.0


class Builder:
    """Wraps the file so raw profile geometry can be created in file units."""

    def __init__(self, f, body):
        self.f = f
        self.body = body
        self.scale = ifcopenshell.util.unit.calculate_unit_scale(f)

    def u(self, metres: float) -> float:
        return metres / self.scale

    def i_profile(self, name, depth, width, web_t, flange_t):
        return self.f.createIfcIShapeProfileDef(
            "AREA", name, None, self.u(width), self.u(depth),
            self.u(web_t), self.u(flange_t))

    def u_profile(self, name, depth, flange_w, web_t, flange_t):
        return self.f.createIfcUShapeProfileDef(
            "AREA", name, None, self.u(depth), self.u(flange_w),
            self.u(web_t), self.u(flange_t))

    def rect_profile(self, name, width, depth):
        return self.f.createIfcRectangleProfileDef(
            "AREA", name, None, self.u(width), self.u(depth))

    def poly_profile(self, name, points):
        pts = [self.f.createIfcCartesianPoint((self.u(px), self.u(py))) for px, py in points]
        return self.f.createIfcArbitraryClosedProfileDef(
            "AREA", name, self.f.createIfcPolyline(pts + [pts[0]]))

    def extrude(self, profile, depth):
        place = self.f.createIfcAxis2Placement3D(
            self.f.createIfcCartesianPoint((0.0, 0.0, 0.0)))
        solid = self.f.createIfcExtrudedAreaSolid(
            profile, place, self.f.createIfcDirection((0.0, 0.0, 1.0)), self.u(depth))
        return self.f.createIfcShapeRepresentation(self.body, "Body", "SweptSolid", [solid])


def provenance(f, product, source: str, confidence: str, note: str = ""):
    """Every element says where its dimensions came from and how sure that is.

    This is the course's 'record the source and the date' rule applied to the
    model rather than to a spreadsheet. A student opening any element in Bonsai
    can see whether they are looking at a measured figure or a guess.
    """
    pset = api.pset.add_pset(f, product=product, name="Farnsworth_Provenance")
    props = {"dimension_source": source, "confidence": confidence}
    if note:
        props["note"] = note
    api.pset.edit_pset(f, pset=pset, properties=props)


def stage_pset(f, product, status="approved"):
    pset = api.pset.add_pset(f, product=product, name="Bonsai_Upskilling")
    api.pset.edit_pset(f, pset=pset, properties={
        "project_stage": "04 Design Development",
        "design_status": status,
    })


# -------------------------------------------------------------------- build --

def build() -> ifcopenshell.file:
    f = api.project.create_file("IFC4")

    project = api.root.create_entity(f, "IfcProject", name="Edith Farnsworth House")
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
    b = Builder(f, body)

    # Georeferencing. NAD83 / UTM zone 16N covers northern Illinois. The
    # coordinates put the model on the real site, on the north bank of the Fox
    # River, but they are read off a map rather than surveyed -- and the True
    # North rotation is deliberately left at zero, because the building's real
    # bearing is on HABS sheet 1 and this script has not seen it. Do not quote
    # these numbers as survey data.
    api.georeference.add_georeferencing(f)
    api.georeference.edit_georeferencing(
        f,
        projected_crs={
            "Name": "EPSG:26916",
            "Description": "NAD83 / UTM zone 16N",
            "GeodeticDatum": "NAD83",
            "VerticalDatum": "NAVD88",
        },
        coordinate_operation={
            "Eastings": 372400.0,
            "Northings": 4604600.0,
            "OrthogonalHeight": 176.0,
            "XAxisAbscissa": 1.0,
            "XAxisOrdinate": 0.0,
            "Scale": 1.0,
        },
    )

    site = api.root.create_entity(f, "IfcSite", name="Fox River Floodplain")
    building = api.root.create_entity(f, "IfcBuilding", name="Edith Farnsworth House")
    # Storey names follow CORENET X level naming even though the building is in
    # Illinois. The convention is what the course teaches and a reference model
    # that breaks it teaches the opposite. "Main Floor" and "Terrace" are both
    # invalid forms; "1st Storey" and a "_suffix" datum variant are valid.
    terrace_storey = api.root.create_entity(
        f, "IfcBuildingStorey", name="1st Storey_Terrace")
    storey = api.root.create_entity(f, "IfcBuildingStorey", name="1st Storey")
    roof_storey = api.root.create_entity(f, "IfcBuildingStorey", name="Roof")
    terrace_storey.Elevation = TERR_FFL * 1000.0
    storey.Elevation = FFL * 1000.0
    roof_storey.Elevation = ROOF_TOP * 1000.0
    api.aggregate.assign_object(f, products=[site], relating_object=project)
    api.aggregate.assign_object(f, products=[building], relating_object=site)
    api.aggregate.assign_object(
        f, products=[terrace_storey, storey, roof_storey], relating_object=building)

    stage_pset(f, building)
    provenance(f, building, "HABS IL-1105 not consulted; see module docstring",
               "B", "Mies van der Rohe, 1945-1951")
    for s in (terrace_storey, storey, roof_storey):
        stage_pset(f, s)

    # ---- materials
    materials = {
        name: api.material.add_material(f, name=name, category=cat)
        for name, cat in [
            ("Structural steel, painted white", "steel"),
            ("Travertine", "stone"),
            ("Precast concrete plank", "concrete"),
            ("Primavera plywood", "wood"),
            ("Plate glass", "glass"),
            ("Reinforced concrete", "concrete"),
        ]
    }

    # ---- types
    floor_type = api.root.create_entity(
        f, "IfcSlabType", predefined_type="FLOOR", name="FLR-TRAV-PLANK-STEEL")
    attach_layers(f, floor_type, [
        ("Travertine", ft(0, 1.25)),
        ("Precast concrete plank", ft(0, 4)),
        ("Structural steel, painted white", CHANNEL - ft(0, 5.25)),
    ], materials)

    roof_type = api.root.create_entity(
        f, "IfcSlabType", predefined_type="ROOF", name="ROOF-STEEL-15C")
    attach_layers(f, roof_type, [
        ("Structural steel, painted white", CHANNEL - ft(0, 4)),
        ("Precast concrete plank", ft(0, 4)),
    ], materials)

    terrace_type = api.root.create_entity(
        f, "IfcSlabType", predefined_type="FLOOR", name="TERR-TRAV-RC")
    attach_layers(f, terrace_type, [
        ("Travertine", ft(0, 1.25)),
        ("Reinforced concrete", ft(0, 6.75)),
    ], materials)

    column_type = api.root.create_entity(
        f, "IfcColumnType", predefined_type="COLUMN", name="COL-W8X48")
    api.material.assign_material(
        f, products=[column_type], type="IfcMaterial",
        material=materials["Structural steel, painted white"])

    beam_type = api.root.create_entity(
        f, "IfcBeamType", predefined_type="BEAM", name="BM-C15-EDGE")
    api.material.assign_material(
        f, products=[beam_type], type="IfcMaterial",
        material=materials["Structural steel, painted white"])

    cw_type = api.root.create_entity(
        f, "IfcCurtainWallType", predefined_type="NOTDEFINED", name="CW-PLATE-GLASS")
    plate_type = api.root.create_entity(
        f, "IfcPlateType", predefined_type="CURTAIN_PANEL", name="GL-PLATE-6MM")
    api.material.assign_material(
        f, products=[plate_type], type="IfcMaterial", material=materials["Plate glass"])
    member_type = api.root.create_entity(
        f, "IfcMemberType", predefined_type="MULLION", name="MULL-STEEL-50X100")
    api.material.assign_material(
        f, products=[member_type], type="IfcMaterial",
        material=materials["Structural steel, painted white"])

    core_type = api.root.create_entity(
        f, "IfcWallType", predefined_type="SOLIDWALL", name="CORE-PRIMAVERA-100")
    attach_layers(f, core_type, [("Primavera plywood", CORE_T)], materials)

    door_type = api.root.create_entity(
        f, "IfcDoorType", predefined_type="DOOR", name="DR-GLASS-1067")

    types = {
        "core": core_type, "cw": cw_type, "plate": plate_type,
        "member": member_type, "door": door_type,
    }

    # ---- floor and roof planes
    for name, top, slab_type, pdef, host in (
        ("A-Slabs-Main-Floor", FFL, floor_type, "FLOOR", storey),
        ("A-Slabs-Roof", ROOF_TOP, roof_type, "ROOF", roof_storey),
    ):
        slab = api.root.create_entity(f, "IfcSlab", predefined_type=pdef, name=name)
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=CHANNEL, polyline=rect(0.0, ENC_Y0, SLAB_L, ENC_Y1))
        api.geometry.assign_representation(f, product=slab, representation=rep)
        api.geometry.edit_object_placement(
            f, product=slab, matrix=matrix((0.0, 0.0, top - CHANNEL)), is_si=True)
        api.type.assign_type(f, related_objects=[slab], relating_type=slab_type)
        api.spatial.assign_container(f, products=[slab], relating_structure=host)
        pset = api.pset.add_pset(f, product=slab, name="Pset_SlabCommon")
        api.pset.edit_pset(f, pset=pset, properties={"IsExternal": True, "LoadBearing": True})
        stage_pset(f, slab)
        provenance(f, slab, DIMS["slab_length"][1], "A",
                   "77'-0\" x 28'-0\", 15\" structural depth")

    # ---- lower terrace
    terrace = api.root.create_entity(f, "IfcSlab", predefined_type="FLOOR", name="A-Slabs-Terrace")
    rep = api.geometry.add_slab_representation(
        f, context=body, depth=ft(0, 8), polyline=rect(TERR_X0, TERR_Y0, TERR_X1, TERR_Y1))
    api.geometry.assign_representation(f, product=terrace, representation=rep)
    api.geometry.edit_object_placement(
        f, product=terrace, matrix=matrix((0.0, 0.0, TERR_FFL - ft(0, 8))), is_si=True)
    api.type.assign_type(f, related_objects=[terrace], relating_type=terrace_type)
    api.spatial.assign_container(f, products=[terrace], relating_structure=terrace_storey)
    stage_pset(f, terrace, status="provisional")
    provenance(f, terrace, DIMS["terrace_length"][1], "C",
               "55'-0\" x 22'-0\"; offset from the house is unverified")

    # ---- the eight columns
    profile = b.i_profile("W8X48", COL_D, COL_BF, COL_TW, COL_TF)
    n = 0
    for gi, x in enumerate(COL_X):
        for row, y in zip("AB", COL_Y):
            n += 1
            col = api.root.create_entity(
                f, "IfcColumn", predefined_type="COLUMN", name=f"A-Columns-{row}{gi + 1}")
            col.Tag = f"{row}{gi + 1}"
            rep = b.extrude(profile, ROOF_TOP)
            api.geometry.assign_representation(f, product=col, representation=rep)
            api.geometry.edit_object_placement(
                f, product=col, matrix=matrix((x, y, 0.0)), is_si=True)
            api.type.assign_type(f, related_objects=[col], relating_type=column_type)
            api.spatial.assign_container(f, products=[col], relating_structure=storey)
            pset = api.pset.add_pset(f, product=col, name="Pset_ColumnCommon")
            api.pset.edit_pset(f, pset=pset, properties={"IsExternal": True, "LoadBearing": True})
            stage_pset(f, col)
            provenance(f, col, "8 wide-flange columns, rows 28'-0\" apart", "A",
                       "welded to the slab edge, not carried through it")

    # ---- 15in edge channels, floor and roof, on the two long sides
    chan = b.u_profile("C15X33.9", CHANNEL, ft(0, 3.4), ft(0, 0.4), ft(0, 0.65))
    for level, top in (("Floor", FFL), ("Roof", ROOF_TOP)):
        for row, y in (("A", ENC_Y0), ("B", ENC_Y1)):
            beam = api.root.create_entity(
                f, "IfcBeam", predefined_type="BEAM", name=f"A-Beams-{level}-{row}")
            rep = b.extrude(chan, SLAB_L)
            api.geometry.assign_representation(f, product=beam, representation=rep)
            # Profile plane vertical, extruded east along the 77' axis.
            api.geometry.edit_object_placement(
                f, product=beam,
                matrix=matrix((0.0, y, top - CHANNEL / 2.0), xdir=(0, 1, 0), zdir=(1, 0, 0)),
                is_si=True)
            api.type.assign_type(f, related_objects=[beam], relating_type=beam_type)
            api.spatial.assign_container(
                f, products=[beam],
                relating_structure=roof_storey if level == "Roof" else storey)
            stage_pset(f, beam)
            provenance(f, beam, "15\" channel sections, Columbia GSAPP", "A",
                       "the white band read as the edge of each plane")

    # ---- the glass skin
    # One IfcCurtainWall per elevation, each aggregating its glass plates and
    # its mullions. This is the correct IFC decomposition and it is why the
    # model can answer "how much glass is there" without measuring anything.
    glass_h = CLEAR_H
    plates = 0
    mullions = 0

    def add_plate(cw, name, x0, y0, x1, y1):
        nonlocal plates
        plates += 1
        plate = api.root.create_entity(
            f, "IfcPlate", predefined_type="CURTAIN_PANEL", name=name)
        length = max(abs(x1 - x0), abs(y1 - y0))
        along = (1.0, 0.0, 0.0) if abs(x1 - x0) >= abs(y1 - y0) else (0.0, 1.0, 0.0)
        prof = b.rect_profile(f"GL-{int(round(length * 1000))}", length, GLASS_T)
        rep = b.extrude(prof, glass_h)
        api.geometry.assign_representation(f, product=plate, representation=rep)
        api.geometry.edit_object_placement(
            f, product=plate,
            matrix=matrix(((x0 + x1) / 2.0, (y0 + y1) / 2.0, FFL), xdir=along),
            is_si=True)
        api.type.assign_type(f, related_objects=[plate], relating_type=types["plate"])
        api.aggregate.assign_object(f, products=[plate], relating_object=cw)
        stage_pset(f, plate)
        return plate

    def add_mullion(cw, name, x, y, along):
        nonlocal mullions
        mullions += 1
        member = api.root.create_entity(
            f, "IfcMember", predefined_type="MULLION", name=name)
        prof = b.rect_profile("MULL-50X100", MULLION_W, MULLION_D)
        rep = b.extrude(prof, glass_h)
        api.geometry.assign_representation(f, product=member, representation=rep)
        api.geometry.edit_object_placement(
            f, product=member, matrix=matrix((x, y, FFL), xdir=along), is_si=True)
        api.type.assign_type(f, related_objects=[member], relating_type=types["member"])
        api.aggregate.assign_object(f, products=[member], relating_object=cw)
        stage_pset(f, member)
        return member

    def curtain_wall(name):
        cw = api.root.create_entity(
            f, "IfcCurtainWall", predefined_type="NOTDEFINED", name=name)
        api.type.assign_type(f, related_objects=[cw], relating_type=types["cw"])
        api.spatial.assign_container(f, products=[cw], relating_structure=storey)
        pset = api.pset.add_pset(f, product=cw, name="Pset_CurtainWallCommon")
        api.pset.edit_pset(f, pset=pset, properties={"IsExternal": True})
        stage_pset(f, cw)
        provenance(f, cw, "single-glazed plate glass, 9'-6\" floor to ceiling", "A",
                   "pane widths are grade C: the rhythm is derived, not measured")
        return cw

    # South and north elevations: five panes of 11'-0".
    for name, y in (("A-Glazing-South", ENC_Y0), ("A-Glazing-North", ENC_Y1)):
        cw = curtain_wall(name)
        for i in range(len(LONG_DIVS) - 1):
            add_plate(cw, f"{name}-P{i + 1:02d}", LONG_DIVS[i], y, LONG_DIVS[i + 1], y)
        for i, x in enumerate(LONG_DIVS):
            add_mullion(cw, f"{name}-M{i + 1:02d}", x, y, (0.0, 1.0, 0.0))

    # East elevation: four panes of 7'-0".
    cw = curtain_wall("A-Glazing-East")
    for i in range(len(END_DIVS) - 1):
        add_plate(cw, f"A-Glazing-East-P{i + 1:02d}", ENC_X1, END_DIVS[i], ENC_X1, END_DIVS[i + 1])
    for i, y in enumerate(END_DIVS):
        add_mullion(cw, f"A-Glazing-East-M{i + 1:02d}", ENC_X1, y, (1.0, 0.0, 0.0))

    # West elevation: the same four bays, but the third is split by the door.
    cw = curtain_wall("A-Glazing-West")
    west_segments = []
    for i in range(len(END_DIVS) - 1):
        y0, y1 = END_DIVS[i], END_DIVS[i + 1]
        if y0 < DOOR_Y0 and y1 > DOOR_Y1:
            west_segments += [(y0, DOOR_Y0), (DOOR_Y1, y1)]
        else:
            west_segments.append((y0, y1))
    for i, (y0, y1) in enumerate(west_segments):
        add_plate(cw, f"A-Glazing-West-P{i + 1:02d}", ENC_X0, y0, ENC_X0, y1)
    for i, y in enumerate(sorted(set(END_DIVS + [DOOR_Y0, DOOR_Y1]))):
        add_mullion(cw, f"A-Glazing-West-M{i + 1:02d}", ENC_X0, y, (1.0, 0.0, 0.0))

    # ---- the entrance
    door = api.root.create_entity(f, "IfcDoor", predefined_type="DOOR", name="A-Doors-D01")
    door.OverallWidth = (DOOR_Y1 - DOOR_Y0) * 1000.0
    door.OverallHeight = glass_h * 1000.0
    door.Tag = "D01"
    prof = b.rect_profile("DR-GLASS", DOOR_Y1 - DOOR_Y0, GLASS_T)
    rep = b.extrude(prof, glass_h)
    api.geometry.assign_representation(f, product=door, representation=rep)
    api.geometry.edit_object_placement(
        f, product=door,
        matrix=matrix((ENC_X0, (DOOR_Y0 + DOOR_Y1) / 2.0, FFL), xdir=(0.0, 1.0, 0.0)),
        is_si=True)
    api.type.assign_type(f, related_objects=[door], relating_type=types["door"])
    api.spatial.assign_container(f, products=[door], relating_structure=storey)
    pset = api.pset.add_pset(f, product=door, name="Pset_DoorCommon")
    api.pset.edit_pset(f, pset=pset, properties={"Reference": "D01", "IsExternal": True})
    stage_pset(f, door)
    provenance(f, door, "entrance from the west porch", "C",
               "3'-6\" leaf; position within the west wall is unverified")

    # ---- the core
    # Four primavera-faced partitions plus two cross walls. The core is the only
    # thing in the house that touches both slabs and is not glass.
    core_walls = [
        ("A-Walls-Core-South", CORE_X0, CORE_Y0, CORE_X1, CORE_Y0),
        ("A-Walls-Core-North", CORE_X0, CORE_Y1, CORE_X1, CORE_Y1),
        ("A-Walls-Core-West",  CORE_X0, CORE_Y0, CORE_X0, CORE_Y1),
        ("A-Walls-Core-East",  CORE_X1, CORE_Y0, CORE_X1, CORE_Y1),
        ("A-Walls-Core-D1",    ft(45),  CORE_Y0, ft(45),  CORE_Y1),
        ("A-Walls-Core-D2",    ft(49),  CORE_Y0, ft(49),  CORE_Y1),
    ]
    for name, x0, y0, x1, y1 in core_walls:
        wall = api.root.create_entity(f, "IfcWall", predefined_type="SOLIDWALL", name=name)
        length = max(abs(x1 - x0), abs(y1 - y0))
        along = (1.0, 0.0, 0.0) if abs(x1 - x0) >= abs(y1 - y0) else (0.0, 1.0, 0.0)
        prof = b.rect_profile(f"CORE-{int(round(length * 1000))}", length, CORE_T)
        rep = b.extrude(prof, CLEAR_H)
        api.geometry.assign_representation(f, product=wall, representation=rep)
        api.geometry.edit_object_placement(
            f, product=wall,
            matrix=matrix(((x0 + x1) / 2.0, (y0 + y1) / 2.0, FFL), xdir=along), is_si=True)
        api.type.assign_type(f, related_objects=[wall], relating_type=types["core"])
        api.spatial.assign_container(f, products=[wall], relating_structure=storey)
        pset = api.pset.add_pset(f, product=wall, name="Pset_WallCommon")
        api.pset.edit_pset(f, pset=pset, properties={"IsExternal": False, "LoadBearing": False})
        stage_pset(f, wall)
        provenance(f, wall, DIMS["core_length"][1], "B",
                   "20'-0\" x 8'-0\" core; sources give three different sizes")

    # ---- fireplace and flue
    # The one element that punctures the roof plane. Everything else stops.
    chimney = api.root.create_entity(
        f, "IfcChimney", predefined_type="NOTDEFINED", name="A-Chimney-Fireplace")
    prof = b.rect_profile("FLUE", ft(6), ft(2))
    rep = b.extrude(prof, ROOF_TOP + ft(2) - FFL)
    api.geometry.assign_representation(f, product=chimney, representation=rep)
    api.geometry.edit_object_placement(
        f, product=chimney, matrix=matrix((ft(49), ft(11), FFL)), is_si=True)
    api.spatial.assign_container(f, products=[chimney], relating_structure=storey)
    api.material.assign_material(
        f, products=[chimney], type="IfcMaterial", material=materials["Primavera plywood"])
    stage_pset(f, chimney)
    provenance(f, chimney, "flue and bathroom vents puncture the roof", "C",
               "size and position derived from the core, not measured")

    # ---- the freestanding wardrobe that screens the sleeping area
    wardrobe = api.root.create_entity(
        f, "IfcFurniture", predefined_type="SHELF", name="A-Fixtures-Wardrobe")
    prof = b.rect_profile("WARDROBE", ft(8), ft(2))
    rep = b.extrude(prof, ft(6))
    api.geometry.assign_representation(f, product=wardrobe, representation=rep)
    api.geometry.edit_object_placement(
        f, product=wardrobe, matrix=matrix((ft(63), ft(19), FFL)), is_si=True)
    api.spatial.assign_container(f, products=[wardrobe], relating_structure=storey)
    api.material.assign_material(
        f, products=[wardrobe], type="IfcMaterial", material=materials["Primavera plywood"])
    stage_pset(f, wardrobe, status="provisional")
    provenance(f, wardrobe, "freestanding wardrobe screens the bed", "C",
               "indicative; the house has no internal doors except the core")

    # ---- the two flights
    # Grade to terrace, then terrace to porch. Broad, low and detached from the
    # building: the approach is the only part of the house that touches ground.
    def stair(name, origin, travel, width_dir, width, risers, rise, going):
        points = [(0.0, 0.0)]
        for i in range(risers):
            points.append((i * going, (i + 1) * rise))
            points.append(((i + 1) * going, (i + 1) * rise))
        points.append((risers * going, 0.0))
        s = api.root.create_entity(
            f, "IfcStair", predefined_type="STRAIGHT_RUN_STAIR", name=name)
        rep = b.extrude(b.poly_profile(name, points), width)
        api.geometry.assign_representation(f, product=s, representation=rep)
        # The profile is drawn in a vertical plane -- local X is the direction of
        # travel, local Y is up -- and extruded sideways, so the local Z axis is
        # the width of the flight. Passing (0,0,1) here would extrude the flight
        # into the sky instead of across it.
        api.geometry.edit_object_placement(
            f, product=s, matrix=matrix(origin, xdir=travel, zdir=width_dir),
            is_si=True)
        api.spatial.assign_container(f, products=[s], relating_structure=terrace_storey)
        api.material.assign_material(
            f, products=[s], type="IfcMaterial", material=materials["Travertine"])
        pset = api.pset.add_pset(f, product=s, name="Pset_StairCommon")
        api.pset.edit_pset(f, pset=pset, properties={
            "NumberOfRiser": risers, "RiserHeight": rise * 1000.0,
            "TreadLength": going * 1000.0, "IsExternal": True})
        stage_pset(f, s, status="provisional")
        provenance(f, s, "two broad flights, grade to terrace to porch", "C",
                   "riser and going derived from the level difference")
        return s

    # Grade to terrace: four 6" risers, travelling east, 8'-0" wide.
    stair("A-Stairs-F1", (ft(-38), ft(-8), 0.0), (1.0, 0.0, 0.0), (0.0, -1.0, 0.0),
          ft(8), 4, TERR_FFL / 4.0, ft(1, 3))
    # Terrace to porch: six 6.5" risers, travelling north, 8'-0" wide.
    stair("A-Stairs-F2", (ft(6), ft(-6, 6), TERR_FFL), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0),
          ft(8), 6, (FFL - TERR_FFL) / 6.0, ft(1, 1))

    # ---- spaces
    for number, name, long_name, r, height, external in SPACES:
        space = api.root.create_entity(
            f, "IfcSpace", predefined_type="EXTERNAL" if external else "INTERNAL", name=name)
        space.LongName = long_name
        space.CompositionType = "ELEMENT"
        poly = rect(*r)
        rep = api.geometry.add_slab_representation(
            f, context=body, depth=height, polyline=poly)
        api.geometry.assign_representation(f, product=space, representation=rep)
        base = TERR_FFL if name == "Terrace" else FFL
        api.geometry.edit_object_placement(
            f, product=space, matrix=matrix((0.0, 0.0, base)), is_si=True)
        api.aggregate.assign_object(
            f, products=[space],
            relating_object=terrace_storey if name == "Terrace" else storey)
        pset = api.pset.add_pset(f, product=space, name="Pset_SpaceCommon")
        api.pset.edit_pset(f, pset=pset, properties={
            "IsExternal": external, "Reference": number})
        qto = api.pset.add_qto(f, product=space, name="Qto_SpaceBaseQuantities")
        api.pset.edit_qto(f, qto=qto, properties={
            "NetFloorArea": round(area_of(poly), 3),
            "FinishCeilingHeight": round(height, 3),
        })
        stage_pset(f, space)
        provenance(f, space, "zones read off the core position", "C",
                   "the house has one room; these are zones, not enclosures")

    # ---- the grid the whole building obeys
    grid = api.root.create_entity(f, "IfcGrid", name="A-Grid")
    api.spatial.assign_container(f, products=[grid], relating_structure=storey)
    for tag, x in GRID_U:
        axis = api.grid.create_grid_axis(f, grid=grid, axis_tag=tag, uvw_axes="UAxes")
        api.grid.create_axis_curve(
            f, p1=np.array([x, ft(-6), 0.0]), p2=np.array([x, SLAB_W + ft(6), 0.0]),
            grid_axis=axis, is_si=True)
    for tag, y in GRID_V:
        axis = api.grid.create_grid_axis(f, grid=grid, axis_tag=tag, uvw_axes="VAxes")
        api.grid.create_axis_curve(
            f, p1=np.array([ft(-6), y, 0.0]), p2=np.array([SLAB_L + ft(6), y, 0.0]),
            grid_axis=axis, is_si=True)

    print(f"  curtain wall: {plates} plates, {mullions} mullions")
    return f


def attach_layers(f, element_type, layers, materials):
    layer_set = api.material.add_material_set(
        f, name=element_type.Name, set_type="IfcMaterialLayerSet")
    for material_name, thickness in layers:
        layer = api.material.add_layer(
            f, layer_set=layer_set, material=materials[material_name], name=material_name)
        layer.LayerThickness = thickness * 1000.0
    api.material.assign_material(
        f, products=[element_type], type="IfcMaterialLayerSet", material=layer_set)


if __name__ == "__main__":
    model = build()
    model.write(str(OUT))
    print(f"wrote {OUT}")
    for cls in ("IfcSlab", "IfcColumn", "IfcBeam", "IfcCurtainWall", "IfcPlate",
                "IfcMember", "IfcWall", "IfcDoor", "IfcChimney", "IfcFurniture",
                "IfcStair", "IfcSpace", "IfcBuildingStorey", "IfcGrid"):
        print(f"  {cls:20} {len(model.by_type(cls))}")
