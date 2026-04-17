# 라운드HR MCP (공식 가이드 반영)

원문은 라운드HR 도움말 **[MCP 연동](https://guide.roundhr.com/round-ai/mcp)** 을 기준으로 했습니다. 설정이 바뀌면 원문을 우선하세요.

## 플랜·권한

- **관리자 권한 이상**만 MCP 연동 가능(엔터프라이즈 플랜 기준; Beta 기간에는 모든 플랜의 관리자 이상 사용 가능이라고 안내).
- **조직별 사전 승인**이 필요합니다. 승인되지 않은 조직은 OAuth에서 차단되며, **[허용]을 눌러도 연동이 완료되지 않고** 라운드HR 홈으로 이동하며 안내 메시지가 표시될 수 있습니다. 사용 신청은 [support@roundhr.com](mailto:support@roundhr.com) 으로 문의합니다.

## MCP 서버 URL (Claude 문서 기준)

| 용도 | URL |
|------|-----|
| 원격 MCP (커스텀 커넥터 등) | `https://mcp.roundhr.com` |
| Smithery 경유 예시 | `https://smithery-mcp.roundhr.com` (Smithery에서 `roundHR` 검색 후 안내하는 connection URL 사용) |

Claude에서는 **사용자 지정 → 커넥터 → 커스텀 커넥터 추가**에 이름 `라운드HR` 과 위 URL을 넣고 **[연결] → 브라우저에서 [허용]** 순으로 진행합니다.

## Cursor에서 쓸 때

공식 문서는 Claude 위주이지만, 프로토콜은 동일합니다. Cursor **설정 → MCP**에서 위 **`https://mcp.roundhr.com`** 을 원격 MCP로 등록하고, 안내에 따라 브라우저 OAuth로 허용합니다. (Cursor UI 문구는 버전에 따라 다를 수 있습니다.)

## 데이터·보안 (FAQ 요지)

- MCP 서버에 연결된 DB는 통계·분석용으로 **비식별화된 데이터**가 별도 구성된다는 설명이 있습니다(원문 FAQ).
- OAuth로 **우리 조직 데이터만** 접근하며, 공고별 권한이 아니라 조직 전체 공고가 대상이므로 **관리자만** 연동할 수 있다는 설명이 있습니다.

## 자주 겪는 현상

| 증상 | 조치 |
|------|------|
| **[허용] 후에도 연동 안 되고 홈으로 이동** | 조직 **MCP 사전 승인** 여부 확인 → [support@roundhr.com](mailto:support@roundhr.com) |
| **MCP를 찾을 수 없다** | Cursor(또는 Claude 앱) **완전 종료 후 재실행** 후 다시 연결 |
| **대화가 길어지면 답이 흔들림** | 새 채팅(새 스레드)으로 다시 질문 (원문 FAQ 권장) |

## 이 레포에서의 역할

조회·선별 프롬프트는 [`../PROMPT_ROUNDHR.md`](../PROMPT_ROUNDHR.md) 를 쓰고, SQL 예시는 [`ROUNDHR_ACCESS.md`](ROUNDHR_ACCESS.md) 를 참고하면 됩니다.
