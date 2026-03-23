<#
.SYNOPSIS
  Run side-by-side comparison of fixed OPMAD vs evolved ontology extraction.
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File pipeline/comparison/run_comparison.ps1
#>

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent (Split-Path -Parent $ScriptDir)
Push-Location $RepoRoot

try {
    $FixedFacts   = Get-ChildItem "pipeline\test_output\facts_*.ttl" -ErrorAction SilentlyContinue
    $EvolvedFacts = Get-ChildItem "pipeline\full_mode\test_output\facts_*.ttl" -ErrorAction SilentlyContinue
    $EvolvedOnto  = Get-ChildItem "pipeline\full_mode\test_output\ontology_*.ttl" -ErrorAction SilentlyContinue
    $SeedOnto     = "pipeline\seed_ontology\opmad_seed.ttl"
    $Output       = "pipeline\comparison\COMPARISON_RESULTS.md"

    if (-not $FixedFacts) {
        Write-Error "No fixed-mode facts found. Run fixed-mode extraction first: powershell -File pipeline\run_extraction.ps1 <pdf>"
        exit 1
    }
    if (-not $EvolvedFacts) {
        Write-Error "No full-mode facts found. Run full-mode extraction first: powershell -File pipeline\full_mode\run_full_extraction.ps1 <pdf>"
        exit 1
    }
    if (-not (Test-Path $SeedOnto)) {
        Write-Error "Seed ontology not found: $SeedOnto"
        exit 1
    }

    $FixedPaths   = ($FixedFacts   | ForEach-Object { $_.FullName }) -join " "
    $EvolvedFPaths = ($EvolvedFacts | ForEach-Object { $_.FullName }) -join " "
    $EvolvedOPaths = if ($EvolvedOnto) { ($EvolvedOnto | ForEach-Object { $_.FullName }) -join " " } else { "" }

    Write-Host "Running side-by-side comparison..."

    $Args = @(
        "pipeline\comparison\compare.py",
        "--fixed-facts"
    ) + ($FixedFacts | ForEach-Object { $_.FullName }) + @(
        "--evolved-facts"
    ) + ($EvolvedFacts | ForEach-Object { $_.FullName })

    if ($EvolvedOnto) {
        $Args += "--evolved-ontology"
        $Args += ($EvolvedOnto | ForEach-Object { $_.FullName })
    }

    $Args += @("--seed-ontology", $SeedOnto, "--output", $Output)

    python @Args

    Write-Host "Comparison report written to: $Output"
} finally {
    Pop-Location
}
