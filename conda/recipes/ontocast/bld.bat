@echo off
setlocal enabledelayedexpansion

set "WHEEL_DIR=%RECIPE_DIR%\wheels"

%PYTHON% -m pip install --no-deps --no-index --find-links "%WHEEL_DIR%" ontocast==0.3.0 || exit /b 1
%PYTHON% -m pip install --no-deps --no-index --find-links "%WHEEL_DIR%" neo4j==6.1.0 || exit /b 1
%PYTHON% -m pip install --no-deps --no-index --find-links "%WHEEL_DIR%" duckduckgo-search==8.1.1 || exit /b 1
%PYTHON% -m pip install --no-deps --no-index --find-links "%WHEEL_DIR%" suthing==0.5.1 || exit /b 1

%PYTHON% -m pip install --no-deps --no-index --find-links "%WHEEL_DIR%" "%WHEEL_DIR%\primp-0.15.0-cp38-abi3-win_amd64.whl" || exit /b 1
%PYTHON% -m pip install --no-deps --no-index --find-links "%WHEEL_DIR%" "%WHEEL_DIR%\robyn-0.81.0-cp312-cp312-win_amd64.whl" || exit /b 1
%PYTHON% -m pip install --no-deps --no-index --find-links "%WHEEL_DIR%" "%WHEEL_DIR%\simsimd-6.5.16-cp312-cp312-win_amd64.whl" || exit /b 1
