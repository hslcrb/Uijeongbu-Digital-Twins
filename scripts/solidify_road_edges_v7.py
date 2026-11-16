"""Give existing mapped surfaces a physical edge, without changing their XY outline."""
import bpy,bmesh
from mathutils import Vector

def solidify_road_edges():
 report=[]
 for name in ['Union surface asphalt','Union surface walk','Union surface curb']:
  o=bpy.data.objects.get(name)
  if not o or o.get('edge_skirts_v7'):continue
  bm=bmesh.new();bm.from_mesh(o.data);before=len(bm.faces)
  bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00002)
  bad=[f for f in bm.faces if len(f.verts)<3 or f.calc_area()<1e-9]
  if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
  boundaries=[e for e in bm.edges if e.is_boundary];lower={};sides=0
  for e in boundaries:
   a,b=e.verts
   for v in (a,b):
    if v not in lower:lower[v]=bm.verts.new((v.co.x,v.co.y,.001))
   if abs(a.co.z-.001)<1e-5 and abs(b.co.z-.001)<1e-5:continue
   try:bm.faces.new((a,b,lower[b],lower[a]));sides+=1
   except ValueError:pass
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update();o['edge_skirts_v7']=True
  report.append({'surface':name,'inputFaces':before,'degenerateRemoved':len(bad),'perimeterSides':sides,'outlineChanged':False,'groundZ':.001})
 return report
