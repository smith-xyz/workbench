#!/usr/bin/env bash
set -euo pipefail

TEMPLATES_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-.vscode}"

templates=()
for f in "$TEMPLATES_DIR"/*.json; do
  [ -f "$f" ] || continue
  templates+=("$(basename "$f" .json)")
done

if [ ${#templates[@]} -eq 0 ]; then
  echo "No templates found in $TEMPLATES_DIR"
  exit 1
fi

if command -v fzf &>/dev/null; then
  choice=$(printf '%s\n' "${templates[@]}" | fzf --prompt="Select project template: ") || true
else
  echo "Available templates:"
  for i in "${!templates[@]}"; do
    echo "  $((i+1))) ${templates[$i]}"
  done
  read -rp "Choose [1-${#templates[@]}]: " num
  if ! [[ "$num" =~ ^[0-9]+$ ]] || [ "$num" -lt 1 ] || [ "$num" -gt ${#templates[@]} ]; then
    echo "Invalid selection."
    exit 1
  fi
  choice="${templates[$((num-1))]}"
fi

if [ -z "${choice:-}" ]; then
  echo "No selection made."
  exit 0
fi

mkdir -p "$TARGET"

if [ -f "$TARGET/settings.json" ]; then
  read -rp "$TARGET/settings.json exists. Overwrite? [y/N] " confirm
  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
  fi
fi

cp "$TEMPLATES_DIR/${choice}.json" "$TARGET/settings.json"
echo "Applied '$choice' template -> $TARGET/settings.json"
