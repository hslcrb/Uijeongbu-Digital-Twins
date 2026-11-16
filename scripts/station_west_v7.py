"""West access: mapped OSM stair alignments + April 2025 photographic structure.
No taxi shelter placed: its footprint is unverified. All heights inferred, not surveyed.
"""
import bpy,math,random
from mathutils import Vector

def add_west_plaza():
 name='21_West_Plaza_v7';old=bpy.data.collections.get(name)
 if old:
  for o in list(old.objects):bpy.data.objects.remove(o,do_unlink=True)
  bpy.data.collections.remove(old)
 col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col)
 def mat(n,c,metal=0,rough=.5,trans=0):
  m=bpy.data.materials.get(n) or bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;p.inputs['Transmission Weight'].default_value=trans;return m
 steel=mat('West photographed pale celadon steel',(.42,.54,.48),.65,.3);glass=mat('West clear canopy glass',(.57,.72,.67),0,.12,.93);stone=mat('West concrete treads',(.53,.55,.53));rubber=mat('West escalator dark handrail',(.035,.04,.038));louver=mat('West aluminium louver',(.24,.27,.26),.5)
 def mesh(n,v,f,m):
  me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.materials.append(m);o=bpy.data.objects.new(n,me);col.objects.link(o);return o
 def box(n,p,s,m):
  p=Vector(p);v=[p+Vector((x*s[0]/2,y*s[1]/2,z*s[2]/2)) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]];return mesh(n,v,[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)],m)
 def beam(n,a,b,w,d,m):
  a,b=Vector(a),Vector(b);o=box(n,(a+b)/2,(w,d,(b-a).length),m);mid=(a+b)/2;rot=Vector((0,0,1)).rotation_difference((b-a).normalized()).to_matrix()
  for v in o.data.vertices:v.co=mid+rot@(v.co-mid)
  return o
 def panel(n,a,b,w,m):
  a,b=Vector(a),Vector(b);d=b-a;side=Vector((-d.y,d.x,0)).normalized()*w/2
  return mesh(n,[a-side,b-side,b+side,a+side],[(0,1,2,3)],m)
 def path(a,b,width,steps,label):
  a,b=Vector(a),Vector(b);delta=b-a;horizontal=Vector((delta.x,delta.y,0));L=horizontal.length;direction=horizontal.normalized();side=Vector((-direction.y,direction.x,0))
  for i in range(steps):
   lo=a+delta*i/steps;hi=a+delta*(i+1)/steps;mid=(lo+hi)/2;mid.z=hi.z-.075
   o=box(label+' tread',mid,(width,L/steps,.15),stone);rot=math.atan2(direction.y,direction.x)-math.pi/2
   R=__import__('mathutils').Matrix.Rotation(rot,3,'Z')
   for v in o.data.vertices:v.co=mid+R@(v.co-mid)
  # Solid side fascia and soffit; unlike a floating ladder, the public ramp has enclosed cheeks.
  for sign in [-1,1]:
   p=a+side*width/2*sign;q=b+side*width/2*sign
   mesh(label+' concrete side fascia',[p-Vector((0,0,.30)),q-Vector((0,0,.30)),q+Vector((0,0,.12)),p+Vector((0,0,.12))],[(0,1,2,3)],stone)
  panel(label+' stair soffit',a-Vector((0,0,.3)),b-Vector((0,0,.3)),width,stone)
  # Narrow green-gray portal framework and transparent roof follow actual mapped ramp.
  roofA=a+Vector((0,0,3.0));roofB=b+Vector((0,0,3.0));count=max(2,math.ceil(L/2.2))
  for j in range(count):
   p=roofA+(roofB-roofA)*j/count;q=roofA+(roofB-roofA)*(j+1)/count;panel(label+' glass roof pane',p+direction*.025,q-direction*.025,width+.7,glass)
  for j in range(count+1):
   p=roofA+(roofB-roofA)*j/count;beam(label+' roof transom',p-side*(width+.7)/2,p+side*(width+.7)/2,.065,.09,steel)
   if j%2==0 or j==count:
    for sign in [-1,1]:
     q=p+side*(width/2+.2)*sign;beam(label+' slender column',(q.x,q.y,max(.12,p.z-3)),q,.13,.13,steel)
  for sign in [-1,1]:
   beam(label+' continuous roof edge',roofA+side*(width+.7)/2*sign,roofB+side*(width+.7)/2*sign,.13,.17,steel)
   ra=a+side*width/2*sign;rb=b+side*width/2*sign
   mesh(label+' transparent balustrade',[ra+Vector((0,0,.15)),rb+Vector((0,0,.15)),rb+Vector((0,0,1.12)),ra+Vector((0,0,1.12))],[(0,1,2,3)],glass)
   beam(label+' handrail',ra+Vector((0,0,1.15)),rb+Vector((0,0,1.15)),.065,.07,rubber)
  return L
 # OSM way770806014/015: southwest lower stair/escalator; north leg770806018/019; upper770806021/022.
 path((-89,28.6,.12),(-72,35.8,6.72),5.4,44,'Southwest access')
 path((-71.2,66.2,.12),(-68.5,46.8,6.72),6,45,'North access')
 path((-62.2,41.4,6.72),(-47.4,43.3,11),7,31,'Upper access')
 panel('Landing floor',(-72,35.8,6.72),(-68.5,46.8,6.72),9,stone)
 for x,y in [(-75,36),(-65,37),(-73,45),(-64,46)]:beam('Landing structural support',(x,y,.12),(x,y,9.72),.22,.22,steel)
 panel('Landing canopy',(-72,35.8,9.72),(-68.5,46.8,9.72),9.7,glass)
 for j in range(7):
  y=34+j*2;beam('Landing canopy grid',(-75,y,9.72),(-62,y+1.5,9.72),.08,.1,steel)
 # Remove old flat mapped step ribbons, not independent other agents' geometry.
 for o in list(bpy.data.objects):
  if o.name in ['Walk '+i for i in ['770806014','770806015','770806018','770806019','770806021','770806022','1365117687']]:bpy.data.objects.remove(o,do_unlink=True)
 # Replace the original invented west stair stack with the correctly mapped approach.
 for o in list(bpy.data.objects):
  if o.type=='MESH' and o.name.startswith(('Plaza stair','Handrail upright')) and o.data.vertices:
   if sum((o.matrix_world@v.co).x for v in o.data.vertices)/len(o.data.vertices)<-40:bpy.data.objects.remove(o,do_unlink=True)
  elif o.type=='CURVE' and o.name.startswith('Stair handrail'):
   pts=[p for sp in o.data.splines for p in sp.points]
   if pts and sum(p.co.x for p in pts)/len(pts)<-40:bpy.data.objects.remove(o,do_unlink=True)
 # v5 batches original boxes by material. Remove only faces entirely inside the
 # exact original west stair-stack envelope from build_scene.py x=-49,width8.
 for o in bpy.data.objects:
  if o.type=='MESH' and o.name.startswith('Batched 03_Station'):
   faces=[];removed=0
   for f in o.data.polygons:
    pts=[o.matrix_world@o.data.vertices[i].co for i in f.vertices]
    inside=all(-53.001<=p.x<=-44.999 and 19.80<=p.y<=31.23 and -.01<=p.z<=11.1 for p in pts)
    if inside:removed+=1
    else:faces.append((tuple(f.vertices),f.material_index))
   if removed:
    vs=[tuple(v.co) for v in o.data.vertices];mats=list(o.data.materials);me=bpy.data.meshes.new(o.data.name+' west-stair-replaced');me.from_pydata(vs,[],[f[0] for f in faces]);
    for m in mats:me.materials.append(m)
    for f,(_,mi) in zip(me.polygons,faces):f.material_index=mi
    o.data=me;o['west_v7_replaced_faces']=removed
 # Photo shows horizontal louvers on utility wall; attach to mapped wall instead of inventing building footprint.
 a=Vector((-58.8,101.2,0));b=Vector((-55,61.9,0));direction=(b-a).normalized();normal=Vector((direction.y,-direction.x,0))
 for k in range(22):
  p=a+direction*25+normal*.06;p.z=2+k*.12;q=a+direction*37+normal*.06;q.z=p.z;beam('Utility facade horizontal louver',p,q,.09,.10,louver)
 for o in col.objects:o['evidence']='OSM west access ways770806011/14/15/18/19/21/22; pocket2025.jpg 2025-04-17. Dimensions/heights photo-interpreted.'
 return {'objects':len(col.objects),'taxi_shelter':'not placed: unverified footprint','datum':'127.046E 37.738N xEast yNorth','height_status':'inferred, not measured','source_photo':'pocket2025.jpg'}
