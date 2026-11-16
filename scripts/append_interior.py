"""Run from exterior scene after constructing it. Offset is photo/OSM approximation."""
import bpy
from mathutils import Vector
from pathlib import Path

def append_concourse(blend_path, offset=(2,57,11)):
    with bpy.data.libraries.load(str(blend_path), link=False) as (src,dst):
        dst.objects=src.objects
    col=bpy.data.collections.new('Concourse_3F_Photo_Study')
    bpy.context.scene.collection.children.link(col)
    root=bpy.data.objects.new('Concourse_approx_alignment',None);col.objects.link(root)
    root.location=offset
    root['alignment_evidence']='3F concourse supported by official Uijeongbu culture station FAQ. World metric offset inferred from OSM min_height/entrance, not surveyed.'
    for obj in dst.objects:
        if obj and obj.type not in {'CAMERA','LIGHT'}:
            col.objects.link(obj);obj.parent=root
    return root
# Hall's south entry local (0,-15,0) -> world (2,42,11)
