@echo off
setlocal enableextensions enabledelayedexpansion

set "REPO_ROOT=%SRC_DIR%"
set "CBR_PROJECT_DIR=%REPO_ROOT%\external\CBR-Ontology-For-Predictive-Maintenance\CBR-Ontology\CBRproject"
set "BUILD_DIR=%REPO_ROOT%\.build\cbr"
set "UPSTREAM_BIN=%BUILD_DIR%\upstream-bin"
set "LOCAL_BIN=%BUILD_DIR%\local-bin"
set "DIST_DIR=%BUILD_DIR%\dist"
set "JAR_PATH=%DIST_DIR%\ontologies-cbr-headless.jar"
set "INSTALL_ROOT=%PREFIX%\share\ontologies-cbr"
set "INSTALL_LIB=%INSTALL_ROOT%\lib"
set "INSTALL_DATA=%INSTALL_ROOT%\data"
set "INSTALL_BIN=%PREFIX%\Scripts"

if exist "%UPSTREAM_BIN%" rmdir /s /q "%UPSTREAM_BIN%"
if exist "%LOCAL_BIN%" rmdir /s /q "%LOCAL_BIN%"
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
mkdir "%UPSTREAM_BIN%" || exit /b 1
mkdir "%LOCAL_BIN%" || exit /b 1
mkdir "%DIST_DIR%" || exit /b 1

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference = 'Stop';" ^
  "$cbrDir = $env:CBR_PROJECT_DIR;" ^
  "$buildDir = $env:BUILD_DIR;" ^
  "$upstreamBin = $env:UPSTREAM_BIN;" ^
  "$localBin = $env:LOCAL_BIN;" ^
  "$jarPath = $env:JAR_PATH;" ^
  "$jars = Get-ChildItem -Path (Join-Path $cbrDir 'external-libs') -Filter *.jar | Sort-Object FullName | ForEach-Object { $_.FullName };" ^
  "$classpath = ($jars -join ';');" ^
  "$sources = Join-Path $buildDir 'upstream-sources.txt';" ^
  "Get-ChildItem -Path (Join-Path $cbrDir 'src') -Filter *.java -Recurse | Sort-Object FullName | ForEach-Object { $_.FullName } | Set-Content -Encoding ascii $sources;" ^
  "& javac -encoding ISO-8859-1 -cp $classpath -d $upstreamBin ('@' + $sources); if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE };" ^
  "$localCp = $upstreamBin + ';' + $classpath;" ^
  "& javac -encoding UTF-8 -cp $localCp -d $localBin (Join-Path $env:REPO_ROOT 'tools\cbr\HeadlessCBR.java'); if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE };" ^
  "& jar --create --file $jarPath -C $upstreamBin . -C $localBin .; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }" || exit /b 1

if not exist "%INSTALL_ROOT%" mkdir "%INSTALL_ROOT%" || exit /b 1
if not exist "%INSTALL_LIB%" mkdir "%INSTALL_LIB%" || exit /b 1
if not exist "%INSTALL_DATA%" mkdir "%INSTALL_DATA%" || exit /b 1
if not exist "%INSTALL_BIN%" mkdir "%INSTALL_BIN%" || exit /b 1

copy /y "%JAR_PATH%" "%INSTALL_ROOT%\ontologies-cbr-headless.jar" >nul || exit /b 1
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference = 'Stop';" ^
  "Copy-Item -Path (Join-Path $env:CBR_PROJECT_DIR 'external-libs\*.jar') -Destination $env:INSTALL_LIB -Force;" ^
  "Copy-Item -Path (Join-Path $env:CBR_PROJECT_DIR 'data\*') -Destination $env:INSTALL_DATA -Recurse -Force" || exit /b 1

echo @echo off> "%INSTALL_BIN%\ontologies-cbr.bat"
echo set "PREFIX_DIR=%%~dp0..">> "%INSTALL_BIN%\ontologies-cbr.bat"
echo set "CBR_HOME=%%PREFIX_DIR%%\share\ontologies-cbr">> "%INSTALL_BIN%\ontologies-cbr.bat"
echo if defined ONTOLOGIES_CBR_DATA_DIR ^(>> "%INSTALL_BIN%\ontologies-cbr.bat"
echo   set "CBR_DATA_DIR=%%ONTOLOGIES_CBR_DATA_DIR%%">> "%INSTALL_BIN%\ontologies-cbr.bat"
echo ^) else ^(>> "%INSTALL_BIN%\ontologies-cbr.bat"
echo   set "CBR_DATA_DIR=%%CBR_HOME%%\data">> "%INSTALL_BIN%\ontologies-cbr.bat"
echo ^)>> "%INSTALL_BIN%\ontologies-cbr.bat"
echo java -Djava.awt.headless=true -cp "%%CBR_HOME%%\ontologies-cbr-headless.jar;%%CBR_HOME%%\lib\*" HeadlessCBR --data-dir "%%CBR_DATA_DIR%%" %%*>> "%INSTALL_BIN%\ontologies-cbr.bat"

if not exist "%INSTALL_BIN%\ontologies-cbr.bat" exit /b 1
