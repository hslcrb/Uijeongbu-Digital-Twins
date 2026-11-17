import bpy,json,math
from mathutils import Vector
from pathlib import Path
R=Path('recovery-output/v18');o=bpy.data.objects['OSM building [1334917247]']
# Reuse v13c footprint, already mapped south of north arcade transition.
poly=[Vector((x,y,0)) for x,y in [(22.3782,109.32737),(25.46819,80.707),(30.565348,24.479267),(32.554913,24.679644),(29.103987,65.255783),(35.1255,81.675484),(31.780214,110.340385)]]
out=[]
for a,b in zip(poly,poly[1:]+poly[:1]):
 if a.y<=80:out.append(a)
 if (a.y<=80)!=(b.y<=80):out.append(a+(b-a)*((80-a.y)/(b.y-a.y)))
poly=out;originalfaces=len(o.data.polygons);bpy.data.objects.remove(o,do_unlink=True)
stone=bpy.data.materials.get('v15 muted concrete');glass=bpy.data.materials.new('v18 south circulation continuous glazing');glass.diffuse_color=(.055,.115,.13,1);glass.use_nodes=True;p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.055,.115,.13,1);p.inputs['Metallic'].default_value=.35;p.inputs['Roughness'].default_value=.24
metal=bpy.data.materials.get('v15 satin railing');verts={};faces={}
def quad(name,pts):
 v=verts.setdefault(name,[]);f=faces.setdefault(name,[]);j=len(v);v.extend([tuple(p) for p in pts]);f.append(tuple(range(j,j+len(pts))))
for a,b in zip(poly,poly[1:]+poly[:1]):
 for z0,z1,kind in [(0,1.05,'stone'),(1.05,3.75,'glass'),(3.75,5.5,'stone'),(5.5,6.15,'stone'),(6.15,9.1,'glass'),(9.1,11,'stone')]:
  quad(kind,[a+Vector((0,0,z0)),b+Vector((0,0,z0)),b+Vector((0,0,z1)),a+Vector((0,0,z1))])
 # slim vertical glazing mullions, not full-height generic concrete piers
 d=b-a;L=d.length;u=d.normalized();n=Vector((u.y,-u.x,0));cnt=max(1,math.ceil(L/2.2))
 for i in range(cnt+1):
  c=a+d*(i/cnt)+n*.025
  for z0,z1 in [(1.05,3.75),(6.15,9.1)]:
   quad('metal',[c-u*.035+Vector((0,0,z0)),c+u*.035+Vector((0,0,z0)),c+u*.035+Vector((0,0,z1)),c-u*.035+Vector((0,0,z1))])
quad('stone',[p+Vector((0,0,11)) for p in poly])
for name,m in [('stone',stone),('glass',glass),('metal',metal)]:
 me=bpy.data.meshes.new('v18 south ribbon '+name);me.from_pydata(verts[name],[],faces[name]);me.update();ob=bpy.data.objects.new('v18 south circulation '+name,me);bpy.context.collection.objects.link(ob);me.materials.append(m)
(R/'validation.json').write_text(json.dumps({'removed_south_generic_faces':originalfaces,'new_faces':{k:len(v) for k,v in faces.items()},'source':'2026-06-23 field photo14 of hhk2001.tistory.com/8063','preserved':'footprint, total relative height11, terrace level5.5, v15 north arcade','assumptions':'band heights and mullion spacing are approximations; not measured as-built dimensions'},indent=2))
s=bpy.context.scene;s.render.filepath=str(R/'east-v18.png');s.cycles.samples=32;bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v18_south_ribbons.blend'),compress=True);bpy.ops.render.render(write_still=True);s.camera=bpy.data.objects['v17 East street-level comparison'];s.render.filepath=str(R/'east-street-v18.png');bpy.ops.render.render(write_still=True)
