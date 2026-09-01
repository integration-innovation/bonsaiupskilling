"""Check the Farnsworth reference model the way a gate check should.

    python exercises/reference-model/check_farnsworth.py [model.ifc]

Every rule here is one the course states somewhere -- in the model standard, in
a stage gate, or in this model's own rule that a dimension without a source is
not a dimension.

Three groups of check matter more than the rest, because they are the ones a
hand-modelled copy of this house usually fails:

  CLOSURE   The plan and section close exactly in feet. 3 bays at 22'-0" plus
            two 5'-6" cantilevers is 77'-0"; 5'-3" plus 9'-6" plus 1'-3" is
            16'-0". If your model does not close, you have rounded something.
  FRAME     Eight columns, welded to the slab edge rather than passing through
            it. The moment a column penetrates a slab, the building stops being
            the building.
  SOURCE    Every element with geometry that is not part of a curtain wall
            carries a Farnsworth_Provenance set saying where its dimensions came
            from and how confident that is.

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

DEFAULT = Path(__file__).resolve().parent / "FARN-A-DD-P01.ifc"

# CORENET X level naming: the valid forms for a low-rise building. The course
# teaches this convention, so the reference model has to obey it even though
# this building is in Illinois and would never be submitted through CORENET X.
VALID_STOREY = re.compile(
    r"^(Storey \d+|\d+(st|nd|rd|th) Storey|Level \d+|\d+(st|nd|rd|th) Level|"
    r"Attic|Attic Storey|Roof|Upper Roof|Lower Roof Storey)(_[A-Za-z0-9]+)?$"
)

FT = 0.3048
TOL = 0.002          # 2 mm. Tighter than the building was ever built.

results: list[tuple[bool, str, str]] = []


def check(ok: bool, rule: str, detail: str = "") -> None:
    results.append((bool(ok), rule, detail))


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def ft_m(feet: float) -> float:
    return feet * FT


def feet(m: float) -> str:
    total = m / FT
    f_ = int(abs(total))
    i_ = (abs(total) - f_) * 12.0
    return f"{'-' if total < 0 else ''}{f_}'-{i_:.2f}\""


def world_bounds(settings, product):
    """World-coordinate bounding box of a product, in metres.

    The shape is bound to a local name on purpose. `.geometry.verts` is a view
    onto memory owned by the shape object, so writing this as a single
    expression -- create_shape(...).geometry.verts -- lets the shape be
    collected before numpy copies the data, and the bounds come back as zeros
    some of the time and not others. Keep the shape alive, then copy.
    """
    shape = ifcopenshell.geom.create_shape(settings, product)
    verts = np.array(shape.geometry.verts, dtype=float).reshape(-1, 3)
    return verts.min(0).copy(), verts.max(0).copy()


def psets_of(product) -> dict:
    return ifcopenshell.util.element.get_psets(product)


def main(path: Path) -> int:
    f = ifcopenshell.open(str(path))
    print(f"{path.name}  schema {f.schema}\n")
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)

    # ---------------------------------------------------------------- project
    check(f.schema == "IFC4", "Schema is IFC4", f.schema)
    check(len(f.by_type("IfcProject")) == 1, "Exactly one IfcProject")
    check(len(f.by_type("IfcSite")) == 1, "Exactly one IfcSite")
    check(len(f.by_type("IfcBuilding")) == 1, "Exactly one IfcBuilding")

    units = {u.UnitType: u for u in f.by_type("IfcSIUnit")}
    length = units.get("LENGTHUNIT")
    check(length is not None and length.Prefix == "MILLI",
          "Length unit is millimetres",
          f"{length.Prefix} {length.Name}" if length else "missing")

    # --------------------------------------------------------- georeferencing
    crs = f.by_type("IfcProjectedCRS")
    check(bool(crs), "Projected CRS declared")
    if crs:
        check(crs[0].Name == "EPSG:26916", "CRS is EPSG:26916 (NAD83 / UTM 16N)",
              str(crs[0].Name))
    check(bool(f.by_type("IfcMapConversion")), "Map conversion declared")

    # ---------------------------------------------------------------- storeys
    storeys = {s.Name: s for s in f.by_type("IfcBuildingStorey")}
    wanted = ("1st Storey_Terrace", "1st Storey", "Roof")
    for name in wanted:
        check(name in storeys, f"Storey {name!r} exists")
    for name in storeys:
        check(bool(VALID_STOREY.match(name)),
              f"Storey {name!r} matches CORENET X level naming", name)
    if set(wanted) <= set(storeys):
        check(close(storeys["1st Storey_Terrace"].Elevation / 1000.0, 2 * FT),
              "Terrace storey at 2'-0\"",
              feet(storeys["1st Storey_Terrace"].Elevation / 1000.0))
        check(close(storeys["1st Storey"].Elevation / 1000.0, 5.25 * FT),
              "1st Storey at 5'-3\"", feet(storeys["1st Storey"].Elevation / 1000.0))
        check(close(storeys["Roof"].Elevation / 1000.0, 16 * FT),
              "Roof storey at 16'-0\"", feet(storeys["Roof"].Elevation / 1000.0))

    # ------------------------------------------------------- CLOSURE: section
    slabs = {s.Name: s for s in f.by_type("IfcSlab")}
    check("A-Slabs-Main-Floor" in slabs, "Main floor slab present")
    check("A-Slabs-Roof" in slabs, "Roof slab present")
    check("A-Slabs-Terrace" in slabs, "Terrace slab present")

    if "A-Slabs-Main-Floor" in slabs and "A-Slabs-Roof" in slabs:
        flo, fhi = world_bounds(settings, slabs["A-Slabs-Main-Floor"])
        rlo, rhi = world_bounds(settings, slabs["A-Slabs-Roof"])

        check(close(fhi[2], 5.25 * FT), "CLOSURE floor slab top at 5'-3\"", feet(fhi[2]))
        check(close(fhi[2] - flo[2], 1.25 * FT), "CLOSURE floor plane is 15\" deep",
              feet(fhi[2] - flo[2]))
        check(close(rhi[2], 16 * FT), "CLOSURE roof top at 16'-0\"", feet(rhi[2]))
        check(close(rhi[2] - rlo[2], 1.25 * FT), "CLOSURE roof plane is 15\" deep",
              feet(rhi[2] - rlo[2]))
        check(close(rlo[2] - fhi[2], 9.5 * FT), "CLOSURE clear height is 9'-6\"",
              feet(rlo[2] - fhi[2]))
        # 5'-3" + 9'-6" + 1'-3" = 16'-0", exactly.
        check(close(fhi[2] + 9.5 * FT + 1.25 * FT, rhi[2]),
              "CLOSURE section sums to 16'-0\" exactly")

        # ---------------------------------------------------- CLOSURE: plan
        for tag, lo_, hi_ in (("floor", flo, fhi), ("roof", rlo, rhi)):
            check(close(hi_[0] - lo_[0], 77 * FT), f"CLOSURE {tag} slab is 77'-0\" long",
                  feet(hi_[0] - lo_[0]))
            check(close(hi_[1] - lo_[1], 28 * FT), f"CLOSURE {tag} slab is 28'-0\" wide",
                  feet(hi_[1] - lo_[1]))

    # ---------------------------------------------------------- FRAME: columns
    columns = f.by_type("IfcColumn")
    check(len(columns) == 8, "FRAME exactly eight columns", str(len(columns)))

    xs, ys = set(), set()
    for c in columns:
        lo_, hi_ = world_bounds(settings, c)
        xs.add(round((lo_[0] + hi_[0]) / 2.0 / FT, 3))
        ys.add(round((lo_[1] + hi_[1]) / 2.0 / FT, 3))
        check(close(lo_[2], 0.0), f"FRAME {c.Name} starts at grade", feet(lo_[2]))
        check(close(hi_[2], 16 * FT), f"FRAME {c.Name} stops at 16'-0\"", feet(hi_[2]))

    check(sorted(xs) == [5.5, 27.5, 49.5, 71.5],
          "FRAME column lines at 5'-6\", 27'-6\", 49'-6\", 71'-6\"", str(sorted(xs)))
    if len(sorted(xs)) == 4:
        spacings = np.diff(sorted(xs))
        check(all(close(s, 22.0, 1e-6) for s in spacings),
              "FRAME three equal bays of 22'-0\"", str(list(np.round(spacings, 3))))
        check(close(min(xs) * FT, 5.5 * FT) and close((77 - max(xs)) * FT, 5.5 * FT),
              "FRAME 5'-6\" cantilever at each end")
        check(close((3 * 22 + 2 * 5.5) * FT, 77 * FT),
              "CLOSURE plan sums to 77'-0\" exactly")

    # Welded to the slab edge: the section sits outboard, it does not pass through.
    if "A-Slabs-Main-Floor" in slabs:
        flo, fhi = world_bounds(settings, slabs["A-Slabs-Main-Floor"])
        for c in columns:
            lo_, hi_ = world_bounds(settings, c)
            outboard = hi_[1] <= flo[1] + TOL or lo_[1] >= fhi[1] - TOL
            check(outboard, f"FRAME {c.Name} is outboard of the slab edge",
                  f"y {lo_[1] / FT:.3f}..{hi_[1] / FT:.3f} ft")

    # ------------------------------------------------------------ edge beams
    beams = f.by_type("IfcBeam")
    check(len(beams) == 4, "Four 15\" edge channels", str(len(beams)))
    for bm in beams:
        lo_, hi_ = world_bounds(settings, bm)
        check(close(hi_[0] - lo_[0], 77 * FT), f"{bm.Name} runs the full 77'-0\"",
              feet(hi_[0] - lo_[0]))

    # ------------------------------------------------------------ curtain wall
    cws = f.by_type("IfcCurtainWall")
    check(len(cws) == 4, "One curtain wall per elevation", str(len(cws)))
    total_plates = 0
    for cw in cws:
        kids = [o for r in cw.IsDecomposedBy for o in r.RelatedObjects]
        plates = [k for k in kids if k.is_a("IfcPlate")]
        mullions = [k for k in kids if k.is_a("IfcMember")]
        total_plates += len(plates)
        check(bool(plates), f"{cw.Name} aggregates glass plates", str(len(plates)))
        check(bool(mullions), f"{cw.Name} aggregates mullions", str(len(mullions)))
        check(len(mullions) == len(plates) + 1 or cw.Name.endswith("West"),
              f"{cw.Name} has one more mullion than plates",
              f"{len(mullions)} mullions, {len(plates)} plates")
    check(total_plates == len(f.by_type("IfcPlate")),
          "Every plate belongs to a curtain wall",
          f"{total_plates} aggregated of {len(f.by_type('IfcPlate'))}")

    for p in f.by_type("IfcPlate"):
        lo_, hi_ = world_bounds(settings, p)
        check(close(hi_[2] - lo_[2], 9.5 * FT), f"{p.Name} is 9'-6\" tall",
              feet(hi_[2] - lo_[2]))

    # -------------------------------------------------------------------- core
    walls = f.by_type("IfcWall")
    check(len(walls) == 6, "Six core partitions and nothing else", str(len(walls)))
    check(all(w.Name.startswith("A-Walls-Core") for w in walls),
          "The only walls in the house are the core")
    for w in walls:
        lo_, hi_ = world_bounds(settings, w)
        check(close(lo_[2], 5.25 * FT) and close(hi_[2], 14.75 * FT),
              f"{w.Name} runs floor to ceiling", f"{feet(lo_[2])} to {feet(hi_[2])}")

    check(len(f.by_type("IfcChimney")) == 1, "One flue, and it is the only thing "
          "that punctures the roof")
    if f.by_type("IfcChimney"):
        lo_, hi_ = world_bounds(settings, f.by_type("IfcChimney")[0])
        check(hi_[2] > 16 * FT, "Flue passes above the roof plane", feet(hi_[2]))

    # ------------------------------------------------------------------ stairs
    stairs = {s.Name: s for s in f.by_type("IfcStair")}
    check(len(stairs) == 2, "Two flights: grade to terrace, terrace to porch",
          str(len(stairs)))
    if "A-Stairs-F1" in stairs:
        lo_, hi_ = world_bounds(settings, stairs["A-Stairs-F1"])
        check(close(lo_[2], 0.0) and close(hi_[2], 2 * FT),
              "F1 climbs grade to terrace", f"{feet(lo_[2])} to {feet(hi_[2])}")
    if "A-Stairs-F2" in stairs:
        lo_, hi_ = world_bounds(settings, stairs["A-Stairs-F2"])
        check(close(lo_[2], 2 * FT) and close(hi_[2], 5.25 * FT),
              "F2 climbs terrace to floor", f"{feet(lo_[2])} to {feet(hi_[2])}")

    # ------------------------------------------------------------------ spaces
    spaces = {s.Name: s for s in f.by_type("IfcSpace")}
    for name in ("Living", "Dining", "Kitchen", "Sleeping", "Bathroom W",
                 "Bathroom E", "Utility", "West Porch", "Terrace"):
        check(name in spaces, f"Space {name!r} exists")
    for s in f.by_type("IfcSpace"):
        check(bool(s.LongName), f"{s.Name} carries a LongName")
        q = ifcopenshell.util.element.get_psets(s, qtos_only=True)
        area = q.get("Qto_SpaceBaseQuantities", {}).get("NetFloorArea")
        check(area is not None, f"{s.Name} carries NetFloorArea")

    internal = 0.0
    for s in f.by_type("IfcSpace"):
        if s.PredefinedType == "EXTERNAL":
            continue
        q = ifcopenshell.util.element.get_psets(s, qtos_only=True)
        internal += q.get("Qto_SpaceBaseQuantities", {}).get("NetFloorArea", 0.0)
    sqft = internal / 0.09290304
    check(1400 <= sqft <= 1650,
          "Enclosed area is within the published ~1,500 sq ft", f"{sqft:.0f} sq ft")

    # -------------------------------------------------- CLOSURE: the paving module
    # The travertine is 2'-9" x 2'-0", derived from 220 pieces on the terrace.
    # If that derivation is right, every principal dimension is a whole number
    # of pavers -- six closures, and they are the reason the figure is trusted.
    PL, PW = 2.75, 2.0
    for label, feet_, module in (
        ("77'-0\" slab length", 77, PL), ("55'-0\" enclosure", 55, PL),
        ("22'-0\" structural bay", 22, PL), ("5'-6\" cantilever", 5.5, PL),
        ("28'-0\" slab width", 28, PW), ("22'-0\" terrace width", 22, PW),
    ):
        n = feet_ / module
        check(abs(n - round(n)) < 1e-9,
              f"CLOSURE {label} is a whole number of pavers", f"{n:g}")

    coverings = {c.Name: c for c in f.by_type("IfcCovering")}
    check(len(coverings) == 2, "Travertine modelled as a covering per plane",
          str(len(coverings)))
    expected_pieces = {"A-Finishes-Floor-Travertine": 392,
                       "A-Finishes-Terrace-Travertine": 220}
    for name, want in expected_pieces.items():
        check(name in coverings, f"{name} present")
        if name in coverings:
            ps = psets_of(coverings[name]).get("Farnsworth_Paving", {})
            check(ps.get("pieces_total") == want,
                  f"CLOSURE {name} lays up in {want} pieces",
                  str(ps.get("pieces_total")))
            check(abs((ps.get("module_long_mm") or 0) / 1000.0 - PL * FT) < TOL,
                  f"{name} module is 2'-9\" long")
            check(abs((ps.get("module_short_mm") or 0) / 1000.0 - PW * FT) < TOL,
                  f"{name} module is 2'-0\" across")

    # The 220 figure is the published one. It is what the derivation was built
    # from, so it failing here means the terrace size has been edited without
    # revisiting the module.
    if "A-Finishes-Terrace-Travertine" in coverings:
        ps = psets_of(coverings["A-Finishes-Terrace-Travertine"]).get("Farnsworth_Paving", {})
        check(ps.get("pieces_long") == 20 and ps.get("pieces_short") == 11,
              "Terrace lays up 20 x 11, as the published piece count requires",
              f"{ps.get('pieces_long')} x {ps.get('pieces_short')}")

    # ------------------------------------------------- the only openable windows
    windows = f.by_type("IfcWindow")
    check(len(windows) == 2, "Exactly two operable windows in the whole house",
          str(len(windows)))
    for w in windows:
        lo_, hi_ = world_bounds(settings, w)
        check(close(lo_[0], ft_m(77), 0.01) or close(hi_[0], ft_m(77), 0.01),
              f"{w.Name} is in the east wall", f"x {hi_[0] / FT:.2f} ft")
        vent = psets_of(w).get("Farnsworth_Ventilation", {})
        check(vent.get("operable") is True, f"{w.Name} is recorded as operable")
        check("hopper" in str(vent.get("operation", "")).lower(),
              f"{w.Name} records its operation", str(vent.get("operation")))

    doors = f.by_type("IfcDoor")
    check(len(doors) == 1, "One entrance", str(len(doors)))

    # -------------------------------------------------------------------- grid
    grids = {g.Name: g for g in f.by_type("IfcGrid")}
    check(len(grids) == 2, "Two grids: the structure, and the paving it obeys",
          str(len(grids)))
    check("A-Grid-Paving" in grids, "The paving module is modelled as a grid")
    if "A-Grid-Paving" in grids:
        pg = grids["A-Grid-Paving"]
        check(len(pg.UAxes) == 29, "Paving grid has 29 lines across 28 bays of 2'-9\"",
              str(len(pg.UAxes)))
        check(len(pg.VAxes) == 15, "Paving grid has 15 lines across 14 bays of 2'-0\"",
              str(len(pg.VAxes)))
    if "A-Grid" in grids:
        g = grids["A-Grid"]
        check([a.AxisTag for a in g.UAxes] == ["1", "2", "3", "4"],
              "Grid U axes 1-4 on the column lines")
        check([a.AxisTag for a in g.VAxes] == ["A", "B"],
              "Grid V axes A-B on the column rows")

    # ------------------------------------------------------------ SOURCE rules
    # A dimension without a source is not a dimension. Curtain wall plates and
    # mullions are exempt: they inherit the provenance of the wall they belong to.
    aggregated = {o for cw in cws for r in cw.IsDecomposedBy for o in r.RelatedObjects}
    graded = {"A", "B", "C"}
    for p in f.by_type("IfcProduct"):
        if not p.Representation or p in aggregated:
            continue
        ps = psets_of(p).get("Farnsworth_Provenance")
        check(ps is not None, f"SOURCE {p.Name} declares its dimensional source")
        if ps:
            check(ps.get("confidence") in graded,
                  f"SOURCE {p.Name} carries a valid confidence grade",
                  str(ps.get("confidence")))
            check(bool(ps.get("dimension_source")),
                  f"SOURCE {p.Name} names a source")

    # ---------------------------------------------------------------- geometry
    broken = []
    for p in f.by_type("IfcProduct"):
        if not p.Representation:
            continue
        try:
            shape = ifcopenshell.geom.create_shape(settings, p)
            v = np.array(shape.geometry.verts, dtype=float)
            if v.size == 0:
                broken.append(p.Name)
        except Exception:
            broken.append(p.Name)
    check(not broken, "Every product with a representation generates geometry",
          ", ".join(broken[:5]))

    # ----------------------------------------------------------------- report
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
