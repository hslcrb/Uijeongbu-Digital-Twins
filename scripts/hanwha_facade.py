"""Specific Hanwha Life facade, 2025 photograph and OSM footprint; dimensions inferred."""
import bpy,gzip,math,random,xml.etree.ElementTree as ET
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def enhance_hanwha():
 name='15_Hanwha_photo_facade'; old=bpy.data.collections.get(name)
 if old:return
 col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col)
 r=ET.parse(gzip.open(ROOT/'data/map.osm.gz')).getroot();ns={n.get('id'):Vector(((float(n.get('lon'))-127.046)*111320*math.cos(math.radians(37.738)),(float(n.get('lat'))-37.738)*111320,0)) for n in r.findall('node')}
 w=next(w for w in r.findall('way') if w.get('id')=='1466029481');pts=[ns[n.get('ref')] for n in w.findall('nd')][:-1]
 # Remove generic facade object AND its windows/room bays, not only the base solid.
 remove=[o for o in bpy.context.scene.objects if o.get('osm_way_id')=='1466029481'];bpy.data.batch_remove(ids=remove)
 def in_region(p):return 173.0<p.x<191.9 and -10.1<p.y<24.8 and -.5<p.z<43
 batch=bpy.data.collections.get('12_Window_room_proxies')
 removed=0
 if batch:
  for ob in batch.objects:
   if ob.type!='MESH':continue
   vs=[tuple(v.co) for v in ob.data.vertices];fs=[]
   for face in ob.data.polygons:
    if in_region(ob.matrix_world@face.center):removed+=1
    else:fs.append(tuple(face.vertices))
   ob.data.clear_geometry();ob.data.from_pydata(vs,[],fs);ob.data.update()
 def mat(n,c,metal=0,rough=.4,trans=0,emit=0):
  m=bpy.data.materials.new(n);m.use_nodes=True;m.diffuse_color=(*c,1);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;p.inputs['Transmission Weight'].default_value=trans;p.inputs['IOR'].default_value=1.46
  if emit:
   p.inputs['Emission Color'].default_value=(*c,1)
   for f,v in [(1,0),(120,emit*.35),(240,emit)]:p.inputs['Emission Strength'].default_value=v;p.inputs['Emission Strength'].keyframe_insert('default_value',frame=f)
  return m
 glass=[mat('Hanwha bronze glazing '+str(i),(.24+i*.018,.155+i*.012,.09+i*.008),.35,.14,.5) for i in range(3)]
 black=mat('Hanwha black metal',(.025,.025,.024),.7,.28);silver=mat('Hanwha silver mullion',(.22,.21,.2),.7,.3);white=mat('Hanwha sign backing',(.88,.88,.82));letter=mat('Hanwha sign letters',(.08,.1,.11));inter=mat('Hanwha interior shade',(.095,.085,.075));lit=mat('Hanwha warm interior',(.85,.64,.38),emit=.9)
 batches={}
 def q(m,ps):
  vs,fs=batches.setdefault(m.name,([],[]));i=len(vs);vs.extend(tuple(p) for p in ps);fs.append((i,i+1,i+2,i+3))
 def cube(m,loc,sz):
  p=Vector(loc);a,b,c=[s/2 for s in sz];vs=[p+Vector((x*a,y*b,z*c)) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
  for face in [(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]:q(m,[vs[j] for j in face])
 h=42; rng=random.Random(1466029481)
 for a,b in zip(pts,pts[1:]+pts[:1]):
  dv=b-a;L=dv.length;u=dv/L;n=Vector((u.y,-u.x,0));center=sum(pts,Vector())/4
  if n.dot((a+b)/2-center)<0:n=-n
  def P(x,z,dep=0):return a+u*x+Vector((0,0,z))+n*dep
  cols=max(3,round(L/1.7));pitch=L/cols
  # Ground4.5m + 9 upper floors4m = 10F; horizontal panels subdivide each floor.
  levels=[0,4.5]+[4.5+i*4 for i in range(1,10)]
  for row in range(10):
   za,zb=levels[row],levels[row+1]
   for j in range(cols):
    xa=j*pitch;xb=(j+1)*pitch
    q(glass[rng.randrange(3)],[P(xa,za,.02),P(xb,za,.02),P(xb,zb,.02),P(xa,zb,.02)])
    roommat=lit if rng.random()<.28 else inter
    q(roommat,[P(xa,za,-1.2),P(xb,za,-1.2),P(xb,zb,-1.2),P(xa,zb,-1.2)])
    q(inter,[P(xa,za),P(xa,zb),P(xa,zb,-1.2),P(xa,za,-1.2)])
    q(inter,[P(xa,za),P(xb,za),P(xb,za,-1.2),P(xa,za,-1.2)])
    q(silver,[P(xa-.035,za,.05),P(xa+.035,za,.05),P(xa+.035,zb,.05),P(xa-.035,zb,.05)])
   # midfloor and floor narrow bronze grid, observed rather than big repeated square holes.
   for z in [za,(za+zb)/2]:q(silver,[P(0,z-.04,.055),P(L,z-.04,.055),P(L,z+.04,.055),P(0,z+.04,.055)])
  q(black,[P(0,40.5,.04),P(L,40.5,.04),P(L,42,.04),P(0,42,.04)])
 q(black,[Vector((p.x,p.y,42)) for p in pts])
 cube(white,(177.5,16,45),(8,12,5))
 # Confirmed text only; no invented logo vector.
 fontpath=ROOT/'assets/hanwha-label.otf';font=bpy.data.fonts.load(str(fontpath))
 cu=bpy.data.curves.new('Hanwha confirmed sign','FONT');cu.body='한화생명';cu.font=font;cu.size=2;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.02
 ob=bpy.data.objects.new('Hanwha photographed rooftop lettering',cu);col.objects.link(ob);ob.location=(173.45,16,45);ob.rotation_euler=(math.pi/2,0,-math.pi/2);cu.materials.append(letter);font.pack()
 # Hana Bank lettering visible in official building photograph, no unverified tenant additions.
 cu=bpy.data.curves.new('Hana bank confirmed text','FONT');cu.body='하나은행';cu.font=font;cu.size=1.2;cu.align_x='CENTER';cu.extrude=.015
 ob=bpy.data.objects.new('Hana bank photographed upper lettering',cu);col.objects.link(ob);ob.location=(182,24.55,38.8);ob.rotation_euler=(math.pi/2,0,math.pi);cu.materials.append(mat('Hana green lettering',(.05,.3,.29)))
 for mn,(vs,fs) in batches.items():
  me=bpy.data.meshes.new(mn);me.from_pydata(vs,[],fs);me.materials.append(bpy.data.materials[mn]);me.update();o=bpy.data.objects.new(mn,me);col.objects.link(o)
 bpy.context.scene['hanwha_evidence']='OSM1466029481 footprint/42m; official10F/B4; 2025-03 exterior photo. Glass spacing and unobserved elevations inferred.'
 print('HANWHA removed generic window faces',removed,flush=True)
 return {'removed_generic_faces':removed,'objects':len(col.objects)}

if __name__=='__main__':
 enhance_hanwha();out=Path('/workspace/shared/uijeongbu-lighting');bpy.ops.wm.save_as_mainfile(filepath=str(out/'hanwha-study.blend'),compress=True)
 s=bpy.context.scene;data=bpy.data.cameras.new('Hanwha QA');cam=bpy.data.objects.new('Hanwha QA',data);s.collection.objects.link(cam);cam.location=(110,75,32);target=Vector((182,8,22));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();data.lens=45;s.camera=cam;s.frame_set(1);s.cycles.samples=24;s.render.resolution_x=1000;s.render.resolution_y=850;s.render.resolution_percentage=100;s.render.filepath=str(out/'hanwha-study.png');bpy.ops.render.render(write_still=True)
