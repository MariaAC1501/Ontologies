$Scripts = Join-Path $env:CONDA_PREFIX "Scripts"

# Remove the broken hardcoded launchers
Remove-Item -Force "$Scripts\ontocast.exe" -ErrorAction SilentlyContinue
Remove-Item -Force "$Scripts\cmp-states.exe" -ErrorAction SilentlyContinue

# Create dynamic batch wrappers pointing to the active Python environment
"@echo off`n`"%~dp0..\python.exe`" -m ontocast.cli.serve %*" | Out-File -Encoding ascii -FilePath "$Scripts\ontocast.bat"
"@echo off`n`"%~dp0..\python.exe`" -m ontocast.cli.cmp_states %*" | Out-File -Encoding ascii -FilePath "$Scripts\cmp-states.bat"

Write-Host "Replaced broken launchers with working .bat wrappers!"
Write-Host "Try running: ontocast --help"
