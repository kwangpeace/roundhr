# 채용 서류 지원자 요약 → Slack

**라운드HR**에서 `applied`(지원) 단계 지원자를 **Cursor + 라운드HR MCP**로 조회하고, `config/hiring_rubric_2026.md` 기준으로 **S / A / B / C** 등급을 매긴 뒤, 정리한 내용을 **Slack**으로 보냅니다.

## 한 줄 흐름

1. Cursor 채팅: [`PROMPT_ROUNDHR.md`](PROMPT_ROUNDHR.md) 안의 블록을 붙여넣기 (`@config/hiring_rubric_2026.md` 포함).
2. 응답을 `message.md`로 저장.
3. 터미널에서 **토큰·채널을 파일에 넣지 않고** 한 번에 전달:

```powershell
cd automations\recruitment_slack
.\.venv\Scripts\python send_slack.py "xoxb-여기토큰|C여기채널ID"
```

또는 `send_slack.bat "xoxb-...|C..."` 더블클릭(인자 넣는 방법은 배치 파일 안내 참고).

## 문서

| 경로 | 내용 |
|------|------|
| [manuals/README.md](manuals/README.md) | 단계별 매뉴얼 (한국어) |
| [PROMPT_ROUNDHR.md](PROMPT_ROUNDHR.md) | Cursor용 프롬프트 (기간은 요청 시 직접 지정) |
| [config/hiring_rubric_2026.md](config/hiring_rubric_2026.md) | 포지션별 JD·평가지표 통합본 |
| [docs/SLACK_SETUP.md](docs/SLACK_SETUP.md) | Slack 봇 권한·채널 ID |
| [docs/ROUNDHR_ACCESS.md](docs/ROUNDHR_ACCESS.md) | MCP로만 조회한다는 점·SQL 예시 |
| [docs/RUBRIC.md](docs/RUBRIC.md) | S/A/B/C 의미 (보조) |
| [docs/JD_SOURCE.md](docs/JD_SOURCE.md) | 루브릭 파일 위치 |

## 로컬 준비 (Slack 전송용)

```powershell
cd automations\recruitment_slack
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

미리보기만:

```powershell
.\.venv\Scripts\python send_slack.py "xoxb-...|C..." --dry-run
```

## 제한 사항 (중요)

- **라운드HR MCP는 Cursor 안에서만** 동작합니다. 일반 터미널 스크립트가 라운드HR에 자동 로그인·조회할 수는 없습니다. 조회·선별은 항상 Cursor 채팅에서 합니다.
- **Slack API**는 봇 토큰이 필요합니다. 레포에는 키를 두지 말고, 실행할 때만 인자로 넘기세요.

## 주의

- AI·루브릭 기반 출력은 **보조 의견**이며, 최종 채용 판단은 담당자가 합니다.
