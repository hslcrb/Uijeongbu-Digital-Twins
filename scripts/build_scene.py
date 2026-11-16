"""Reproducible station study. OSM footprints/parts; photo-interpreted facade detail."""
import faulthandler;faulthandler.dump_traceback_later(60, repeat=True)
import bpy, gzip, math, json, random, sys, os, xml.etree.ElementTree as ET
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];random.seed(110)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.collections):
 if d.name!='Collection':bpy.data.collections.remove(d)
scene=bpy.context.scene
COL={}
for n in ['01_Terrain','02_Roads_Rail','03_Station','04_Shinsegae','05_Context_OSM','06_Street_Detail','07_Trees_LOD0','08_Trees_LOD1','09_Lighting','10_Cameras']:
 c=bpy.data.collections.new(n);scene.collection.children.link(c);COL[n]=c
current=COL['01_Terrain']
def link(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 current.objects.link(o);return o
def mat(n,c,metal=0,rough=.6,emit=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emit:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emit
 return m
M={n:mat(n,c,me,ro,em) for n,c,me,ro,em in [('Concrete',(.48,.49,.48),0,.8,0),('Pavement',(.39,.37,.32),0,.85,0),('Asphalt',(.075,.085,.095),0,.92,0),('Metal',(.55,.60,.64),.7,.32,0),('Brown_panel',(.22,.18,.15),.25,.5,0),('Glass',(.075,.17,.21),.65,.2,0),('Dark',(.035,.045,.05),.4,.45,0),('White',(.85,.85,.8),0,.7,0),('Blue',(.015,.11,.5),.2,.35,0),('WarmLight',(1,.55,.19),0,.3,3),('Green',(.12,.22,.11),0,.9,0),('Mark',(.9,.78,.4),0,.8,0)]}
def mesh(n,vs,fs,m):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);current.objects.link(o);o.data.materials.append(m);return o
def box(n,p,s,m):
 x,y,z=p;a,b,c=[v/2 for v in s];return mesh(n,[(x+u*a,y+v*b,z+w*c) for u,v,w in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)],m)
def line(n,pts,width,m):
 cu=bpy.data.curves.new(n,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=width/2;cu.bevel_resolution=0;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for v,p in zip(sp.points,pts):v.co=(*p,1)
 o=bpy.data.objects.new(n,cu);current.objects.link(o);o.data.materials.append(m);return o
def ribbon(n,pts,w,z,m):
 vs=[]
 for i,p in enumerate(pts):
  d=Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(0,i-1)]);d.normalize();per=Vector((-d.y,d.x))*w/2;vs.extend([(p[0]+per.x,p[1]+per.y,z),(p[0]-per.x,p[1]-per.y,z)])
 return mesh(n,vs,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(pts)-1)],m)
def extrude(n,pts,z,h,m):
 if pts[0]==pts[-1]:pts=pts[:-1]
 L=len(pts);vs=[(x,y,v) for v in (z,h) for x,y in pts];fs=[tuple(range(L-1,-1,-1)),tuple(range(L,L*2))]+[(i,(i+1)%L,(i+1)%L+L,i+L) for i in range(L)]
 return mesh(n,vs,fs,m)
def beam(n,p,q,w,d,m):
 dv=Vector(q)-Vector(p);o=box(n,(Vector(p)+Vector(q))/2,(w,d,dv.length),m)
 # box vertices world based; rotate about midpoint by matrix
 mid=(Vector(p)+Vector(q))/2;R=Vector((0,0,1)).rotation_difference(dv.normalized()).to_matrix()
 for v in o.data.vertices:v.co=mid+R@(v.co-mid)
 return o
font=bpy.data.fonts.load(str(ROOT/'assets/station-labels.otf'))
def text(n,txt,p,size,m,rot=(math.pi/2,0,0)):
 cu=bpy.data.curves.new(n,'FONT');cu.body=txt;cu.size=size;cu.align_x='CENTER';cu.extrude=.025
 if font:cu.font=font
 o=bpy.data.objects.new(n,cu);current.objects.link(o);o.location=p;o.rotation_euler=rot;o.data.materials.append(m);return o
