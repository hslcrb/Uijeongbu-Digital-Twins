import bpy,math,os,json
from mathutils import Vector
P=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,metal=0,rough=.45,emit=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emit:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emit
 return m
stone=mat('Gray polished granite',(.36,.39,.39),.12,.22);wall=mat('Pale granite walls',(.58,.6,.59),.05,.35);steel=mat('Brushed stainless',(.4,.45,.46),.8,.24);black=mat('Black trim',(.018,.023,.026),.2,.3);ceil=mat('Metal ceiling tiles',(.32,.35,.35),.65,.35);yellow=mat('Tactile ochre',(.83,.57,.08),0,.5);blue=mat('Korail blue signs',(.018,.04,.21),.1,.4);white=mat('Sign white',(.9,.95,.94),0,.35, .3);lamp=mat('Luminous ceiling panels',(.79,.88,1),0,.4,5);screen=mat('Ticket screens',(.025,.12,.19),.2,.15,.8);red=mat('Departure red',(.9,.07,.025),0,.5,2);green=mat('Gate indicator',(.08,.9,.18),0,.5,3)
glass=mat('Transparent partition',(.58,.75,.77),0,.12);p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.82;p.inputs['IOR'].default_value=1.45
font=bpy.data.fonts.load('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
def box(n,loc,dim,m,bev=0):
 x,y,z=[d/2 for d in dim];me=bpy.data.meshes.new(n);me.from_pydata([(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)],[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);o.location=loc;o.data.materials.append(m)
 if bev:mod=o.modifiers.new('small manufactured edge','BEVEL');mod.width=bev;mod.segments=2
 return o
def text(n,body,loc,size=.3,m=white):
 cu=bpy.data.curves.new(n,'FONT');cu.body=body;cu.font=font;cu.size=size*2.3;cu.align_x='CENTER';cu.extrude=.0006;o=bpy.data.objects.new(n,cu);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);cu.materials.append(m);return o
def rail(a,b,r=.035,m=steel):
 v=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=v.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(m);return o
def area(n,loc,power,size,target):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=n;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
# footprint proportions are photo estimates, not surveyed
box('Structural left',(-11.5,1,-.18),(5,32,.3),stone)
box('Structural right',(4,1,-.18),(20,32,.3),stone)
box('Structural middle',(-7.5,-2,-.18),(3,26,.3),stone)
for ix in range(-14,14):
 for iy in range(-15,17):
  if -9<=ix<-6 and iy>=11:continue
  box('Individual floor tile',(ix+.5,iy+.5,-.015),(.992,.992,.045),stone)
for x in [-14,14]:box('Side granite wall',(x,1,2.2),(.22,32,4.4),wall);box('Wall skirting',(x*.994,1,.12),(.13,32,.24),black)
# columns and ceiling modular seams
for x in [-10,10]:
 for y in [-7,7,15]:
  box('Granite pillar',(x,y,2.2),(.75,.75,4.4),wall,.015);box('Pillar skirting',(x,y,.12),(.79,.79,.24),black)
for ix in range(-14,14):
 for iy in range(-15,17):
  light=(ix%5==0 and iy%5==0)
  box('Ceiling light' if light else 'Ceiling panel',(ix+.5,iy+.5,4.45),(.98,.98,.06),lamp if light else ceil)
# window wall, metal frames
for x in range(-13,14,2):
 box('Back glazing',(x,16,2.5),(1.92,.055,3.1),glass)
 box('Window mullion',(x-1,16,2.5),(.065,.09,3.1),steel)
for z in [1,2.5,4.1]:box('Window horizontal mullion',(0,16,z),(28,.1,.065),steel)
# partition at y=5 with open central doors
for x in [-12,-10,-8,-6,-4,4,6,8,10,12]:
 box('Glass partition',(x,5,1.7),(1.9,.045,3.4),glass)
 for xx in [x-.97,x+.97]:box('Partition stainless jamb',(xx,5,1.7),(.055,.09,3.4),steel)
 box('Frosted privacy band',(x,5,1.35),(1.9,.05,.45),wall)
box('Partition header',(0,5,3.5),(28,.12,.12),steel)
for x in [-2.8,2.8]:
 o=box('Open glass door',(x,4.4,1.6),(1.3,.04,3.2),glass);o.rotation_euler.z=.55 if x<0 else -.55
# ticket zone left
box('Ticket counter backdrop',(-11,-2,1.7),(5,.45,3.4),wall)
for x in [-12.5,-11,-9.5]:
 box('Ticket vending body',(x,-2.45,.95),(1.15,.8,1.9),steel,.035);box('Ticket black fascia',(x,-2.87,1.25),(.94,.025,1.05),black)
 box('Touch display',(x,-2.895,1.42),(.68,.02,.42),screen)
 box('Ticket slot',(x,-2.9,.65),(.45,.03,.06),black)
 text('Ticket UI','승차권',(x,-2.92,1.45),.12)
box('Ticket sign',(-11,-2.4,3.25),(4,.16,.5),blue);text('Ticket lettering','승차권 사는 곳',(-11,-2.5,3.18),.28)
# functional circulation and doors
for x in [-5,-3,-1,1,3,5]:
 box('Ticket gate pedestal',(x,9,.52),(.36,1.5,1.04),steel,.06);box('Card reader',(x,8.45,1.07),(.25,.32,.05),black)
 box('Gate green arrow',(x,8.23,.72),(.12,.015,.14),green)
 box('Glass gate flap',(x+.58,9,.55),(.76,.045,.85),glass)
# tactile paths actual photo demonstrates T junction
for y in range(-14,10):
 for dx in [-.14,0,.14]:box('Tactile longitudinal rib',(dx,y+.5,.008),(.055,.96,.006),yellow,.015)
for x in range(-13,14):
 for dy in [-.14,0,.14]:box('Tactile cross rib',(x+.5,-5+dy,.008),(.96,.055,.006),yellow,.015)
# stairwell landing and descending flight as observed side section
# stairwell remains a true floor opening
for i in range(14):box('Descending step',(-7.5,11.2+i*.32,-.12-i*.16),(2.5,.33,.16),stone)
for x in [-9,-6]:
 rail((x,10.8,1.1),(x,15.4,-1.15))
 for i in range(7):rail((x,11+i*.64,-i*.32),(x,11+i*.64,1.1-i*.32))
# escalator references, side balustrades alongside stairs
for x in [-10.5,-4.5]:
 for i in range(14):box('Escalator tread',(x,11.2+i*.32,-.1-i*.16),(1,.32,.13),steel)
 for xx in [x-.55,x+.55]:
  rail((xx,10.8,1.05),(xx,15.5,-1.25),.09,black)
  rail((xx,10.8,.65),(xx,15.5,-1.65),.15,glass)
# photo-based wayfinding layout, no invented commercial logos
box('Main direction board',(0,4.8,3.65),(8,.22,.65),blue)
text('Main wayfinding','← 5·6   타는 곳     ① 1–4 →',(0,4.65,3.54),.32)
box('Stair direction',(-7.3,10.5,3.6),(4.3,.18,.65),blue);text('Stair sign','↑ 5·6   타는 곳',(-7.3,10.38,3.48),.32)
for x in [-6,6]:
 box('Departure display',(x,2.8,3.55),(2.4,.18,1),black)
 text('Departure title','열차 출발 안내',(x,2.68,3.78),.15,white)
 text('Display generic','운행 정보',(x,2.67,3.43),.2,red)
for x in [-12.8,12.8]:
 box('Information kiosk',(x,1,1.2),(.8,.5,2.4),blue,.03);box('Kiosk panel',(x,.73,1.35),(.65,.02,1.55),white)
 text('Kiosk information','안내',(x,.70,1.85),.25,blue)
print('GEOMETRY_DONE',flush=True)
# lighting
for x in [-9,0,9]:
 for y in [-9,0,9]:area('Soft ceiling illumination',(x,y,4.28),300,3,(x,y,0))
area('Daylight from rear',(0,15,3),1800,12,(0,0,1))
world=bpy.data.worlds.new('Interior ambient');bpy.context.scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.75,.85,1);world.node_tree.nodes['Background'].inputs[1].default_value=.18
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_x=1400;s.render.resolution_y=900;s.render.resolution_percentage=100
bpy.ops.object.camera_add(location=(1,-12,1.75));cam=bpy.context.object;cam.name='Concourse_eye_level';cam.rotation_euler=(Vector((-1,6,1.9))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=23;s.camera=cam
s['evidence']='Photo observations from 2025-03-23, three views. Dimensions and linkage estimated, not a surveyed floorplan.'
s['scene_role']='Independent public concourse reconstruction study. Do not position as surveyed inside exterior automatically.'
# convert font, pack and batch meshes by material to keep web draw calls low
for o in list(bpy.data.objects):
 if o.type=='FONT':
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
bpy.ops.object.select_all(action='DESELECT')
for m in list(bpy.data.materials):
 obs=[o for o in s.objects if o.type=='MESH' and len(o.data.materials)==1 and o.data.materials[0]==m and not o.modifiers]
 if len(obs)>1:
  for o in obs:o.select_set(True)
  bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();obs[0].name='Batch_'+m.name;bpy.ops.object.select_all(action='DESELECT')
print('BATCH_DONE',flush=True)
bpy.ops.wm.save_as_mainfile(filepath=P+'/Uijeongbu_Concourse_Study.blend',compress=True)
s.render.filepath=P+'/interior-concourse.jpg';s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=92;bpy.ops.render.render(write_still=True)
# GLB excludes lamps/cameras, retains materials
bpy.ops.export_scene.gltf(filepath=P+'/uijeongbu-concourse.glb',export_format='GLB',export_cameras=False,export_lights=False)
json.dump({'objects':len(s.objects),'mesh_objects':sum(o.type=='MESH' for o in s.objects),'missing_images':[i.filepath for i in bpy.data.images if i.source=='FILE' and not i.packed_file and not os.path.exists(bpy.path.abspath(i.filepath))],'version':bpy.app.version_string,'surveyed':False},open(P+'/validation.json','w'),indent=2)
