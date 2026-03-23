@echo off
setlocal enabledelayedexpansion

set "INSTALL_ROOT=%PREFIX%\share\ontologies-pipeline"
set "INSTALL_PKG=%SP_DIR%\ontologies_pipeline"

mkdir "%INSTALL_ROOT%\seed_ontology" || exit /b 1
mkdir "%INSTALL_ROOT%\tests" || exit /b 1
mkdir "%INSTALL_PKG%" || exit /b 1

copy /Y "%SRC_DIR%\pipeline\__init__.py" "%INSTALL_PKG%\__init__.py" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\extraction_schema.py" "%INSTALL_PKG%\extraction_schema.py" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\facts_to_csv.py" "%INSTALL_PKG%\facts_to_csv.py" >nul || exit /b 1

copy /Y "%SRC_DIR%\pipeline\__init__.py" "%INSTALL_ROOT%\__init__.py" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\extraction_schema.py" "%INSTALL_ROOT%\extraction_schema.py" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\facts_to_csv.py" "%INSTALL_ROOT%\facts_to_csv.py" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\SCHEMA_MAPPING.md" "%INSTALL_ROOT%\SCHEMA_MAPPING.md" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\ontocast_config.env" "%INSTALL_ROOT%\ontocast_config.env" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\run_extraction.sh" "%INSTALL_ROOT%\run_extraction.sh" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\seed_ontology\opmad_seed.ttl" "%INSTALL_ROOT%\seed_ontology\opmad_seed.ttl" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\tests\test_e2e.sh" "%INSTALL_ROOT%\tests\test_e2e.sh" >nul || exit /b 1
copy /Y "%SRC_DIR%\pipeline\tests\test_facts_to_csv.py" "%INSTALL_ROOT%\tests\test_facts_to_csv.py" >nul || exit /b 1
