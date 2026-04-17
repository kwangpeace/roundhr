# 매일 아침 운영 가이드 (Cursor + 라운드HR MCP)

라운드HR에 외부 API가 없어서, 지금은 **Cursor에 연결한 라운드HR MCP로 지원자 JSON을 뽑아** 배치를 돌리는 **반자동** 방식으로 운영합니다. Railway 크론 대신 **아침에 `.bat` 한 번만 누르면** 끝납니다.

## 1) Cursor에서 지원자 추출 (약 1~2분)

Cursor 채팅에서 라운드HR MCP를 호출해 아래 형태로 JSON을 받습니다. 아래 프롬프트를 복붙해 쓰세요.

### 프롬프트 템플릿

> 라운드HR MCP로 **지난 영업일 09:50 KST부터 지금까지** `job_stage_kind == "applied"` 인 지원자 목록을 조회해 주세요.
> 단, **월요일에 실행할 때는 "직전 금요일 10:00 KST부터 지금까지"** 로 조회해 주세요.
>
> 결과는 **배열(JSON)** 하나로만 주고, 각 항목은 아래 필드를 포함합니다 (없으면 빈 문자열):
>
> `candidate_id`, `job_id`, `job_title`, `team_title`, `position_group_title`, `position_title`,
> `candidate_name`, `job_stage_kind`, `candidate_introduction`, `candidate_recent_education`,
> `candidate_recent_experience`, `candidate_skill_titles`, `candidate_from_title`,
> `candidate_applied_at` (KST ISO8601, 예: `2026-04-17T10:00:00+09:00`).
>
> 그 외 설명 문장은 쓰지 말고, **순수 JSON만** 출력해 주세요.

### JSON 저장

1. 위 결과에서 **대괄호 `[ ... ]`** 로 시작/끝나는 JSON 텍스트만 복사합니다.
2. 이 프로젝트의 `automations/recruitment_slack/` 폴더에 **`today.json`** 파일을 만들어 붙여 넣고 저장합니다.
   - 구조 참고: `today.template.json`
   - UTF-8로 저장하세요.

## 2) `.bat` 한 번 실행

1. 파일 탐색기에서 `automations/recruitment_slack/run_today.bat` 더블클릭
2. 창에서 `[done] batch succeeded.` 메시지를 확인
3. Slack 채널에 등급별로 정렬된 요약이 도착하는지 확인

`today.json`이 없으면 안전하게 `examples/sample_candidates.json`으로 실행됩니다(테스트).

## 3) 결과 해석

- `S` / `A` 지원자 = **서류 합격 권장**
- `B` = 리뷰 필요 (추가 정보·포트폴리오 확인)
- `C` = 서류 통과 비권장 (자동 탈락 아님, 담당자가 최종 판단)

등급 정의: [RUBRIC.md](RUBRIC.md)

## 4) 주의

- `today.json`은 **개인정보가 들어 있으므로 `.gitignore`에 의해 커밋되지 않습니다.**
- 값이 긴 필드(자기소개 등)는 그대로 Slack 메시지 길이에 영향을 줄 수 있어, 배치는 자동으로 메시지를 분할해 전송합니다.
- Slack 전송이 `not_in_channel`이면 **봇을 해당 채널에 초대** 후 다시 실행하세요.

## 나중에 자동화가 필요해지면

- 라운드HR에서 **CSV 내보내기 URL**이나 **읽기 전용 API 키**를 받을 수 있게 되면, `ROUNDHR_API_URL` / `ROUNDHR_API_TOKEN` 에 넣어 Railway 크론으로 완전 자동 전환이 가능합니다. 지금 구조는 그대로 두고, 데이터 소스만 바꾸면 됩니다.
