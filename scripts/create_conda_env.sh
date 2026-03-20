#!/usr/bin/env bash
set -euo pipefail

CONDA_ROOT="${CONDA_ROOT:-$HOME/miniforge3}"
ENV_PREFIX="${1:-$CONDA_ROOT/envs/ontologies}"

if [ ! -f "$CONDA_ROOT/etc/profile.d/conda.sh" ]; then
  echo "Conda not found at $CONDA_ROOT" >&2
  exit 1
fi

source "$CONDA_ROOT/etc/profile.d/conda.sh"
conda activate base
conda index "$CONDA_ROOT/conda-bld"
conda create -y -p "$ENV_PREFIX" -c "file://$CONDA_ROOT/conda-bld" -c conda-forge ontologies-stack=0.1.0

echo "Created environment: $ENV_PREFIX"
echo "Activate with: conda activate $ENV_PREFIX"
