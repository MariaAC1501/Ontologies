#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
BUILD_DIR="$ROOT_DIR/.build/cbr"

"$ROOT_DIR/scripts/build_cbr.sh" >/dev/null
CLASSPATH=$(<"$BUILD_DIR/jar-classpath.txt")

java -Djava.awt.headless=true -cp "$CLASSPATH" HeadlessCBR "$@"
