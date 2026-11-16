# Street furniture v2

## Integration
`from street_furniture import add_street_furniture; report=add_street_furniture(repo_root)`
Reads existing `data/map.osm.gz`. Idempotent own collection `16_Street_furniture_OSM`. Main scene is untouched by QA. Fixtures batched by material into 8 meshes plus 6 text objects, 28 local downlights. Text font NotoSansCJK, pack fonts when saving. World origin longitude127.046 latitude37.738, xEast/yNorth, meters. Only ground-level objects. Road candidate selection excludes bridges, tunnels and cutting ramps.

## Evidence / verification
- OSM: 2 actual traffic_signals nodes (height=6m), 8 signalized crossing anchors, 28 street_lamp nodes, 35 tree anchors within existing scene boundary.
- Road names 시민로, 평화로, 신흥로 are read from OSM tags. Sign boards and their roadside positions are interpretive, not separately surveyed.
- https://zenith2.tistory.com/15862539 (2025-03-23 photos 22/23): directly inspected east station/Citizen Road street view. Slender dark poles and right-angle arms, black signal housings. Photo's foreground junction is not the two northerly OSM signal poles; do not claim exact photo correspondence.
- https://dldduxhrl.tistory.com/269 (2018-05-01): researcher inspected park lamp form; dated visual reference, not current inventory.
- Fixture proportions, arm orientation, near-road/park lamp style selection are approximations. No geographic claim of millimetric survey or exact current street furniture completeness.

## Rendering / z separation
Signal lenses offset 0.07m from housing, sign text offset beyond panel face 0.025m, lamp emitter below housing 0.015m, tree grates above path0.16m. No coplanar duplicate quads. Signals static and illustrative, red active only; not real traffic phase simulation.

## Web day/night
Material `Street lamp`: linear RGB(1,.72,.43), emission .05 at frame1; 2 at120; 5 at240. `Street red` RGB(.8,.025,.012), emission2 static. Amber/green are intentionally non-emissive. glTF export at day frame may discard emission curves: runtime needs explicit night material update. Spot lights `Street downlight <osm-id>`: warm RGB(1,.78,.53), 700W artistic render intensity at frame240, 0 at frame1, local -Z direction. On web cap active real-time lights to closest 4–8; keep all lamp meshes/emission visible. Do not enable 28 shadow maps. Fallback baked lighting preserves performance.

## Known limitations
Existing scene masses/road widths may differ from OSM fixture positioning. Do not move evidence-based nodes to match a guessed road mesh. Old lamp meshes may already be joined by earlier generators; duplicate removal by individual name is best-effort, integrator should remove prior illustrative lamp batch if duplicated. QA images are study copies, not proof of live deployment.
