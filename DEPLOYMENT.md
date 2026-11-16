# Static web deployment

Cloudflare Workers Static Assets + native Workers Builds watches GitHub `main`. GitHub Actions is deliberately not used.

Build: `npm ci && npm run build` (the native build installs dependencies). Deploy: `npm run deploy` using pinned `cf` CLI.

`node build.mjs` produces only `web-dist/`, excludes source Blender files, photographs and credentials. Models are explicitly exported as `web/assets/station.glb`. Three.js and Draco decoders are locally served, not CDN dependencies. No tracking scripts, accounts, user input storage or backend data.

The browser viewer uses frustum culling, no real-time shadows, DPR caps, demand rendering when orbiting is inactive and stops animation when hidden. Quality button raises DPR. Existing Blender model uncertainty and source citations are available in the information dialog.

Custom hostname: `twin.uijeongbu.rhee.life`. No pre-existing DNS record found before setup. Cloudflare-issued certificate handled by Worker Custom Domain.
