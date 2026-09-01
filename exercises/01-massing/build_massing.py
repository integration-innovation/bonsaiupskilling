"""Reference massing for Stage 02, Concept Design: the Farnsworth House as five moves.

    blender -b --python exercises/01-massing/build_massing.py

Writes exercises/01-massing/farnsworth_massing.blend. Plain Blender mesh --
deliberately not IFC, because Stage 02 classifies nothing.

The whole building is five decisions, and this file is those five decisions as
five boxes:

    1  a floor plane, held 5'-3" clear of the floodplain
    2  a roof plane, 9'-6" above it
    3  eight columns holding both, outboard of the slab edges
    4  a glass line 22'-0" in from the west end, leaving a porch under the roof
    5  a terrace, one step down, to land on before you arrive

Everything after Stage 02 is detail. If the massing is wrong, no amount of
Design Development rescues it -- which is the argument this exercise exists to
make.

Dimensions come from the reference model's DIMS table. They are authored in feet
and inches and converted, because the building was designed that way; see
exercises/reference-model/build_farnsworth.py for their sources and confidence
grades. The grade-C figures here are the terrace position and the porch line.

Licensed GPL-3.0-or-later, matching Bonsai.
"""

from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "01-massing" / "farnsworth_massing.blend"


def ft(feet: float, inches: float = 0.0) -> float:
    """Feet and inches to metres. The sign belongs to the whole dimension."""
    sign = -1.0 if (feet < 0 or (feet == 0 and inches < 0)) else 1.0
    return sign * (abs(feet) + abs(inches) / 12.0) * 0.3048


SLAB_L, SLAB_W = ft(77), ft(28)
FFL, CLEAR_H, CHANNEL = ft(5, 3), ft(9, 6), ft(1, 3)
CEILING = FFL + CLEAR_H
ROOF_TOP = CEILING + CHANNEL              # ft(16), exactly
PORCH_L = ft(22)
TERR_FFL = ft(2)
COL_X = [ft(5, 6) + i * ft(22) for i in range(4)]


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        bpy.data.collections.remove(collection)


def collection(name):
    item = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(item)
    return item


def move_to(obj, target):
    for owner in list(obj.users_collection):
        owner.objects.unlink(obj)
    target.objects.link(obj)


def material(name, colour):
    item = bpy.data.materials.new(name)
    item.diffuse_color = (*colour, 1.0)
    return item


def box(name, centre, size, target, mat, role, grade="A"):
    """A box by centre and overall size, so the numbers read as dimensions."""
    bpy.ops.mesh.primitive_cube_add(location=centre)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, target)
    obj.data.materials.append(mat)
    obj["project_stage"] = "02 Concept Design"
    obj["design_status"] = "provisional"
    obj["role"] = role
    obj["confidence"] = grade
    return obj


def add_text(name, body, location, target, size=0.6):
    curve = bpy.data.curves.new(name + "_Curve", type="FONT")
    curve.body = body
    curve.align_x = "CENTER"
    curve.size = size
    obj = bpy.data.objects.new(name, curve)
    target.objects.link(obj)
    obj.location = location
    obj["project_stage"] = "02 Concept Design"
    obj["role"] = "design annotation"
    return obj


def main():
    clear_scene()
    site = collection("A-Site")
    massing = collection("A-Massing")
    annotations = collection("A-Annotations")

    site_mat = material("Fox River floodplain", (0.30, 0.42, 0.28))
    plane_mat = material("Horizontal plane study", (0.88, 0.88, 0.86))
    col_mat = material("Frame study", (0.92, 0.92, 0.90))
    glass_mat = material("Glazed enclosure study", (0.45, 0.62, 0.68))
    terr_mat = material("Terrace study", (0.78, 0.74, 0.66))

    # Grade. The site is the reason for everything above it.
    box("A-Site_Floodplain", (ft(20), ft(3), -ft(0, 3)),
        (ft(160), ft(90), ft(0, 6)), site, site_mat, "existing grade, Fox River floodplain")

    # 1 and 2 -- the two planes. 15" of structure each, and nothing between them
    # but glass and one core.
    for name, top in (("A-Massing_FloorPlane", FFL), ("A-Massing_RoofPlane", ROOF_TOP)):
        box(name, (SLAB_L / 2, SLAB_W / 2, top - CHANNEL / 2),
            (SLAB_L, SLAB_W, CHANNEL), massing, plane_mat,
            "77'-0\" x 28'-0\" plane, 15\" structural depth")

    # 3 -- eight columns, welded to the slab edges rather than passing through.
    # Massing them as 8" squares is enough to test the rhythm; the W8x48 section
    # is a Stage 04 decision.
    for i, x in enumerate(COL_X, start=1):
        for row, y in (("A", -ft(0, 4)), ("B", SLAB_W + ft(0, 4))):
            box(f"A-Massing_Column{row}{i}", (x, y, ROOF_TOP / 2),
                (ft(0, 8), ft(0, 8), ROOF_TOP), massing, col_mat,
                "column outboard of the slab edge")

    # 4 -- the glass line. The eastern 55'-0" is enclosed; the western 22'-0"
    # stays open under the same roof. This is the move that makes the house a
    # pavilion rather than a box.
    box("A-Massing_GlazedEnclosure",
        (PORCH_L + (SLAB_L - PORCH_L) / 2, SLAB_W / 2, FFL + CLEAR_H / 2),
        (SLAB_L - PORCH_L, SLAB_W, CLEAR_H), massing, glass_mat,
        "glazed enclosure, 55'-0\" x 28'-0\"", grade="C")

    # 5 -- the terrace. Position relative to the house is grade C: it comes from
    # photographs, not from a plan. Correct it at Stage 04 against HABS sheet 3.
    box("A-Massing_Terrace", (ft(-5, 6), ft(-11), TERR_FFL - ft(0, 4)),
        (ft(55), ft(22), ft(0, 8)), massing, terr_mat,
        "lower terrace, 55'-0\" x 22'-0\"", grade="C")

    add_text("A-Annotations_North", "NORTH", (SLAB_L / 2, ft(40), 0.02), annotations)
    add_text("A-Annotations_Length", "77'-0\"", (SLAB_L / 2, ft(32), 0.02), annotations)
    add_text("A-Annotations_Bays", "22'-0\"  |  22'-0\"  |  22'-0\"",
             (SLAB_L / 2, ft(-6), 0.02), annotations)
    add_text("A-Annotations_Stage", "STAGE 02 - CONCEPT", (SLAB_L / 2, SLAB_W / 2, 0.02),
             annotations)

    scene = bpy.context.scene
    scene["project_name"] = "Edith Farnsworth House"
    scene["project_stage"] = "02 Concept Design"
    scene["design_status"] = "provisional"
    scene["north_assumption"] = (
        "Positive Y is north; true bearing is on HABS sheet 1 and is not yet known.")
    scene["module"] = "3 bays at 22'-0\" + 5'-6\" cantilever each end = 77'-0\""
    scene["next_exercise"] = (
        "Open in Bonsai Sketch Mode. Push/Pull the glazed enclosure west and watch the "
        "porch disappear -- then argue for where the glass line belongs.")
    scene.world.color = (0.08, 0.10, 0.12)

    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
