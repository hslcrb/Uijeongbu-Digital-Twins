"""Export visible daytime exterior; meshes shared, hidden LOD collection excluded."""
import bpy
from pathlib import Path
root=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.frame_set(1)
bpy.ops.object.select_all(action='DESELECT')
for o in s.objects:
 if o.type in {'MESH','CURVE','FONT'} and not o.hide_render and not any(c.hide_render for c in o.users_collection):o.select_set(True)
(root/'web/assets').mkdir(parents=True,exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str(root/'web/assets/station.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_apply=False,export_yup=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
