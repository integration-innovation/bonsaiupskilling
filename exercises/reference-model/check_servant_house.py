"""Check the Servant and Served House the way a gate check should.

    python exercises/reference-model/check_servant_house.py [model.ifc]

Every rule here is one the course states somewhere -- in the model standard, in
a stage gate, or in IFC+SG and CORENET X's General Modelling Practices.

Four groups matter more than the rest:

  SHELTER   The household shelter satisfies SCDF's dimensional limits, carries
            its construction method and internal dimensions as data, and its
            declared internal size actually multiplies out to its floor area.
            A shelter whose data and geometry disagree is worse than no data.
  TOWER     The servant towers are founded and continuous: every tower wall
            exists on every storey. A tower that stops halfway is not a tower,
            and a shelter under a discontinuous tower is not a shelter.
  CORENET   Level naming, one site, SVY21 easting and northing, SHD elevation,
            a True North rotation.
  VAF       Every element says which Value Articulation Framework component it
            serves, so the model can be read against the fee rather than beside
            it.

Exits non-zero on any failure, so it works as a CI gate.

Licensed GPL-3.0-or-later, matching Bonsai.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element

DEFAULT = Path(__file__).resolve().parent / "SERV-A-SCH-P03.ifc"

VALID_STOREY = re.compile(
    r"^(Storey \d+|\d+(st|nd|rd|th) Storey|Level \d+|\d+(st|nd|rd|th) Level|"
    r"Attic|Attic Storey|Roof|Upper Roof|Lower Roof Storey)(_[A-Za-z0-9]+)?$"
)

# SCDF Technical Requirements for Household Shelters 2023, as this course reads
# them. Find the current requirement yourself; do not trust these because a
# script contained them.
HS_MIN_WIDTH, HS_MAX_LENGTH, HS_MAX_AREA = 1200, 4000, 4.8
HS_MIN_HEIGHT, HS_MAX_HEIGHT = 2400, 3900

results: list[tuple[bool, str, str]] = []


def check(ok: bool, rule: str, detail: str = "") -> None:
    results.append((bool(ok), rule, detail))


def psets(product):
    return ifcopenshell.util.element.get_psets(product)


def qtos(product):
    return ifcopenshell.util.element.get_psets(product, qtos_only=True)


def main(path: Path) -> int:
    f = ifcopenshell.open(str(path))
    print(f"{path.name}  schema {f.schema}\n")
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)

    check(f.schema == "IFC4", "Schema is IFC4", f.schema)
    check(len(f.by_type("IfcProject")) == 1, "Exactly one IfcProject")
    check(len(f.by_type("IfcSite")) == 1, "CORENET exactly one IfcSite (block mechanism)")
    site = f.by_type("IfcSite")[0]
    check(bool(site.Name), "CORENET IfcSite is named for its block", f"Name={site.Name!r}")

    units = {u.UnitType: u for u in f.by_type("IfcSIUnit")}
    length_unit = units.get("LENGTHUNIT")
    check(length_unit is not None and length_unit.Prefix == "MILLI",
          "Length unit is millimetres",
          f"{length_unit.Prefix} {length_unit.Name}" if length_unit else "missing")

    crs = f.by_type("IfcProjectedCRS")
    check(bool(crs), "CORENET projected CRS declared")
    if crs:
        check(crs[0].Name == "EPSG:3414",
              "CORENET CRS is EPSG:3414 (SVY21 / Singapore TM)", str(crs[0].Name))
        check(crs[0].VerticalDatum == "SHD", "CORENET vertical datum is SHD",
              str(crs[0].VerticalDatum))
    mc = f.by_type("IfcMapConversion")
    check(bool(mc), "CORENET map conversion declared")
    if mc:
        m = mc[0]
        rotated = (abs((m.XAxisAbscissa or 1.0) - 1.0) > 1e-9
                   or abs(m.XAxisOrdinate or 0.0) > 1e-9)
        check(rotated, "CORENET model is rotated to True North")
        check(m.Eastings is not None and m.Northings is not None,
              "CORENET easting and northing are stated")

    storeys = {s.Name: s for s in f.by_type("IfcBuildingStorey")}
    for name in ("1st Storey", "2nd Storey", "Roof"):
        check(name in storeys, f"CORENET storey {name!r} exists")
    for name in storeys:
        check(bool(VALID_STOREY.match(name)),
              f"CORENET storey {name!r} matches level naming", name)
    elevations = [s.Elevation for s in f.by_type("IfcBuildingStorey")]
    check(len(set(elevations)) == len(elevations),
          "CORENET every storey has a distinct elevation")

    # ------------------------------------------------------- SHELTER: the HS
    shelters = [s for s in f.by_type("IfcSpace") if s.Name == "Household Shelter"]
    check(len(shelters) == 1, "SHELTER exactly one household shelter", str(len(shelters)))

    if shelters:
        hs = shelters[0]
        sg = psets(hs).get("IFCSG_Demo", {})
        q = qtos(hs).get("Qto_SpaceBaseQuantities", {})

        check("Construction Method" in sg, "SHELTER declares its construction method",
              str(sg.get("Construction Method")))
        check("concrete" in str(sg.get("Construction Method", "")).lower(),
              "SHELTER construction method is reinforced concrete",
              str(sg.get("Construction Method")))

        length = sg.get("Internal Length")
        width = sg.get("Internal Width")
        height = sg.get("Clear Height")
        check(length is not None, "SHELTER declares internal length")
        check(width is not None, "SHELTER declares internal width")
        check(height is not None, "SHELTER declares clear height")

        if length and width and height:
            check(width >= HS_MIN_WIDTH,
                  f"SHELTER internal width >= {HS_MIN_WIDTH} mm", f"{width} mm")
            check(length <= HS_MAX_LENGTH,
                  f"SHELTER internal length <= {HS_MAX_LENGTH} mm", f"{length} mm")
            check(HS_MIN_HEIGHT <= height <= HS_MAX_HEIGHT,
                  f"SHELTER clear height {HS_MIN_HEIGHT}-{HS_MAX_HEIGHT} mm", f"{height} mm")
            area = length * width / 1e6
            check(area <= HS_MAX_AREA + 1e-9,
                  f"SHELTER internal area <= {HS_MAX_AREA} m2", f"{area:.3f} m2")
            net = q.get("NetFloorArea")
            check(net is not None, "SHELTER carries NetFloorArea")
            if net is not None:
                check(abs(net - area) < 1e-6,
                      "SHELTER declared internal size multiplies out to its floor area",
                      f"{length} x {width} = {area:.3f} against NetFloorArea {net:.3f}")

        check(bool(psets(hs).get("Bonsai_Upskilling", {}).get("project_stage")),
              "SHELTER carries a project stage")

    hs_walls = [w for w in f.by_type("IfcWall") if w.Name and "A-Walls-HS-" in w.Name]
    check(len(hs_walls) >= 4, "SHELTER enclosed on four sides", str(len(hs_walls)))
    for w in hs_walls:
        t = ifcopenshell.util.element.get_type(w)
        check(t is not None and "HS-250-RC" in (t.Name or ""),
              f"SHELTER {w.Name} uses the 250mm RC type", (t.Name if t else "no type"))
        check(psets(w).get("Pset_WallCommon", {}).get("LoadBearing") is True,
              f"SHELTER {w.Name} is load bearing")

    # ------------------------------------------------- TOWER: founded, continuous
    occupied = [n for n in ("1st Storey", "2nd Storey") if n in storeys]
    tower_tags = {w.Name.rsplit("-L", 1)[0] for w in f.by_type("IfcWall")
                  if w.Name and ("-Tower-" in w.Name or "A-Walls-HS-" in w.Name)}
    check(bool(tower_tags), "TOWER servant towers are present", str(len(tower_tags)))
    for tag in sorted(tower_tags):
        levels = {w.Name.rsplit("-L", 1)[1] for w in f.by_type("IfcWall")
                  if w.Name and w.Name.startswith(tag + "-L")}
        check(len(levels) == len(occupied),
              f"TOWER {tag} is continuous through every storey", f"storeys {sorted(levels)}")

    # ------------------------------------------------------- IFC+SG structure
    gfa = [s for s in f.by_type("IfcSpace") if s.ObjectType == "AREA_GFA"]
    check(len(gfa) == len(occupied), "IFCSG one GFA space per occupied storey", str(len(gfa)))
    for g in gfa:
        check(g.PredefinedType == "USERDEFINED", f"IFCSG {g.Name} is USERDEFINED",
              str(g.PredefinedType))
        sg = psets(g).get("IFCSG_Demo", {})
        for key in ("AGF_Name", "AGF_Development Use", "AGF_Use Quantum"):
            check(key in sg, f"IFCSG {g.Name} carries {key}")

    for s in f.by_type("IfcSpace"):
        check(bool(s.LongName), f"{s.Name} carries a LongName")
        check(s.CompositionType == "ELEMENT", f"{s.Name} composition is ELEMENT")

    # ------------------------------------------------------------------- VAF
    for p in f.by_type("IfcProduct"):
        if not p.Representation:
            continue
        if p.is_a("IfcOpeningElement") or p.is_a("IfcDoor") or p.is_a("IfcWindow"):
            continue
        check(bool(psets(p).get("VAF_Demo", {}).get("component")),
              f"VAF {p.Name} names the component it serves")

    for cls in ("IfcWall", "IfcSlab", "IfcDoor", "IfcWindow"):
        for e in f.by_type(cls):
            check(ifcopenshell.util.element.get_type(e) is not None,
                  f"{e.Name} comes from a type")

    for o in f.by_type("IfcOpeningElement"):
        check(bool(o.VoidsElements), f"{o.Name} voids a host element")
        check(bool(o.HasFillings), f"{o.Name} is filled by a door or window")

    for cls in ("IfcWall", "IfcSlab", "IfcDoor", "IfcWindow", "IfcGrid"):
        for e in f.by_type(cls):
            check(bool(e.ContainedInStructure) or bool(e.Decomposes),
                  f"{e.Name} is in a spatial container")

    broken = []
    for p in f.by_type("IfcProduct"):
        if not p.Representation:
            continue
        try:
            shape = ifcopenshell.geom.create_shape(settings, p)
            if np.array(shape.geometry.verts, dtype=float).size == 0:
                broken.append(p.Name)
        except Exception:
            broken.append(p.Name)
    check(not broken, "Every product with a representation generates geometry",
          ", ".join(broken[:5]))

    failures = [r for r in results if not r[0]]
    for ok, rule, detail in results:
        if not ok:
            print(f"  FAIL  {rule}" + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(results) - len(failures)}/{len(results)} checks passed")
    if failures:
        print(f"{len(failures)} FAILED")
        return 1
    print("clean")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    sys.exit(main(target))
