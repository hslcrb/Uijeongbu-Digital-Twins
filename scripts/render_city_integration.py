import bpy,math
from mathutils import Vector
from pathlib import Path
base=Path('/workspace/shared/uijeongbu-twin/repo')
bpy.ops.wm.open_mainfile(filepath=str(base/'Uijeongbu_Station_v1.blend'))
with bpy.data.libraries.load('/workspace/shared/uijeongbu-city/output/Uijeongbu_City_Outline.blend',link=False) as (a,b):b.objects=[n for n in a.objects if n.startswith('city_')]
for o in b.objects:
 if o:bpy.context.scene.collection.objects.link(o)
s=bpy.context.scene;s.frame_set(1);s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=False;s.render.resolution_x=1400;s.render.resolution_y=900;s.render.resolution_percentage=100
cam=s.camera;cam.data.type='PERSP';cam.data.lens=40;cam.data.clip_end=50000
for name,pos,target in [('city-integration',(2800,-3500,2800),(200,1000,0)),('city-seam',(600,-700,500),(0,0,0))]:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();s.render.image_settings.file_format='JPEG';s.render.filepath=str(base/'renders'/f'{name}.jpg');bpy.ops.render.render(write_still=True)
