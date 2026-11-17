# Fictional cab interaction, 2026-11-17

## Scope and design choice
The user requested fewer overlay buttons and direct door/cab interaction. This iteration adds one clearly turquoise, fictional single-car training vehicle at the selected route station, alongside the autonomous fleet. It is NOT a faithful train simulator, not instructions to operate real equipment, and not a replacement of every fleet train's passenger interior.

Click the turquoise door within 18 metres to open it, click again to board the vestibule, then click the cab door. Three coloured world controls are power, brake, and doors. Keyboard alternatives: aim at interaction and E; in cab W power, S brake, X coast, O doors, R direction, Esc disembark. Minimal status text remains for discoverability. Home/city navigation safely resets the experience.

## Mechanics
Position integrates a fictional acceleration/braking model on actual sampled route geometry. Velocity is bounded, frame delta capped. Doors can only operate while stopped and within 3 metres of a sourced station's route coordinate. Open doors prevent traction. A simple glass screen-door representation at the currently nearest station follows the same door state. No real screen-door location, dimensions, safety certification, or signalling is asserted.

## Limits
Only the training vehicle and its one nearest-station gate are interactive. Existing platform screen doors are not comprehensively reconstructed; gate placement is approximate. Other trains continue their illustrative schedule and do not perform collision avoidance against the training car. Cab camera is a fixed forward view, and click boarding is a game transition, not continuous walking aboard a physically simulated moving carriage. Endpoints stop the car. Route grade remains the application's existing approximation. World UI remains elsewhere; this feature does not claim all overlay controls have been eliminated.

## Tests
Pure state tests cover blocked boarding, cab sequence, door/traction interlock, motion lock, platform alignment, endpoints, and bounded long-frame integration. Full project tests and build run. GPU interaction quality still requires a browser with functional WebGL; not claimed verified here.
