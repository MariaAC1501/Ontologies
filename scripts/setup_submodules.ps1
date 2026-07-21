$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$Python = if ($env:PYTHON) { $env:PYTHON } else { 'python' }

& $Python (Join-Path $RootDir 'scripts\install_submodule_stack.py') @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
