"""OSM/Mapzen coarse city terrain: source-tagged buildings, 1km batching, station exclusion."""
import bpy,json,math,gzip,xml.etree.ElementTree as ET,numpy as np
from pathlib import Path
from mathutils import Vector
import sys
sys.path.insert(0,"/workspace/shared/python-deps")
import subprocess
D=Path(__file__).parent; OUT=D/'output';OUT.mkdir(exist_ok=True)
O=(127.046,37.738);CX=111320*math.cos(math.radians(O[1]));CY=111320
xy=lambda lon,lat:((lon-O[0])*CX,(lat-O[1])*CY)
ll=lambda x,y:(x/CX+O[0],y/CY+O[1])
b=json.loads((D/'boundary-search.json').read_text())[0];ring=[xy(*v) for v in b['geojson']['coordinates'][0]]
def inside(x,y):
 c=False
 for (a,b),(d,e) in zip(ring,ring[1:]+ring[:1]):
  if (b>y)!=(e>y) and x<(d-a)*(y-b)/(e-b)+a:c=not c
 return c
raw=gzip.open(D/'N37E127.hgt.gz','rb').read();N=int(math.sqrt(len(raw)/2));H=np.frombuffer(raw,dtype='>i2').reshape(N,N)
def elev_abs(lon,lat):
 r=max(0,min(N-2,(38-lat)*(N-1)));c=max(0,min(N-2,(lon-127)*(N-1)));i,j=int(r),int(c);u,v=r-i,c-j
 return float(H[i,j]*(1-u)*(1-v)+H[i+1,j]*u*(1-v)+H[i,j+1]*(1-u)*v+H[i+1,j+1]*u*v)
Z0=elev_abs(*O)
def z(x,y):
 # preserve station local 0 datum and blend coarse terrain over 150m at its border.
 dz=elev_abs(*ll(x,y))-Z0
 dist=max(-285-x,x-375,-250-y,y-360,0)
 return dz*min(1,dist/150)
def surface(x,y):
 a=math.floor(x/80)*80;b=math.floor(y/80)*80;u=(x-a)/80;v=(y-b)/80
 h00=z(a,b);h10=z(a+80,b);h11=z(a+80,b+80);h01=z(a,b+80)
 return h00+(h10-h00)*u+(h11-h10)*v if u>=v else h00+(h11-h01)*u+(h01-h00)*v
def exclusion(x,y):return -265<x<355 and -225<y<335
nodes={};ways={}
for f in sorted((D/'osm').glob('*.osm')):
 try:
  r=ET.parse(f).getroot()
  for n in r.findall('node'):nodes[n.get('id')]=xy(float(n.get('lon')),float(n.get('lat')))
  for w in r.findall('way'):ways[w.get('id')]=w
 except Exception as e:print('SKIP',f,e)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene; buffers={};stats={'buildings':0,'height_tagged':0,'height_estimated':0,'roads':0,'terrain_cells':0}
def buf(key):return buffers.setdefault(key,[[],[]])
def face(key,pts):
 vs,fs=buf(key);i=len(vs);vs.extend(pts);fs.append(tuple(range(i,i+len(pts))))
def tag(w):return {t.get('k'):t.get('v') for t in w.findall('tag')}
def number(s,default):
 try:return float(str(s).split(';')[0].replace('m','').strip())
 except:return default
