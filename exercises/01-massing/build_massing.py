import math
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "01-massing" / "bungalow_massing.blend"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        if collection.name != "Collection":
            bpy.data.collections.remove(collection)
    if bpy.data.collections.get("Collection"):
        bpy.data.collections.remove(bpy.data.collections["Collection"])


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


def cube(name, location, scale, target, mat, role):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (scale[0] / 2, scale[1] / 2, scale[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, target)
    obj.data.materials.append(mat)
    obj["project_stage"] = "01 Massing Design Planning"
    obj["design_status"] = "provisional"
    obj["role"] = role
    return obj


def roof(name, location, width, depth, height, target, mat):
    mesh = bpy.data.meshes.new(name + "_Mesh")
    half_width = width / 2
    half_depth = depth / 2
    vertices = [
        (-half_width, -half_depth, 0),
        (half_width, -half_depth, 0),
        (half_width, half_depth, 0),
        (-half_width, half_depth, 0),
        (0, -half_depth, height),
        (0, half_depth, height),
    ]
    faces = [
        (0, 1, 4),
        (1, 2, 5, 4),
        (2, 3, 5),
        (3, 0, 4, 5),
        (0, 3, 2, 1),
    ]
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    target.objects.link(obj)
    obj.location = location
    obj.data.materials.append(mat)
    obj["project_stage"] = "01 Massing Design Planning"
    obj["design_status"] = "provisional"
    obj["role"] = "pitched roof study"
    return obj


def add_text(name, body, location, target):
    curve = bpy.data.curves.new(name + "_Curve", type="FONT")
    curve.body = body
    curve.align_x = "CENTER"
    curve.size = 0.45
    obj = bpy.data.objects.new(name, curve)
    target.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (0, 0, 0)
    obj["project_stage"] = "01 Massing Design Planning"
    obj["role"] = "design annotation"
    return obj


def main():
    clear_scene()
    site = collection("A-Site")
    massing = collection("A-Massing")
    annotations = collection("A-Annotations")

    site_mat = material("Site", (0.32, 0.48, 0.25))
    slab_mat = material("Floor slab study", (0.42, 0.42, 0.42))
    mass_mat = material("Main mass study", (0.78, 0.64, 0.40))
    porch_mat = material("Covered outdoor room", (0.32, 0.50, 0.55))
    roof_mat = material("Roof study", (0.18, 0.20, 0.22))

    cube("A-Site_Datum", (0, 0, -0.10), (20, 30, 0.20), site, site_mat, "site datum")
    cube("A-Massing_FloorSlab", (0, 0, 0.15), (12, 10, 0.30), massing, slab_mat, "12 m x 10 m floor slab")
    cube("A-Massing_MainVolume", (0, 0, 1.75), (12, 10, 3.00), massing, mass_mat, "single-storey bungalow volume")
    cube("A-Massing_CoveredEntry", (0, -6.25, 1.65), (4.00, 2.50, 2.80), massing, porch_mat, "covered entry / outdoor room")
    roof("A-Massing_RoofStudy", (0, 0, 3.25), 13.0, 11.0, 2.20, massing, roof_mat)

    add_text("A-Annotations_North", "NORTH", (0, -10, 0.02), annotations)
    add_text("A-Annotations_Footprint", "12 m x 10 m", (0, 5.6, 0.02), annotations)
    add_text("A-Annotations_Stage", "STAGE 01 - MASSING", (0, 0, 0.02), annotations)

    scene = bpy.context.scene
    scene["project_name"] = "Courtyard Bungalow"
    scene["project_stage"] = "01 Massing Design Planning"
    scene["design_status"] = "provisional"
    scene["north_assumption"] = "Negative Y is north; entrance faces north."
    scene["next_exercise"] = "Open in Bonsai Sketch Mode. Test Push/Pull on the main mass and porch."
    scene.world.color = (0.08, 0.10, 0.12)

    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
