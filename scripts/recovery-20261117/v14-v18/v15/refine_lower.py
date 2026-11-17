import bpy,json,math
from mathutils import Vector
from pathlib import Path
R=Path('recovery-output/v15')
def mat(name,col,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.5;return m
stone=mat('v15 muted concrete',(.32,.34,.34));steel=mat('v15 satin railing',(.34,.37,.39),.7);dark=mat('v15 recessed arcade wall',(.035,.045,.05));removed={}
# Remove generic transportation facade only within north segment.
o=bpy.data.objects['OSM building [1334917247]'];me=o.data;fs=[];mids=[];vs=[]
for p in me.polygons:
 poly=[me.vertices[i].co.copy() for i in p.vertices];out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ina=a.y<=80;inb=b.y<=80
  if ina:out.append(a)
  if ina!=inb:out.append(a+(b-a)*((80-a.y)/(b.y-a.y)))
 if len(out)<3:continue
 j=len(vs);vs.extend([tuple(v) for v in out]);fs.append(tuple(range(j,j+len(out))));mids.append(p.material_index)
new=bpy.data.meshes.new('v15 south legacy clipped at north segment');new.from_pydata(vs,[],fs);new.update()
for m in me.materials:new.materials.append(m)
for p,i in zip(new.polygons,mids):p.material_index=i
removed[o.name]=len(me.polygons)-len(fs);o.data=new
# Nearby generic glazing within replaced footprint only.
for o in list(bpy.data.objects):
 if not(o.type=='MESH' and (o.name.startswith('Context ') or o.name.startswith('Room glow'))):continue
 me=o.data;fs=[];mi=[]
 for p in me.polygons:
  c=o.matrix_world@p.center
  if 21<c.x<36 and 80<c.y<111 and c.z<11.1:continue
  fs.append(list(p.vertices));mi.append(p.material_index)
 if len(fs)==len(me.polygons):continue
 new=bpy.data.meshes.new('v15 generic local cleanup');new.from_pydata([tuple(v.co) for v in me.vertices],[],fs);new.update()
 for m in me.materials:new.materials.append(m)
 for p,i in zip(new.polygons,mi):p.material_index=i
 removed[o.name]=len(me.polygons)-len(fs);o.data=new
parts=[]
def box(name,loc,scale,material,angle=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;o.rotation_euler.z=angle;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);parts.append(o);return o
A=Vector((35.1255,81.6755,0));B=Vector((31.7802,110.3404,0));d=(B-A).normalized();L=(B-A).length;n=Vector((d.y,-d.x,0));ang=math.atan2(d.y,d.x)
# Slab using original curved-approach level 5.5m, not measured.
box('v15 sheltered lower backing',tuple((A+B)/2-n*8.5+Vector((0,0,2.0))),(L,.20,4.0),dark,ang)
for i in range(7):
 p=A+d*(L*i/6)
 box('v15 open arcade pier',tuple(p-n*.7+Vector((0,0,2.0))),(.7,.7,4.0),stone,ang)
box('v15 recessed upper passage backing',tuple((A+B)/2-n*3.5+Vector((0,0,8.75))),(L,.15,6.5),dark,ang)
# terrace railing: visible thin horizontal rails and balusters rather than window storeys.
for z in [5.75,6.25,6.65]:box('v15 terrace handrail',tuple((A+B)/2+Vector((0,0,z))),(L,.055,.055),steel,ang)
for i in range(97):
 p=A+d*(L*i/96);box('v15 terrace baluster',tuple(p+Vector((0,0,6.1))),(.035,.035,1.1),steel)
# one batched object per material, reducing draw calls.
groups=[(m,[o for o in parts if o.data.materials[0]==m]) for m in [stone,dark,steel]]
for material,obs in groups:
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();obs[0].name='v15 arcade '+material.name
s=bpy.context.scene;s.render.filepath=str(R/'east-v15.png');s.cycles.samples=32
(R/'validation.json').write_text(json.dumps({'removed_faces':removed,'source_osm':'way1334917247 transportation height11 layer-1','new_elements':'local open lower arcade, recessed upper passage backing, thin terrace railings; existing slab retained','all_dimensions':'estimated from existing relative levels, not measured'},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v15_lower_arcade.blend'),compress=True);bpy.ops.render.render(write_still=True)
