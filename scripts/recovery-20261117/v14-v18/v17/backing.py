import bpy,json
from mathutils import Vector
R='recovery-output/v17/';o=bpy.data.objects['East elevation individual pale panels'];origin=Vector((31.531,71.647,0));u=Vector((.341,.940,0)).normalized();n=Vector((u.y,-u.x,0))
ps=[o.data.vertices[i].co for p in list(o.data.polygons)[-90:] for i in p.vertices];a=min((v-origin).dot(u) for v in ps);b=max((v-origin).dot(u) for v in ps);z=min(v.z for v in ps);top=max(v.z for v in ps)
v=[tuple(origin+u*t-n*.04+Vector((0,0,h))) for t,h in [(a,z),(b,z),(b,top),(a,top)]];me=bpy.data.meshes.new('v17 infill opaque backing');me.from_pydata(v,[],[(0,1,2,3)]);me.update();ob=bpy.data.objects.new('v17 infill daylight leak backing',me);bpy.context.collection.objects.link(ob);m=bpy.data.materials.new('v17 infill inner backing neutral');m.diffuse_color=(.35,.35,.35,1);me.materials.append(m)
s=bpy.context.scene;s.render.filepath=R+'east-v17.png';bpy.ops.wm.save_as_mainfile(filepath=R+'Uijeongbu_Station_v17_forecourt_shelters.blend',compress=True);bpy.ops.render.render(write_still=True);s.camera=bpy.data.objects['v17 East street-level comparison'];s.render.filepath=R+'east-street-v17.png';bpy.ops.render.render(write_still=True)
