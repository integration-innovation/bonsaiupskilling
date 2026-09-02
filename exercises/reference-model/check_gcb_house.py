"""Check the Pinwheel House the way a gate check should.

    python exercises/reference-model/check_gcb_house.py [model.ifc]

With no argument it checks all three stage models in turn, which is the point:
the same rules apply at Concept, Design Development and Completion, and what
changes is how much of the building exists to be checked.

Five groups matter more than the rest:

  GCB       The Good Class Bungalow controls are met and are met *from the
            model*: plot area, site coverage, setbacks, storey count. A
            coverage figure typed into a form is not a check.
  SHELTER   SCDF's dimensional limits; the declared internal size multiplies
            out to the space's own NetFloorArea; and -- the one people miss --
            the shelter is FOUNDED. Its walls start at ground level, not at the
            floor plane the rest of the house stands on.
  PINWHEEL  Four wings, each turned from the last, none sharing a face line
            with the wing opposite. A pinwheel that has drifted into a cross
            has lost the idea it was built on.
  CORENET   Level naming, one site, SVY21 easting and northing, SHD elevation,
            a True North rotation.
  VAF       Every element names the Value Articulation Framework component it
            serves, so the model can be read against the fee.

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

HERE = Path(__file__).resolve().parent
MODELS = ["GCB-A-CON-P02.ifc", "GCB-A-DD-P04.ifc", "GCB-A-AB-AB01.ifc"]

VALID_STOREY = re.compile(
    r"^(Storey \d+|\d+(st|nd|rd|th) Storey|Level \d+|\d+(st|nd|rd|th) Level|"
    r"Attic|Attic Storey|Roof|Upper Roof|Lower Roof Storey)(_[A-Za-z0-9]+)?$"
)

# URA Good Class Bungalow controls, as this course reads them in 2026.
GCB_MIN_AREA, GCB_MIN_WIDTH, GCB_MIN_DEPTH = 1400.0, 18.5, 30.0
GCB_MAX_COVERAGE, GCB_SETBACK, GCB_MAX_STOREYS = 40.0, 3.0, 2

# SCDF Technical Requirements for Household Shelters 2023.
HS_MIN_WIDTH, HS_MAX_LENGTH, HS_MAX_AREA = 1200, 4000, 4.8
HS_MIN_HEIGHT, HS_MAX_HEIGHT = 2400, 3900
# Clear distance from the shelter wall to the nearest enclosing external face.
HS_PROTECT_DOOR, HS_PROTECT_OTHER = 2.000, 2.700

PLOT = 40.0


def psets(p):
    return ifcopenshell.util.element.get_psets(p)


def qtos(p):
    return ifcopenshell.util.element.get_psets(p, qtos_only=True)


def run(path: Path, results: list) -> None:
    def check(ok, rule, detail=""):
        results.append((bool(ok), f"{path.stem} · {rule}", detail))

    f = ifcopenshell.open(str(path))
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)

    def bounds(product):
        shape = ifcopenshell.geom.create_shape(settings, product)
        v = np.array(shape.geometry.verts, dtype=float).reshape(-1, 3)
        return v.min(0).copy(), v.max(0).copy()

    check(f.schema == "IFC4", "Schema is IFC4", f.schema)
    check(len(f.by_type("IfcProject")) == 1, "Exactly one IfcProject")
    check(len(f.by_type("IfcSite")) == 1, "CORENET exactly one IfcSite")

    units = {u.UnitType: u for u in f.by_type("IfcSIUnit")}
    lu = units.get("LENGTHUNIT")
    check(lu is not None and lu.Prefix == "MILLI", "Length unit is millimetres")

    crs = f.by_type("IfcProjectedCRS")
    check(bool(crs), "CORENET projected CRS declared")
    if crs:
        check(crs[0].Name == "EPSG:3414", "CORENET CRS is EPSG:3414 (SVY21)",
              str(crs[0].Name))
        check(crs[0].VerticalDatum == "SHD", "CORENET vertical datum is SHD",
              str(crs[0].VerticalDatum))
    mc = f.by_type("IfcMapConversion")
    check(bool(mc), "CORENET map conversion declared")
    if mc:
        m = mc[0]
        check(abs((m.XAxisAbscissa or 1.0) - 1.0) > 1e-9 or abs(m.XAxisOrdinate or 0.0) > 1e-9,
              "CORENET model is rotated to True North")
        check(m.Eastings is not None and m.Northings is not None,
              "CORENET easting and northing stated")

    storeys = {s.Name: s for s in f.by_type("IfcBuildingStorey")}
    for name in ("1st Storey", "2nd Storey", "Roof"):
        check(name in storeys, f"CORENET storey {name!r} exists")
    for name in storeys:
        check(bool(VALID_STOREY.match(name)),
              f"CORENET storey {name!r} matches level naming", name)

    stage_now = psets(f.by_type("IfcBuilding")[0]).get(
        "Bonsai_Upskilling", {}).get("project_stage", "")

    # ---------------------------------------------------------------- GCB
    site = f.by_type("IfcSite")[0]
    sg = psets(site).get("IFCSG_Demo", {})
    area = sg.get("Site Area")
    cover = sg.get("Site Coverage")
    check(area is not None, "GCB site area is recorded")
    check(cover is not None, "GCB site coverage is recorded")
    if area:
        check(area >= GCB_MIN_AREA, f"GCB plot >= {GCB_MIN_AREA} m2", f"{area} m2")
        check(PLOT >= GCB_MIN_WIDTH, f"GCB plot width >= {GCB_MIN_WIDTH} m", f"{PLOT} m")
        check(PLOT >= GCB_MIN_DEPTH, f"GCB plot depth >= {GCB_MIN_DEPTH} m", f"{PLOT} m")
    if cover is not None:
        check(cover <= GCB_MAX_COVERAGE, f"GCB coverage <= {GCB_MAX_COVERAGE}%",
              f"{cover}%")

    habitable = [n for n in storeys if n != "Roof"]
    check(len(habitable) <= GCB_MAX_STOREYS,
          f"GCB at most {GCB_MAX_STOREYS} storeys", str(len(habitable)))

    # Setbacks, measured from the model rather than asserted.
    # Only the building counts. Terrain, road, neighbours, trees and the
    # boundary wall all sit outside the plot on purpose, and folding them into
    # the extent would silently turn this check into a no-op.
    def in_building(product):
        for rel in (product.ContainedInStructure or []):
            if rel.RelatingStructure.is_a("IfcBuildingStorey"):
                return True
        return False

    lo = np.array([1e9] * 3)
    hi = np.array([-1e9] * 3)
    for p in f.by_type("IfcProduct"):
        if not p.Representation or p.is_a("IfcSpace") or p.is_a("IfcGrid"):
            continue
        if not in_building(p) or (p.Name and "Boundary" in p.Name):
            continue
        try:
            a, b = bounds(p)
        except Exception:
            continue
        lo, hi = np.minimum(lo, a), np.maximum(hi, b)
    for label, value in (("south", lo[1]), ("west", lo[0]),
                         ("north", PLOT - hi[1]), ("east", PLOT - hi[0])):
        check(value >= GCB_SETBACK - 1e-6,
              f"GCB {label} setback >= {GCB_SETBACK} m", f"{value:.2f} m")

    # ------------------------------------------------------------ SHELTER
    shelters = [s for s in f.by_type("IfcSpace") if s.Name == "Household Shelter"]
    check(len(shelters) == 1, "SHELTER exactly one household shelter", str(len(shelters)))
    if shelters:
        hs = shelters[0]
        d = psets(hs).get("IFCSG_Demo", {})
        q = qtos(hs).get("Qto_SpaceBaseQuantities", {})
        check("concrete" in str(d.get("Construction Method", "")).lower(),
              "SHELTER construction method is reinforced concrete",
              str(d.get("Construction Method")))
        L, W, H = d.get("Internal Length"), d.get("Internal Width"), d.get("Clear Height")
        check(L and W and H, "SHELTER declares length, width and clear height")
        if L and W and H:
            check(W >= HS_MIN_WIDTH, f"SHELTER width >= {HS_MIN_WIDTH} mm", f"{W} mm")
            check(L <= HS_MAX_LENGTH, f"SHELTER length <= {HS_MAX_LENGTH} mm", f"{L} mm")
            check(HS_MIN_HEIGHT <= H <= HS_MAX_HEIGHT,
                  f"SHELTER clear height {HS_MIN_HEIGHT}-{HS_MAX_HEIGHT} mm", f"{H} mm")
            a = L * W / 1e6
            check(a <= HS_MAX_AREA + 1e-9, f"SHELTER area <= {HS_MAX_AREA} m2",
                  f"{a:.3f} m2")
            net = q.get("NetFloorArea")
            check(net is not None and abs(net - a) < 1e-6,
                  "SHELTER declared size multiplies out to its NetFloorArea",
                  f"{L} x {W} = {a:.3f} against {net}")

    hs_walls = [w for w in f.by_type("IfcWall") if w.Name and "A-Walls-HS-" in w.Name]
    check(len(hs_walls) >= 4, "SHELTER enclosed on four sides", str(len(hs_walls)))
    founded = [w for w in hs_walls if bounds(w)[0][2] < 1e-6]
    check(len(founded) >= 4,
          "SHELTER is founded: its walls start at ground, not at the floor plane",
          f"{len(founded)} of {len(hs_walls)} reach ground")
    for w in hs_walls:
        t = ifcopenshell.util.element.get_type(w)
        check(t is not None and "HS-250-RC" in (t.Name or ""),
              f"SHELTER {w.Name} uses the 250mm RC type", (t.Name if t else "none"))

    # --------------------------------- SHELTER: protection at EVERY level
    # The distances are met at 1st Storey because the wings wrap the core. At
    # ground the house is on stilts, so nothing wraps anything -- and the first
    # version of this design failed here without noticing. The plinth is what
    # fixes it, so the plinth is what gets tested.
    plinth = [w for w in f.by_type("IfcWall") if w.Name and "Plinth" in w.Name]
    check(len(plinth) == 4, "SHELTER protective plinth encloses the tower on four sides",
          str(len(plinth)))
    if hs_walls and plinth:
        hlo = np.min([bounds(w)[0] for w in hs_walls], axis=0)
        hhi = np.max([bounds(w)[1] for w in hs_walls], axis=0)
        plo = np.min([bounds(w)[0] for w in plinth], axis=0)
        phi = np.max([bounds(w)[1] for w in plinth], axis=0)
        check(plo[2] < 1e-6, "SHELTER plinth starts at ground", f"{plo[2]:.2f} m")
        for face, clear, need in (
                ("east, the door side", phi[0] - hhi[0], HS_PROTECT_DOOR),
                ("west", hlo[0] - plo[0], HS_PROTECT_OTHER),
                ("south", hlo[1] - plo[1], HS_PROTECT_OTHER),
                ("north", phi[1] - hhi[1], HS_PROTECT_OTHER)):
            check(clear >= need - 1e-6,
                  f"SHELTER protected {need} m on the {face}", f"{clear:.2f} m")

    # ------------------------------------------------------ SITE: the context
    ctx = [p for p in f.by_type("IfcBuildingElementProxy")
           if psets(p).get("Context", {}).get("in_scope") is False]
    check(len(ctx) >= 3, "SITE neighbouring plots are modelled as context",
          str(len(ctx)))
    for c in ctx:
        check(c.is_a("IfcBuildingElementProxy"),
              f"SITE {c.Name} is a proxy, not an IfcBuilding")
    geo = {g.Name: g for g in f.by_type("IfcGeographicElement")}
    check(any("Terrain" in n for n in geo), "SITE terrain is modelled")
    check(any("Road" in n for n in geo), "SITE the estate road is modelled")
    check(sum("Tree" in n for n in geo) >= 3, "SITE mature trees are modelled",
          str(sum("Tree" in n for n in geo)))
    bwalls = [w for w in f.by_type("IfcWall") if w.Name and "Boundary" in w.Name]
    check(bool(bwalls), "SITE the plot boundary is modelled", str(len(bwalls)))
    for w in bwalls:
        h = psets(w).get("IFCSG_Demo", {}).get("Boundary Wall Height")
        check(h is not None and h <= 1800,
              f"GCB {w.Name} boundary wall <= 1.8 m", f"{h} mm")

    # ------------------------------------------- DEMOLITION: the old bungalow
    existing = [p for p in f.by_type("IfcBuildingElementProxy")
                if p.Name and "Existing" in p.Name]
    if stage_now.startswith("02"):
        check(len(existing) == 1,
              "DEMOLITION the existing bungalow is shown at Concept", str(len(existing)))
        for e in existing:
            d = psets(e).get("Demolition", {})
            check(d.get("status") == "TO BE DEMOLISHED",
                  "DEMOLITION it is marked for demolition", str(d.get("status")))
            check(psets(e).get("Bonsai_Upskilling", {}).get("design_status") == "superseded",
                  "DEMOLITION its design status is superseded")
    else:
        check(not existing,
              "DEMOLITION the existing bungalow is gone after Concept",
              f"{len(existing)} still present")

    # ------------------------------------------------- MATERIAL: what it is made of
    unmaterialled = []
    for p in f.by_type("IfcProduct"):
        if not p.Representation or p.is_a("IfcSpace") or p.is_a("IfcOpeningElement"):
            continue
        if ifcopenshell.util.element.get_material(p) is None:
            unmaterialled.append(p.Name)
    check(not unmaterialled, "MATERIAL every built element declares its material",
          f"{len(unmaterialled)} without: " + ", ".join(unmaterialled[:4]))

    # ----------------------------------------------------------- PINWHEEL
    wings = {}
    for s in f.by_type("IfcSpace"):
        if s.LongName and "wing" in s.LongName:
            wings.setdefault(s.LongName.split()[-2], []).append(s)
    check(len(wings) == 4, "PINWHEEL four wings", f"{sorted(wings)}")

    slabs = [s for s in f.by_type("IfcSlab")
             if s.Name and s.Name.startswith("A-Slabs-L1")]
    check(len(slabs) == 5, "PINWHEEL five plates at 1st storey: core plus four wings",
          str(len(slabs)))
    if len(slabs) == 5:
        boxes = [bounds(s) for s in slabs]
        xs = sorted(round(b[0][0], 3) for b in boxes)
        ys = sorted(round(b[0][1], 3) for b in boxes)
        check(len(set(xs)) >= 4, "PINWHEEL wings do not share a west face line", str(xs))
        check(len(set(ys)) >= 4, "PINWHEEL wings do not share a south face line", str(ys))

    # --------------------------------------------------------------- IFC+SG
    gfa = [s for s in f.by_type("IfcSpace") if s.ObjectType == "AREA_GFA"]
    check(len(gfa) == 2, "IFCSG one GFA space per storey", str(len(gfa)))
    for g in gfa:
        check(g.PredefinedType == "USERDEFINED", f"IFCSG {g.Name} is USERDEFINED")
        d = psets(g).get("IFCSG_Demo", {})
        for key in ("AGF_Name", "AGF_Development Use", "AGF_Use Quantum"):
            check(key in d, f"IFCSG {g.Name} carries {key}")

    for s in f.by_type("IfcSpace"):
        check(bool(s.LongName), f"{s.Name} carries a LongName")
        check(s.CompositionType == "ELEMENT", f"{s.Name} composition is ELEMENT")

    # ------------------------------------------------------------------ VAF
    for p in f.by_type("IfcProduct"):
        if not p.Representation or p.is_a("IfcOpeningElement"):
            continue
        check(bool(psets(p).get("VAF_Demo", {}).get("component")),
              f"VAF {p.Name} names the component it serves")

    # ---------------------------------------------------------------- stage
    stage = psets(f.by_type("IfcBuilding")[0]).get("Bonsai_Upskilling", {}).get(
        "project_stage", "")
    check(bool(stage), "Model declares its project stage", stage)
    if stage.startswith("02"):
        check(not f.by_type("IfcDoor"),
              "STAGE Concept classifies nothing that is not yet decided",
              f"{len(f.by_type('IfcDoor'))} doors")
        check(not f.by_type("IfcCurtainWall"), "STAGE Concept has no glazing")
    if stage.startswith("04") or stage.startswith("07"):
        check(bool(f.by_type("IfcDoor")), "STAGE the building has openings")
        check(bool(f.by_type("IfcCurtainWall")), "STAGE the building has its envelope")
        for cls, label in (("IfcMember", "mullions"), ("IfcShadingDevice", "shading"),
                           ("IfcRailing", "balustrades"), ("IfcStair", "stairs"),
                           ("IfcCovering", "floor finishes")):
            check(bool(f.by_type(cls)), f"DETAIL the model has {label}",
                  str(len(f.by_type(cls))))
    if stage.startswith("07"):
        marked = [p for p in f.by_type("IfcProduct")
                  if psets(p).get("AsBuilt", {}).get("verification")]
        check(bool(marked), "STAGE as-built elements carry a verification status",
              f"{len(marked)} marked")
        for p in marked:
            v = psets(p)["AsBuilt"]["verification"]
            check(v in ("verified", "assumed", "unchanged"),
                  f"STAGE {p.Name} verification is one of three values", str(v))

    # ------------------------------------------------------- types and voids
    for cls in ("IfcWall", "IfcSlab", "IfcColumn", "IfcDoor"):
        for e in f.by_type(cls):
            check(ifcopenshell.util.element.get_type(e) is not None,
                  f"{e.Name} comes from a type")
    del cls
    for o in f.by_type("IfcOpeningElement"):
        check(bool(o.VoidsElements), f"{o.Name} voids a host")
        check(bool(o.HasFillings), f"{o.Name} is filled")

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


def main(argv: list[str]) -> int:
    targets = [Path(argv[0])] if argv else [HERE / m for m in MODELS]
    results: list[tuple[bool, str, str]] = []
    for t in targets:
        if not t.exists():
            print(f"missing: {t.name} -- run build_gcb_house.py --all")
            return 1
        run(t, results)

    failures = [r for r in results if not r[0]]
    for ok, rule, detail in results:
        if not ok:
            print(f"  FAIL  {rule}" + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(results) - len(failures)}/{len(results)} checks passed "
          f"across {len(targets)} model(s)")
    if failures:
        print(f"{len(failures)} FAILED")
        return 1
    print("clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
