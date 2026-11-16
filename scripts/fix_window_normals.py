"""Rebuild existing procedural context bays with winding-independent outward normals.
This corrects geometry, not surveyed facade/window dimensions. No new draw calls.
"""
import bpy,json,sys

def fix_window_normals(script_dir):
 s=bpy.context.scene
 if s.get('window_normal_fix_v1'):return json.loads(s['window_normal_fix_v1'])
 col=bpy.data.collections.get('12_Window_room_proxies')
 if not col:raise RuntimeError('Expected existing window-room proxy collection')
 candidates=[];reversed_count=0;old_counts={}
 for ob in bpy.data.collections['05_Context_OSM'].objects:
  if ob.type!='MESH' or 'osm_way_id' not in ob:continue
  me=ob.data;old_counts[ob.name]=len(me.polygons)
  if len(me.polygons)<2:raise RuntimeError('Missing extrusion caps: '+ob.name)
  bottom,top=me.polygons[:2]
  if abs(bottom.normal.z)<.9 or abs(top.normal.z)<.9:raise RuntimeError('Unrecognized context topology: '+ob.name)
  # The first two faces are retained original extrusion caps, even after window cuts.
  pts=[me.vertices[i].co.copy() for i in top.vertices]
  area=sum(a.x*b.y-b.x*a.y for a,b in zip(pts,pts[1:]+pts[:1]))/2
  if abs(area)<1e-6:raise RuntimeError('Degenerate footprint: '+ob.name)
  if area<0:pts.reverse();reversed_count+=1
  z0=min(me.vertices[i].co.z for i in bottom.vertices);z1=max(p.z for p in pts);n=len(pts)
  vs=[(p.x,p.y,z) for z in (z0,z1) for p in pts]
  fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
  candidates.append((ob,vs,fs))
 # Validate all candidates before mutating, then reset only derived procedural geometry.
 for ob,vs,fs in candidates:
  ob.data.clear_geometry();ob.data.from_pydata(vs,[],fs);ob.data.update()
 for ob in list(col.objects):bpy.data.objects.remove(ob,do_unlink=True)
 bpy.data.collections.remove(col)
 sys.path.insert(0,str(script_dir));from building_lighting_corrected import enhance_building_windows
 before=json.loads(s.get('window_room_proxy_stats','{}'));after=enhance_building_windows()
 changed=[(o.name,old_counts[o.name],len(o.data.polygons)) for o,_,_ in candidates if old_counts[o.name]!=len(o.data.polygons)]
 # Thin shell cells intentionally stay opaque instead of generating impossible bays.
 assert all(o.data.polygons[1].normal.z>.99 for o,_,_ in candidates)
 assert not any(o.get('osm_way_id')=='1466029481' for o,_,_ in candidates) if bpy.data.collections.get('15_Hanwha_photo_facade') else True
 report={'context_buildings_checked':len(candidates),'clockwise_footprints_corrected':reversed_count,'before':before,'after':after,'unchanged_building_polygon_counts':len(candidates)-len(changed),'thin_shell_buildings_changed':changed,'all_roofs_positive_z':True,'hanwha_facade_preserved':bool(bpy.data.collections.get('15_Hanwha_photo_facade')),'old_stats_note':'Prior stats may include the 288-window generic Hanwha facade removed by specific enhancement.','basis':'Signed footprint area, not centroid; valid for concave simple polygons. All restored extrusion roof normals +Z. Room depth follows inward -normal.','scope':'Procedural geometry correction only; facade measurements and occupancies remain unverified.'}
 s['window_normal_fix_v1']=json.dumps(report);return report
