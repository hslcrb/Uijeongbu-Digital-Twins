import bpy,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'));s=bpy.context.scene
from rail_detail import add_rail_detail
add_rail_detail(R)
# Correct the packed sign font, not only the source asset on disk.
f=bpy.data.fonts.load(str(R/'assets/station-labels.otf'),check_existing=False);f.pack()
for o in s.objects:
 if o.type=='FONT':o.data.font=f
col=bpy.data.collections.get('Concourse_3F_Photo_Study')
for x in [-7,2,11]:
 for y in [48,57,66]:
  d=bpy.data.lights.new('Concourse ceiling bounced light','AREA');o=bpy.data.objects.new(d.name,d);col.objects.link(o);o.location=(x,y,15.25);d.energy=220;d.shape='DISK';d.size=3
# Broad reflected daylight at the photographed opening, rather than unlit black doorway.
d=bpy.data.lights.new('Entrance reflected sky','AREA');o=bpy.data.objects.new(d.name,d);col.objects.link(o);o.location=(2,34,14);o.rotation_euler=(Vector((2,50,13))-o.location).to_track_quat('-Z','Y').to_euler();d.size=12
for fr,en in [(1,1800),(120,600),(240,200)]:d.energy=en;d.keyframe_insert('energy',frame=fr)
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v1.blend'),compress=True)
s.camera=bpy.data.objects['02_Plaza_eye_level'];s.cycles.samples=64;s.render.filepath=str(R/'renders/plaza-v4.jpg');bpy.ops.render.render(write_still=True)
exec(compile((R/'scripts/export_web.py').read_text(),str(R/'scripts/export_web.py'),'exec'))
