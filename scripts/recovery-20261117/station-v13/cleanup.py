import bpy,json
from mathutils import Vector
from pathlib import Path
R=Path('/workspace/shared/station-v13');removed={};origin=Vector((31.531,71.647,0));u=Vector((.341,.940,0)).normalized();n=Vector((u.y,-u.x,0))
for o in list(bpy.data.objects):
 if o.type!='MESH':continue
 generic=o.name.startswith('Context ') or o.name.startswith('Room glow')
 north=o.name in ['North photographed window ribbons','North window interior backs']
 if not(generic or north):continue
 me=o.data;vs=[o.matrix_world@v.co for v in me.vertices];keep=[];mids=[];count=0
 for p in me.polygons:
  ps=[vs[i] for i in p.vertices];c=sum(ps,Vector())/len(ps)
  bad=generic and -56<c.x<49 and 38<c.y<114 and 0<c.z<32
  if north and (c-origin).dot(n)>.005:bad=True
  if bad:count+=1
  else:keep.append(list(p.vertices));mids.append(p.material_index)
 if count:
  new=bpy.data.meshes.new(me.name+' historical envelope cleaned');new.from_pydata([tuple(v.co) for v in me.vertices],[],keep);new.update()
  for m in me.materials:new.materials.append(m)
  for p,i in zip(new.polygons,mids):p.material_index=i
  o.data=new;removed[o.name]=count
s=bpy.context.scene;s.render.filepath=str(R/'east-v13b-clean.png');s.cycles.samples=32
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v13b_envelope_clean.blend'),compress=True)
(R/'cleanup-validation.json').write_text(json.dumps({'removed_generic_or_outward_faces':removed,'note':'generic context window details removed only in station envelope; north strips protruding east facade removed','remaining':'east wall mass height and topology still require more validation'},indent=2))
bpy.ops.render.render(write_still=True)
