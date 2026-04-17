# Slack Bot 설정 (chat.postMessage)

## 1. Slack 앱 생성

1. [Slack API](https://api.slack.com/apps) → **Create New App** → From scratch.
2. 앱 이름·워크스페이스 선택.

## 2. Bot Token 권한

**OAuth & Permissions** → **Bot Token Scopes**에 다음 추가:

- `chat:write`
- (선택) `chat:write.public` — 봇을 채널에 초대하지 않고 공개 채널에 쓸 때

비공개 채널에는 **봇을 채널에 초대**(`/invite @봇이름`)해야 합니다.

## 3. 워크스페이스에 설치

**Install to Workspace** → 표시되는 **Bot User OAuth Token** (`xoxb-...`)을 복사합니다.

## 4. 채널 ID

Slack 데스크톱에서 채널 우클릭 → 채널 세부정보 보기 → 맨 아래 **채널 ID** (예: `C01234567`).

## 5. GitHub Actions 시크릿

저장소 **Settings → Secrets and variables → Actions** 에 추가:

| Name | Value |
|------|--------|
| `SLACK_BOT_TOKEN` | `xoxb-...` |
| `SLACK_CHANNEL_ID` | `C01234567` |

## 6. 로컬 실행

[`../.env.example`](../.env.example)를 참고해 동일 키를 `.env`에 두거나 export 합니다.

## 보안

- 토큰을 커밋하지 마세요.
- 메시지에 불필요한 개인정보를 넣지 마세요. 필요 시 `MASK_CANDIDATE_NAMES=true` 사용.
