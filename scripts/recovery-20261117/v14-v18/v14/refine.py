import bpy,json
from mathutils import Vector
from pathlib import Path
R=Path('recovery-output/v14'); origin=Vector((31.531,71.647,0));u=Vector((.341,.940,0)).normalized();n=Vector((u.y,-u.x,0))
o=bpy.data.objects['East elevation individual pale panels'];me=o.data
# 2025 photograph: uninterrupted upper fascia rather than staircase silhouette.
# Preserve existing panel grid and window cuts; fill ONLY missing upper front fascia.
cols={}
for p in me.polygons:
 ps=[v.co for v in [me.vertices[i] for i in p.vertices]];a=round(min((v-origin).dot(u) for v in ps),4);b=round(max((v-origin).dot(u) for v in ps),4)
 cols[(a,b)]=max(cols.get((a,b),10),max(v.z for v in ps))
vs=[tuple(v.co) for v in me.vertices];fs=[list(p.vertices) for p in me.polygons];added=0
for (a,b),top in cols.items():
 if top<21 or top>27.99:continue
 z=top+.024
 while z<27.997:
  j=len(vs);vs.extend([tuple(origin+u*t+Vector((0,0,zz))) for t,zz in [(a,z),(b,z),(b,min(z+.576,27.998)),(a,min(z+.576,27.998))]]);fs.append((j,j+1,j+2,j+3));added+=1;z+=.6
new=bpy.data.meshes.new('v14 continuous east fascia');new.from_pydata(vs,[],fs);new.update()
for m in me.materials:new.materials.append(m)
o.data=new
# Match less dominant sign panel proportion (not a surveyed size).
for name in ['Photographed station rooftop sign plate','East station rooftop sign']:
 o=bpy.data.objects[name];points=[o.matrix_world@v.co for v in o.data.vertices];c=sum(points,Vector())/len(points);inv=o.matrix_world.inverted()
 for v,p in zip(o.data.vertices,points):v.co=inv@(c+(p-c)*.84)
# Remove two visible ribbon-end fragments protruding through east facade.
o=bpy.data.objects['North window interior backs'];me=o.data;fs=[];mids=[];removed=0
for p in me.polygons:
 ps=[o.matrix_world@me.vertices[i].co for i in p.vertices]
 if max((v-origin).dot(n) for v in ps)>-.03:removed+=1
 else:fs.append(list(p.vertices));mids.append(p.material_index)
new=bpy.data.meshes.new('v14 north backs confined inside skin');new.from_pydata([tuple(v.co) for v in me.vertices],[],fs);new.update()
for m in me.materials:new.materials.append(m)
for p,i in zip(new.polygons,mids):p.material_index=i
o.data=new
s=bpy.context.scene;s.render.filepath=str(R/'east-v14.png');s.cycles.samples=32
(R/'validation.json').write_text(json.dumps({'added_upper_front_panels':added,'removed_outward_back_faces':removed,'sign_scale':.84,'note':'facade-only visual correction, no surveyed height claim; roads/building footprints unchanged'},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v14_east_fascia.blend'),compress=True)
bpy.ops.render.render(write_still=True)
