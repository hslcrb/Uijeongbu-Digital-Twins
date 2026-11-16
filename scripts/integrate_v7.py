"""Integrate the photo-supported west access without replacing the shared scene."""
import bpy,bmesh,json,sys,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from station_west_v7 import add_west_plaza
report=add_west_plaza();col=bpy.data.collections['21_West_Plaza_v7'];groups={}
from fix_platform_lights_v7 import correct_platform_lights
report['platform_lights']=correct_platform_lights(col)
for o in list(col.objects):
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);
 if o.data.materials[0].name=='West clear canopy glass':bmesh.ops.solidify(bm,geom=list(bm.faces),thickness=.012)
 bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
 mat=o.data.materials[0];groups.setdefault(mat.name,[]).append(o)
for name,objects in groups.items():
 vs=[];fs=[];names=[];mat=objects[0].data.materials[0]
 for o in objects:
  off=len(vs);vs.extend([tuple(o.matrix_world@v.co) for v in o.data.vertices]);fs.extend([tuple(off+i for i in p.vertices) for p in o.data.polygons]);names.append(o.name)
 me=bpy.data.meshes.new('West photo '+name);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update();new=bpy.data.objects.new('West v7 batch '+name,me);col.objects.link(new);new['source_objects']=json.dumps(names);new['evidence']='WEST_V7_EVIDENCE.md; dimensions inferred'
 for o in objects:bpy.data.objects.remove(o,do_unlink=True)
report['batched_objects']=len(col.objects)
from solidify_road_edges_v7 import solidify_road_edges
report['physical_road_edges']=solidify_road_edges()
# Audit, do not silently delete unrelated mapped geometry.
audit=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH' or not (o.name.startswith(('Road','Walk','Pedestrian','Unified','Union surface','Batched 02'))):continue
 deg=sum(p.area<1e-8 for p in o.data.polygons);dups=0;seen=set()
 for p in o.data.polygons:
  key=tuple(sorted(tuple(round(c,5) for c in o.matrix_world@o.data.vertices[i].co) for i in p.vertices))
  if key in seen:dups+=1
  seen.add(key)
 if deg or dups:audit.append({'name':o.name,'degenerate':deg,'duplicate':dups})
from deduplicate_road_skirts import deduplicate
report['exact_duplicate_cleanup']=deduplicate()
report['road_audit_before_duplicate_cleanup']=audit;report['road_wedges']='Existing mapped pedestrian outlines visible; no unrelated surfaces removed'
s=bpy.context.scene;s.frame_set(1);s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=94
oldcam=bpy.data.objects.get('v7 west comparison')
if oldcam:bpy.data.objects.remove(oldcam,do_unlink=True)
bpy.ops.object.camera_add(location=(-117,-5,16));cam=bpy.context.object;cam.name='v7 west comparison';cam.rotation_euler=(Vector((-65,42,7))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=35;s.camera=cam
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v1.blend'),compress=True)
for frame,label in [(1,'west-v7'),(240,'west-night-v7')]:
 s.frame_set(frame);s.render.filepath=str(R/'renders'/f'{label}.jpg');bpy.ops.render.render(write_still=True)
s.frame_set(1);report['objects']=len(s.objects);(R/'docs/v7-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(report)
exec(compile((R/'scripts/export_web.py').read_text(),str(R/'scripts/export_web.py'),'exec'))
