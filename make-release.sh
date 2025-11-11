#!/usr/bin/env bash
# Creates a distributable plugin ZIP and optionally adds a version tag

PLUGIN_NAME="field_connect"
VERSION=$(grep -E "^version=" metadata.txt | cut -d'=' -f2 | tr -d ' ')

if [ -z "$VERSION" ]; then
  echo "❌ Could not read version from metadata.txt"
  exit 1
fi

ZIPFILE="${PLUGIN_NAME}-v${VERSION}.zip"

echo "📦 Creating release archive: $ZIPFILE"
git archive --format=zip --output="$ZIPFILE" --prefix="${PLUGIN_NAME}/" HEAD
echo "✅ Archive created."

# --- Optional tagging ---
# echo ""
# read -p "🏷️  Create a Git tag 'v${VERSION}' and push it? [y/N] " answer
# if [[ "$answer" =~ ^[Yy]$ ]]; then
#   git tag -a "v${VERSION}" -m "Release version ${VERSION}"
#   git push origin "v${VERSION}"
#   echo "✅ Tag 'v${VERSION}' created and pushed."
# else
#   echo "ℹ️  Skipped tagging."
# fi
