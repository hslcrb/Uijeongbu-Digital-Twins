# In-world scheduled-fleet cab interaction, 2026-11-17

## Current scope (supersedes the separate training car)
The separate single-car training vehicle has been removed. Every generated scheduled train gets a turquoise boarding marker on its first car. The marker appears only while the train is stopped and close to the camera. Clicking within 18 metres takes control of that exact existing train; a second click boards, and the cab door enters the simplified cab. The existing whole consist follows the player's route distance and car-by-car curve transforms. Other trains retain their automatic simulation.

The game gives direct in-world controls rather than a drive button: green power, red brake, yellow doors. Keyboard alternatives: aim at the marker and E, then W power, S brake, X coast, O doors, R direction, Escape disembark. Home/city resets release the train. Cab mode hides unrelated controls. Camera transitions are a game concession, not continuous walking physics inside a moving carriage.

## State and schedule
Manual override lives on the existing train object, not a cloned vehicle. Opening the boarding marker freezes the stopped train. Doors can only open while stopped and within 3m of the nearest station's route distance; open doors block power. On release, the automatic loop gets a per-train time offset matching the current distance/direction, preventing a teleport back to the old timetable. Automatic ETA panels omit manually controlled trains (their future arrival is unknown) and use adjusted offsets after handback.

## Screen door and visual limitations
One illustrative nearby platform screen door follows the active train's door state. It is not a reconstruction of every station's screen doors. The turquoise overlay visibly shifts, but the procedural stock's original merged door/body geometry is not fully remodelled into independently animated door leaves. Thus boarding is an interaction/camera transition rather than a physically opened accurate aperture. Interior furnishings and console are generic. Exact real controls, interlocking, signals, collision avoidance between trains, and continuous passenger movement aboard are not implemented. No real-world operating instructions are represented.

## Validation
44 tests and build passed: existing fleet override, position-continuous handback, manual ETA exclusion, actual Three scene binding, boarding/cab flow, door/traction locks, route endpoint bounds, and existing world/rail/physics regressions. GPU visual/interaction QA still requires functional WebGL and is not claimed complete.

## Conservative game spacing, next iteration
All visible automatic and manual trains now share a proximity guard before their positions are applied. It compares swept horizontal centre paths with a conservative radius based on each whole consist's length plus a margin; elevation-separated layers are ignored. On conflict both stop for the current step, manual power is cleared, and automatic phase offsets are held instead of jumping through the obstruction. Repeated checks propagate a stop through following trains. Initially overlapping automatic spawns are temporarily hidden and held until space opens. ETA panels exclude held trains, since release time is unknown.

This is deliberately NOT a real signal/interlocking system, braking-distance simulation, track circuit, or guarantee of real railway safety. Whole-consist circles can stop trains on nearby parallel tracks unnecessarily; opposing trains sharing a simplified single centreline can remain waiting and need a player's reversal. Hidden conflicting spawns reduce visible fleet count. Collision meshes and precise coupler contact are not simulated. These limitations avoid falsely promising an operational traffic control system.

### Review correction: narrow collision shapes and automatic dispatch yield
Whole-train circles were rejected in review: they incorrectly stopped parallel tracks and caused the simplified shared centreline fleet to deadlock. They are now only a broad phase. The narrow phase uses each car's longitudinal capsule width, swept convex hulls in route-distance intervals no larger than 5m, and includes an explicit 4m-parallel-track regression.

Automatic trains do not both stop indefinitely at a shared-centreline conflict. The lower-priority automatic consist is temporarily removed from the visible simulation and its phase held until it can re-enter without overlap. Player-occupied trains take priority. Two player-occupied trains still stop. This is a disclosed game dispatch approximation: an automatic train may disappear temporarily mid-route; no physical passing manoeuvre, real signal block, siding, or accurate timetable is claimed. It prevents the previous all-fleet freeze without pretending a fully modelled bidirectional track network exists.
