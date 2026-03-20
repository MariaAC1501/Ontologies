$ErrorActionPreference = 'Stop'

$CondaRoot = if ($env:CONDA_ROOT) { $env:CONDA_ROOT } else { Join-Path $HOME 'miniforge3' }
$DefaultPrefix = Join-Path $CondaRoot 'envs\ontologies'
$EnvPrefix = if ($args.Length -gt 0) { $args[0] } else { $DefaultPrefix }
$CondaExe = Join-Path $CondaRoot 'condabin\conda.bat'

if (-not (Test-Path $CondaExe)) {
    throw "Conda not found at $CondaRoot"
}

& $CondaExe index (Join-Path $CondaRoot 'conda-bld')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $CondaExe create -y -p $EnvPrefix -c "file:///$($CondaRoot -replace '\\','/')/conda-bld" -c conda-forge ontologies-stack=0.1.0
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Created environment: $EnvPrefix"
Write-Host "Activate with: conda activate $EnvPrefix"
