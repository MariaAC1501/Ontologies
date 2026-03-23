#!/usr/bin/env bash
set -euo pipefail

INSTALL_ROOT="$PREFIX/share/ontologies-pipeline"
INSTALL_PKG="$SP_DIR/ontologies_pipeline"

mkdir -p "$INSTALL_ROOT/seed_ontology" "$INSTALL_ROOT/tests" "$INSTALL_ROOT/full_mode" "$INSTALL_ROOT/comparison" "$INSTALL_PKG"

cp "$SRC_DIR/pipeline/__init__.py" "$INSTALL_PKG/__init__.py"
cp "$SRC_DIR/pipeline/extraction_schema.py" "$INSTALL_PKG/extraction_schema.py"
cp "$SRC_DIR/pipeline/facts_to_csv.py" "$INSTALL_PKG/facts_to_csv.py"

cp "$SRC_DIR/pipeline/__init__.py" "$INSTALL_ROOT/__init__.py"
cp "$SRC_DIR/pipeline/extraction_schema.py" "$INSTALL_ROOT/extraction_schema.py"
cp "$SRC_DIR/pipeline/facts_to_csv.py" "$INSTALL_ROOT/facts_to_csv.py"
cp "$SRC_DIR/pipeline/SCHEMA_MAPPING.md" "$INSTALL_ROOT/SCHEMA_MAPPING.md"
cp "$SRC_DIR/pipeline/ontocast_config.env" "$INSTALL_ROOT/ontocast_config.env"
cp "$SRC_DIR/pipeline/run_extraction.sh" "$INSTALL_ROOT/run_extraction.sh"
cp "$SRC_DIR/pipeline/run_extraction.ps1" "$INSTALL_ROOT/run_extraction.ps1"
cp "$SRC_DIR/pipeline/seed_ontology/opmad_seed.ttl" "$INSTALL_ROOT/seed_ontology/opmad_seed.ttl"
cp "$SRC_DIR/pipeline/tests/test_e2e.sh" "$INSTALL_ROOT/tests/test_e2e.sh"
cp "$SRC_DIR/pipeline/tests/test_facts_to_csv.py" "$INSTALL_ROOT/tests/test_facts_to_csv.py"

# Full mode
cp "$SRC_DIR/pipeline/full_mode/ontocast_full_config.env" "$INSTALL_ROOT/full_mode/ontocast_full_config.env"
cp "$SRC_DIR/pipeline/full_mode/run_full_extraction.sh" "$INSTALL_ROOT/full_mode/run_full_extraction.sh"
cp "$SRC_DIR/pipeline/full_mode/run_full_extraction.ps1" "$INSTALL_ROOT/full_mode/run_full_extraction.ps1"
cp "$SRC_DIR/pipeline/full_mode/sparql_query.py" "$INSTALL_ROOT/full_mode/sparql_query.py"
cp "$SRC_DIR/pipeline/full_mode/README.md" "$INSTALL_ROOT/full_mode/README.md"

# Comparison
cp "$SRC_DIR/pipeline/comparison/compare.py" "$INSTALL_ROOT/comparison/compare.py"
cp "$SRC_DIR/pipeline/comparison/run_comparison.sh" "$INSTALL_ROOT/comparison/run_comparison.sh"
cp "$SRC_DIR/pipeline/comparison/run_comparison.ps1" "$INSTALL_ROOT/comparison/run_comparison.ps1"

# Tests
cp "$SRC_DIR/pipeline/tests/test_regression.sh" "$INSTALL_ROOT/tests/test_regression.sh"
cp "$SRC_DIR/pipeline/tests/test_sparql_query.py" "$INSTALL_ROOT/tests/test_sparql_query.py"

chmod +x "$INSTALL_ROOT/run_extraction.sh" "$INSTALL_ROOT/tests/test_e2e.sh" \
         "$INSTALL_ROOT/full_mode/run_full_extraction.sh" \
         "$INSTALL_ROOT/comparison/run_comparison.sh" \
         "$INSTALL_ROOT/tests/test_regression.sh"