# Geographical mapping: x East, y North. Geometry from OSM, not a cadastral survey.
origin=(127.046,37.738)
def xy(lon,lat):return ((lon-origin[0])*111320*math.cos(math.radians(origin[1])),(lat-origin[1])*111320)
r=ET.parse(gzip.open(ROOT/'data/map.osm.gz','rb')).getroot();nodes={e.get('id'):xy(float(e.get('lon')),float(e.get('lat'))) for e in r.findall('node')}
ways={e.get('id'):e for e in r.findall('way')}
def tags(e):return {t.get('k'):t.get('v') for t in e.findall('tag')}
def coords(w):return [nodes[n.get('ref')] for n in w.findall('nd') if n.get('ref') in nodes]
def inside(p):return -265<p[0]<355 and -225<p[1]<335
stationparts=set();mallparts=set();outlines=set()
for e in r.findall('relation'):
 if e.get('id') in ('17978072','17978074'):
  dst=stationparts if e.get('id')=='17978072' else mallparts
  for a in e.findall('member'):
   (outlines if a.get('role')=='outline' else dst).add(a.get('ref'))
box('Study area / not surveyed terrain',(45,55,-.6),(660,610,1.2),M['Pavement'])
# Ground is intentionally a flat reference datum, not invented terrain survey.
current=COL['02_Roads_Rail']; roadpaths=[]
for id,w in ways.items():
 t=tags(w);pts=coords(w)
 pts=[p for p in pts if inside(p)]
 if len(pts)<2 or not any(inside(p) for p in pts) or t.get('indoor')=='yes' or t.get('tunnel') in ('yes','building_passage'):continue
 if t.get('railway') in ('rail','light_rail'):
  z=7 if t.get('railway')=='light_rail' else .1
  ribbon('Track ballast '+id,pts,3.3,z,M['Dark'])
  for off in [-.72,.72]:line('Rail '+id,[(p[0]+off,p[1],z+.13) for p in pts],.13,M['Metal'])
 elif t.get('highway'):
  typ=t['highway'];width={'secondary':20,'secondary_link':7,'tertiary':12,'residential':7,'service':4,'footway':2.2,'pedestrian':13,'living_street':6,'steps':3}.get(typ)
  if not width:continue
  try:width=float(t.get('width',width))
  except:pass
  z=.045 if width>3 else .08
  if typ in ('footway','steps','pedestrian'):
   ribbon('Walk '+id,pts,width,z,M['Concrete'])
  else:
   ribbon('Road '+id,pts,width+.8,z-.02,M['Concrete']);ribbon('Road surface '+id,pts,width,z,M['Asphalt']);roadpaths.append((pts,width))
   if width>=10:
    for a,b in zip(pts,pts[1:]):
     dv=Vector(b)-Vector(a);L=dv.length
     if L>400:continue
     for k in range(0,int(L),8):
      p=Vector(a)+dv.normalized()*k;q=Vector(a)+dv.normalized()*min(k+3,L);line('Lane dash',[(p.x,p.y,.07),(q.x,q.y,.07)],.13,M['White'])
