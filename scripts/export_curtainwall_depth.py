import bpy,gzip,json,hashlib,sys
from pathlib import Path
s=bpy.context.scene;s.frame_set(1)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
out=Path(args[0] if args else 'renders/facade-study');out.mkdir(parents=True,exist_ok=True)
# Apply only the two explicitly added visual frame modifiers; preserve every other modifier behavior.
o=bpy.data.objects['Hanwha silver mullion'];bpy.context.view_layer.objects.active=o
for m in list(o.modifiers):
 if m.name.startswith(('Curtainwall frame','Frame edge')):bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.object.select_all(action='DESELECT')
for o in s.objects:
 if o.type in {'MESH','CURVE','FONT'} and not o.hide_render and not any(c.hide_render for c in o.users_collection):o.select_set(True)
kw=dict(export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_apply=False,export_yup=True)
bpy.ops.export_scene.gltf(filepath=str(out/'station-v19-facade-physics.glb'),**kw)
bpy.ops.export_scene.gltf(filepath=str(out/'station-v19-facade.glb'),export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=20,export_draco_normal_quantization=12,**kw)
p=out/'station-v19-facade.glb';(out/'station-v19-facade.glb.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0));print('SHA',hashlib.sha256(p.read_bytes()).hexdigest())
