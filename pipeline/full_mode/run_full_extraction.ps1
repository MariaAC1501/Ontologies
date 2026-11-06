<#
.SYNOPSIS
  Run OntoCast full ontology-evolution extraction on a PDF.
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File pipeline/full_mode/run_full_extraction.ps1 example_paper.pdf
  powershell -ExecutionPolicy Bypass -File pipeline/full_mode/run_full_extraction.ps1 example_paper.pdf 2
#>
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$PdfPath,

    [Parameter(Position=1)]
    [int]$HeadChunks = 0
)

$ErrorActionPreference = "Stop"
if ($HeadChunks -lt 0) {
    Write-Error "HeadChunks must be zero (complete document) or a positive development limit."
    exit 2
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$ConfigFile = Join-Path $ScriptDir "ontocast_full_config.env"
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
    Write-Error "OntoCast CLI not found. Activate the repo venv and run the submodule setup first: .\.venv\Scripts\Activate.ps1; .\scripts\setup_submodules.ps1"
    exit 1
}

# Load optional .env for subscription-proxy settings only.
$EnvFile = Join-Path $RepoRoot ".env"
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim(), "Process")
        }
    }
}

$SubscriptionProxyBase = if ($env:LLM_BASE_URL) { $env:LLM_BASE_URL } else { "http://127.0.0.1:8977/v1" }
python (Join-Path $RepoRoot "pipeline/subscription_proxy.py") --base-url $SubscriptionProxyBase
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
# Non-secret SDK placeholder; the local proxy authenticates with Pi subscription OAuth.
$env:LLM_PROVIDER = "openai"
$env:LLM_API_KEY = "subscription-proxy"
$env:LLM_BASE_URL = $SubscriptionProxyBase
$env:ONTOLOGY_CRITIC_PASSES = "0"

# Prepare directories
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
New-Item -ItemType Directory -Force -Path $InputDir  | Out-Null
Remove-Item -Force -ErrorAction SilentlyContinue "$OutputDir\*.ttl","$OutputDir\*.json","$OutputDir\*.jsonl","$OutputDir\*.log","$InputDir\*"
Copy-Item $PdfPath -Destination $InputDir
"" | Set-Content $LogFile

$PdfName = Split-Path -Leaf $PdfPath
Write-Host "Running OntoCast full-mode extraction"
Write-Host "  config: $ConfigFile"
Write-Host "  input:  $PdfPath"
Write-Host "  staged: $InputDir\$PdfName"
Write-Host "  output: $OutputDir"
Write-Host "  log:    $LogFile"
if ($HeadChunks -gt 0) {
    Write-Host "  chunks: first $HeadChunks (development limit)"
    $ChunkArgument = " --head-chunks $HeadChunks"
} else {
    Write-Host "  chunks: complete document"
    $ChunkArgument = ""
}
Write-Host "  llm:    Pi Codex subscription proxy ($SubscriptionProxyBase)"

Push-Location $RepoRoot
try {
    $OldErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    # Execute through cmd.exe to prevent PowerShell from wrapping stderr in fatal ErrorRecords
    cmd.exe /c "ontocast --env-file `"$ConfigFile`" process --input-path `"$InputDir`" --output-dir `"$OutputDir`" --keep-provenance --exclude-sections `"`"$ChunkArgument 2>&1" | Tee-Object -FilePath $LogFile -Append
    $OntocastExitCode = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $OldErrorAction
    Pop-Location
}
if ($OntocastExitCode -ne 0) { exit $OntocastExitCode }

# Verify outputs
$OntologyFiles = Get-ChildItem "$OutputDir\*.ontology.ttl" -ErrorAction SilentlyContinue
$FactsFiles    = Get-ChildItem "$OutputDir\*.facts.ttl" -ErrorAction SilentlyContinue

if (-not $OntologyFiles) {
    Write-Error "No evolved ontology TTL found in $OutputDir"
    exit 1
}
if (-not $FactsFiles) {
    Write-Error "No facts TTL found in $OutputDir"
    exit 1
}

Write-Host ""
Write-Host "Full-mode extraction completed"
$OntologyFiles | ForEach-Object { Write-Host "  ontology: $_" }
$FactsFiles    | ForEach-Object { Write-Host "  facts:    $_" }