# Buildings and photo-guided detailed facade modules.
counts={'osm_buildings':0,'station_parts':0,'mall_parts':0,'estimated_heights':0}; detailed=[]
for id,w in ways.items():
 t=tags(w);pts=coords(w)
 if len(pts)<4 or pts[0]!=pts[-1] or id in outlines:continue
 if not (t.get('building') or t.get('building:part') or id in mallparts|stationparts):continue
 center=Vector((sum(p[0] for p in pts)/len(pts),sum(p[1] for p in pts)/len(pts)))
 if not inside(center):continue
 if id=='1364007203':continue # outline height 0.01 is invalid; use mapped station parts
 try:h=float(t.get('height','0'))
 except:h=0
 estimated=h<2
 if estimated:
  try:h=float(t.get('building:levels','3'))*3.3
  except:h=10
  counts['estimated_heights']+=1
 z=float(t.get('min_height','0'));h=max(z+.3,h)
 if id in mallparts:current=COL['04_Shinsegae'];m=M['Brown_panel'] if id=='608705745' else M['Concrete'];counts['mall_parts']+=1
 elif id in stationparts:current=COL['03_Station'];m=M['Glass'] if id in ('1311394048','1311394063') else M['Concrete'];counts['station_parts']+=1
 else:current=COL['05_Context_OSM'];m=mat('Facade '+id,random.choice([(.46,.43,.38),(.57,.57,.52),(.3,.29,.27),(.65,.59,.49),(.45,.48,.48)]));counts['osm_buildings']+=1
 o=extrude((t.get('name') or 'OSM building')+' ['+id+']',pts,z,h,m);o['osm_way_id']=id;o['height_evidence']='estimated from levels or default' if estimated else 'OSM height tag, unverified survey';o['height_m']=h
 near=center.length<210
 if id in mallparts|stationparts or near:
  for ei,(a,b) in enumerate(zip(pts,pts[1:])):
   d=Vector(b)-Vector(a);L=d.length
   if L<3:continue
   dn=d.normalized();normal=Vector((dn.y,-dn.x));a=Vector(a)
   # stand-off fins are photo-based, individual dimensions estimated.
   if id=='608705745':
    for u in range(int(L/.85)):
     if .24*L<u*.85<.76*L:continue
     p=a+dn*(u*.85)+normal*.28;beam('Mall silver fin',(p.x,p.y,9),(p.x,p.y,h-3),.22,.65,M['Metal'])
    # panel joints on closed walls
    for level in range(12,int(h),5):line('Panel seam',[(a.x,a.y,level),(b[0],b[1],level)],.06,M['Dark'])
   elif id in mallparts:
    for level in range(max(12,int(z+2)),int(h-2),5):line('Parking window band',[(a.x+normal.x*.12,a.y+normal.y*.12,level),(b[0]+normal.x*.12,b[1]+normal.y*.12,level)],1.6,M['Glass'])
    for u in range(0,int(L),3):
     p=a+dn*u+normal*.2;beam('Parking fin',(p.x,p.y,max(z,10)),(p.x,p.y,h),.16,.3,M['Metal'])
   elif id in stationparts:
    for u in range(0,int(L),3):
     p=a+dn*u+normal*.15;beam('Station mullion',(p.x,p.y,z),(p.x,p.y,h),.12,.16,M['Metal'])
   elif L<80 and h<85:
    for floor in range(2,int(h-1),4):
     for u in range(2,int(L-1),4):
      p=a+dn*u+normal*.05; q=p+dn*2.5;beam('Context window',(p.x,p.y,floor),(q.x,q.y,floor),1.65,.09,M['Glass'])
# Readable signs: photographed permanent station/department store names only.
current=COL['03_Station']
box('Station name backing',(1,112.3,29),(30,.3,4.4),M['White']);text('의정부역 sign','의정부역',(1,112.55,28),3.4,M['Blue'],(math.pi/2,0,math.pi))
text('Station English','UIJEONGBU STATION',(1,112.6,26.9),.8,M['Blue'],(math.pi/2,0,math.pi))
current=COL['04_Shinsegae'];text('Department store name','신세계',(38,25.9,57),4,M['White'],(math.pi/2,0,math.pi));text('SHINSEGAE','SHINSEGAE',(1,26.5,10),2,M['WarmLight'],(math.pi/2,0,math.pi))
# Stylized permanent flower sign, not a claimed exact vector asset.
for a in range(8):
 an=a*math.pi/4;o=box('Flower petal',(38+2*math.cos(an),26,64+2*math.sin(an)),(1.25,.25,2.2),M['WarmLight']);o.rotation_euler.y=-an
# Plaza between mall north and station south. Curved canopy mesh based on Haeahn photos.
current=COL['03_Station']
for side in [-1,1]:
 vs=[]
 for i in range(25):
  t=i/24; x=-44+t*90; y=39+3*math.sin(t*math.pi);z=18+1.5*math.sin(t*math.pi)
  vs.extend([(x,y+side*2,z),(x,y+side*7,z+.8)])
 mesh('Curved plaza canopy',vs,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(24)],M['Metal'])
for x in [-40,-25,-10,5,20,35]:beam('Canopy support',(x,39,8),(x,39,18),.35,.35,M['Metal'])
for side in [-1,1]:
 x=side*54
 for i in range(28):box('Plaza stair',(x,45+i*.38,.15+i*.25),(9,.38,.3+i*.5),M['Concrete'])
 line('Stair handrail',[(x-4.5,45,1),(x-4.5,55.5,8)],.08,M['Metal'])
