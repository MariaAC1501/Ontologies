$ErrorActionPreference = 'Stop'

$CondaRoot = if ($env:CONDA_ROOT) { $env:CONDA_ROOT } else { Join-Path $HOME 'miniforge3' }
$CondaExe = Join-Path $CondaRoot 'condabin\conda.bat'

if (-not (Test-Path $CondaExe)) {
    throw "Conda not found at $CondaRoot"
}

& $CondaExe build conda/recipes/ontologies-cbr
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $CondaExe build conda/recipes/ontocast
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $CondaExe build conda/recipes/ontologies-stack
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $CondaExe index (Join-Path $CondaRoot 'conda-bld')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Built packages in: $(Join-Path $CondaRoot 'conda-bld')"
