"""East station cladding: 2025-03-23 photograph; tile module sizes inferred."""
import bpy,math,random
from mathutils import Vector

def add_station_cladding():
 s=bpy.context.scene;name='15_Station_east_cladding';old=bpy.data.collections.get(name)
 if old:
  north=bpy.data.collections.get('17_Station_north_windows')
  if not north:north=bpy.data.collections.new('17_Station_north_windows');s.collection.children.link(north)
  for o in list(old.objects):
   if o.name.startswith('North '):old.objects.unlink(o);north.objects.link(o)
   else:bpy.data.objects.remove(o,do_unlink=True)
  bpy.data.collections.remove(old)
 col=bpy.data.collections.new(name);s.collection.children.link(col);rng=random.Random(225)
 mats=[]
 for i,c in enumerate([.75,.76,.77,.78]):
  m=bpy.data.materials.get('Station pale ceramic '+str(i)) or bpy.data.materials.new('Station pale ceramic '+str(i));m.diffuse_color=(c,c+.01,c+.015,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=.34;mats.append(m)
 vs=[];fs=[];mi=[]
 # The east OSM boundary is collinear; module grid is photographic interpretation.
 a=Vector((31.498506,71.645552));b=Vector((46.085713,111.887732));d=(b-a).normalized();n=Vector((d.y,-d.x));L=(b-a).length
 for u in range(math.ceil(L/1.2)):
  lo=u*1.2+.012;hi=min((u+1)*1.2-.012,L)
  for row in range(30):
   z=10.01+row*.6;mid=a+d*((lo+hi)/2)
   if z>=21.99 and mid.y<81.6755:continue
   if any(abs(mid.y-y)<1.1 for y in [79,82,94,97]) and 14.1<z<15.9:continue
   p=a+d*lo+n*.03;q=a+d*hi+n*.03;i=len(vs);vs.extend([(p.x,p.y,z+.012),(q.x,q.y,z+.012),(q.x,q.y,z+.588),(p.x,p.y,z+.588)]);fs.append((i,i+1,i+2,i+3));mi.append(rng.randrange(4))
 me=bpy.data.meshes.new('Station ceramic grid');me.from_pydata(vs,[],fs)
 for m in mats:me.materials.append(m)
 for p,i in zip(me.polygons,mi):p.material_index=i
 ob=bpy.data.objects.new('East elevation individual pale panels',me);col.objects.link(ob);ob['evidence']='2025-03-23 zenith2 station exterior photo. Tile pitch and tone are inferred, not measured.'
 # Correct lettering plane to follow the mapped facade, rather than hovering several metres away.
 sign=bpy.data.objects.get('East station rooftop sign')
 if sign:
  p=a+d*(L*.59)+n*.4;sign.location=(p.x,p.y,29);sign.rotation_euler=(math.pi/2,0,math.atan2(n.x,-n.y));sign.data.size=5.5
  p0=p-d*7-n*.1;p1=p+d*7-n*.1
  me=bpy.data.meshes.new('Rooftop sign backing');me.from_pydata([(p0.x,p0.y,28.45),(p1.x,p1.y,28.45),(p1.x,p1.y,32.0),(p0.x,p0.y,32.0)],[],[(0,1,2,3)]);me.materials.append(mats[2]);ob=bpy.data.objects.new('Photographed station rooftop sign plate',me);col.objects.link(ob)
  cu=bpy.data.curves.new('Station sign English subtitle','FONT');cu.body='Uijeongbu Station';cu.font=sign.data.font;cu.size=1.1;cu.align_x='CENTER';cu.extrude=.01;cu.materials.append(sign.data.materials[0]);ob=bpy.data.objects.new(cu.name,cu);col.objects.link(ob);ob.location=(p.x,p.y,28.6);ob.rotation_euler=sign.rotation_euler
 return {'ceramic_panels':len(fs),'source_date':'2025-03-23','surveyed':False}


def add_north_window_bands():
 """North face has long horizontal windows in hb2025, unlike the nearly closed east face."""
 s=bpy.context.scene;col=bpy.data.collections.get('15_Station_east_cladding')
 target=next((o for o in s.objects if o.get('osm_way_id')=='1311394019'),None)
 if not target or target.get('north_bands_done'):return
 vs=[tuple(v.co) for v in target.data.vertices];faces=[];gv=[];gf=[];rv=[];rf=[]
 for f in target.data.polygons:
  pp=[Vector(vs[i]) for i in f.vertices]
  if len(pp)!=4 or max(p.z for p in pp)-min(p.z for p in pp)<2 or sum(p.y for p in pp)/4<99:
   faces.append(tuple(f.vertices));continue
  low=sorted(pp,key=lambda p:p.z)[:2];a,b=low;d=(b-a);d.z=0
  if d.length<2:faces.append(tuple(f.vertices));continue
  normal=Vector((-d.y,d.x,0)).normalized()
  if normal.y<0:normal=-normal
  for za,zb in [(10,14),(15.4,18),(19.4,22)]:
   i=len(vs);vs.extend([(a.x,a.y,za),(b.x,b.y,za),(b.x,b.y,zb),(a.x,a.y,zb)]);faces.append((i,i+1,i+2,i+3))
  for za,zb in [(14,15.4),(18,19.4)]:
   count=max(1,round(d.length/2.4))
   for j in range(count):
    p=a+d*(j/count)+normal*.03;q=a+d*((j+1)/count)+normal*.03;i=len(gv);gv.extend([(p.x,p.y,za+.025),(q.x,q.y,za+.025),(q.x,q.y,zb-.025),(p.x,p.y,zb-.025)]);gf.append((i,i+1,i+2,i+3))
    p-=normal*2;q-=normal*2;i=len(rv);rv.extend([(p.x,p.y,za),(q.x,q.y,za),(q.x,q.y,zb),(p.x,p.y,zb)]);rf.append((i,i+1,i+2,i+3))
 oldm=list(target.data.materials);me=bpy.data.meshes.new('North perforated wall');me.from_pydata(vs,[],faces)
 for m in oldm:me.materials.append(m)
 target.data=me;target['north_bands_done']=True
 for name,v,f,mat in [('North photographed window ribbons',gv,gf,bpy.data.materials.get('Context transparent thin glazing')),('North window interior backs',rv,rf,bpy.data.materials.get('Context room wall'))]:
  me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.materials.append(mat);o=bpy.data.objects.new(name,me);col.objects.link(o)
 return {'window_modules':len(gf),'source':'hb2025 architecture photo; module dimensions inferred'}
