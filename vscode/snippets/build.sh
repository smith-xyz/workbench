#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src"

for lang_dir in "$SRC_DIR"/*/; do
  lang=$(basename "$lang_dir")
  out="$SCRIPT_DIR/$lang.json"

  python3 - "$lang_dir" "$out" "$lang" << 'PYEOF'
import json, glob, sys, os

lang_dir = sys.argv[1]
out = sys.argv[2]
lang = sys.argv[3]

merged = {}
files = sorted(glob.glob(os.path.join(lang_dir, '*.json')))
for f in files:
    d = json.load(open(f))
    dupes = set(merged.keys()) & set(d.keys())
    if dupes:
        print(f'WARNING: duplicate keys in {os.path.basename(f)}: {dupes}', file=sys.stderr)
    merged.update(d)

with open(out, 'w') as o:
    json.dump(merged, o, indent='\t')
    o.write('\n')

print(f'  {lang}.json: {len(merged)} snippets (from {len(files)} files)')
PYEOF
done
