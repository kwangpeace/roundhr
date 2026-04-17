# 채용 지원자 Slack 자동 추천

라운드HR(또는 JSON 입력)에서 **지원(`applied`) 단계** 지원자를 읽어, LLM으로 **S/A/B/C** 등급과 추천 사유를 붙인 뒤 **Slack**으로 요약 전송합니다.

## 문서

| 문서 | 내용 |
|------|------|
| [docs/CURSOR_ONLY_WORKFLOW.md](docs/CURSOR_ONLY_WORKFLOW.md) | **Cursor만으로 판정·Slack 전송 (Gemini 없이)** |
| [docs/DAILY_WORKFLOW.md](docs/DAILY_WORKFLOW.md) | 매일 아침 운영 순서 (Cursor + MCP + run_today.bat, Gemini 자동 판정) |
| [docs/ROUNDHR_ACCESS.md](docs/ROUNDHR_ACCESS.md) | 배치용 데이터 접근·수동 SQL 추출 |
| [docs/JD_SOURCE.md](docs/JD_SOURCE.md) | 공고 전문 `config/jd/{job_id}.txt` |
| [docs/RUNTIME.md](docs/RUNTIME.md) | 스케줄(UTC)·평가 기간 규칙 |
| [docs/RAILWAY.md](docs/RAILWAY.md) | Railway Cron Job 배포 |
| [docs/RUBRIC.md](docs/RUBRIC.md) | 등급 정의·JSON 스키마 |
| [docs/SLACK_SETUP.md](docs/SLACK_SETUP.md) | Slack Bot 토큰·시크릿 |

## 로컬 실행

```bash
cd automations/recruitment_slack
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

- `INPUT_JSON_PATH`를 라운드HR에서 뽑은 JSON으로 지정하거나, 비워 두면 `examples/sample_candidates.json`을 사용합니다.
- API 키 없이 출력만 보려면:

```bash
set DRY_RUN=true
python -m src.main --dry-run
```

- 실제 LLM·Slack을 쓰려면 `.env`에 `LLM_PROVIDER`, `LLM_API_KEY`, `LLM_MODEL`, `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`를 채우고 `DRY_RUN=false`로 실행합니다.
- Slack 전송이 `not_in_channel`이면 봇을 해당 채널에 초대하거나, 봇에 `channels:join` 권한이 있으면 `conversations.join`으로 채널에 입장시키세요.

## 환경 변수

| 변수 | 설명 |
|------|------|
| `INPUT_JSON_PATH` | 지원자 배열 JSON 파일 경로 |
| `ROUNDHR_API_URL` | (선택) 라운드HR이 제공 시 POST 쿼리 엔드포인트 |
| `ROUNDHR_API_TOKEN` | 위 URL용 Bearer 토큰 |
| `ROUNDHR_QUERY` | (선택) 커스텀 SQL; 미설정 시 `applied` 조회 기본 쿼리 |
| `LLM_PROVIDER` | `openai` 또는 `gemini` |
| `LLM_API_KEY` | 선택한 제공자의 API 키 |
| `LLM_MODEL` | 예: `gpt-4o-mini`, `gemini-2.5-flash` |
| `GEMINI_FALLBACK_MODELS` | (선택) Gemini 모델 과부하 시 폴백(쉼표 구분). 미설정 시 기본 폴백 사용 |
| `LLM_BASE_URL` | (선택) OpenAI 호환 API Base URL |
| `OPENAI_API_KEY` | (호환) OpenAI API 키 |
| `OPENAI_MODEL` | (호환) 기본 `gpt-4o-mini` |
| `GEMINI_API_KEY` | (호환) Gemini API 키 |
| `MOCK_LLM` | `true`면 고정 B등급(테스트) |
| `SLACK_BOT_TOKEN` | `xoxb-...` |
| `SLACK_CHANNEL_ID` | 채널 ID |
| `JD_DIR` | JD 텍스트 디렉터리 (기본 `config/jd`) |
| `JD_FALLBACK` | JD 파일 없을 때 공통 문단 |
| `MASK_CANDIDATE_NAMES` | `true`면 Slack에 이름 대신 `후보#id` |
| `DRY_RUN` | `true`면 Slack 미전송, stdout만 |
| `APPLIED_TIME_FILTER` | `true`면 `candidate_applied_at` 기준으로 일일(월요일은 주말 포함) 구간만 평가. 미설정 시 **GitHub Actions** 또는 **Railway**에서는 기본 `true` |

## GitHub Actions

워크플로: [`.github/workflows/recruitment-recommend.yml`](../../.github/workflows/recruitment-recommend.yml)

- **스케줄(UTC)**: `50 0 * * 1-5` → 한국 시각 **월~금 09:50** (1일 1회).
- **Secrets**: `CANDIDATES_JSON`(전체 JSON 문자열), `LLM_API_KEY`, `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`.
- `CANDIDATES_JSON`이 비어 있으면 샘플 데이터로 실행됩니다.
- `LLM_API_KEY`가 비어 있으면 `MOCK_LLM`으로 자동 대체(슬랙에는 목 등급이 갑니다). 운영에서는 반드시 키를 넣으세요.

Repository variables(선택): `LLM_PROVIDER`, `LLM_MODEL`, `GEMINI_FALLBACK_MODELS`, `MASK_CANDIDATE_NAMES`.

## 주의

- AI 출력은 **보조 의견**이며, 최종 채용 판단은 담당자가 합니다.
- 개인정보 최소화를 위해 `MASK_CANDIDATE_NAMES` 사용을 검토하세요.
