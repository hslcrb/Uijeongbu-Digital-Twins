import bpy,json,hashlib
from pathlib import Path
R=Path('/workspace/shared/korail-font')
f=bpy.data.fonts.load(str(R/'KORAIL-old.ttf'))
changed=[]
for name in ['Entrance Korean','East station rooftop sign','의정부역 sign']:
 o=bpy.data.objects.get(name)
 if not o:continue
 width=o.dimensions.x;o.data.font=f;bpy.context.view_layer.update()
 if o.dimensions.x:o.scale*=width/o.dimensions.x
 o['font_source']='KORAIL Version 1.01 2004.04.23';o['font_download']='https://t1.daumcdn.net/cfile/tistory/993FF63F5E1AD89F0A';changed.append(name)
 # Store actual signage as mesh, not a redistributable font file.
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
if f.users==0:bpy.data.fonts.remove(f)
s=bpy.context.scene;s.render.resolution_x=1200;s.render.resolution_y=850;s.render.resolution_percentage=100;s.cycles.samples=48;s.cycles.use_denoising=True;s.render.filepath=str(R/'entrance-korail.png')
(R/'validation.json').write_text(json.dumps({'updated':changed,'font_file_sha256':hashlib.sha256((R/'KORAIL-old.ttf').read_bytes()).hexdigest(),'font_raw_embedded':False,'deployment':'not uploaded'},ensure_ascii=False,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_korail.blend'),compress=True)
bpy.ops.render.render(write_still=True)
