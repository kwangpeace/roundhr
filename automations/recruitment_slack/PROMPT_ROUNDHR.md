# Cursor에서 쓰는 프롬프트 (라운드HR MCP + 채용 기준)

> **중요**: 라운드HR MCP는 **Cursor 안에서만** 동작합니다. 터미널 스크립트가 자동으로 라운드HR에 로그인할 수는 없습니다.  
> 연동·401·조직 승인은 [docs/ROUNDHR_MCP.md](docs/ROUNDHR_MCP.md) · 원문 [MCP 연동](https://guide.roundhr.com/round-ai/mcp) 을 참고하세요.

## 1) 채용 기준 파일

전사 기준 전문은 아래 파일을 Cursor에서 `@` 로 붙여 참조하세요.

- `config/hiring_rubric_2026.md`

## 2) 아래 블록을 Cursor 채팅에 붙여넣기

**지원일시·기간 조건은 두지 않습니다.** 다만 지원자는 **삭제되지 않았고 채용이 진행 중(`in_progress`)인 공고**에 지원한 경우만 포함합니다. (`vw_jobs`와 `INNER JOIN`, 아래 1번.)

```
@config/hiring_rubric_2026.md

라운드HR MCP로 다음을 수행해 주세요.

1) MCP SQL은 `vw_candidates c` 와 `vw_jobs j` 를 `j.id = c.job_id` 로 **INNER JOIN** 합니다. `WHERE` 에 반드시 `c.job_stage_kind = 'applied'` 와 `j.deleted = 0` 과 `j.application_form_status = 'in_progress'` 를 넣습니다. (마감·보관·삭제된 공고·종료된 공고 지원자는 제외.) 지원일·기간으로 행을 거르지 마세요. `SELECT` 에 `candidate_applied_at` 을 포함하는 것은 괜찮습니다.  
   - (선택) 조직에서 지원서 접수만 열린 공고로 더 좁히려면 `j.application_form_open_status = 1` 을 추가할 수 있습니다. 이 조건으로 0건이면 제외하고 진행 중 공고만 사용하세요.
2) 공고(`job_id`)별로 지원자를 묶고, 위에 첨부한 채용 기준 문서에서 **해당 포지션**에 맞는 JD·평가지표를 적용해 **S / A / B / C** 로 서류 단계 등급을 매겨 주세요.
   - S: 서류 즉시 통과 권장 (우수)
   - A: 서류 통과 권장
   - B: 조건부·추가 검토
   - C: 서류 통과 비권장 (최종은 담당자 판단)
3) 필수 자격 미충족이 명확하면 C에 가깝게 두고, 근거를 한 줄로 적어 주세요.

출력은 **JSON이나 코드 설명 없이**, Slack용 마크다운 **한 덩어리**만 주세요. 형식:

:briefcase: *서류 단계 지원자 선별 요약*
_범위_: `applied` + **진행 중 공고** (`vw_jobs` · `in_progress` · 미삭제)만, 지원일시 필터 없음
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
