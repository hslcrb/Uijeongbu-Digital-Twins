"""Non-destructive v18 curtainwall study. No measured-depth claim; not deployment input."""
import bpy,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
out=Path(args[0] if args else 'renders/facade-study');out.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene;s.frame_set(1)
o=bpy.data.objects.get('Hanwha silver mullion');assert o and len(o.data.polygons)==700
before={x.name:hashlib.sha256(b''.join(bytes(str(tuple(v.co)),'utf8') for v in x.data.vertices)).hexdigest() for x in s.objects if x.type=='MESH'}
# Preserve original front faces/material and add shallow returns behind them.
m=o.modifiers.new('Curtainwall frame shallow return - estimated 60mm','SOLIDIFY');m.thickness=.06;m.offset=-1;m.use_even_offset=True
m=o.modifiers.new('Frame edge highlight - estimated 2mm','BEVEL');m.width=.002;m.segments=2
s['curtainwall_depth_note']='Visual study only: 60mm return and 2mm bevel inferred, not field-measured. Original panel grid unchanged.'
data=bpy.data.cameras.new('Curtainwall oblique detail');cam=bpy.data.objects.new(data.name,data);s.collection.objects.link(cam);cam.location=(157,40,31);target=Vector((179,18,24));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();data.lens=45;s.camera=cam
s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=True;s.render.resolution_x=1200;s.render.resolution_y=1000;s.render.resolution_percentage=100
for mod in o.modifiers:mod.show_render=False
s.render.filepath=str(out/'curtainwall-before.png');bpy.ops.render.render(write_still=True)
for mod in o.modifiers:mod.show_render=True
s.render.filepath=str(out/'curtainwall-depth-study.png');bpy.ops.render.render(write_still=True)
after={x.name:hashlib.sha256(b''.join(bytes(str(tuple(v.co)),'utf8') for v in x.data.vertices)).hexdigest() for x in s.objects if x.type=='MESH'}
assert before==after
bpy.ops.wm.save_as_mainfile(filepath=str(out/'curtainwall-depth-study.blend'),compress=True)
(out/'validation.json').write_text(json.dumps({'original_mesh_geometry_unchanged':True,'mesh_count':len(before),'frame_front_faces':700,'depth_m':.06,'depth_is_measured':False,'deployment':False},indent=2))
