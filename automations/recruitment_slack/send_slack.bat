@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

if not "%~1"=="" (
  set "CRED=%~1"
) else (
  echo.
  echo Slack 인증 한 줄 입력: xoxb-토큰^|C채널ID  ^(가운데 파이프, 공백 없음^)
  set /p "CRED=> "
)

if "!CRED!"=="" (
  echo [error] 입력이 비었습니다.
  exit /b 2
)

if not exist ".venv\Scripts\python.exe" (
  echo [setup] 가상환경 생성 및 패키지 설치...
  python -m venv .venv
  .\.venv\Scripts\python -m pip install -r requirements.txt
)

if not exist "message.md" (
  echo [error] message.md 가 없습니다. Cursor에서 정리한 내용을 저장한 뒤 다시 실행하세요.
  exit /b 2
)

.\.venv\Scripts\python send_slack.py "!CRED!" -f message.md
set EXITCODE=!ERRORLEVEL!
if !EXITCODE! EQU 0 (echo [done] Slack 전송 완료.) else (echo [error] 실패 코드 !EXITCODE!.)
pause
endlocal
