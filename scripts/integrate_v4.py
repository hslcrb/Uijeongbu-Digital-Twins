"""Integrate verified rail/window modules and remove coplanar road ribbons."""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'));s=bpy.context.scene
# Replace overlapping OSM road strips with polygon-unioned surfaces.
for o in list(s.objects):
 if o.name.startswith(('Road ','Road surface ','Walk ','Pedestrian area ','Rail ','Track ballast ')):
  bpy.data.objects.remove(o,do_unlink=True)
col=bpy.data.collections.get('13_Roads_nonoverlap')
if col:
 for o in list(col.objects):bpy.data.objects.remove(o,do_unlink=True)
else:col=bpy.data.collections.new('13_Roads_nonoverlap');s.collection.children.link(col)
for g in json.loads((R/'data/road-surfaces-unioned.json').read_text()):
 vs=[];fs=[]
 for t in g['triangles']:
  i=len(vs);vs.extend([(x,y,g['z']) for x,y in t]);fs.append((i,i+1,i+2))
 me=bpy.data.meshes.new(g['kind']);me.from_pydata(vs,[],fs);me.materials.append(bpy.data.materials[g['material']]);o=bpy.data.objects.new('Union surface '+g['kind'],me);col.objects.link(o)
# markings must remain above the newly unified asphalt plane.
for o in s.objects:
 if o.name.startswith('Lane dash'):o.location.z=.06
# Rear pillar is unsupported over the inferred escalator opening. Remove it, not a floating prop.
for o in list(s.objects):
 if o.name.startswith('Granite pillar') and o.parent and abs(o.location.x+10)<.1 and abs(o.location.y-15)<.1:bpy.data.objects.remove(o,do_unlink=True)
from building_lighting import enhance_building_windows
print('WINDOWS',enhance_building_windows(),flush=True)
from rail_detail import add_rail_detail
print('RAIL',add_rail_detail(R),flush=True)
s.frame_set(1);s.cycles.use_denoising=False;s.cycles.samples=24;s.render.resolution_x=1440;s.render.resolution_y=1000
s['v4_review']='Union road topology; 20-bit Draco position; 3 platform islands; thin glazing and room proxies. Architectural dimensions remain inferred.'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v1.blend'),compress=True)
# Same camera views before and after enable genuine comparison.
s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=92
for frame,name,cam in [(1,'day-v4','01_East_Station_overview'),(240,'night-v4','01_East_Station_overview'),(1,'plaza-v4','02_Plaza_eye_level')]:
 s.frame_set(frame);s.camera=bpy.data.objects[cam];s.render.filepath=str(R/'renders'/f'{name}.jpg');bpy.ops.render.render(write_still=True)
exec(compile((R/'scripts/export_web.py').read_text(),str(R/'scripts/export_web.py'),'exec'))
