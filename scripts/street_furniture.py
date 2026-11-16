"""Mapped signal anchors; road-aligned street furniture with explicit inferred placements."""
import bpy,math,gzip,json,xml.etree.ElementTree as ET
from pathlib import Path
from mathutils import Vector

def add_street_furniture(root):
 root=Path(root);s=bpy.context.scene
 name='16_Street_furniture_OSM'
 col=bpy.data.collections.get(name)
 if col:
  bpy.data.batch_remove(list(col.objects));bpy.data.collections.remove(col)
 col=bpy.data.collections.new(name);s.collection.children.link(col)
 mats={}; batches={}
 def mat(n,c,metal=0,emit=0):
  m=bpy.data.materials.get('Street '+n) or bpy.data.materials.new('Street '+n);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.55
  p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emit;mats[n]=m;batches[n]=[[],[]];return m
 for n,c,metal,emit in [('steel',(.18,.21,.22),.65,0),('black',(.018,.02,.019),.15,0),('blue',(.015,.12,.38),.2,0),('white',(.8,.85,.85),.1,0),('red',(.8,.025,.012),0,2),('amber',(.1,.055,.01),0,0),('green',(.01,.12,.045),0,0),('lamp',(1,.72,.43),0,4),('stone',(.27,.28,.26),0,0)]:mat(n,c,metal,emit)
 for f,v in [(1,.05),(120,2),(240,5)]:mats['lamp'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=v;mats['lamp'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].keyframe_insert(data_path='default_value',frame=f)
 def box(p,size,m,angle=0):
  vs,fs=batches[m];i=len(vs);c=math.cos(angle);sn=math.sin(angle);a,b,d=[x/2 for x in size]
  for x,y,z in [(-a,-b,-d),(-a,-b,d),(-a,b,-d),(-a,b,d),(a,-b,-d),(a,-b,d),(a,b,-d),(a,b,d)]:vs.append((p[0]+x*c-y*sn,p[1]+x*sn+y*c,p[2]+z))
  fs.extend(tuple(i+j for j in face) for face in [(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)])
 def rod(a,b,r,m):
  a,b=Vector(a),Vector(b);d=(b-a).normalized();u=d.cross(Vector((0,0,1)))
  if u.length<.01:u=d.cross(Vector((0,1,0)))
  u.normalize();v=d.cross(u);vs,fs=batches[m];i=len(vs);N=8
  for p in [a,b]:
   for j in range(N):vs.append(tuple(p+r*(u*math.cos(j*2*math.pi/N)+v*math.sin(j*2*math.pi/N))))
  fs.extend([tuple(i+j for j in range(N-1,-1,-1)),tuple(i+N+j for j in range(N))]);fs.extend((i+j,i+(j+1)%N,i+(j+1)%N+N,i+j+N) for j in range(N))
 r=ET.parse(gzip.open(root/'data/map.osm.gz','rb')).getroot()
 def tags(e):return {x.get('k'):x.get('v') for x in e.findall('tag')}
 def xy(n):return ((float(n.get('lon'))-127.046)*111320*math.cos(math.radians(37.738)),(float(n.get('lat'))-37.738)*111320)
 ns={n.get('id'):xy(n) for n in r.findall('node')};roads=[]
 def inside(p):return -265<p[0]<355 and -225<p[1]<335
 for w in r.findall('way'):
  t=tags(w)
  if t.get('highway') not in ['primary','secondary','tertiary','residential','unclassified'] or t.get('tunnel')=='yes' or t.get('bridge')=='yes' or t.get('cutting')=='yes':continue
  ps=[ns[n.get('ref')] for n in w.findall('nd') if n.get('ref') in ns]
  width={'primary':17,'secondary':13,'tertiary':10,'residential':7,'unclassified':7}[t['highway']]
  for a,b in zip(ps,ps[1:]):
   if inside(a) and inside(b) and math.dist(a,b)>2:roads.append((a,b,t.get('name',''),width,w.get('id')))
 def near(p):
  choices=[]
  for a,b,n,w,id in roads:
   a,b=Vector(a),Vector(b);d=b-a;q=a+d*max(0,min(1,(Vector(p)-a).dot(d)/d.length_squared));choices.append(((Vector(p)-q).length,math.atan2(d.y,d.x),n,w,id))
  return min(choices)
 report={'mapped_signal_nodes':[],'signal_crossing_nodes':[],'road_names':[],'lamp_positions_inferred':[],'tree_grate_nodes':[]}
 # Two explicit signal poles in map have 6m height. Crossing anchors use proxy geometry at map node.
 for n in r.findall('node'):
  t=tags(n);p=xy(n)
  if not inside(p):continue
  sig=t.get('highway')=='traffic_signals';cross=t.get('crossing')=='traffic_signals' or t.get('crossing:signals')=='yes'
  if not(sig or cross):continue
  dist,ang,nm,w,wid=near(p);x,y=p;H=float(t.get('height',6)) if sig else 3.1
  rod((x,y,.16),(x,y,H),'0' if False else .095,'steel');box((x,y,.33),(.32,.32,.34),'steel')
  # Signal lens separation is 7cm from housing plane, not coplanar.
  if sig:
   d=Vector((math.cos(ang+math.pi/2),math.sin(ang+math.pi/2)));end=Vector(p)+d*3.4;rod((x,y,H),(*end,H),.07,'steel');center=Vector(p)+d*2.7
   box((*center,H-.3),(1.35,.25,.45),'black',ang)
   for j,key in enumerate(['red','amber','green']):
    pos=center+Vector((math.cos(ang),math.sin(ang)))*((j-1)*.42);normal=Vector((math.sin(ang),-math.cos(ang)));rod((*pos+normal*.14,H-.3),(*pos+normal*.22,H-.3),.145,key)
   report['mapped_signal_nodes'].append(n.get('id'))
  else:
   box((x,y,2.45),(.32,.24,.64),'black',ang)
   normal=Vector((math.sin(ang),-math.cos(ang)))
   box((x+normal.x*.15,y+normal.y*.15,2.6),(.16,.04,.16),'red',ang)
   box((x+normal.x*.15,y+normal.y*.15,2.29),(.16,.04,.16),'green',ang)
   report['signal_crossing_nodes'].append(n.get('id'))
 # Actual mapped streetlamp anchors; photographic typology, not surveyed dimensions.
 report['mapped_lamp_nodes']=[]
 for n in r.findall('node'):
  t=tags(n);p=xy(n)
  if t.get('highway')!='street_lamp' or not inside(p):continue
  dist,ang,nm,w,wid=near(p);x,y=p
  # Straight dark steel street fixture, or slim park fixture when away from road.
  park=dist>w/2+5;H=4.6 if park else 7.6
  d=Vector((math.cos(ang),math.sin(ang)));per=Vector((-d.y,d.x))
  tip=Vector(p)+per*(.55 if park else 1.7)
  rod((x,y,.16),(x,y,H),.065,'white' if park else 'black')
  rod((x,y,H),(*tip,H),.045,'white' if park else 'black')
  box((*tip,H),(.75,.28,.13),'black',ang)
  box((*tip,H-.08),(.65,.22,.035),'lamp',ang)
  ld=bpy.data.lights.new('Street downlight '+n.get('id'),'SPOT');ld.color=(1,.78,.53);ld.spot_size=math.radians(110);ld.spot_blend=.65;ld.shadow_soft_size=.22
  for f,e in [(1,0),(120,200),(240,700)]:ld.energy=e;ld.keyframe_insert(data_path='energy',frame=f)
  lo=bpy.data.objects.new('Street downlight '+n.get('id'),ld);col.objects.link(lo);lo.location=(*tip,H-.11)
  report['mapped_lamp_nodes'].append({'node':n.get('id'),'xy':list(p),'type_inferred':'park' if park else 'road'})
 # Replace ambiguous old illustrative lamp row only when it is still named individually.
 old=[o for o in s.objects if o.name.startswith(('Street lamp','Lamp arm','Luminaire'))]
 if old:bpy.data.batch_remove(old)
 # Grates at actual mapped trees, don't duplicate actual tree assets.
 for n in r.findall('node'):
  if tags(n).get('natural')!='tree' or not inside(xy(n)):continue
  x,y=xy(n)
  for a in [-.7,.7]:box((x+a,y,.195),(.09,1.5,.04),'steel');box((x,y+a,.195),(1.5,.09,.04),'steel')
  for a in [-.48,-.3,.3,.48]:box((x+a,y,.195),(.025,1.25,.035),'steel')
  report['tree_grate_nodes'].append(n.get('id'))
 # Road names are verified OSM names; sign positions/form are interpretive.
 fontpath='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
 try:font=bpy.data.fonts.load(fontpath)
 except:font=None
 for i,nm in enumerate(['시민로','평화로','신흥로']):
  rr=[q for q in roads if q[2]==nm]
  if not rr:continue
  a,b,_,w,wid=min(rr,key=lambda q:abs(q[0][0])+abs(q[0][1]));d=Vector(b)-Vector(a);d.normalize();per=Vector((-d.y,d.x));p=Vector(a)+per*(w/2+1.5);ang=math.atan2(d.y,d.x);x,y=p
  rod((x,y,.16),(x,y,4.2),.065,'steel');box((x,y,3.85),(2.5,.10,.66),'blue',ang)
  for side in [-1,1]:
   cu=bpy.data.curves.new('Verified road name '+nm,'FONT');cu.body=nm;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=.42;cu.extrude=.003
   if font:cu.font=font
   o=bpy.data.objects.new('Road sign '+nm,cu);col.objects.link(o);o.location=(x+math.sin(ang)*.075*side,y-math.cos(ang)*.075*side,3.85);o.rotation_euler=(math.pi/2,0,ang+(math.pi if side==-1 else 0));cu.materials.append(mats['white']);o['evidence']='Name from OSM; board placement/size inferred, not surveyed'
  report['road_names'].append({'name':nm,'way':wid,'placement':'inferred roadside'})
 for n,(vs,fs) in batches.items():
  if not vs:continue
  me=bpy.data.meshes.new('Street batch '+n);me.from_pydata(vs,[],fs);me.materials.append(mats[n]);me.update();o=bpy.data.objects.new('Street batch '+n,me);col.objects.link(o);o['evidence']='OSM anchors + photo typology; inferred fixture dimensions. Not traffic simulation.'
 s['street_furniture_evidence']='OSM signal/tree/lamp anchors; mapped road names; fixture shapes and sign pole positions inferred'
 report['objects']=len(col.objects);report['version']='v2';return report
