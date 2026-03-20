#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CBR_DIR="$ROOT_DIR/external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject"
BUILD_DIR="$ROOT_DIR/.build/cbr"
UPSTREAM_BIN="$BUILD_DIR/upstream-bin"
LOCAL_BIN="$BUILD_DIR/local-bin"

mkdir -p "$UPSTREAM_BIN" "$LOCAL_BIN"

CLASSPATH=$(find "$CBR_DIR/external-libs" -name '*.jar' | sort | paste -sd: -)

find "$CBR_DIR/src" -name '*.java' | sort > "$BUILD_DIR/upstream-sources.txt"

javac \
  -encoding ISO-8859-1 \
  -cp "$CLASSPATH" \
  -d "$UPSTREAM_BIN" \
  @"$BUILD_DIR/upstream-sources.txt"

javac \
  -encoding UTF-8 \
  -cp "$UPSTREAM_BIN:$CLASSPATH" \
  -d "$LOCAL_BIN" \
  "$ROOT_DIR/tools/cbr/HeadlessCBR.java"

printf '%s\n' "$LOCAL_BIN:$UPSTREAM_BIN:$CLASSPATH" > "$BUILD_DIR/classpath.txt"

echo "Built CBR classes"
echo "  upstream: $UPSTREAM_BIN"
echo "  local:    $LOCAL_BIN"
echo "  cp file:  $BUILD_DIR/classpath.txt"
