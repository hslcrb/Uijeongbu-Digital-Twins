import sys,json
from pathlib import Path
sys.path.insert(0,'/workspace/shared/python-deps')
from shapely.geometry import Polygon,box
from shapely.ops import unary_union,triangulate
D=Path(__file__).parent;out={}
for key,ps in json.loads((D/'road-input.json').read_text()).items():
 m=unary_union([Polygon(p).buffer(0) for p in ps]).difference(box(-265,-225,355,335));out[key]=[list(t.exterior.coords)[:-1] for t in triangulate(m) if m.covers(t)]
(D/'road-union.json').write_text(json.dumps(out))
