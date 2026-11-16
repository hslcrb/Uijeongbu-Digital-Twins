import bpy,bmesh,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from station_west_v8 import refine_west_access
report=refine_west_access();col=bpy.data.collections['22_West_access_photo_v8'];groups={}
for o in list(col.objects):
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data)
 if o.data.materials[0].name=='West clear canopy glass':bmesh.ops.solidify(bm,geom=list(bm.faces),thickness=.012)
 bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free();groups.setdefault(o.data.materials[0].name,[]).append(o)
for name,objects in groups.items():
 vs=[];fs=[];mat=objects[0].data.materials[0]
 for o in objects:
  n=len(vs);vs.extend(tuple(o.matrix_world@v.co) for v in o.data.vertices);fs.extend(tuple(n+i for i in f.vertices) for f in o.data.polygons)
 me=bpy.data.meshes.new('West v8 '+name);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update();new=bpy.data.objects.new('West v8 '+name,me);col.objects.link(new)
 for o in objects:bpy.data.objects.remove(o,do_unlink=True)
report['batched_objects']=len(col.objects)
s=bpy.context.scene;s.frame_set(1);s.camera=bpy.data.objects.get('v7 west comparison');s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=94
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v1.blend'),compress=True)
for f,label in [(1,'west-v8'),(240,'west-night-v8')]:
 s.frame_set(f);s.render.filepath=str(R/'renders'/f'{label}.jpg');bpy.ops.render.render(write_still=True)
(R/'docs/v8-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(report)
s.frame_set(1)
exec(compile((R/'scripts/export_web.py').read_text(),str(R/'scripts/export_web.py'),'exec'))
