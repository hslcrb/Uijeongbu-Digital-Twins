import bpy,math,json
from mathutils import Vector
from pathlib import Path
R=Path('recovery-output/v17');changes=[];bounds=[]
mat=bpy.data.materials.get('v16 cycle canopy pale metal');trim=bpy.data.materials.get('v15 satin railing')
for id in ['1144299903','1144299904']:
 o=bpy.data.objects['OSM building ['+id+']'];foot=[o.matrix_world@v.co for v in o.data.vertices[:4]]
 edges=[(foot[(i+1)%4]-foot[i]).length for i in range(4)];i=max(range(4),key=lambda k:edges[k]);a=foot[i];b=foot[(i+1)%4];d=(b-a).normalized();center=sum(foot,Vector())/4;n=Vector((-d.y,d.x,0));L=edges[i];width=min(edges)
 A=center-d*L/2;A.z=0
 lo=[min(v[k] for v in foot) for k in range(2)];hi=[max(v[k] for v in foot) for k in range(2)];bounds.append((lo,hi));bpy.data.objects.remove(o,do_unlink=True)
 V=[];F=[]
 for k in range(25):
  th=math.pi*k/24
  for t in [0,L]:V.append(tuple(A+d*t+n*(width*.5*math.cos(th))+Vector((0,0,1+1.5*math.sin(th)))))
 for k in range(24):j=k*2;F.append((j,j+1,j+3,j+2))
 me=bpy.data.meshes.new('v17 OSM round roof '+id);me.from_pydata(V,[],F);me.update();ob=bpy.data.objects.new('v17 bicycle shelter '+id,me);bpy.context.collection.objects.link(ob);me.materials.append(mat)
 V=[];F=[]
 # open supporting poles, no fictitious multi-floor glazing
 for side in [-1,1]:
  for k in range(6):
   c=A+d*(L*k/5)+n*(side*width*.49);j=len(V)
   V.extend([tuple(c+d*x+n*y+Vector((0,0,z))) for x,y,z in [(-.04,-.04,0),(.04,-.04,0),(.04,.04,0),(-.04,.04,0),(-.04,-.04,1),(.04,-.04,1),(.04,.04,1),(-.04,.04,1)]])
   F.extend([tuple(j+i for i in f) for f in [(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]])
 me=bpy.data.meshes.new('v17 shelter supports '+id);me.from_pydata(V,[],F);me.update();ob=bpy.data.objects.new('v17 bicycle supports '+id,me);bpy.context.collection.objects.link(ob);me.materials.append(trim)
 changes.append({'osm':id,'old_generic_height':9.9,'new_eave':1,'new_crown':2.5,'height_status':'OSM height1 / roofheight1.5 conflict; interpreted eave+rise provisionally, not field verified','length':L,'width':width})
removed={}
for o in list(bpy.data.objects):
 if not(o.type=='MESH' and (o.name.startswith('Context ') or o.name.startswith('Room glow'))):continue
 me=o.data;fs=[];mi=[]
 for p in me.polygons:
  c=o.matrix_world@p.center
  if any(lo[0]-.2<c.x<hi[0]+.2 and lo[1]-.2<c.y<hi[1]+.2 and c.z<11 for lo,hi in bounds):continue
  fs.append(list(p.vertices));mi.append(p.material_index)
 if len(fs)==len(me.polygons):continue
 nm=bpy.data.meshes.new('v17 shelter context clean');nm.from_pydata([tuple(v.co) for v in me.vertices],[],fs);nm.update()
 for m in me.materials:nm.materials.append(m)
 for p,i in zip(nm.polygons,mi):p.material_index=i
 removed[o.name]=len(me.polygons)-len(fs);o.data=nm
(R/'validation.json').write_text(json.dumps({'changes':changes,'generic_faces_removed':removed},indent=2))
s=bpy.context.scene;s.render.filepath=str(R/'east-v17.png');s.cycles.samples=32
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v17_forecourt_shelters.blend'),compress=True);bpy.ops.render.render(write_still=True)
