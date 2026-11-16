import sys,json
from pathlib import Path
sys.path.insert(0,'/workspace/shared/python-deps')
from shapely.geometry import Polygon,box
from shapely.ops import triangulate
D=Path(__file__).parent;out={}
for key,ps in json.loads((D/'terrain-input.json').read_text()).items():
 tris=[]
 for p in ps:
  poly=Polygon(p).difference(box(-285,-250,375,360))
  tris.extend([list(t.exterior.coords)[:-1] for t in triangulate(poly) if poly.covers(t)])
 out[key]=tris
(D/'terrain-clipped.json').write_text(json.dumps(out))
