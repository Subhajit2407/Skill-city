# Skill City

Image-based Next.js app with nine distinct districts and one live district navigation dock. No Three.js or WebGL.

## Run

Run `npm install`, `npm run build`, then `npm start`. Open http://127.0.0.1:4173.

## City and skills

Each district has three unique illustrations: exterior, interior, and a profession-specific Claude workspace. Enter a building to see twelve skill targets per floor; pagination and district search expose every guide in that district. Select an agent to see the actual skill command, overview, use cases, example prompts, save control, and guide. LinkedIn Roast is in Documents; Shark Panel is in Startup; Marketing Council is in Marketing; Local Client Finder is in Sales.

The catalog indexes 610 guides: 162 personal/built-in and 448 plugin guides from the latest cached plugin versions. Plugin labels identify their source; required tools and account connections must be configured separately. The local refresh endpoint rebuilds this catalog. Commands are copied into Codex, not executed by the web app. Artwork is illustrated, not independent live agents.

The homepage welcome is dismissible and automatically hides after ten seconds. Images contain no embedded navigation, leaving one actual bottom district menu.

## Files and verification

`src/app`: Next.js shell/API; `src/components/ui`: interface; `src/components/scene`: district artwork and hit targets; `src/lib`: routes/catalog types; `scripts/build_catalog.py`: catalog; `public/images/districts`: nine sets of three illustrations. `docs/design/district-artwork.json` records source paths and hashes. Original user references remain untouched.

Run `npm run check`, `npm run typecheck`, `npm run build`; then `CITY_URL=http://127.0.0.1:4173 npm run test:browser` and `node checks/district-art.mjs` with the app running. Browser checks use local Chrome.

## Responsive layout and branding

Desktop artwork and inspector sit side by side; tablet/mobile pages stack them. Images and Claude targets share the same fitted artboard. The welcome notice supports dismissal, remembers it, and automatically hides after ten seconds. The generated Skill City logo is used in the header and browser icon. Run `node checks/responsive.mjs` to check eight viewport sizes and welcome behavior.

The bundled catalog works without a local Codex installation. Refreshing it requires Python 3 and locally installed skills under `$CODEX_HOME` (defaults to `~/.codex`); configure plugin tools separately.
