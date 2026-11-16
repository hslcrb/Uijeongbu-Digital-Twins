"""Remove geometrically identical road faces only, preserving every unique outline."""
import bpy,bmesh,json
from pathlib import Path

def deduplicate():
 report=[]
 for o in bpy.data.objects:
  if o.type!='MESH' or not o.name.startswith('Union surface'):continue
  bm=bmesh.new();bm.from_mesh(o.data);seen=set();duplicates=[]
  for f in bm.faces:
   key=tuple(sorted(tuple(round(c,5) for c in o.matrix_world@v.co) for v in f.verts))
   if key in seen:duplicates.append(f)
   else:seen.add(key)
  if duplicates:
   report.append({'object':o.name,'removedFaces':len(duplicates),'area_m2':sum(f.calc_area() for f in duplicates)})
   bmesh.ops.delete(bm,geom=duplicates,context='FACES_ONLY');bm.to_mesh(o.data);o.data.update()
  bm.free()
 return report

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1]
 report=deduplicate();(root/'docs/v7-skirt-deduplication.json').write_text(json.dumps(report,indent=2));print(report)
 bpy.ops.wm.save_as_mainfile(filepath=str(root/'Uijeongbu_Station_v1.blend'),compress=True)
 exec(compile((root/'scripts/export_web.py').read_text(),str(root/'scripts/export_web.py'),'exec'))
