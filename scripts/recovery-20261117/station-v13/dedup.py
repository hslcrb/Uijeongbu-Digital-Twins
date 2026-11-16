import bpy,json
from mathutils import Vector
from pathlib import Path
R=Path('/workspace/shared/station-v13');origin=Vector((31.531,71.647,0));u=Vector((.341,.940,0)).normalized();n=Vector((u.y,-u.x,0))
# restore full original cladding columns from v12, filling misplaced former holes
with bpy.data.libraries.load('/workspace/shared/west-v12/Uijeongbu_Station_v12_west_pylon.blend',link=False) as (src,dst):dst.objects=['East elevation individual pale panels']
old=dst.objects[0];columns={}
for p in old.data.polygons:
 ps=[old.data.vertices[i].co for i in p.vertices];a=round(min((v-origin).dot(u) for v in ps),4);b=round(max((v-origin).dot(u) for v in ps),4);columns[(a,b)]=max(columns.get((a,b),10),max(v.z for v in ps))
# shared subtract function
exec(open('/workspace/shared/station-v13/punched_windows.py').read().split('V=[];F=[]')[0].split("o=bpy.data.objects['East elevation individual pale panels'];")[1].replace("holes=", "holes=",1)) if False else None
holes=[(t-.48,t+.48,14.9,15.9) for t in [21.5,24.8,33.5,36.8]]
def sub(r,h):
 a,b,c,d=r;x,y,z,w=h
 if b<=x or a>=y or d<=z or c>=w:return[r]
 x=max(a,x);y=min(b,y);z=max(c,z);w=min(d,w);return [q for q in [(a,x,c,d),(y,b,c,d),(x,y,c,z),(x,y,w,d)] if q[1]-q[0]>.0001 and q[3]-q[2]>.0001]
vs=[];fs=[]
for (a,b),top in columns.items():
 z=10.022
 while z<top-.001:
  parts=[(a,b,z,min(z+.576,top))]
  for h in holes:parts=[q for r in parts for q in sub(r,h)]
  for aa,bb,cc,dd in parts:
   j=len(vs);vs.extend([tuple(origin+u*t+Vector((0,0,zz))) for t,zz in [(aa,cc),(bb,cc),(bb,dd),(aa,dd)]]);fs.append((j,j+1,j+2,j+3))
  z+=.6
ob=bpy.data.objects['East elevation individual pale panels'];me=bpy.data.meshes.new('east only four photo windows');me.from_pydata(vs,[],fs);me.update()
for m in ob.data.materials:me.materials.append(m)
ob.data=me;bpy.data.objects.remove(old,do_unlink=True)
for name in ['Batched 03_Station Glass','North photographed window ribbons','North window interior backs']:
 ob=bpy.data.objects[name];me=ob.data;fs=[];mids=[]
 for p in me.polygons:
  c=ob.matrix_world@p.center;t=(c-origin).dot(u);d=(c-origin).dot(n)
  bad=(0<t<43 and -1<d<5 and 14<c.z<17) if name.startswith('Batched') else ((c-origin).dot(n)>-.15)
  if not bad:fs.append(tuple(p.vertices));mids.append(p.material_index)
 new=bpy.data.meshes.new(name+'clean');new.from_pydata([tuple(v.co) for v in me.vertices],[],fs);new.update()
 for m in me.materials:new.materials.append(m)
 for p,i in zip(new.polygons,mids):p.material_index=i
 ob.data=new
s=bpy.context.scene;s.render.filepath=str(R/'east-v13c-clean.png');bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v13c_east_corrected.blend'),compress=True);bpy.ops.render.render(write_still=True)
