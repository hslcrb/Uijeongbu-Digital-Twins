"""Photo-supported façade and mapped street furniture refinement, without changing datum."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from station_cladding_v5 import add_station_cladding,add_north_window_bands
from hanwha_facade import enhance_hanwha
from enhance_rail_bed import enhance_rail_bed
from street_furniture import add_street_furniture
report={'station':add_station_cladding(),'hanwha':enhance_hanwha(),'rail_bed':enhance_rail_bed(R),'street':add_street_furniture(R)}
report['north_facade']=add_north_window_bands()
s=bpy.context.scene;s.frame_set(1);s.camera=bpy.data.objects['01_East_Station_overview'];s.cycles.samples=32;s.cycles.use_denoising=False;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=92
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v1.blend'),compress=True)
report['objects']=len(s.objects);(R/'docs/v5-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str));print(report,flush=True)
for fr,n in [(1,'day-v5'),(240,'night-v5')]:
 s.frame_set(fr);s.render.filepath=str(R/'renders'/f'{n}.jpg');bpy.ops.render.render(write_still=True)
s.frame_set(1);bpy.ops.object.camera_add(location=(-6,175,7));c=bpy.context.object;c.rotation_euler=(Vector((-12,95,2))-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=35;s.camera=c;s.render.filepath=str(R/'renders/rail-v5.jpg');bpy.ops.render.render(write_still=True)
exec(compile((R/'scripts/export_web.py').read_text(),str(R/'scripts/export_web.py'),'exec'))
