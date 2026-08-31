<#
.SYNOPSIS
  Prepare and run one complete-document publication extraction.
.EXAMPLE
  .\pipeline\run_complete_extraction.ps1 fixed corpus\manifest.json paper-0001 runs\paper-0001
#>
param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet("fixed", "evolved")]
    [string]$Condition,

    [Parameter(Mandatory=$true, Position=1)]
    [string]$Manifest,

    [Parameter(Mandatory=$true, Position=2)]
    [string]$CorpusId,

    [Parameter(Mandatory=$true, Position=3)]
    [string]$RunDir,

    [switch]$PrepareOnly
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$Arguments = @(
    "-m", "pipeline.fulltext_run",
    "--condition", $Condition,
    "--manifest", $Manifest,
    "--corpus-id", $CorpusId,
    "--run-dir", $RunDir
)
if ($PrepareOnly) {
    $Arguments += "--prepare-only"
}

Push-Location $RepoRoot
try {
    & python @Arguments
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
