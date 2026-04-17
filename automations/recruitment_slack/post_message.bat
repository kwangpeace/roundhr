@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [setup] create venv
  python -m venv .venv
  .\.venv\Scripts\python -m pip install -r requirements.txt
)

if not exist "message.md" (
  echo [error] message.md 가 없습니다. Cursor에서 정리한 내용을 message.md 로 저장한 뒤 다시 실행해 주세요.
  pause
  exit /b 2
)

.\.venv\Scripts\python -m src.post_message -f message.md
set EXITCODE=%ERRORLEVEL%

echo.
if %EXITCODE% EQU 0 (
  echo [done] Slack 전송 성공.
) else (
  echo [error] 전송 실패: exit %EXITCODE%.
)

pause
endlocal
