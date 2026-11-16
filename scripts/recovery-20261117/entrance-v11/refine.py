import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/shared/entrance-v11')
# Replace only the provisional v10 ceiling/light meshes, preserving the rest.
for o in list(bpy.data.objects):
 if o.name.startswith('v10 batched '):bpy.data.objects.remove(o,do_unlink=True)
materials=[bpy.data.materials['v10 soffit satin aluminium'],bpy.data.materials['v10 downlight recessed baffle'],bpy.data.materials['v10 warm opal diffuser']]
verts=[[],[],[]];faces=[[],[],[]]
def face(points,mi):
 i=len(verts[mi]);verts[mi]+=points;faces[mi].append(tuple(range(i,i+len(points))))
def ring(x,y,r,z,n=48):return [(x+r*math.cos(i*math.tau/n),y+r*math.sin(i*math.tau/n),z) for i in range(n)]
def bridge(a,b,mi):
 for i in range(len(a)):j=(i+1)%len(a);face([a[i],a[j],b[j],b[i]],mi)
z=16.4325; lamps=[]
for ix in range(15):
 for iy in range(5):
  x=-13+ix*2;y=29.9+iy*1.8;hw=.9925;hh=.8925
  if ix in [1,4,7,10,13] and iy in [0,2,4]:
   lamps.append((x,y));a=ring(x,y,.10,z);b=[]
   for i in range(48):
    u=math.cos(i*math.tau/48);v=math.sin(i*math.tau/48);t=min(hw/max(abs(u),1e-10),hh/max(abs(v),1e-10));b.append((x+u*t,y+v*t,z))
   bridge(a,b,0) # actual open circular aperture, not a disk placed on top
   bridge(ring(x,y,.102,z-.002),ring(x,y,.084,z-.002),0)
   bridge(ring(x,y,.084,z-.002),ring(x,y,.067,z+.037),1)
   face(list(reversed(ring(x,y,.067,z+.037))),2)
  else:face([(x-hw,y-hh,z),(x+hw,y-hh,z),(x+hw,y+hh,z),(x-hw,y+hh,z)],0)
for mi,m in enumerate(materials):
 me=bpy.data.meshes.new('v11 physical recessed ceiling mesh');me.from_pydata(verts[mi],[],faces[mi]);me.update();o=bpy.data.objects.new('v11 '+['perforated panel ceiling','recessed dark baffles','recessed diffusers'][mi],me);bpy.context.collection.objects.link(o);o.data.materials.append(m);o['source']='https://hhk2001.tistory.com/8063';o['estimated']='panel size, lamp layout and cavity depth'
# Adjust sign proportions seen in entrance reference: English smaller than Korean.
sign=bpy.data.objects['Blue station entrance fascia'];sign.dimensions.x=13.0
eng=bpy.data.objects['Entrance English'];eng.scale*=1.90/eng.dimensions.x
if eng.type=='FONT':eng.data.extrude=.004;eng.data.bevel_depth=.001
white=bpy.data.materials.new('v11 matte station sign white');white.diffuse_color=(.92,.94,.94,1);white.use_nodes=True;p=white.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.92,.94,.94,1);p.inputs['Roughness'].default_value=.65
for n in ['Entrance English','Entrance Korean','Photo station number 110','Photo station number roundel']:
 o=bpy.data.objects.get(n)
 if o:o.data.materials.clear();o.data.materials.append(white)
# Upper hood must terminate below soffit, rather than intersect and disappear into slab.
for o in bpy.data.objects:
 if o.name.startswith('Photo aluminium sloping hood'):
  for v in o.data.vertices:
   if v.co.z>16.8:v.co.z=16.40
 o2=None
edge=bpy.data.objects.get('Photo hood top edge');edge.location.z=16.40
s=bpy.context.scene;s.cycles.samples=48;s.render.filepath=str(R/'entrance-v11-wide.png');s.camera.location=(-12,28.6,13.6);s.camera.rotation_euler=(Vector((2,40,14.4))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.lens=24
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v11_recessed.blend'),compress=True)
bpy.ops.render.render(write_still=True)
s.camera.location=(-2,33.7,15.0);s.camera.rotation_euler=(Vector((1,35,16.43))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.lens=36;s.render.filepath=str(R/'ceiling-v11-closeup.png');bpy.ops.render.render(write_still=True)
(R/'validation.json').write_text(json.dumps({'lights':15,'aperture_diameter_m':.20,'diffuser_recess_m':.037,'meshes':3,'objects':len(bpy.data.objects),'source':'https://hhk2001.tistory.com/8063','estimated':['dimensions','lamp layout','sign ratio'],'preserved':['Korail mesh text','tactile paving','door detail','whole city model'],'deploy_status':'local only'},indent=2))
