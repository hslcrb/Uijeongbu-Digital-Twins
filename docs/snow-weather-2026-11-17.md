# Snow weather effect

User request: selectable falling snow while exploring the digital twin.

Implementation: a single 6,000-seed GPU point pool, with 2,400 flakes at normal quality and 6,000 at high quality. Camera-local volume scales between 26 and 500 world units so both street and overview navigation retain visible flakes. The existing day/sunset/night selection remains independent of weather. A keyboard-accessible Korean select controls clear/snow. Animation resumes only for active weather/rotation, caps weather drawing to roughly 30fps, and stops while the tab is hidden. Delta clamping avoids teleporting flakes after background suspension.

Physical scope: this is a visual snowfall effect, not snow accumulation, temperature or slippery-surface simulation. A camera-upward roof test every half second hides the local field under cover; existing depth testing masks flakes behind opaque geometry. It does not simulate individual flake collisions and cannot reproduce snow viewed through windows while the camera is indoors. No forecast or live weather claim.

Validation: settings/budgets/volume assertions; actual Three scene lifecycle, quality changes and roof sheltering; existing city-stream tests; JS syntax; full build, including restoration of 104 city tiles. Chromium visual smoke was attempted but the environment rejected Chromium's process-singleton socket, including the permitted escalated launch. GPU shader/appearance requires runtime visual validation before claiming it has been visually verified.
