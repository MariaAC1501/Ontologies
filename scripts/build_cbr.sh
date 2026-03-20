#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CBR_DIR="$ROOT_DIR/external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject"
BUILD_DIR="$ROOT_DIR/.build/cbr"
UPSTREAM_BIN="$BUILD_DIR/upstream-bin"
LOCAL_BIN="$BUILD_DIR/local-bin"
DIST_DIR="$BUILD_DIR/dist"
JAR_PATH="$DIST_DIR/ontologies-cbr-headless.jar"

rm -rf "$UPSTREAM_BIN" "$LOCAL_BIN"
mkdir -p "$UPSTREAM_BIN" "$LOCAL_BIN" "$DIST_DIR"

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

jar --create --file "$JAR_PATH" -C "$UPSTREAM_BIN" . -C "$LOCAL_BIN" .

printf '%s\n' "$LOCAL_BIN:$UPSTREAM_BIN:$CLASSPATH" > "$BUILD_DIR/classpath.txt"
printf '%s\n' "$JAR_PATH:$CLASSPATH" > "$BUILD_DIR/jar-classpath.txt"

echo "Built CBR classes and jar"
echo "  upstream:      $UPSTREAM_BIN"
echo "  local:         $LOCAL_BIN"
echo "  jar:           $JAR_PATH"
echo "  cp file:       $BUILD_DIR/classpath.txt"
echo "  jar cp file:   $BUILD_DIR/jar-classpath.txt"
