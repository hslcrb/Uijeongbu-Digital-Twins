import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/shared/entrance-v11');vs=[];fs=[];hw=.9925;hh=.8925
for ix in [1,4,7,10,13]:
 for iy in [0,2,4]:
  x=-13+ix*2;y=29.9+iy*1.8
  for sx,sy in [(1,1),(-1,1),(-1,-1),(1,-1)]:
   a=math.atan2(sy*hh,sx*hw)%math.tau;k=math.floor(a/(math.tau/48));p=[]
   for ang in [k*math.tau/48,(k+1)*math.tau/48]:
    u=math.cos(ang);v=math.sin(ang);t=min(hw/max(abs(u),1e-10),hh/max(abs(v),1e-10));p.append((x+u*t,y+v*t,16.4325))
   start=len(vs);vs.extend([p[0],(x+sx*hw,y+sy*hh,16.4325),p[1]]);fs.append((start,start+1,start+2))
me=bpy.data.meshes.new('exact rectangular panel corner closure');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('v11 exact panel corners',me);bpy.context.collection.objects.link(o);o.data.materials.append(bpy.data.materials['v10 soffit satin aluminium'])
# Join exact corner patches to the existing panel material mesh without changing count.
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);p=bpy.data.objects['v11 perforated panel ceiling'];p.select_set(True);bpy.context.view_layer.objects.active=p;bpy.ops.object.join()
s=bpy.context.scene;s.cycles.samples=32;bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v11c_recessed.blend'),compress=True);s.render.filepath=str(R/'entrance-v11c-wide.png');bpy.ops.render.render(write_still=True)
s.camera.location=(-2,32.7,15.1);s.camera.rotation_euler=(Vector((1,33.5,16.43))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.lens=44;s.render.filepath=str(R/'ceiling-v11c-closeup.png');bpy.ops.render.render(write_still=True)
