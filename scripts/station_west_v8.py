"""Photographic west-access refinements, additive to v7. No speculative furniture."""
import bpy, math
from mathutils import Vector

def refine_west_access():
 name='22_West_access_photo_v8';old=bpy.data.collections.get(name)
 if old:
  for o in list(old.objects):bpy.data.objects.remove(o,do_unlink=True)
  bpy.data.collections.remove(old)
 col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col)
 def mat(n,c,metal=0,rough=.5):
  m=bpy.data.materials.get(n) or bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
 steel=mat('West photo cylindrical pale steel',(.55,.60,.56),.5,.34);stone=mat('West photo sidewall ceramic',(.62,.65,.63),0,.6);joint=mat('West photo sidewall shadow joint',(.25,.29,.27),0,.7)
 glass=bpy.data.materials.get('West clear canopy glass')
 def mesh(n,vs,fs,m):
  me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.materials.append(m);o=bpy.data.objects.new(n,me);col.objects.link(o);return o
 def rod(n,a,b,r,m,segments=12):
  a,b=Vector(a),Vector(b);d=(b-a).normalized();u=d.cross(Vector((0,0,1)))
  if u.length<.01:u=d.cross(Vector((0,1,0)))
  u.normalize();v=d.cross(u);vs=[p+r*(u*math.cos(j*2*math.pi/segments)+v*math.sin(j*2*math.pi/segments)) for p in [a,b] for j in range(segments)];faces=[tuple(range(segments-1,-1,-1)),tuple(range(segments,2*segments))]+[(j,(j+1)%segments,(j+1)%segments+segments,j+segments) for j in range(segments)];return mesh(n,vs,faces,m)
 def pane(n,a,b,side,width,m):return mesh(n,[a-side*width/2,b-side*width/2,b+side*width/2,a+side*width/2],[(0,1,2,3)],m)
 for label,A,B,width in [('Southwest',(-89,28.6,.12),(-72,35.8,6.72),5.4),('North',(-71.2,66.2,.12),(-68.5,46.8,6.72),6),('Upper',(-62.2,41.4,6.72),(-47.4,43.3,11),7)]:
  a,b=Vector(A),Vector(B);d=Vector((b.x-a.x,b.y-a.y,0)).normalized();side=Vector((-d.y,d.x,0));ra=a+Vector((0,0,3));rb=b+Vector((0,0,3))
  # Longitudinal roof grid omitted from v7: continuous narrow steel bars.
  for off in [-width*.25,0,width*.25]:rod(label+' longitudinal glazing bar',ra+side*off,rb+side*off,.045,steel,8)
  if label!='Upper':
   # mapped roof projects beyond low stair endpoint; photo shows level entrance cover.
   start=ra-d*2.0;end=ra-d*.035
   for k in range(3):
    p=start+(end-start)*k/3;q=start+(end-start)*(k+1)/3
    pane(label+' flat entrance glass',p+d*.015,q-d*.015,side,width+.7,glass)
    rod(label+' flat canopy crossbar',p-side*(width+.7)/2,p+side*(width+.7)/2,.075,steel)
   for off in [-width/2,0,width/2]:rod(label+' flat canopy longitudinal',start+side*off,end+side*off,.06,steel)
   for sign in [-1,1]:
    p=start+side*(width/2-.25)*sign+d*.45
    rod(label+' round entrance main column',(p.x,p.y,.12),p,.21,steel,20)
    rod(label+' column cap collar',p-Vector((0,0,.25)),p-Vector((0,0,.12)),.235,steel,20)
   rod(label+' round portal cross tube',start-side*(width/2-.25)+d*.45,start+side*(width/2-.25)+d*.45,.16,steel,20)
   # Photo confirms solid triangular outer cheeks with ceramic joints below glass balustrade.
   for sign in [-1,1]:
    pa=a+side*(width/2+.035)*sign;pb=b+side*(width/2+.035)*sign
    mesh(label+' closed ramp sidewall',[Vector((pa.x,pa.y,.12)),Vector((pb.x,pb.y,.12)),pb,pa],[(0,1,2,3)],stone)
    L=(Vector((b.x,b.y,0))-Vector((a.x,a.y,0))).length
    for j in range(1,math.ceil(L/1.2)):
     t=j*1.2/L
     if t>=1:continue
     p=pa+(pb-pa)*t;out=side*.007*sign
     rod(label+' ceramic vertical joint',Vector((p.x,p.y,.13))+out,p+out,.008,joint,4)
    for h in [1.2,2.4,3.6,4.8,6.0]:
     t=(h-a.z)/(b.z-a.z)
     if not 0<t<1:continue
     p=pa+(pb-pa)*t;q=pb.copy();q.z=h;rod(label+' ceramic horizontal joint',p+side*.007*sign,q+side*.007*sign,.008,joint,4)
 for o in col.objects:o['source']='old2014-3/4 portal cross-section; pocket2025 sidewall and frame continuity';o['dimension_status']='photo-interpreted, not survey'
 return {'objects':len(col.objects),'flat_entrance_canopies':2,'grounded_round_main_columns':4,'source_continuity':'2014 portal detail+2025 wide photograph; current material exactness unverified'}
