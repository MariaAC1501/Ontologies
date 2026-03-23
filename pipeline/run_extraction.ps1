<#
.SYNOPSIS
  Run OntoCast fixed-ontology extraction on a PDF.
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File pipeline/run_extraction.ps1 example_paper.pdf
  powershell -ExecutionPolicy Bypass -File pipeline/run_extraction.ps1 example_paper.pdf 2
#>
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$PdfPath,

    [Parameter(Position=1)]
    [int]$HeadChunks = 3
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent $ScriptDir
$ConfigFile = Join-Path $ScriptDir "ontocast_config.env"
$OutputDir  = Join-Path $ScriptDir "test_output"
$InputDir   = Join-Path $OutputDir "input"
$LogFile    = Join-Path $OutputDir "run.log"

# Resolve PDF to absolute path
$PdfPath = (Resolve-Path $PdfPath).Path

if (-not (Test-Path $PdfPath)) {
    Write-Error "Input PDF not found: $PdfPath"
    exit 1
}

# Check ontocast is available
$OntocastBin = Get-Command ontocast -ErrorAction SilentlyContinue
if (-not $OntocastBin) {
    Write-Error "OntoCast CLI not found. Activate the Conda environment first: conda activate ontologies"
    exit 1
}

# Load .env
$EnvFile = Join-Path $RepoRoot ".env"
if (-not (Test-Path $EnvFile)) {
    Write-Error "Repo root .env not found: $EnvFile"
    exit 1
}
Get-Content $EnvFile | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim(), "Process")
    }
}
if (-not $env:OPENAI_API_KEY) {
    Write-Error "OPENAI_API_KEY is not set after loading $EnvFile"
    exit 1
}

# Prepare directories
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
New-Item -ItemType Directory -Force -Path $InputDir  | Out-Null
Remove-Item -Force -ErrorAction SilentlyContinue "$InputDir\*"
Copy-Item $PdfPath -Destination $InputDir
"" | Set-Content $LogFile

$PdfName = Split-Path -Leaf $PdfPath
Write-Host "Running OntoCast extraction"
Write-Host "  config: $ConfigFile"
Write-Host "  input:  $PdfPath"
Write-Host "  staged: $InputDir\$PdfName"
Write-Host "  output: $OutputDir"
Write-Host "  log:    $LogFile"
Write-Host "  chunks: $HeadChunks"

Push-Location $RepoRoot
try {
    $OldErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    # Execute through cmd.exe to prevent PowerShell from wrapping stderr in fatal ErrorRecords
    cmd.exe /c "ontocast --env-file `"$ConfigFile`" --input-path `"$InputDir`" --head-chunks $HeadChunks 2>&1" | Tee-Object -FilePath $LogFile -Append
} finally {
    $ErrorActionPreference = $OldErrorAction
    Pop-Location
}
