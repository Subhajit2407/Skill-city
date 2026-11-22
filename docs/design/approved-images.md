# Skill City image design record

The user approved the image-based city, building, and agent-office style and explicitly replaced the earlier Three.js direction.

## Current design

The later request requires distinct artwork for every district. The current implementation uses 28 new images: one city homepage and nine triples of exterior, interior, and working-agent workspace. Each profession has its own architectural motif, equipment, outfit, and tools. All artwork is free of baked navigation and text. Real React controls supply the current catalog labels and the single bottom district dock.

`district-artwork.json` records each retained runtime asset, original generation path and SHA-256 hash. Original references are preserved in the user's generated-images folder. The old shared Marketing building/room copies were removed from runtime assets after verifying all 28 replacements.

The catalog currently contains 610 guides: 162 personal/built-in and 448 plugin guides. All can be searched or browsed through the appropriate district. Plugins are identified as guides with separately configured tools/connections. LinkedIn Roast remains in Documents, Shark Panel in Startup, Local Client Finder in Sales and Marketing Council in Marketing.

## Superseded reference set

- Original home style: exec-b54acab7-9357-4dac-93ed-75a7b5886e35.png
- Original Marketing building style: exec-47917472-7db5-475e-8b0f-3a3fb1483924.png
- Original room style: exec-14c03fb2-3cb9-4e94-aa8c-b79b1356a409.png

These remain reference history, not shared art for unrelated districts. This is an illustrated app; image characters are not autonomous executing agents.

## Verification

Production build, TypeScript, all 610 catalog route round trips, 28 unique artwork hashes, every district's exterior/interior/workspace flow, panel routes, clipboard, bookmark persistence, guide dismissal, search and mobile overflow checks passed. All 27 district images were also inspected together for profession-specific art. No canvas or WebGL dependency remains.
