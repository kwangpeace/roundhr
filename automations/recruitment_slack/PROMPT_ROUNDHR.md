# Cursor에서 쓰는 프롬프트 (라운드HR MCP + 채용 기준)

> **중요**: 라운드HR MCP는 **Cursor 안에서만** 동작합니다. 터미널 스크립트가 자동으로 라운드HR에 로그인할 수는 없습니다.

## 1) 채용 기준 파일

전사 기준 전문은 아래 파일을 Cursor에서 `@` 로 붙여 참조하세요.

- `config/hiring_rubric_2026.md`

## 2) 아래 블록을 Cursor 채팅에 붙여넣기

**조회 기간은 요일 자동 규칙 없음.** 같은 메시지에 한 줄로 적어 주세요.  
예: `기간(KST): 2026-04-10 00:00 ~ 2026-04-18 18:00`  
기간이 없으면 MCP 조회 전에 **한 문장으로 기간만** 물어보고, 답을 받은 뒤 진행합니다.

```
@config/hiring_rubric_2026.md

기간(KST): (여기에 시작 ~ 끝을 적거나, 비워 두면 에이전트가 질문하게 둠)

라운드HR MCP로 다음을 수행해 주세요.

1) `job_stage_kind == "applied"` 인 지원자만 조회합니다.
2) `candidate_applied_at` 은 위에서 정한 **기간(KST)** 안에 드는 행만 포함합니다. (MCP 쿼리에 동일 조건을 넣습니다.)
3) 공고(`job_id`)별로 지원자를 묶고, 위에 첨부한 채용 기준 문서에서 **해당 포지션**에 맞는 JD·평가지표를 적용해 **S / A / B / C** 로 서류 단계 등급을 매겨 주세요.
   - S: 서류 즉시 통과 권장 (우수)
   - A: 서류 통과 권장
   - B: 조건부·추가 검토
   - C: 서류 통과 비권장 (최종은 담당자 판단)
4) 필수 자격 미충족이 명확하면 C에 가깝게 두고, 근거를 한 줄로 적어 주세요.

출력은 **JSON이나 코드 설명 없이**, Slack용 마크다운 **한 덩어리**만 주세요. 형식:

:briefcase: *서류 단계 지원자 선별 요약*
_기간_: (위에서 쓴 기간) KST
_대상_: `applied` N명 / 공고 M건

*{team_title}* · *{job_title}* (`job_id={job_id}`)
_요약_: 한 문장

*{등급}* · {candidate_name} (id `{candidate_id}`)
  - 추천·평가: 근거
  - 리스크: 있으면 한 줄

---

(공고마다 반복, 등급은 S→A→B→C 순)
```

## 3) 결과 저장

Cursor 응답 전체를 복사해 `message.md` 로 저장합니다.

## 4) Slack 전송 (터미널, 토큰은 레포/파일에 저장하지 않음)

`automations/recruitment_slack` 폴더에서:

```powershell
.\.venv\Scripts\python send_slack.py "xoxb-여기에토큰|C여기에채널ID"
```

또는 `send_slack.bat` 더블클릭 → 화면에 **`xoxb-...|C...` 한 줄**만 붙여넣기.  
인자로 넘기려면: `send_slack.bat "xoxb-토큰|C채널ID"`

`--dry-run` 을 붙이면 Slack으로 안 보내고 화면에만 출력합니다.
