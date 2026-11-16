"""OSM-aligned visual railway study. Geometry details/elevations are approximations.
Call add_rail_detail(root) in existing scene. Never saves or changes main.
"""
import bpy, math, gzip, xml.etree.ElementTree as ET
from pathlib import Path
from mathutils import Vector

def add_rail_detail(root):
 root=Path(root); name='12_Railway_Detail'
 old=bpy.data.collections.get(name)
 if old:
  bpy.data.batch_remove(list(old.objects));bpy.data.collections.remove(old)
 col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col)
 batches={}
 def mat(n,c,metal=0):
  m=bpy.data.materials.get(n) or bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.6;return m
 steel=mat('Rail polished steel',(.25,.29,.31),.75);rust=mat('Rail web oxidized',(.23,.12,.07),.4);con=mat('Rail sleeper concrete',(.34,.34,.31));ballast=mat('Rail crushed stone',(.12,.115,.105));edge=mat('Platform safety ochre',(.8,.57,.09));pave=mat('Platform pale concrete',(.43,.45,.44));roof=mat('Platform shelter steel',(.22,.25,.27),.5)
 def facebatch(v,f,m):
  vs,fs=batches.setdefault(m.name,([],[]));off=len(vs);vs.extend(v);fs.extend([tuple(i+off for i in a) for a in f])
 def box(p,s,m,angle=0):
  x,y,z=p;a,b,c=[v/2 for v in s];ca,sa=math.cos(angle),math.sin(angle)
  v=[(x+u*a*ca-vv*b*sa,y+u*a*sa+vv*b*ca,z+w*c) for u,vv,w in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
  facebatch(v,[tuple(reversed(f)) for f in [(0,2,6,4),(1,5,7,3),(0,4,5,1),(2,3,7,6),(0,1,3,2),(4,6,7,5)]],m)
 def segment(a,b,w,h,z,m):
  d=b-a;box(((a.x+b.x)/2,(a.y+b.y)/2,z),(d.length,w,h),m,math.atan2(d.y,d.x))
 r=ET.parse(gzip.open(root/'data/map.osm.gz','rb')).getroot();origin=(127.046,37.738)
 nodes={e.get('id'):Vector(((float(e.get('lon'))-origin[0])*111320*math.cos(math.radians(origin[1])),(float(e.get('lat'))-origin[1])*111320)) for e in r.findall('node')}
 def within(p):return -265<=p.x<=355 and -225<=p.y<=335
 counts={'rail_segments':0,'sleepers':0,'platform_polygons':0}
 used=[]
 allways={w.get("id"):w for w in r.findall("way")}
 for w in r.findall('way'):
  t={e.get('k'):e.get('v') for e in w.findall('tag')};ps=[nodes[e.get('ref')] for e in w.findall('nd') if e.get('ref') in nodes]
  if t.get('railway')=='rail':
   used.append(w.get('id'))
   for a,b in zip(ps,ps[1:]):
    if not(within(a) and within(b)) or (b-a).length<.05:continue
    d=b-a;u=d.normalized();per=Vector((-u.y,u.x));L=d.length;z=.19
    segment(a,b,3.5,.22,z-.1,ballast)
    for off in [-.7175,.7175]:
     segment(a+per*off,b+per*off,.13,.12,z+.12,rust);segment(a+per*off,b+per*off,.07,.055,z+.205,steel)
    for i in range(int(L/.7)):
     p=a+u*(i*.7+.2);box((p.x,p.y,z),(2.55,.24,.17),con,math.atan2(u.y,u.x)+math.pi/2);counts['sleepers']+=1
    if t.get('electrified')=='contact_line':
     segment(a,b,.025,.025,5.6,steel)
     # Sparse visual poles; spacing is a depiction, not surveyed infrastructure.
     if not t.get('covered')=='yes':
      for j in range(0,int(L),45):
       p=a+u*j+per*2.2;box((p.x,p.y,3),( .17,.17,6),steel)
    counts['rail_segments']+=1
  elif t.get('railway')=='platform' and ps and any(within(p) for p in ps):
   pairs={'624679785':'624679786','624679787':'624679788','624679789':'624679790'}
   if w.get('id') in pairs.values():continue
   if w.get('id') in pairs:
    ps+= [nodes[e.get('ref')] for e in allways[pairs[w.get('id')]].findall('nd') if e.get('ref') in nodes]
    from mathutils.geometry import convex_hull_2d
    ps=[ps[i] for i in convex_hull_2d(ps)]
   if ps[0]==ps[-1]:ps=ps[:-1]
   n=len(ps);v=[(p.x,p.y,z) for z in (.35,1.2) for p in ps];f=[tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];facebatch(v,f,pave);counts['platform_polygons']+=1
   # Long outer edges receive safety strips. Two OSM polygons comprise each island.
   for a,b in zip(ps,ps[1:]+ps[:1]):
    if (b-a).length>15:segment(a,b,.22,.03,1.23,edge)
   # Canopy/pillars use polygon centerline (paired OSM polygons share center).
   lo=min(ps,key=lambda p:p.y);hi=max(ps,key=lambda p:p.y);d=hi-lo
   if d.length>30:
    u=d.normalized();mid=sum(ps,Vector((0,0)))/len(ps);a=mid-u*d.length*.42;b=mid+u*d.length*.42
    segment(a,b,6.2,.18,4.6,roof)
    for j in range(0,int((b-a).length),18):
     p=a+u*j;box((p.x,p.y,2.85),(.25,.25,3.3),pave)
 for m,(vs,fs) in batches.items():
  me=bpy.data.meshes.new(m);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(m,me);col.objects.link(o);o.data.materials.append(bpy.data.materials[m]);o['visual_approximation']=True
 col['source']='OSM map.osm.gz; ODbL; origin 127.046,37.738';col['limitations']='Rail Z, sleeper spacing, platform height/canopy not surveyed; no operational assertions.'
 counts['objects']=len(col.objects);counts['osm_rail_ways']=len(used);print('RAIL_DETAIL',counts);return counts