# South parking ramp, approximate photo-interpreted shape, independent supports.
current=COL['04_Shinsegae'];pts=[]
for i in range(65):
 t=i/64;angle=math.pi+t*math.pi;pts.append((5+48*math.cos(angle),-175+23*math.sin(angle),2+t*9))
for off in [-4.2,4.2]:line('Ramp parapet',[(x,y+off,z+.6) for x,y,z in pts],.55,M['Concrete'])
# 3D ramp surface and curved roof
vs=[]
for x,y,z in pts:vs.extend([(x,y-4,z),(x,y+4,z)])
mesh('Parking ramp deck',vs,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(64)],M['Asphalt'])
for i in range(0,65,8):
 x,y,z=pts[i];beam('Ramp pier',(x,y,0),(x,y,z),.7,.7,M['Concrete'])
for j in range(9):
 off=-4+j;line('Ramp roof ribbon',[(x,y+off,z+3+1.2*math.sqrt(max(0,1-(off/4)**2))) for x,y,z in pts],.14,M['Metal'])
# Street furniture based on observed type, positions are illustrative unless OSM mapped.
current=COL['06_Street_Detail']
for x in [-58,70]:
 for y in range(-150,130,22):
  beam('Street lamp',(x,y,.2),(x,y,6.5),.14,.14,M['Metal']);line('Lamp arm',[(x,y,6.5),(x+2,y,7)],.12,M['Metal']);box('Luminaire',(x+2,y,7),(.9,.35,.13),M['WarmLight'])
for y in range(28,38,3):
 for x in range(-42,46,4):box('Plaza tile seam',(x,y,.105),(3.9,.025,.02),M['Dark'])
# OSM tree positions plus documented illustrative plaza planting.
current=COL['07_Trees_LOD0']
with bpy.data.libraries.load(str(ROOT/'assets/trees.blend'),link=False) as (a,b):b.objects=[n for n in a.objects if 'LOD' in n]
protos={o.name:o for o in b.objects if o}
positions=[]
for n in r.findall('node'):
 if tags(n).get('natural')=='tree' and inside(nodes[n.get('id')]):positions.append((*nodes[n.get('id')],True))
positions += [(x,y,False) for x in [-61,73] for y in range(-145,145,16)]
for i,(x,y,mapped) in enumerate(positions):
 species=['Ginkgo_Autumn','Maple_Autumn','Pine_Evergreen'][i%3]
 for lod in [0,1]:
  current=COL['07_Trees_LOD0' if lod==0 else '08_Trees_LOD1'];p=protos[species+'_LOD'+str(lod)];o=bpy.data.objects.new(species+' instance',p.data);current.objects.link(o);o.location=(x,y,0);o.rotation_euler.z=random.random()*6.28;o.scale=(.8+i%4*.08,)*3;o.hide_render=False;o['placement']='OSM tree point' if mapped else 'illustrative street planting, unmeasured'
# Actual downloaded CC0 asset, explicitly a non-native landscaping approximation.
with bpy.data.libraries.load(str(ROOT/'assets/polyhaven-tree-small02-seasonal.blend'),link=False) as (a,b):b.objects=[n for n in a.objects if n=='PH_TreeSmall02_Autumn_LOD2']
ph=b.objects[0]
for i,y in enumerate(range(-110,115,20)):
 o=ph.copy();o.data=ph.data;COL['07_Trees_LOD0'].objects.link(o);o.location=(77,y,.1);o.rotation_euler.z=i*.7;o.hide_render=False;o.hide_set(False);o['placement']='Illustrative; Poly Haven CC0 Burkea africana is not verified local species'
COL['08_Trees_LOD1'].hide_render=True;COL['08_Trees_LOD1'].hide_viewport=True
# Batch repeated facade modules by collection/material while preserving OSM source objects.
for cn in ['03_Station','04_Shinsegae','05_Context_OSM','06_Street_Detail']:
 groups={}
 for o in list(COL[cn].objects):
  if o.type=='MESH' and 'osm_way_id' not in o and not o.name.startswith('OSM'):
   groups.setdefault(tuple(m.name for m in o.data.materials),[]).append(o)
 for key,obs in groups.items():
  if len(obs)<2:continue
  vs=[];fs=[]
  for o in obs:
   off=len(vs);vs.extend([tuple(o.matrix_world@v.co) for v in o.data.vertices]);fs.extend([tuple(off+j for j in f.vertices) for f in o.data.polygons])
  current=COL[cn];combined=mesh('Batched '+cn+' '+','.join(key),vs,fs,obs[0].data.materials[0])
  for o in obs:bpy.data.objects.remove(o,do_unlink=True)
