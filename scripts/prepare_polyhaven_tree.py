"""Import CC0 Poly Haven Tree Small 02, create explicit seasonal/optimized derivatives."""
import bpy,math,json,bmesh
from pathlib import Path
from mathutils import Vector
BASE=Path('/workspace/shared/uijeongbu-assets/polyhaven-tree-small02')
OUT=Path('/workspace/shared/uijeongbu-twin/repo/assets')
bpy.ops.wm.open_mainfile(filepath=str(BASE/'tree_small_02_1k.blend'))
master=bpy.data.objects['tree_small_02_LOD1']
for o in list(bpy.data.objects):
 if o!=master:bpy.data.objects.remove(o,do_unlink=True)
master.hide_set(False);master.hide_render=False
for c in list(master.users_collection):c.objects.unlink(master)
bpy.context.scene.collection.objects.link(master)
bpy.context.view_layer.objects.active=master;master.select_set(True)
mod=master.modifiers.new('City_Optimization','DECIMATE');mod.ratio=.25;bpy.ops.object.modifier_apply(modifier=mod.name)
master.name='PH_TreeSmall02_Summer_LOD1'
master.asset_mark();master['source']='https://polyhaven.com/a/tree_small_02';master['license']='CC0';master['species']='Burkea africana, not verified local species'
fall=master.copy();fall.data=master.data;bpy.context.scene.collection.objects.link(fall);fall.name='PH_TreeSmall02_Autumn_LOD1';fall.asset_mark()
for slot in fall.material_slots:
 original=slot.material;slot.link='OBJECT';slot.material=original.copy()
 if 'leaves' in slot.material.name:
  nt=slot.material.node_tree
  for node in list(nt.nodes):
   if node.type=='TEX_IMAGE' and node.image and 'leaves_diff' in node.image.name:
    links=list(node.outputs['Color'].links)
    h=nt.nodes.new('ShaderNodeHueSaturation');h.inputs['Hue'].default_value=.34;h.inputs['Saturation'].default_value=1.5
    nt.links.new(node.outputs['Color'],h.inputs['Color'])
    for link in links:
     target=link.to_socket;nt.links.remove(link);nt.links.new(h.outputs['Color'],target)
fall['seasonal_derivative']='Autumn color transformation, not source season'
proxy=fall.copy();proxy.data=fall.data.copy();bpy.context.scene.collection.objects.link(proxy);proxy.name='PH_TreeSmall02_Autumn_LOD2'
bpy.context.view_layer.objects.active=proxy;proxy.select_set(True)
m=proxy.modifiers.new('Distance_Optimization','DECIMATE');m.ratio=.25;bpy.ops.object.modifier_apply(modifier=m.name);proxy.asset_mark()
# Pack 256px derivatives; original 1k files are preserved separately.
for im in bpy.data.images:
 if im.source=='FILE' and im.size[0]:
  im.scale(256,256);im.filepath_raw='/tmp/derived_'+im.name.replace('.exr','.png');im.file_format='PNG';im.save();im.pack()
for _ in range(3):bpy.data.orphans_purge(do_recursive=True)
for mesh in bpy.data.meshes:
 bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(mesh);bm.free()
for o in [master,fall,proxy]:o.location=(0,0,0);o.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'polyhaven-tree-small02-seasonal.blend'),compress=True)
print('STATS',[(o.name,len(o.data.polygons)) for o in [master,fall,proxy]])
# Render only for QA without modifying saved assets.
master.hide_render=False;fall.hide_render=False;master.location.x=-2.3;fall.location.x=2.3
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.world.color=(.4,.4,.4)
bpy.ops.object.light_add(type='AREA',location=(0,-4,8));bpy.context.object.data.energy=1400;bpy.context.object.data.size=8
bpy.ops.object.camera_add(location=(11,-17,8));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,2.3))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=10.5;scene.camera=cam
scene.render.resolution_x=1100;scene.render.resolution_y=700;scene.render.resolution_percentage=100;scene.render.filepath=str(OUT/'polyhaven-tree-small02-preview.png');bpy.ops.render.render(write_still=True)
