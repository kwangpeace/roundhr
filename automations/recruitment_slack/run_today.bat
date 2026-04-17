@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [setup] create venv
  python -m venv .venv
  .\.venv\Scripts\python -m pip install -r requirements.txt
)

if exist "today.json" (
  set "INPUT_JSON_PATH=%cd%\today.json"
) else (
  echo [warn] today.json not found. Using examples/sample_candidates.json
  set "INPUT_JSON_PATH=%cd%\examples\sample_candidates.json"
)

set "APPLIED_TIME_FILTER=true"
set "DRY_RUN=false"
set "MOCK_LLM=false"

.\.venv\Scripts\python -m src.main
set EXITCODE=%ERRORLEVEL%

echo.
if %EXITCODE% EQU 0 (
  echo [done] batch succeeded.
) else (
  echo [error] batch exited with code %EXITCODE%.
)

pause
endlocal
