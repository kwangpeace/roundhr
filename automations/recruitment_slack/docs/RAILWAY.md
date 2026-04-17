# Railway 배포 (스케줄 실행)

GitHub Actions 대신 **Railway Cron Job**으로 `python -m src.main`을 주기 실행하는 방법입니다.

## 전제

- 이 디렉터리(`automations/recruitment_slack`)에 `Dockerfile`·`railway.toml`이 있습니다.
- 배치는 **실행 시 한 번 끝나고 종료**하는 형태입니다 (장시간 웹 서버가 아님).

## 1) Railway 프로젝트 만들기

1. [Railway](https://railway.app)에서 **New Project** → **Deploy from GitHub repo** (또는 CLI로 연결).
2. 저장소를 선택한 뒤, 해당 서비스의 **Root Directory**를  
   `automations/recruitment_slack`  
   로 지정합니다.  
   (루트를 안 바꾸면 Dockerfile 위치를 찾지 못할 수 있습니다.)

## 2) Cron Job 서비스 추가

1. 같은 프로젝트에서 **New** → **Cron Job** (또는 **Empty Service** 후 템플릿에서 Cron)을 선택합니다.
2. **같은 GitHub 저장소·같은 Root Directory**를 쓰도록 연결합니다.
3. **Schedule (cron)**  
   - 요구사항: **매주 월~금 09:50 KST, 1회**  
   - Railway 크론은 보통 **UTC** 기준이므로 다음을 사용합니다:  
     `50 0 * * 1-5`  
     → UTC **00:50**, 요일 **월~금** = KST **09:50** 월~금  
4. **Start command**  
   - `python -m src.main`  
   (또는 `railway.toml`의 `[deploy] startCommand`와 동일하게 유지)

> UI에 타임존 선택이 있으면 **UTC**로 두고 위 cron을 쓰는 것이 안전합니다.

## 3) 환경 변수 (Variables)

서비스(또는 프로젝트) **Variables**에 아래를 넣습니다. 값은 저장소에 커밋하지 마세요.

| 변수 | 설명 |
|------|------|
| `LLM_PROVIDER` | `gemini` 권장 |
| `LLM_API_KEY` 또는 `GEMINI_API_KEY` | Gemini API 키 |
| `LLM_MODEL` | 예: `gemini-2.5-flash` |
| `SLACK_BOT_TOKEN` | `xoxb-...` |
| `SLACK_CHANNEL_ID` | `C...` |
| `CANDIDATES_JSON` | 지원자 배열 JSON **전체 문자열** (GitHub Actions와 동일) |
| `APPLIED_TIME_FILTER` | 비워 두면 Railway에서는 **기본 true** (Railway가 넣는 `RAILWAY_*` 변수가 있으면 자동). 테스트 시만 `false` |
| `MASK_CANDIDATE_NAMES` | 선택, `true` / `false` |
| `GEMINI_FALLBACK_MODELS` | 선택, 쉼표 구분 |

RoundHR HTTP로 직접 가져올 경우:

- `ROUNDHR_API_URL`, `ROUNDHR_API_TOKEN`  
- 이 경우 `CANDIDATES_JSON` 없이 동작 가능(코드 기본 쿼리 사용).

## 4) 데이터 소스 정리

둘 중 하나만 있으면 됩니다.

1. **`CANDIDATES_JSON`**  
   - Actions 때와 같이 JSON 문자열을 Variable에 넣습니다.  
   - 줄바꿈이 많으면 Railway UI의 multiline 입력을 사용합니다.
2. **`ROUNDHR_API_URL` + `ROUNDHR_API_TOKEN`**  
   - 배치가 실행될 때마다 API로 `applied` 후보를 받아옵니다.

## 5) 수동 실행으로 검증

Cron을 기다리기 전에:

1. 해당 Cron 서비스에서 **Run now** / **Deploy** 후 로그에서 `python -m src.main` 성공 여부 확인.
2. Slack 채널에 메시지가 오는지 확인.
3. 봇이 채널에 없으면 `not_in_channel`이 납니다. 채널에 봇 초대 또는 `channels:join` 권한으로 입장 처리.

## 6) GitHub Actions와 중복 실행 방지

같은 Slack 채널로 보낸다면 **한쪽만** 켜 두세요.

- GitHub: `.github/workflows/recruitment-recommend.yml` 비활성화(파일 삭제 또는 `on: workflow_dispatch`만 남기기)  
- Railway: Cron만 사용

## 기간 필터 동작

코드는 `RAILWAY_ENVIRONMENT`가 있으면 `APPLIED_TIME_FILTER`를 비워도 **기본으로 기간 필터를 켭니다**.  
자세한 구간은 [RUNTIME.md](RUNTIME.md)를 참고하세요.
