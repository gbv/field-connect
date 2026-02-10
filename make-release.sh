#!/usr/bin/env bash
# Creates a distributable plugin ZIP and optionally adds a version tag

PLUGIN_NAME="field_connect"
VERSION=$(grep -E "^version=" metadata.txt | cut -d'=' -f2 | tr -d ' ')

if [ -z "$VERSION" ]; then
  echo "❌ Could not read version from metadata.txt"
  exit 1
fi

# --- Output ZIP in plugin folder ---
ZIPFILE="$(pwd)/${PLUGIN_NAME}-v${VERSION}.zip"

# Create temp dir safely
TMPDIR=$(mktemp -d)
echo "📁 Using temporary directory: $TMPDIR"

cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Export plugin to temp folder
git archive --format=tar --prefix="${PLUGIN_NAME}/" HEAD | tar -x -C "$TMPDIR"

# Strip # comments but keep docstrings, shebangs, and spacing
echo "🧹 Stripping comments from Python files..."
find "$TMPDIR/$PLUGIN_NAME" -name "*.py" | while read -r file; do
  sed -i -E '
    /^\s*#/d        # delete full-line comments
    s/\s+#.*$//     # strip inline comments
  ' "$file"
done

# Create final ZIP in plugin folder
echo "📦 Creating release archive: $ZIPFILE"
(cd "$TMPDIR" && zip -r "$ZIPFILE" "$PLUGIN_NAME")
echo "✅ Archive created: $ZIPFILE"

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
