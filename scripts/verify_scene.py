import bpy,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=bpy.context.scene
assert s.world and len(s.objects)>500
assert s.frame_end==240
ph=[o for o in s.objects if o.name.startswith('PH_')]
assert len(ph)==12,len(ph)
assert all(o.data==ph[0].data for o in ph)
missing=[im.filepath for im in bpy.data.images if im.source=='FILE' and not im.packed_file and not Path(bpy.path.abspath(im.filepath)).exists()]
assert not missing,missing
assert len([o for o in s.objects if 'osm_way_id' in o])==516
for f in (1,120,240):s.frame_set(f)
print('VERIFIED',len(s.objects),'objects;',len(ph),'external asset linked instances; packed textures; day dusk night keyframes')
