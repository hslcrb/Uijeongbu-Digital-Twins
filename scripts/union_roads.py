"""Bake non-overlapping road surfaces; run with Python + Shapely on dumped Blender faces."""
import json,sys
from pathlib import Path
from shapely.geometry import Polygon
from shapely.ops import unary_union,triangulate
root=Path(__file__).resolve().parents[1]
source=json.load(open(sys.argv[1]));groups={}
for p in source:
 if p['points'][0][2]<=0:continue
 kind='asphalt' if p['name'].startswith('Road surface ') else 'walk' if p['name'].startswith(('Walk ','Pedestrian area ')) else 'curb'
 poly=Polygon([(x,y) for x,y,z in p['points']]).buffer(0)
 if not poly.is_empty:groups.setdefault(kind,[]).append(poly)
u={k:unary_union(v) for k,v in groups.items()};u['walk']=u['walk'].difference(u['asphalt']);u['curb']=u['curb'].difference(unary_union([u['asphalt'],u['walk']]))
out=[]
for k,g in u.items():
 tris=[]
 for poly in (g.geoms if hasattr(g,'geoms') else [g]):
  for t in triangulate(poly):
   if poly.covers(t):tris.append(list(t.exterior.coords)[:-1])
 out.append({'kind':k,'z':{'asphalt':.09,'walk':.16,'curb':.08}[k],'material':'Asphalt' if k=='asphalt' else 'Concrete','triangles':tris})
(root/'data/road-surfaces-unioned.json').write_text(json.dumps(out,separators=(',',':')))
print([(o['kind'],len(o['triangles'])) for o in out])
