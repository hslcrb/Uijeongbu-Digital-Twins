# Railway visual detail study

## Source and mapping
- Existing OSM `data/map.osm.gz`, origin longitude 127.046, latitude 37.738, x east/y north.
- OSM rail ways use `railway=rail`, gauge 1435 tags. Light rail is not treated as the same railway.
- Platforms: 624679785–624679790. These are six platform-edge areas forming three islands, not six separate islands.
- Existing station/road model must resolve rail elevation with its shared ground datum. Current height is illustrative, not surveyed.

## Implementation
- Rail offsets are computed normal to each segment, unlike previous constant x-offset lines.
- Two-part metal rail profile, aggregate concrete sleepers, ballast, simple contact wire only where electrified=contact_line.
- Platform polygons retain source coordinates. Safety edge strips, supports and canopy are illustrative, not measured reconstruction.
- Material batches keep object count low.
- No train model, real train timetable or signalling semantics inferred.

## Visual evidence limits
Image search found a Kyeongin image showing signs pointing toward Uijeongbu, so it is NOT proof of Uijeongbu Station's own platform geometry. It was inspected but not used as site-specific source. Dedicated researcher is supplying actual station photos. Exact canopy, platform screen doors and elevation require subsequent source matching.

## Validation
Blender 5.2.4 Cycles executed successfully. 105 segment bodies, 5,872 sleepers, three merged platform islands, seven material-batched objects. Preview rail-study.png was inspected. This is an isolated geometry QA render, not a finished station view. Canopy width subsequently adjusted to 6.2m as visual approximation.

## Pass 5
`enhance_rail_bed.py` adds 24,821 angular procedural chips and 11,744 rectangular rail baseplates in six material batches. It assigns a packed 512px original generated ballast texture with explicit UV coordinates so glTF export does not depend on Blender procedural shading. Not a photographic CC0 asset; no external texture claimed. `generate_ballast_texture.py` reproduces it using Pillow. Rail fasteners are simplified baseplates, not exact measured clip replicas. Cycles render verified. Tile density/stone counts are decorative approximations and must not be described as field measurements. All generated closed meshes have recalculated outward normals.
