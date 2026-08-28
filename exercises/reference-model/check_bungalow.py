"""Check the reference model the way a gate check should.

    python exercises/reference-model/check_bungalow.py [model.ifc]

Every rule here is one the course states somewhere -- in the model standard, in a
stage gate, or in CORENET X's General Modelling Practices. Run it, read the
failures, and treat a clean run as the minimum rather than as praise.

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
import ifcopenshell.util.placement

DEFAULT = Path(__file__).resolve().parent / "BUNG-A-SCH-P03.ifc"

# CORENET X level naming: valid forms for a low-rise building.
VALID_STOREY = re.compile(
    r"^(Storey \d+|\d+(st|nd|rd|th) Storey|Level \d+|\d+(st|nd|rd|th) Level|"
    r"Attic|Attic Storey|Roof|Upper Roof|Lower Roof Storey)(_[A-Za-z0-9]+)?$"
)

results: list[tuple[bool, str, str]] = []


def check(ok: bool, rule: str, detail: str = "") -> None:
    results.append((bool(ok), rule, detail))


def main(path: Path) -> int:
    f = ifcopenshell.open(str(path))
    print(f"{path.name}  schema {f.schema}\n")

    # ---------------------------------------------------------------- project
    check(len(f.by_type("IfcProject")) == 1, "Exactly one IfcProject")
    check(len(f.by_type("IfcSite")) == 1, "Exactly one IfcSite (block mechanism)")
    site = f.by_type("IfcSite")[0]
    check(bool(site.Name), "IfcSite is named for its block", f"Name={site.Name!r}")

    units = {u.UnitType: u for u in f.by_type("IfcSIUnit")}
    length = units.get("LENGTHUNIT")
    check(length is not None and length.Prefix == "MILLI",
          "Length unit is millimetres",
          f"{length.Prefix} {length.Name}" if length else "missing")

    # --------------------------------------------------------- georeferencing
    crs = f.by_type("IfcProjectedCRS")
    check(bool(crs), "Projected CRS declared")
    if crs:
        c = crs[0]
        check(c.Name == "EPSG:3414", "CRS is EPSG:3414 (SVY21 / Singapore TM)", f"{c.Name}")
        check(c.VerticalDatum == "SHD", "Vertical datum is SHD", f"{c.VerticalDatum}")
    mc = f.by_type("IfcMapConversion")
    check(bool(mc), "Map conversion declared")
    if mc:
        m = mc[0]
        rotated = abs((m.XAxisAbscissa or 1.0) - 1.0) > 1e-9 or abs(m.XAxisOrdinate or 0.0) > 1e-9
        check(rotated, "Model is rotated to True North",
              f"XAxisAbscissa={m.XAxisAbscissa:.4f} XAxisOrdinate={m.XAxisOrdinate:.4f}")

    # --------------------------------------------------------------- storeys
    storeys = f.by_type("IfcBuildingStorey")
    check(len(storeys) >= 1, "At least one storey")
    for s in storeys:
        check(bool(VALID_STOREY.match(s.Name or "")),
              f"Storey name follows CORENET X convention: {s.Name!r}")
        check(s.Elevation is not None, f"Storey {s.Name!r} has an elevation",
              f"{s.Elevation}")

    # ---------------------------------------------------- spatial containment
    loose = []
    for el in f.by_type("IfcElement"):
        if el.is_a("IfcOpeningElement"):
            continue
        if ifcopenshell.util.element.get_container(el) is None:
            loose.append(el)
    check(not loose, "Every element sits in a storey",
          ", ".join(e.Name or e.is_a() for e in loose[:5]))

    # ------------------------------------------------------------------ types
    untyped = []
    for cls in ("IfcWall", "IfcSlab", "IfcDoor", "IfcWindow"):
        for el in f.by_type(cls):
            if ifcopenshell.util.element.get_type(el) is None:
                untyped.append(el)
    check(not untyped, "Every wall, slab, door and window has a type",
          ", ".join(e.Name or e.is_a() for e in untyped[:5]))

    # material layer sets on the types
    for t in f.by_type("IfcWallType") + f.by_type("IfcSlabType"):
        mat = ifcopenshell.util.element.get_material(t)
        ok = mat is not None and mat.is_a("IfcMaterialLayerSet")
        total = sum(l.LayerThickness for l in mat.MaterialLayers) if ok else 0
        check(ok, f"Type {t.Name!r} carries a material layer set",
              f"{len(mat.MaterialLayers)} layers, {total:.0f} mm" if ok else "none")

    # ------------------------------------------------------ openings and fills
    for opening in f.by_type("IfcOpeningElement"):
        voids = opening.VoidsElements
        fills = opening.HasFillings
        check(len(voids) == 1, f"Opening {opening.Name!r} voids exactly one host")
        check(len(fills) == 1, f"Opening {opening.Name!r} is filled")

    for el in f.by_type("IfcDoor") + f.by_type("IfcWindow"):
        filled = el.FillsVoids
        check(len(filled) == 1, f"{el.Name!r} fills an opening")
        if filled:
            host = filled[0].RelatingOpeningElement.VoidsElements[0].RelatingBuildingElement
            check(host.is_a("IfcWall"), f"{el.Name!r} is hosted by a wall", host.is_a())
        check(bool(el.Tag), f"{el.Name!r} carries a mark", f"Tag={el.Tag}")

    # ----------------------------------------------------------------- spaces
    spaces = f.by_type("IfcSpace")
    check(bool(spaces), "Spaces exist")
    total_internal = 0.0
    for sp in spaces:
        check(bool(sp.Name), "Space is named", sp.Name or "")
        psets = ifcopenshell.util.element.get_psets(sp)
        ref = psets.get("Pset_SpaceCommon", {}).get("Reference")
        check(bool(ref), f"Space {sp.Name!r} has a number", f"Reference={ref}")
        area = psets.get("IFCSG_Demo", {}).get("Area")
        if area and sp.PredefinedType == "INTERNAL":
            total_internal += float(area)
    print(f"  net internal area from space data: {total_internal:.1f} m2\n")

    hs = [s for s in spaces if s.Name == "Household Shelter"]
    check(bool(hs), "Household shelter is modelled")
    if hs:
        p = ifcopenshell.util.element.get_psets(hs[0]).get("IFCSG_Demo", {})
        check(all(k in p for k in ("Construction Method", "Internal Length", "Internal Width")),
              "Household shelter carries its conceptual-stage data",
              f"{p.get('Internal Length')} x {p.get('Internal Width')} mm")

    entrances = [d for d in f.by_type("IfcDoor")
                 if ifcopenshell.util.element.get_psets(d).get("IFCSG_Demo", {}).get("Main Entrance")]
    check(len(entrances) == 1, "Exactly one door is flagged as the main entrance",
          ", ".join(d.Tag for d in entrances))

    # ------------------------------------------------------------------- grid
    grids = f.by_type("IfcGrid")
    check(bool(grids), "A grid exists")
    if grids:
        g = grids[0]
        check(len(g.UAxes or []) >= 2 and len(g.VAxes or []) >= 2,
              "Grid has axes in both directions",
              f"{len(g.UAxes or [])} U, {len(g.VAxes or [])} V")

    # --------------------------------------------------------------- geometry
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)
    mins, maxs = [], []
    failed = []
    for el in f.by_type("IfcElement"):
        if el.is_a("IfcOpeningElement") or not el.Representation:
            continue
        try:
            shape = ifcopenshell.geom.create_shape(settings, el)
        except Exception:
            failed.append(el.Name or el.is_a())
            continue
        v = np.array(shape.geometry.verts).reshape(-1, 3)
        mins.append(v.min(0))
        maxs.append(v.max(0))
    check(not failed, "Every element produces geometry", ", ".join(failed[:5]))
    lo, hi = np.array(mins).min(0), np.array(maxs).max(0)
    print(f"  model extent: {np.round(lo, 3)} to {np.round(hi, 3)} m\n")
    check(hi[2] <= 3.5, "Nothing rises above the roof level", f"max z = {hi[2]:.3f} m")
    check(lo[2] >= -0.1, "Nothing sinks below the site datum", f"min z = {lo[2]:.3f} m")

    # -------------------------------------------------------- naming standard
    stray = [e for e in f.by_type("IfcElement")
             if (e.Name or "").startswith("X-")]
    check(not stray, "No X- working geometry left in the model",
          ", ".join(e.Name for e in stray[:5]))

    unnamed = [e for e in f.by_type("IfcElement")
               if not e.is_a("IfcOpeningElement") and not (e.Name or "").startswith("A-")]
    check(not unnamed, "Every issued element is named to the A- standard",
          ", ".join((e.Name or e.is_a()) for e in unnamed[:5]))

    # ----------------------------------------------------------------- report
    passed = sum(1 for ok, _, _ in results if ok)
    for ok, rule, detail in results:
        if not ok:
            print(f"  FAIL  {rule}" + (f"  [{detail}]" if detail else ""))
    print(f"\n{passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    sys.exit(main(target))
