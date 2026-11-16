import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH' or o.hide_render:continue
 for p in o.data.polygons:
  pts=[o.matrix_world@o.data.vertices[i].co for i in p.vertices]
  if not pts or max(v.z for v in pts)>1.5 or min(v.z for v in pts)<-.2 or max(v.z for v in pts)-min(v.z for v in pts)>.01:continue
  if not any(-155<v.x<-35 and -20<v.y<110 for v in pts):continue
  out.append({'object':o.name,'face':p.index,'material':o.data.materials[p.material_index].name if o.data.materials else '', 'points':[[v.x,v.y,v.z] for v in pts]})
(R/'docs/west-surfaces-audit-input.json').write_text(json.dumps(out));print('SURFACES',len(out))
