"""Photo-informed surface treatment, not a surveyed paving-layout reconstruction.
2025 station photos show granular pale stone and repeated paving joints.
Baked deterministic atlas and real-world UVs remain portable in GLB.
"""
import bpy,random,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
def enhance_surfaces():
 rng=random.Random(915); n=256
 def texture(name,base,joints=False):
  old=bpy.data.images.get(name)
  if old:bpy.data.images.remove(old)
  im=bpy.data.images.new(name,width=n,height=n,alpha=False); pixels=[]
  for y in range(n):
   for x in range(n):
    noise=rng.uniform(-.035,.035); grain=-.075 if rng.random()<.028 else 0
    joint=(x<2 or y<2) if joints else False
    c=[max(0,min(1,v+noise+grain)) for v in base]
    if joint:c=[v*.68 for v in c]
    pixels.extend((*c,1))
  im.pixels.foreach_set(pixels);im.file_format='PNG';out=ROOT/'assets'/'surface-v9';out.mkdir(exist_ok=True);im.filepath_raw=str(out/(name+'.png'));im.save();im.pack();return im
 stone=texture('pale-granular-stone',(.73,.74,.72))
 paving=texture('pale-paver-module',(.68,.68,.64),True)
 concrete=texture('cast-concrete-grain',(.61,.62,.60))
 targets={'West photo sidewall ceramic':(stone,.9),'West concrete treads':(stone,.9),'Concrete':(concrete,2.4)}
 # Restrict paving to the raised public plaza; not entire unsurveyed terrain.
 plaza=bpy.data.objects.get('Brilliant Plaza elevated approach')
 if plaza:
  mat=bpy.data.materials.get('Plaza photo interpreted paving') or plaza.data.materials[0].copy();mat.name='Plaza photo interpreted paving';plaza.data.materials[0]=mat;targets[mat.name]=(paving,.6)
 report={'objects':0,'polygons':0,'extra_polygons':0,'textures':3,'uv_meters':{},'inferred':'Paver module 0.6m, stone grain and roughness are material approximations; no measured layout or surface scan.'}
 for name,(im,scale) in targets.items():
  mat=bpy.data.materials.get(name)
  if not mat:continue
  mat.use_nodes=True; nodes=mat.node_tree.nodes;p=nodes.get('Principled BSDF');t=nodes.new('ShaderNodeTexImage');t.image=im;t.extension='REPEAT';t.interpolation='Linear';mat.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.8
  for o in list(bpy.context.scene.objects):
   if o.type!='MESH' or name not in o.data.materials:continue
   uv=o.data.uv_layers.get('PhotoSurfaceUV') or o.data.uv_layers.new(name='PhotoSurfaceUV');o.data.uv_layers.active=uv
   for f in o.data.polygons:
    normal=o.matrix_world.to_3x3()@f.normal;axis=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=axis]
    for li in f.loop_indices:
     co=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]/scale,co[axes[1]]/scale)
   o['surface_v9']='Photographic material character, non-surveyed module dimensions';report['objects']+=1;report['polygons']+=len(o.data.polygons)
  uvnode=nodes.new('ShaderNodeUVMap');uvnode.uv_map='PhotoSurfaceUV';mat.node_tree.links.new(uvnode.outputs['UV'],t.inputs['Vector']);report['uv_meters'][name]=scale
 return report
if __name__=='__main__':
 report=enhance_surfaces();print(json.dumps(report));(ROOT/'docs/v9-surface-validation.json').write_text(json.dumps(report,indent=2));s=bpy.context.scene;s.frame_set(1);s.camera=bpy.data.objects.get('v7 west comparison');s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=94
 out=ROOT/'blender/v9';out.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(out/'Uijeongbu_Station_v9.blend'),compress=True)
 s.render.filepath=str(ROOT/'renders/west-v9.jpg');bpy.ops.render.render(write_still=True)
 exec(compile((ROOT/'scripts/export_web.py').read_text(),str(ROOT/'scripts/export_web.py'),'exec'))
