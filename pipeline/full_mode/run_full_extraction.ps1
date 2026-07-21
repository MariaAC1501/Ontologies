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
    [int]$HeadChunks = 2
)

$ErrorActionPreference = "Stop"

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

if ($env:OPENAI_API_KEY -or $env:LLM_API_KEY) {
    Write-Error "Direct OpenAI API keys are disabled for this workflow. Use the local Pi Codex subscription proxy instead: node tools/pi_codex_openai_proxy.mjs"
    exit 1
}

$SubscriptionProxyBase = if ($env:LLM_BASE_URL) { $env:LLM_BASE_URL } else { "http://127.0.0.1:8977/v1" }
$SubscriptionProxyHealthBase = $SubscriptionProxyBase.TrimEnd('/') -replace '/v1$',''
$SubscriptionProxyHealth = "$SubscriptionProxyHealthBase/health"
try {
    Invoke-RestMethod -Uri $SubscriptionProxyHealth -TimeoutSec 5 | Out-Null
} catch {
    Write-Error "Subscription proxy is not reachable at $SubscriptionProxyHealth. Start it with: node tools/pi_codex_openai_proxy.mjs"
    exit 1
}

# Prepare directories
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
New-Item -ItemType Directory -Force -Path $InputDir  | Out-Null
Remove-Item -Force -ErrorAction SilentlyContinue "$OutputDir\*.ttl","$OutputDir\*.json","$OutputDir\*.log","$InputDir\*"
Copy-Item $PdfPath -Destination $InputDir
"" | Set-Content $LogFile

$PdfName = Split-Path -Leaf $PdfPath
Write-Host "Running OntoCast full-mode extraction"
Write-Host "  config: $ConfigFile"
Write-Host "  input:  $PdfPath"
Write-Host "  staged: $InputDir\$PdfName"
Write-Host "  output: $OutputDir"
Write-Host "  log:    $LogFile"
Write-Host "  chunks: $HeadChunks"
Write-Host "  llm:    Pi Codex subscription proxy ($SubscriptionProxyBase)"

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

# Verify outputs
$OntologyFiles = Get-ChildItem "$OutputDir\ontology_*.ttl" -ErrorAction SilentlyContinue
$FactsFiles    = Get-ChildItem "$OutputDir\facts_*.ttl" -ErrorAction SilentlyContinue

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
