"""Align inherited plaza posts with the existing 11m deck, not beneath it."""
import bpy,math

def correct_platform_lights(col):
 xs=(-30,-12,16,35);removed=0
 for o in bpy.data.objects:
  if o.type!='MESH' or not o.name.startswith('Batched 03_Station'):continue
  faces=[]
  for p in o.data.polygons:
   pts=[o.matrix_world@o.data.vertices[i].co for i in p.vertices]
   hit=any(all(abs(v.x-x)<.12 and abs(v.y-30)<.12 and 5.9<v.z<11.1 for v in pts) for x in xs)
   if hit:removed+=1
   else:faces.append((tuple(p.vertices),p.material_index))
  if len(faces)<len(o.data.polygons):
   me=bpy.data.meshes.new('Platform post corrected');me.from_pydata([tuple(v.co) for v in o.data.vertices],[],[f[0] for f in faces]);
   for m in o.data.materials:me.materials.append(m)
   for p,(_,mi) in zip(me.polygons,faces):p.material_index=mi
   o.data=me
 for o in bpy.data.objects:
  if o.type=='CURVE' and o.name.startswith('Plaza light disc') and not o.get('v7_deck_aligned'):
   o.location.z+=4.05;o['v7_deck_aligned']=True
 mat=bpy.data.materials['West photographed pale celadon steel']
 for x in xs:
  vs=[(x+.08*math.cos(j*math.tau/8),30+.08*math.sin(j*math.tau/8),z) for z in (11.05,15.05) for j in range(8)]
  fs=[tuple(range(7,-1,-1)),tuple(range(8,16))]+[(j,(j+1)%8,(j+1)%8+8,j+8) for j in range(8)]
  me=bpy.data.meshes.new('Deck supported lamp');me.from_pydata(vs,[],fs);me.materials.append(mat);o=bpy.data.objects.new('Deck supported lamp post',me);col.objects.link(o)
 return {'removedUnderDeckPostFaces':removed,'newBaseZ':11.05,'newHeadZ':15.05,'height':'inferred relative to existing deck, not surveyed'}
