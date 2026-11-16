import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/shared/west-v12')
def mat(n,c,metal=0,rough=.5):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
blue=mat('v12 pylon cobalt blue',(.016,.045,.26));white=mat('v12 sign white',(.91,.93,.92));steel=mat('v12 pylon silver sides',(.36,.39,.4),.7);stone=mat('v12 pylon grey plinth',(.14,.16,.17),0,.8)
def box(n,pos,size,m):
 x,y,z=pos;a,b,c=[v/2 for v in size];vs=[(x+dx*a,y+dy*b,z+dz*c) for dx,dy,dz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]];fs=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);o.data.materials.append(m);return o
# Reference shows tall freestanding pylon between approach pavement and road.
# Position/height estimated within the existing model, not geospatially surveyed.
x,y=-98,27
box('v12 station pylon plinth',(x,y,1.25),(1.15,.60,2.5),stone)
box('v12 station pylon silver housing',(x,y,5.4),(1.10,.52,6.2),steel)
box('v12 station pylon blue face',(x,y-.269,5.45),(1.02,.018,5.9),blue)
font=bpy.data.fonts.load('/workspace/shared/korail-font/KORAIL-old.ttf')
def text(n,body,z,size,font=None):
 cu=bpy.data.curves.new(n,'FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.extrude=.001
 if font:cu.font=font
 ob=bpy.data.objects.new(n,cu);bpy.context.collection.objects.link(ob);ob.location=(x,y-.285,z);ob.rotation_euler=(math.pi/2,0,0);cu.materials.append(white);return ob
objs=[]
for ch,z in zip('의정부역',[7.35,6.35,5.35,4.35]):objs.append(text('v12 pylon Korail '+ch,ch,z,.85,font))
objs.append(text('v12 pylon English','Uijeongbu',3.68,.17));objs.append(text('v12 pylon station label','Station',3.42,.17));objs.append(text('v12 pylon header','KORAIL',8.18,.20))
for o in objs:
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
if font.users==0:bpy.data.fonts.remove(font)
# Preserve all canopy members; neutral optical glass reveals structure.
m=bpy.data.materials['West clear canopy glass'];p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.88,.96,.93,1);p.inputs['Transmission Weight'].default_value=1;p.inputs['Roughness'].default_value=.055;p.inputs['IOR'].default_value=1.45
for n in ['West photographed pale celadon steel','West photo cylindrical pale steel']:
 m=bpy.data.materials[n];p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.65,.70,.64,1);p.inputs['Roughness'].default_value=.33
s=bpy.context.scene;s.camera=bpy.data.objects['v7 west comparison'];s.cycles.samples=40;s.cycles.use_denoising=True;s.cycles.transmission_bounces=12;s.render.filepath=str(R/'west-v12-day.png')
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v12_west_pylon.blend'),compress=True)
(R/'validation.json').write_text(json.dumps({'source':'https://hhk2001.tistory.com/8063','observed':['blue vertical station pylon','pale steel canopy','glass reveals structure'],'estimated':['pylon position -98,27','pylon height8.5m','optical parameters'],'objects':len(bpy.data.objects),'deployment':'not deployed'},ensure_ascii=False,indent=2))
bpy.ops.render.render(write_still=True)