for _ in range(2):bpy.data.orphans_purge(do_recursive=True)

print('BATCHED',len(bpy.context.scene.objects),flush=True)
# World controls and keyframes. Saved scene gives editable sun/night animation.
current=COL['09_Lighting'];world=bpy.data.worlds.new('UIJEONGBU Sky system');scene.world=world;world.use_nodes=True;nt=world.node_tree;nt.nodes.clear();sky=nt.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING' if bpy.app.version >= (5,0,0) else 'NISHITA';sky.sun_disc=True;sky.sun_rotation=2.4;sky.altitude=.05;bg=nt.nodes.new('ShaderNodeBackground');out=nt.nodes.new('ShaderNodeOutputWorld');nt.links.new(sky.outputs['Color'],bg.inputs[0]);nt.links.new(bg.outputs[0],out.inputs[0])
for frame,elev,power in [(1,38,.04),(120,7,.03),(240,-6,.008)]:
 sky.sun_elevation=math.radians(elev);sky.keyframe_insert('sun_elevation',frame=frame);bg.inputs[1].default_value=power;bg.inputs[1].keyframe_insert('default_value',frame=frame)
bpy.ops.object.light_add(type='SUN',location=(0,0,120));sun=link(bpy.context.object);sun.name='Sun / day dusk night';sun.data.angle=.06
for f,en,rot in [(1,2,(.45,-.5,-.4)),(120,.5,(1.35,-.2,-.4)),(240,0,(1.7,0,0))]:sun.data.energy=en;sun.data.keyframe_insert('energy',frame=f);sun.rotation_euler=rot;sun.keyframe_insert('rotation_euler',frame=f)
for p in [(0,30,24),(60,-20,22),(-50,55,18),(65,-105,20)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=link(bpy.context.object);o.data.color=(1,.64,.34);o.data.shape='DISK';o.data.size=30
 for f,en in [(1,0),(120,1800),(240,5500)]:o.data.energy=en;o.data.keyframe_insert('energy',frame=f)
current=COL['10_Cameras']
def camera(n,p,target,lens):
 bpy.ops.object.camera_add(location=p);c=link(bpy.context.object);c.name=n;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=lens;c.data.clip_end=3000;return c
cam=camera('01_East_Station_overview',(275,305,175),(5,-10,20),42);camera('02_Plaza_eye_level',(85,135,20),(5,35,28),30);camera('03_Parking_ramp',(160,-290,90),(0,-85,24),40);scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.resolution_x=1440;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX';scene.view_settings.exposure=-.8;scene.frame_end=240;scene.frame_set(1)
scene['README']='OSM-driven exterior study; photographic facade interpretation. Not a surveyed or fully photoreal final twin. See docs.'
scene['LOD']='Disable 07_Trees_LOD0 and enable 08_Trees_LOD1 for far/interactive view.'
scene['Origin_lon_lat']='127.046,37.738';scene['Sky_presets']='frame 1 day /120 dusk /240 night'
# Pack Korean font so signs survive transfer.
if font:font.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Uijeongbu_Station_v1.blend'),compress=True)
counts.update(objects=len(scene.objects),mesh_datablocks=len(bpy.data.meshes),tree_instances=len(positions),unique_tree_meshes=6,vertices=sum(len(m.vertices) for m in bpy.data.meshes),polygons=sum(len(m.polygons) for m in bpy.data.meshes))
(ROOT/'docs/model-stats.json').write_text(json.dumps(counts,indent=2))
scene.render.filepath=str(ROOT/'renders/day-overview.png');bpy.ops.render.render(write_still=True)
scene.frame_set(240);scene.render.filepath=str(ROOT/'renders/night-overview.png');bpy.ops.render.render(write_still=True)
scene.frame_set(1);scene.camera=bpy.data.objects['02_Plaza_eye_level'];scene.render.filepath=str(ROOT/'renders/plaza.png');bpy.ops.render.render(write_still=True)
