"""Original procedural approximation assets. Not scanned or external-library assets."""
import bpy, math, random
from mathutils import Vector
from pathlib import Path
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
OUT=Path(__file__).resolve().parents[1]/'assets'/'trees.blend'
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.82
 return m
bark=mat('Bark',(0.13,.085,.05))
palettes={'Ginkgo':[(.66,.43,.035),(.9,.66,.08),(.57,.52,.07),(.79,.52,.035)],'Maple':[(.52,.085,.025),(.78,.22,.035),(.68,.36,.045),(.4,.12,.02)],'Pine':[(.04,.12,.045),(.055,.2,.07),(.08,.25,.085),(.1,.18,.07)]}
mats={s:[bark]+[mat(s+str(i),c) for i,c in enumerate(cols)] for s,cols in palettes.items()}
def make(spec,lod):
 random.seed(301+list(palettes).index(spec));vs=[];fs=[];mi=[]
 def face(points,idx):
  st=len(vs);vs.extend([tuple(p) for p in points]);fs.append(tuple(range(st,st+len(points))));mi.append(idx)
 def rod(a,b,ra,rb,sides=6):
  a=Vector(a);b=Vector(b);d=(b-a).normalized();u=d.cross(Vector((0,1,0))).normalized();v=d.cross(u).normalized();rings=[]
  for c,r in [(a,ra),(b,rb)]:rings.append([c+r*(u*math.cos(t*math.tau/sides)+v*math.sin(t*math.tau/sides)) for t in range(sides)])
  for i in range(sides): face([rings[0][i],rings[0][(i+1)%sides],rings[1][(i+1)%sides],rings[1][i]],0)
  face(rings[1],0)
 h=8 if spec!='Maple' else 6.8
 for i in range(8): rod((.08*math.sin(i),0,h*i/8),(.08*math.sin(i+1),0,h*(i+1)/8),.22*(1-i/9),.22*(1-(i+1)/9),8)
 nb=19 if lod==0 else 12
 for i in range(nb):
  z=2.1+(h-2.6)*i/nb;angle=i*2.399;radius=(2.4 if spec=='Maple' else 2.0)*(1-(z/h)*.60)
  if spec=='Pine':radius=2.8*(1-z/h)+.25
  start=Vector((0,0,z));end=Vector((radius*math.cos(angle),radius*math.sin(angle),z+(.8 if spec!='Pine' else .2)))
  rod(start,end,.07*(1-z/h)+.015,.014)
  for j in range(5 if lod==0 else 3):
   mid=start.lerp(end,.4+j*.12);ang=angle+(-1 if j%2 else 1)*.65
   tip=mid+Vector((.7*math.cos(ang),.7*math.sin(ang),.55 if spec!='Pine' else .12));rod(mid,tip,.014,.004,5)
   for k in range(21 if lod==0 else 10):
    c=mid.lerp(tip,random.uniform(.2,1.2))+Vector((random.uniform(-.35,.35),random.uniform(-.35,.35),random.uniform(-.2,.25)))
    a=random.random()*math.tau;u=Vector((math.cos(a),math.sin(a),random.uniform(-.5,.5))).normalized();v=u.cross(Vector((0,0,1))).normalized();size=random.uniform(.065,.12)*(1.25 if lod else 1)
    idx=random.randint(1,4)
    if spec=='Ginkgo':
     points=[c-v*size*.55]+[c+(u*math.cos(t)*size+v*math.sin(t)*size) for t in [0,.45,.9,1.35,1.8,2.25,2.7,math.pi]]
    elif spec=='Maple':
     points=[c+(u*math.cos(t*math.tau/10)+v*math.sin(t*math.tau/10))*size*(1 if t%2==0 else .45) for t in range(10)]
    else:
     points=[c-u*size*.15,c+u*size*.15,c+v*size*2.6+Vector((0,0,.045))]
    face(points,idx)
 mesh=bpy.data.meshes.new(spec+f'_LOD{lod}_Mesh');mesh.from_pydata(vs,[],fs);mesh.update()
 ob=bpy.data.objects.new(spec+f'_Autumn_LOD{lod}' if spec!='Pine' else f'Pine_Evergreen_LOD{lod}',mesh);bpy.context.collection.objects.link(ob)
 for m in mats[spec]: mesh.materials.append(m)
 for p,idx in zip(mesh.polygons,mi):p.material_index=idx;p.use_smooth=(idx==0)
 ob.asset_mark();ob.asset_data.description='Original procedural approximate '+spec+'; not surveyed. Origin at ground. Linked instance ready.'
 ob['source']='Original procedural asset, generated for Uijeongbu twin';ob['height_m']=h;ob['LOD']=lod
 ob['surveyed_species']=False
 return ob
objs=[make(s,l) for s in palettes for l in [0,1]]
for o in objs:o.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
print([(o.name,len(o.data.vertices),len(o.data.polygons)) for o in objs])
