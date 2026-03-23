#!/usr/bin/env bash
set -euo pipefail

WHEEL_DIR="$RECIPE_DIR/wheels"

install_pkg() {
  "$PYTHON" -m pip install --no-deps --no-index --find-links "$WHEEL_DIR" "$@"
}

install_pkg "$WHEEL_DIR/ontocast-0.3.0-py3-none-any.whl"
install_pkg "$WHEEL_DIR/neo4j-6.1.0-py3-none-any.whl"
install_pkg "$WHEEL_DIR/duckduckgo_search-8.1.1-py3-none-any.whl"
install_pkg "$WHEEL_DIR/suthing-0.5.1-py3-none-any.whl"
"$PYTHON" "$RECIPE_DIR/patch_ontocast.py"

if [[ "${target_platform:-}" == osx-* ]]; then
  install_pkg "$WHEEL_DIR/primp-0.15.0-cp38-abi3-macosx_11_0_arm64.whl"
  install_pkg "$WHEEL_DIR/robyn-0.81.0-cp312-cp312-macosx_10_12_x86_64.macosx_11_0_arm64.macosx_10_12_universal2.whl"
  install_pkg "$WHEEL_DIR/simsimd-6.5.16-cp312-cp312-macosx_11_0_arm64.whl"
elif [[ "${target_platform:-}" == linux-* ]]; then
  install_pkg "$WHEEL_DIR/primp-0.15.0-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
  install_pkg "$WHEEL_DIR/robyn-0.81.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
  install_pkg "$WHEEL_DIR/simsimd-6.5.16-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl"
else
  echo "Unsupported target_platform for build.sh: ${target_platform:-unknown}" >&2
  exit 1
fi
