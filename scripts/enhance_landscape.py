"""OSM mapped grass + observed architectural lighting, intensity/plant heights inferred."""
import bpy,gzip,math,random,xml.etree.ElementTree as ET
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];random.seed(71);s=bpy.context.scene
col=bpy.data.collections.new('11_Landscape_photo_OSM');s.collection.children.link(col)
def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.82;return m
mats=[material('Grass blade '+str(i),c) for i,c in enumerate([(.11,.18,.055),(.2,.27,.08),(.07,.13,.04),(.25,.3,.12)])]
def mesh(name,vs,fs,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(mat);ob=bpy.data.objects.new(name,me);col.objects.link(ob);return ob
r=ET.parse(gzip.open(ROOT/'data/map.osm.gz','rb')).getroot();ns={n.get('id'):((float(n.get('lon'))-127.046)*111320*math.cos(math.radians(37.738)),(float(n.get('lat'))-37.738)*111320) for n in r.findall('node')}
def contains(poly,p):
 x,y=p;v=False
 for (x1,y1),(x2,y2) in zip(poly,poly[1:]+poly[:1]):
  if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1:v=not v
 return v
blades=[([],[]) for _ in mats];areas=0
for w in r.findall('way'):
 tags={t.get('k'):t.get('v') for t in w.findall('tag')}
 if tags.get('landuse')!='grass':continue
 pts=[ns[n.get('ref')] for n in w.findall('nd') if n.get('ref') in ns]
 if len(pts)<4 or not any(-265<x<355 and -225<y<335 for x,y in pts):continue
 pts=pts[:-1];areas+=1;ob=mesh('OSM grass '+w.get('id'),[(x,y,.14) for x,y in pts],[tuple(range(len(pts)))],mats[0]);ob['evidence']='OSM landuse grass; blade height and species inferred'
 x0=min(x for x,y in pts);x1=max(x for x,y in pts);y0=min(y for x,y in pts);y1=max(y for x,y in pts)
 for j in range(min(1000,int((x1-x0)*(y1-y0)*.25))):
  x=random.uniform(x0,x1);y=random.uniform(y0,y1)
  if not contains(pts,(x,y)):continue
  vs,fs=blades[j%4];h=random.uniform(.12,.35);a=random.uniform(0,6.28)
  for angle in [a,a+1.6]:
   dx=math.cos(angle)*.035;dy=math.sin(angle)*.035;o=len(vs);vs.extend([(x-dx,y-dy,.15),(x+dx,y+dy,.15),(x+dx*.8,y+dy*.8,.15+h)]);fs.append((o,o+1,o+2))
for i,(vs,fs) in enumerate(blades):mesh('Instanced-looking grass batch '+str(i),vs,fs,mats[i])
# Photo fn2025: white-blue corner fin wash, warm curved-canopy stripes and underpass lighting.
def lamp(name,typ,p,target,color,power,size=5):
 d=bpy.data.lights.new(name,typ);ob=bpy.data.objects.new(name,d);col.objects.link(ob);ob.location=p;d.color=color
 if typ=='AREA':d.shape='DISK';d.size=size;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
 for f,en in [(1,0),(120,power*.5),(240,power)]:d.energy=en;d.keyframe_insert('energy',frame=f)
 return ob
for x,y in [(49,30),(-43,20),(52,-44),(-35,-55)]:lamp('Facade cool-white wash','AREA',(x+3,y+6,34),(x,y,36),(.5,.7,1),12000,18)
for x in [-30,-15,0,15,30]:lamp('Canopy warm pool','POINT',(x,39,15),(x,39,11),(1,.65,.34),350,2)
for x in range(-90,61,20):lamp('Underpass warm lighting','POINT',(x,58+x*.08,-1),(x,58+x*.08,-5),(1,.59,.24),450,2)
# Frame240 is a photographic lighting study, not measured photometric reconstruction.
s['landscape_evidence']='OSM grass polygons; 2025 architecture night photo and 2018 park observations; intensities illustrative'
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Uijeongbu_Station_v1.blend'),compress=True)
s.frame_set(240);s.camera=bpy.data.objects['01_East_Station_overview'];s.cycles.samples=32;s.render.filepath=str(ROOT/'renders/night-landscape.png');bpy.ops.render.render(write_still=True)
print('GRASS_AREAS',areas)
