# Context facade bay direction correction

## Verified defects
- Original generator assumed `poly.normal` was outward. 220 of 493 retained context extrusion footprints were clockwise: the roof normal was -Z and a nominal inward room bay was extruded into the street.
- Correcting winding alone did not remove all protrusions. The comparison render still showed boxes on a shallow frontage. OSM building:part footprints include thin strips; an unconditional 0.9m bay can cross the opposite edge.

## Correction
1. Restore the original retained cap outline, preserving object/material identities and heights; orient the footprint CCW. This works for concave simple rings without assuming the centroid lies inside the footprint.
2. Rebuild derived room proxies once, not on top of old geometry. The photographed Hanwha collection is untouched and its removed generic context object is not recreated.
3. For each potential window, cast inward rays at its left/center/right positions against its own footprint boundary. Bay depth is the smaller of 0.9m and 45% of the minimum boundary distance. If less than 0.08m, preserve an opaque wall cell rather than invent an impossible room.
4. Keep the existing material batching and offset glazing/mullions. No extra objects/draw calls are needed.

## Verification
- 493 context building footprints inspected, 220 winding corrections.
- 489 building polygon counts unchanged; 4 very thin objects retain wall cells instead of 36 impossible bays.
- 16,135 generated windows in 319 buildings. Prior scene statistic 16,459 was stale and included 288 generic Hanwha windows already removed by the specific enhancement.
- All restored roof normals point +Z. Hanwha-specific facade collection preserved.
- Cycles before/after, camera (250,10,21) aimed at (220,50,0), 1000×750, same lighting/frame: directly inspected. Both right-side protrusions and remaining center-front cubes are gone.
- `before.png`, `after.png`, `validation.json` and a separate `corrected.blend` supplied.

## Integration
Copy `fix_window_normals.py` and `building_lighting_corrected.py` together into the repo scripts directory. After existing facade enhancements, call `fix_window_normals(repo_scripts_path)`. It is idempotent via scene marker `window_normal_fix_v1`. For a fresh build, use the corrected generator instead of the old `building_lighting` generator to prevent recurrence.

## Limits
This is a verified geometry defect fix, not evidence of real window spacing, occupancy, room depth or measured facade appearance. Those properties remain procedural. Complex overlapping OSM parts may still require source-data cleanup. Real WebGL visual QA remains separate from these Blender renders.
