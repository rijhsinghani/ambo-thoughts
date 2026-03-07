#!/bin/bash
# convert-heic.sh — Batch convert HEIC images to JPEG using macOS sips
# Usage: ./scripts/convert-heic.sh <input-directory> <output-directory>

set -euo pipefail

INPUT_DIR="${1:?Usage: $0 <input-dir> <output-dir>}"
OUTPUT_DIR="${2:?Usage: $0 <input-dir> <output-dir>}"

if [ ! -d "$INPUT_DIR" ]; then
  echo "ERROR: Input directory does not exist: $INPUT_DIR"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

count=0
total=$(find "$INPUT_DIR" -iname "*.heic" | wc -l | tr -d ' ')

if [ "$total" -eq 0 ]; then
  echo "No HEIC files found in $INPUT_DIR"
  exit 0
fi

echo "Found $total HEIC file(s) in $INPUT_DIR"
echo "Converting to JPEG in $OUTPUT_DIR ..."
echo ""

find "$INPUT_DIR" -iname "*.heic" | while IFS= read -r f; do
  basename_noext=$(basename "$f" | sed 's/\.[hH][eE][iI][cC]$//')
  # Replace spaces with hyphens for web-friendly filenames
  outname=$(echo "$basename_noext" | tr ' ' '-')
  outpath="$OUTPUT_DIR/${outname}.jpg"

  count=$((count + 1))
  echo "[$count/$total] Converting: $(basename "$f") -> ${outname}.jpg"
  sips -s format jpeg "$f" --out "$outpath" >/dev/null 2>&1
done

echo ""
echo "Done. Converted $total file(s) to $OUTPUT_DIR"
