import bpy
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/shared/entrance-v11')
m=bpy.data.materials['v10 downlight recessed baffle'];me=bpy.data.meshes.new('continuous dark soffit backing');me.from_pydata([(-14,29,16.49),(16,29,16.49),(16,38.9,16.49),(-14,38.9,16.49)],[],[(0,1,2,3)]);me.update();o=bpy.data.objects.new('v11 backing prevents sky leaks through panel joints',me);bpy.context.collection.objects.link(o);o.data.materials.append(m)
s=bpy.context.scene;s.cycles.samples=32
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Uijeongbu_Station_v11b_recessed.blend'),compress=True)
s.render.filepath=str(R/'entrance-v11b-wide.png');bpy.ops.render.render(write_still=True)
s.camera.location=(-2,33.7,15.0);s.camera.rotation_euler=(Vector((1,35,16.43))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.lens=36;s.render.filepath=str(R/'ceiling-v11b-closeup.png');bpy.ops.render.render(write_still=True)
