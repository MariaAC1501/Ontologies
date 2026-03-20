#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$SRC_DIR"
CBR_PROJECT_DIR="$REPO_ROOT/external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject"
INSTALL_ROOT="$PREFIX/share/ontologies-cbr"
INSTALL_LIB="$INSTALL_ROOT/lib"
INSTALL_DATA="$INSTALL_ROOT/data"
INSTALL_BIN="$PREFIX/bin"

bash "$REPO_ROOT/scripts/build_cbr.sh"

mkdir -p "$INSTALL_ROOT" "$INSTALL_LIB" "$INSTALL_DATA" "$INSTALL_BIN"

cp "$REPO_ROOT/.build/cbr/dist/ontologies-cbr-headless.jar" "$INSTALL_ROOT/ontologies-cbr-headless.jar"
find "$CBR_PROJECT_DIR/external-libs" -name '*.jar' -exec cp {} "$INSTALL_LIB/" \;
cp -R "$CBR_PROJECT_DIR/data/." "$INSTALL_DATA/"

cat > "$INSTALL_BIN/ontologies-cbr" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
PREFIX_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CBR_HOME="$PREFIX_DIR/share/ontologies-cbr"
CBR_DATA_DIR="${ONTOLOGIES_CBR_DATA_DIR:-$CBR_HOME/data}"

java -Djava.awt.headless=true \
  -cp "$CBR_HOME/ontologies-cbr-headless.jar:$CBR_HOME/lib/*" \
  HeadlessCBR \
  --data-dir "$CBR_DATA_DIR" \
  "$@"
EOF

chmod +x "$INSTALL_BIN/ontologies-cbr"