for wid,w in ways.items():
 t=tag(w);p=[nodes[n.get('ref')] for n in w.findall('nd') if n.get('ref') in nodes]
 if len(p)<2:continue
 x=sum(v[0] for v in p)/len(p);y=sum(v[1] for v in p)/len(p)
 if not inside(x,y) or exclusion(x,y):continue
 tile=(int(x//1000),int(y//1000))
 if 'building' in t and t['building'] not in ['no','roof'] and len(p)>=4 and p[0]==p[-1]:
  p=p[:-1];h=number(t.get('height'),0);lev=number(t.get('building:levels'),0)
  if h>.1:stats['height_tagged']+=1
  else:h=lev*3.1 if lev else (18 if t['building'] in ['apartments','office'] else 7.5);stats['height_estimated']+=1
  h=min(180,max(2.5,h));base=surface(x,y);key=(*tile,'buildings');face(key,[(a,b,base+h) for a,b in p])
  for a,b in zip(p,p[1:]+p[:1]):face(key,[(a[0],a[1],base),(b[0],b[1],base),(b[0],b[1],base+h),(a[0],a[1],base+h)])
  stats['buildings']+=1
 elif 'highway' in t and t['highway'] not in ['proposed','construction']:
  width={'motorway':12,'trunk':12,'primary':10,'secondary':8,'tertiary':7,'residential':5,'service':3,'footway':1.5,'path':1.2}.get(t['highway'],3)
  key=(*tile,'roads');stats['roads']+=1
  for a,b in zip(p,p[1:]):
   dx=b[0]-a[0];dy=b[1]-a[1];le=math.hypot(dx,dy)
   if le<.01:continue
   nx=-dy/le*width/2;ny=dx/le*width/2
   steps=max(1,math.ceil(le/40))
   for i in range(steps):
    q=(a[0]+dx*i/steps,a[1]+dy*i/steps);r=(a[0]+dx*(i+1)/steps,a[1]+dy*(i+1)/steps)
    if exclusion(*q):continue
    face(key,[(q[0]+nx,q[1]+ny,z(*q)+.35),(q[0]-nx,q[1]-ny,z(*q)+.35),(r[0]-nx,r[1]-ny,z(*r)+.35),(r[0]+nx,r[1]+ny,z(*r)+.35)])
# 80m ground grid, inside administrative boundary, exclude station footprint.
step=80;minx=min(p[0] for p in ring);maxx=max(p[0] for p in ring);miny=min(p[1] for p in ring);maxy=max(p[1] for p in ring)
for x in range(math.floor(minx/step)*step,math.ceil(maxx/step)*step,step):
 for y in range(math.floor(miny/step)*step,math.ceil(maxy/step)*step,step):
  if not inside(x+step/2,y+step/2) :continue
  key=(int(x//1000),int(y//1000),'terrain');face(key,[(x,y,z(x,y)),(x+step,y,z(x+step,y)),(x+step,y+step,z(x+step,y+step))]);face(key,[(x,y,z(x,y)),(x+step,y+step,z(x+step,y+step)),(x,y+step,z(x,y+step))]);stats['terrain_cells']+=1
materials={}
for n,c in [('buildings',(.58,.61,.62,1)),('roads',(.085,.10,.12,1)),('terrain',(.19,.28,.16,1))]:
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=c;m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9;materials[n]=m
# Union road surfaces externally with installed Shapely (Blender ABI differs).
road_input={str(key):[[[vs[i][0],vs[i][1]] for i in f] for f in fs] for key,(vs,fs) in buffers.items() if key[2]=='roads'}
(D/'road-input.json').write_text(json.dumps(road_input))
subprocess.run(['/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python',str(D/'union_city.py')],check=True)
for k,tris in json.loads((D/'road-union.json').read_text()).items():
 import ast
 key=ast.literal_eval(k);buffers[key]=[[],[]]
 for tri in tris:face(key,[(a,b,surface(a,b)+.65) for a,b in tri])
terrain_input={str(key):[[[vs[i][0],vs[i][1]] for i in f] for f in fs] for key,(vs,fs) in buffers.items() if key[2]=='terrain'}
(D/'terrain-input.json').write_text(json.dumps(terrain_input))
subprocess.run(['/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python',str(D/'clip_station.py')],check=True)
for k,tris in json.loads((D/'terrain-clipped.json').read_text()).items():
 key=ast.literal_eval(k);buffers[key]=[[],[]]
 for tri in tris:face(key,[(a,b,0.0 if ((abs(a+285)<1e-5 or abs(a-375)<1e-5) and -250-1e-5<=b<=360+1e-5) or ((abs(b+250)<1e-5 or abs(b-360)<1e-5) and -285-1e-5<=a<=375+1e-5) else surface(a,b)) for a,b in tri])
manifest=[]
for key,(vs,fs) in buffers.items():
 if not vs:continue
 me=bpy.data.meshes.new('city');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('city_%s_%s_%s'%key,me);scene.collection.objects.link(o);me.materials.append(materials[key[2]]);o['source']='OSM / Mapzen terrain';o['lod']='outline'
 stats['objects']=len(buffers);manifest.append({'name':o.name,'tile':list(key[:2]),'layer':key[2],'vertices':len(vs)})
scene.world.color=(.25,.25,.25);world=bpy.data.worlds.new('City sky');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.48,.62,.75,1);world.node_tree.nodes['Background'].inputs[1].default_value=.5;scene.world=world
sunD=bpy.data.lights.new('Sun','SUN');sunD.energy=3;sun=bpy.data.objects.new('Sun',sunD);scene.collection.objects.link(sun);sun.rotation_euler=(.5,-.4,-.7)
cD=bpy.data.cameras.new('City overview');c=bpy.data.objects.new('City overview',cD);scene.collection.objects.link(c);center=Vector(((minx+maxx)/2,(miny+maxy)/2,0));c.location=center+Vector((9000,-12500,14000));c.rotation_euler=(center-c.location).to_track_quat('-Z','Y').to_euler();cD.type='ORTHO';cD.ortho_scale=18000;cD.clip_end=100000;scene.camera=c
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene['source_ground_datum_m']=Z0;scene['accuracy']='OSM footprints, estimated unspecified building heights; coarse elevation terrain; outline only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Uijeongbu_City_Outline.blend'),compress=True)
(OUT/'manifest.json').write_text(json.dumps({'origin':O,'ground_reference_elevation_m':Z0,'stats':stats,'tiles':manifest,'excluded_station_xy':[-265,-225,355,335],'source':'OSM/Mapzen'},indent=2))
scene.render.filepath=str(OUT/'city-overview.png');bpy.ops.render.render(write_still=True)
print('CITY_DONE',stats)
