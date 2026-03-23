#!/usr/bin/env bash
set -euo pipefail

CONDA_ROOT="${CONDA_ROOT:-$HOME/miniforge3}"
if [ ! -f "$CONDA_ROOT/etc/profile.d/conda.sh" ]; then
  echo "Conda not found at $CONDA_ROOT" >&2
  exit 1
fi

source "$CONDA_ROOT/etc/profile.d/conda.sh"
conda activate base

conda build conda/recipes/ontologies-cbr
conda build conda/recipes/ontocast
conda build conda/recipes/ontologies-pipeline
conda build conda/recipes/ontologies-stack
conda index "$CONDA_ROOT/conda-bld"

echo "Built packages in: $CONDA_ROOT/conda-bld"
