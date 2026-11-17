import bpy,json,math
from mathutils import Vector,Matrix
from pathlib import Path
R=Path('recovery-output/v16')
origin=Vector((-98,27,0));target=Vector((49.4,111.7,0));angle=math.atan2(.940,.341)
T=Matrix.Translation(target)@Matrix.Rotation(angle,4,'Z')@Matrix.Translation(-origin)
names=[]
for o in list(bpy.data.objects):
 if not(o.name.startswith('v12 pylon ') or o.name.startswith('v12 station pylon ')):continue
 new=o.copy();new.data=o.data.copy();new.name=o.name.replace('v12','v16 east',1);bpy.context.collection.objects.link(new);new.matrix_world=T@o.matrix_world;names.append(new.name)
# Correct OSM bicycle parking misread as generic multi-storey building.
o=bpy.data.objects['OSM building [1311394039]'];bpy.data.objects.remove(o,do_unlink=True)
removed={}
for o in list(bpy.data.objects):
 if not(o.type=='MESH' and (o.name.startswith('Context ') or o.name.startswith('Room glow'))):continue
 me=o.data;fs=[];mi=[]
 for p in me.polygons:
  c=o.matrix_world@p.center
  if 54<c.x<100 and 68<c.y<78 and c.z<11:continue
  fs.append(list(p.vertices));mi.append(p.material_index)
 if len(fs)==len(me.polygons):continue
 nm=bpy.data.meshes.new('v16 bicycle context cleaned');nm.from_pydata([tuple(v.co) for v in me.vertices],[],fs);nm.update()
 for m in me.materials:nm.materials.append(m)
 for p,i in zip(nm.polygons,mi):p.material_index=i
 removed[o.name]=len(me.polygons)-len(fs);o.data=nm
A=Vector((55.28085,70.61584,0));B=Vector((98.6639,75.10204,0));d=(B-A).normalized();n=Vector((-d.y,d.x,0));L=(B-A).length
roofmat=bpy.data.materials.new('v16 cycle canopy pale metal');roofmat.diffuse_color=(.56,.59,.59,1)
glassmat=bpy.data.materials.new('v16 cycle shelter blue-grey glazing');glassmat.diffuse_color=(.10,.19,.21,1)
V=[];F=[]
for i in range(17):
 th=math.pi*i/16
 for t in [0,L]:V.append(tuple(A+d*t+n*(1.49*math.cos(th))+Vector((0,0,2.5+.60*math.sin(th)))))
for i in range(16):j=i*2;F.append((j,j+1,j+3,j+2))
me=bpy.data.meshes.new('v16 curved cycle canopy mesh');me.from_pydata(V,[],F);me.update();o=bpy.data.objects.new('v16 bicycle parking curved canopy',me);bpy.context.collection.objects.link(o);me.materials.append(roofmat)
V=[];F=[]
for side in [-1,1]:
 for k in range(14):
  a=L*k/14+.045;b=L*(k+1)/14-.045;j=len(V)
  V.extend([tuple(A+d*t+n*(side*1.47)+Vector((0,0,z))) for t,z in [(a,.3),(b,.3),(b,2.47),(a,2.47)]]);F.append((j,j+1,j+2,j+3))
me=bpy.data.meshes.new('v16 cycle glazing separated panels');me.from_pydata(V,[],F);me.update();o=bpy.data.objects.new('v16 bicycle parking side glazing',me);bpy.context.collection.objects.link(o);me.materials.append(glassmat)
# narrow rectangular posts fill the panel divisions, not building storeys.
V=[];F=[]
for side in [-1,1]:
 for k in range(15):
  c=A+d*(L*k/14)+n*(side*1.49);j=len(V)
  V.extend([tuple(c+d*x+n*y+Vector((0,0,z))) for x,y,z in [(-.04,-.04,.1),(.04,-.04,.1),(.04,.04,.1),(-.04,.04,.1),(-.04,-.04,2.5),(.04,-.04,2.5),(.04,.04,2.5),(-.04,.04,2.5)]])
  F.extend([tuple(j+i for i in face) for face in [(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]])
me=bpy.data.meshes.new('v16 cycle canopy posts mesh');me.from_pydata(V,[],F);me.update();o=bpy.data.objects.new('v16 bicycle parking posts',me);bpy.context.collection.objects.link(o);me.materials.append(roofmat)
(R/'bicycle-validation.json').write_text(json.dumps({'old_height':9.9,'new_eave':2.5,'new_crown':3.1,'height_status':'photo proportion estimate; source has no height','removed_generic_faces':removed,'source':'OSM way1311394039 amenity=bicycle_parking bicycle_parking=building'},indent=2))

s=bpy.context.scene;s.render.filepath=str(R/'east-v16.png');s.cycles.samples=32
(R/'validation.json').write_text(json.dumps({'new_objects':names,'source':'2025-03-23 east elevation photo23 zenith2.tistory.com/15862539','position':'estimated existing model coordinates 49.4,111.7,0','geometry':'reuse documented v12 KORAIL-outline pylon design, east placement supported by photo; west retained'},ensure_ascii=False,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v16_east_wayfinding.blend'),compress=True);bpy.ops.render.render(write_still=True)
