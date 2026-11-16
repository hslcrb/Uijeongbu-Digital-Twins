import bpy
from mathutils import Vector
for n in ['East elevation individual pale panels','OSM building [1330839990]']:
 o=bpy.data.objects[n];print(n,'loc',o.location,'rot',o.rotation_euler)
 print('verts',[tuple(round(x,3) for x in o.matrix_world@v.co) for v in o.data.vertices[:24]])
for c in bpy.data.objects:
 if c.type=='CAMERA':print('camera',c.name,list(c.location))
