"""Window-room proxy enhancement. Photo-guided light palette, NOT measured room layouts."""
import bpy, math, random, json
from mathutils import Vector
from pathlib import Path

def enhance_building_windows():
 rng=random.Random(1102025);scene=bpy.context.scene
 old=bpy.data.collections.get('12_Window_room_proxies')
 if old:
  return json.loads(scene.get('window_room_proxy_stats','{}')) # already applied: never perforate twice
 col=bpy.data.collections.new('12_Window_room_proxies');scene.collection.children.link(col)
 def material(name,c,emit=0,trans=0):
  m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*c,1)
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.22 if trans else .75;p.inputs['Metallic'].default_value=0;p.inputs['Transmission Weight'].default_value=trans;p.inputs['IOR'].default_value=1.45
  if emit:
   p.inputs['Emission Color'].default_value=(*c,1)
   for f,v in [(1,0),(120,emit*.35),(240,emit)]:p.inputs['Emission Strength'].default_value=v;p.inputs['Emission Strength'].keyframe_insert('default_value',frame=f)
  return m
 colors=[(1,.7,.38),(.72,.86,1),(1,.89,.66),(.08,.1,.13)]
 mats=[material('Room glow '+str(i),c,1.8 if i<3 else 0) for i,c in enumerate(colors)]
 glass=material('Context transparent thin glazing',(.68,.8,.84),trans=.92)
 frame=material('Context room reveals',(.14,.16,.18));room=material('Context room wall',(.31,.3,.27))
 mats+=[glass,frame,room];batches={m.name:([],[],m) for m in mats}
 def quad(mat,pts):
  vs,fs,_=batches[mat.name];i=len(vs);vs.extend([tuple(p) for p in pts]);fs.append((i,i+1,i+2,i+3))
 context=bpy.data.collections.get('05_Context_OSM');stats={'buildings':0,'windows':0,'lit_windows':0}
 if not context:return stats
 # Existing window skins lie against opaque solids. Replace them, never stack over them.
 obsolete=[o for o in context.objects if o.type=='MESH' and 'osm_way_id' not in o and (o.name.startswith('Context window') or (o.name.startswith('Batched') and all(m.name=='Glass' for m in o.data.materials)))]
 bpy.data.batch_remove(ids=obsolete)
 for ob in list(context.objects):
  if ob.type!='MESH' or 'osm_way_id' not in ob:continue
  me=ob.data;vs=[v.co.copy() for v in me.vertices];faces=[];n_windows=0
  ring=[vs[i] for i in me.polygons[1].vertices]
  signed_area=sum(a.x*b.y-b.x*a.y for a,b in zip(ring,ring[1:]+ring[:1]))/2
  def available_depth(point,direction):
   def cross(a,b):return a.x*b.y-a.y*b.x
   ds=[]
   for a,b in zip(ring,ring[1:]+ring[:1]):
    e=b-a;den=cross(direction,e)
    if abs(den)<1e-8:continue
    delta=a-point;t=cross(delta,e)/den;q=cross(delta,direction)/den
    if t>1e-4 and -.00001<=q<=1.00001:ds.append(t)
   return min(ds) if ds else 0.0
  for poly in me.polygons:
   inds=list(poly.vertices);pts=[vs[i] for i in inds]
   if len(pts)!=4 or abs(poly.normal.z)>.1:
    faces.append(tuple(inds));continue
   # OSM extrusion sides have bottom a,b followed by top b,a.
   a,b,c,d=pts;z0=min(p.z for p in pts);z1=max(p.z for p in pts);dv=Vector((b.x-a.x,b.y-a.y,0));L=dv.length
   if L<5 or z1-z0<4 or L>180:
    faces.append(tuple(inds));continue
   u=dv/L;normal=poly.normal.normalized()*(1 if signed_area>0 else -1);origin=Vector((a.x,a.y,z0))
   def P(x,z,dep=0):return origin+u*x+Vector((0,0,z-z0))+normal*dep
   floors=min(24,max(1,int((z1-z0)/3.3)));cols=min(45,max(1,int(L/4)))
   xs=[L*j/cols for j in range(cols+1)];zs=[z0+(z1-z0)*j/floors for j in range(floors+1)]
   def wall(xa,xb,za,zb):
    i=len(vs);vs.extend([P(xa,za),P(xb,za),P(xb,zb),P(xa,zb)]);faces.append((i,i+1,i+2,i+3))
   for row in range(floors):
    for j in range(cols):
     xa,xb=xs[j],xs[j+1];za,zb=zs[row],zs[row+1];wl=xa+(xb-xa)*.22;wr=xb-(xb-xa)*.22;wb=za+.85;wt=min(zb-.5,wb+1.8)
     if wt<=wb:wall(xa,xb,za,zb);continue
     # Thin OSM building:part strips are shells, not 0.9m deep habitable rooms.
     clearance=min(available_depth(P(x,wb),-normal) for x in (wl,(wl+wr)/2,wr))
     depth=min(.9,clearance*.45)
     if depth<.08:
      wall(xa,xb,za,zb);stats.setdefault('thin_shell_cells_without_bays',0);stats['thin_shell_cells_without_bays']+=1;continue
     wall(xa,wl,za,zb);wall(wr,xb,za,zb);wall(wl,wr,za,wb);wall(wl,wr,wt,zb)
     lit=rng.random()<(.55 if row<3 else .33);mi=rng.randrange(3) if lit else 3;glow=mats[mi]
     # A real hole in original wall, transparent pane and five-sided interior bay.
     quad(glass,[P(wl,wb,.04),P(wr,wb,.04),P(wr,wt,.04),P(wl,wt,.04)])
     quad(glass,[P(wl,wt,.01),P(wr,wt,.01),P(wr,wb,.01),P(wl,wb,.01)])
     for (gx1,gz1),(gx2,gz2) in [((wl,wb),(wr,wb)),((wr,wb),(wr,wt)),((wr,wt),(wl,wt)),((wl,wt),(wl,wb))]:
      quad(glass,[P(gx1,gz1,.01),P(gx2,gz2,.01),P(gx2,gz2,.04),P(gx1,gz1,.04)])
     quad(glow,[P(wl,wb,-depth),P(wr,wb,-depth),P(wr,wt,-depth),P(wl,wt,-depth)])
     for edge in [((wl,wb),(wr,wb)),((wr,wb),(wr,wt)),((wr,wt),(wl,wt)),((wl,wt),(wl,wb))]:
      (x1,zx),(x2,zy)=edge;quad(room,[P(x1,zx),P(x2,zy),P(x2,zy,-depth),P(x1,zx,-depth)])
     # center mullion gives depth cue instead of flat glowing square.
     mid=(wl+wr)/2;quad(frame,[P(mid-.025,wb,.055),P(mid+.025,wb,.055),P(mid+.025,wt,.055),P(mid-.025,wt,.055)])
     n_windows+=1;stats['lit_windows']+=int(lit)
  if n_windows:
   me.clear_geometry();me.from_pydata(vs,[],faces);me.update();ob['window_evidence']='Photo-guided procedural spacing; room shape and occupancy illustrative, not surveyed';stats['buildings']+=1;stats['windows']+=n_windows
 for name,(vs,fs,m) in batches.items():
  me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();ob=bpy.data.objects.new(name,me);col.objects.link(ob);ob['evidence']='2025 night photograph palette; per-window layouts illustrative'
 scene['window_room_proxy_stats']=json.dumps(stats);scene['window_room_proxy_evidence']='Reference fn2025 night image, photo-guided palette only. Facade openings and room bays are procedural inference.'
 scene.frame_set(scene.frame_current);return stats

if __name__=='__main__':
 stats=enhance_building_windows();print('WINDOW_STATS',stats,flush=True)
 out=Path('/workspace/shared/uijeongbu-lighting');out.mkdir(exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'lighting-study.blend'),compress=True)
 s=bpy.context.scene;s.frame_set(240);s.camera=bpy.data.objects.get('01_East_Station_overview');s.cycles.samples=24;s.render.resolution_percentage=65;s.render.filepath=str(out/'night-window-study.png');bpy.ops.render.render(write_still=True)
