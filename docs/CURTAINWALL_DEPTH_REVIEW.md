# Curtainwall review and frame-depth correction — 2026-11-17

## Evidence and scope
Photo 24 in https://zenith2.tistory.com/15862539 (visit 2025-03-23, published 2025-04-07) was fetched and visually inspected again. The east-side Hanwha building shows bronze reflective glazing, a narrow grid, a black upper band and rooftop identification. The existing specific facade, not every generic city building, already represents those components. The image is a reference, not a redistributed texture.

## Problem → action
Inspection of v18 found `Hanwha silver mullion`: 700 disconnected planar polygons, 2,800 vertices and no modifier. These decorative frame planes have no edge/return geometry. The correction preserves their front positions, the original glass grid, all other source meshes and materials. It adds a 60 mm shallow return behind the front and a 2 mm, two-segment edge bevel. Those depths are modeling estimates, NOT surveyed dimensions. Glass composition, rear elevations, room lighting and present-day tenancy remain unverified.

## Validation
Before/after renders use identical camera, frame, illumination and Cycles settings. Both were inspected; the after view shows frame edge highlights and returns without moving the window grid. Hashes of every original mesh vertex sequence are identical before and after; the two modifiers are applied only when exporting the frame. No claim of whole-city curtainwall completion or photorealistic optical calibration is made.

Export produces a new source GLB, so the previous collision bake cannot be used unchanged. Deployment must pair the new GLB with its matching rebaked collision manifest and run the existing concourse regression. Original v18 remains preserved. Blender renders are not browser screenshots. Follow-up checks must distinguish asset deployment from GPU browser verification.
