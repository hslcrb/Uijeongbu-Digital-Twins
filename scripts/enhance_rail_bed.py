"""Non-surveyed procedural ballast/fasteners, GLB-compatible UV texture.
Call enhance_rail_bed(root). Changes only material of existing ballast and own collection.
"""
import bpy,bmesh,math,random,xml.etree.ElementTree as ET,gzip
from pathlib import Path
from mathutils import Vector

def enhance_rail_bed(root):
 root=Path(root);rng=random.Random(1105);name='16_Rail_Bed_Detail'
 old=bpy.data.collections.get(name)
 if old:bpy.data.batch_remove(list(old.objects));bpy.data.collections.remove(old)
 col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col)
 def mat(n,c,metal=0):
  m=bpy.data.materials.get(n) or bpy.data.materials.new(n);m.use_nodes=True;m.diffuse_color=(*c,1);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.85;return m
 # Original procedural image, no external asset or photographic claim.
 path=root/'assets'/'rail-ballast-procedural.png'
 image=bpy.data.images.load(str(path),check_existing=True);image.pack();m=mat('Rail ballast textured',(.3,.29,.27));nt=m.node_tree;tex=nt.nodes.new('ShaderNodeTexImage');tex.image=image;nt.links.new(tex.outputs['Color'],nt.nodes.get('Principled BSDF').inputs['Base Color'])
 for o in bpy.data.objects:
  if o.type=='MESH' and o.name.startswith('Rail crushed stone'):
   o.data.materials.clear();o.data.materials.append(m);uv=o.data.uv_layers.get('UVMap') or o.data.uv_layers.new(name='UVMap')
   for loop in o.data.loops:
    co=o.matrix_world@o.data.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(co.x/1.2,co.y/1.2)
 mats=[mat('Ballast chip '+str(i),(.19+i*.035,.18+i*.034,.165+i*.032)) for i in range(5)];metal=mat('Rail fastener rust',(.18,.105,.065),.65)
 batches={i:([],[]) for i in range(6)}
 def solid(v,f,i):
  vs,fs=batches[i];off=len(vs);vs.extend(v);fs.extend([tuple(q+off for q in a) for a in f])
 def stone(x,y,z,r):
  h=r*rng.uniform(.4,.8);ang=rng.random()*math.tau;v=[(x+math.cos(ang+j*math.pi/2)*r,y+math.sin(ang+j*math.pi/2)*r,z) for j in range(4)]+[(x,y,z+h),(x,y,z-.025)];solid(v,[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(1,0,5),(2,1,5),(3,2,5),(0,3,5)],rng.randrange(5))
 def bolt(p,u,per):
  # Small rectangular baseplates below both rail feet, oriented to track.
  v=[tuple(p+u*a+per*b+Vector((0,0,c))) for a,b,c in [(-.11,-.13,0),(.11,-.13,0),(.11,.13,0),(-.11,.13,0),(-.11,-.13,.025),(.11,-.13,.025),(.11,.13,.025),(-.11,.13,.025)]];solid(v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],5)
 r=ET.parse(gzip.open(root/'data/map.osm.gz','rb')).getroot();nodes={e.get('id'):Vector(((float(e.get('lon'))-127.046)*111320*math.cos(math.radians(37.738)),(float(e.get('lat'))-37.738)*111320,0)) for e in r.findall('node')};chips=plates=0
 for w in r.findall('way'):
  t={e.get('k'):e.get('v') for e in w.findall('tag')}
  if t.get('railway')!='rail':continue
  ps=[nodes[e.get('ref')] for e in w.findall('nd') if e.get('ref') in nodes]
  for a,b in zip(ps,ps[1:]):
   if not all(-265<p.x<355 and -225<p.y<335 for p in [a,b]):continue
   d=b-a;L=d.length
   if L<.1:continue
   u=d.normalized();per=Vector((-u.y,u.x,0))
   # Geometric shoulders, sparse chips complement UV image; deterministic.
   for j in range(int(L*6)):
    p=a+u*rng.uniform(0,L)+per*rng.uniform(-1.67,1.67);stone(p.x,p.y,.18,rng.uniform(.025,.065));chips+=1
   for j in range(int(L/.7)):
    p=a+u*(j*.7+.2)
    for off in [-.7175,.7175]:bolt(p+per*off+Vector((0,0,.28)),u,per);plates+=1
 for i,(vs,fs) in batches.items():
  me=bpy.data.meshes.new('Railbed batch');me.from_pydata(vs,[],fs);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new('Rail bed chips' if i<5 else 'Rail baseplates',me);col.objects.link(o);o.data.materials.append(mats[i] if i<5 else metal)
 col['source']='Original procedural visual approximation; OSM track alignment; not measured stone/fastener count';print('RAIL_BED',{'chips':chips,'baseplates':plates,'objects':len(col.objects)});return col
