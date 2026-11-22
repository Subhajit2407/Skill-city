#!/bin/zsh
cd "$(dirname "$0")" || exit 1
if [[ ! -d node_modules ]]; then npm install || exit 1; fi
if [[ ! -f .next/BUILD_ID ]]; then npm run build || exit 1; fi
open 'http://127.0.0.1:4173'
npm start
