import bpy
from mathutils import Vector
s=bpy.context.scene;c=s.camera;frame=c.data.view_frame(scene=s);xmin=min(v.x for v in frame);xmax=max(v.x for v in frame);ymin=min(v.y for v in frame);ymax=max(v.y for v in frame);z=frame[0].z
for x,y in [(1100,750),(1100,700),(1000,800),(150,600)]:
 v=Vector((xmin+(x/1200)*(xmax-xmin),ymax-(y/850)*(ymax-ymin),z));direction=c.matrix_world.to_quaternion()@v
 r=s.ray_cast(bpy.context.evaluated_depsgraph_get(),c.matrix_world.translation,direction.normalized());print(x,y,r[4].name if r[0] else None,tuple(r[1]))
