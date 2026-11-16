import bpy,bmesh,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=bpy.context.scene
for o in bpy.data.collections['12_Railway_Detail'].objects:
 if o.type=='MESH':
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
s.frame_set(1);s.camera=bpy.data.objects['01_East_Station_overview'];bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v1.blend'),compress=True)
exec(compile((R/'scripts/export_web.py').read_text(),str(R/'scripts/export_web.py'),'exec'))
