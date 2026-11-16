import bpy,json,math,hashlib,os
from pathlib import Path
D=Path(__file__).parent;out=D/'output';bpy.ops.wm.open_mainfile(filepath=str(out/'Uijeongbu_City_Outline.blend'))
for o in bpy.context.scene.objects:
 if o.type=='MESH' and o.name.endswith('_terrain'):
  for v in o.data.vertices:
   a,b=v.co.x,v.co.y
   if ((abs(a+285)<1e-4 or abs(a-375)<1e-4) and -250-1e-4<=b<=360+1e-4) or ((abs(b+250)<1e-4 or abs(b-360)<1e-4) and -285-1e-4<=a<=375+1e-4):v.co.z=0.0
for m in bpy.data.materials:
 if m.name in ['buildings','roads','terrain']:
  col=tuple(m.diffuse_color);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.9
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Uijeongbu_City_Outline.blend'),compress=True)
bpy.context.scene.render.filepath=str(out/'city-overview-color.png')
if not os.environ.get('SKIP_RENDER'):bpy.ops.render.render(write_still=True)
tiles={}
for o in bpy.context.scene.objects:
 if o.type=='MESH' and o.name.startswith('city_'):
  a=o.name.split('_');tiles.setdefault((int(a[1]),int(a[2])),[]).append(o)
folder=out/'tiles';folder.mkdir(exist_ok=True);items=[]
for (x,y),obs in sorted(tiles.items()):
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 path=folder/f'{x}_{y}.glb'
 bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
 coords=[v.co for o in obs for v in o.data.vertices];lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)];center=[(lo[i]+hi[i])/2 for i in range(3)];radius=math.sqrt(sum(((hi[i]-lo[i])/2)**2 for i in range(3)))
 items.append({'id':f'{x}_{y}','url':f'tiles/{x}_{y}.glb','center':[center[0],center[2],-center[1]],'radius':radius,'aabb_min':[lo[0],lo[2],-hi[1]],'aabb_max':[hi[0],hi[2],-lo[1]],'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'layers':[o.name.split('_')[-1] for o in obs]})
(out/'city-stream.json').write_text(json.dumps({'version':1,'origin_lon_lat':[127.046,37.738],'coordinates':'gltf x east, y up, z south; meters','attribution':'© OpenStreetMap contributors, ODbL; SRTM courtesy USGS via Mapzen/Tilezen','tiles':items},ensure_ascii=False,indent=2))
print('EXPORTED',len(items),sum(i['bytes'] for i in items))
