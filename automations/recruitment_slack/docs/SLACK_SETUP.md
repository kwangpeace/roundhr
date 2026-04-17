# Slack Bot 설정 (chat.postMessage)

Slack으로 보내려면 봇 토큰과 채널 ID가 필요합니다. **이 레포에는 저장하지 마세요.** `send_slack.py` 실행 시 `"토큰|채널ID"` 한 덩어리로만 넘깁니다.

## 1. Slack 앱 생성

1. [Slack API](https://api.slack.com/apps) → **Create New App** → From scratch.
2. 앱 이름·워크스페이스 선택.

## 2. Bot Token 권한

**OAuth & Permissions** → **Bot Token Scopes**:

- `chat:write`
- (선택) `chat:write.public` — 봇을 채널에 초대하지 않고 공개 채널에 쓸 때

비공개 채널에는 **봇을 채널에 초대** (`/invite @봇이름`)해야 합니다.

## 3. 워크스페이스에 설치

**Install to Workspace** → **Bot User OAuth Token** (`xoxb-...`) 복사.

## 4. 채널 ID

채널 우클릭 → 채널 세부정보 → 맨 아래 **채널 ID** (예: `C01234567`).

## 5. 이 프로젝트에서 쓰는 방법

```text
xoxb-...복사한토큰|C01234567
```

가운데는 **파이프(`|`) 하나**, 토큰과 채널 사이에 공백 없이 붙입니다. 전체를 큰따옴표로 감싸서:

```powershell
.\.venv\Scripts\python send_slack.py "xoxb-...|C01234567"
```

## 보안

- 토큰을 Git·문서·채팅에 넣지 마세요.
- 노출 의심 시 [Slack에서 토큰 재발급](https://api.slack.com/apps) 후 이전 토큰 폐기.
