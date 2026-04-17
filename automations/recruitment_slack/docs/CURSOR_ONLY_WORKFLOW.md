## Cursor만으로 운영하기 (Gemini 없이)

Cursor 안에서 라운드HR MCP로 지원자를 조회 → **Cursor가 직접 판정·요약** → 결과 텍스트만 Slack에 전송하는 단순한 흐름입니다. 외부 LLM 호출(Gemini/OpenAI)과 `today.json` 저장도 생략합니다.

### 1) Cursor에 요청하는 프롬프트 (그대로 복사해서 쓰기)

> 라운드HR MCP로 `job_stage_kind == "applied"` 지원자 목록을 조회해 주세요. 범위는
> - 화~금: 전날 09:50 KST ~ 지금
> - 월: 직전 금요일 10:00 KST ~ 지금
>
> 그리고 각 지원자를 `automations/recruitment_slack/config/jd/{job_id}.txt` 의 JD와 평가지표에 맞춰 **S / A / B / C** 4등급으로 판정해 주세요.
> - S: 핵심 인재, JD 강한 매치
> - A: 좋은 매치, 소폭 갭
> - B: 보통, 추가 검토 필요
> - C: 서류 통과 비권장
>
> 결과를 아래 Slack용 마크다운 포맷 **하나의 코드블록**으로 출력해 주세요. 공고별로 묶고, 등급은 S → A → B → C 순으로 정렬.
>
> ```
> :briefcase: *서류 단계 지원자 AI 추천 요약*
> _기간_: (계산한 기간) KST
> _대상_: `applied` {N}명 / 공고 {M}건
>
> *{team_title}* · *{job_title}* (`job_id={job_id}`)
> _요약_: {한 문장}
>
> *{등급}* · {candidate_name} (id `{candidate_id}`)
>   - 추천·평가: {핵심 근거}
>   - 리스크: {있으면 한 줄}
>
> ---
> ```
>
> 개인정보가 길면 요약해 주고, JSON이나 추가 설명 문장은 절대 출력하지 말아 주세요.

### 2) 결과를 파일로 저장

Cursor가 준 코드블록 내용(마크다운)을 **그대로 복사**해서
`automations/recruitment_slack/message.md` 로 저장합니다. (참고 양식: `message.template.md`)

### 3) Slack 전송

파일 탐색기에서 `automations/recruitment_slack/post_message.bat` 더블클릭.

또는 터미널에서:

```powershell
.\.venv\Scripts\python -m src.post_message -f message.md
```

- `--dry-run` 을 붙이면 Slack 없이 출력만.
- `message.md` 는 `.gitignore` 로 커밋되지 않습니다(개인정보 보호).

### 언제 이 방식이 좋나

- 지원자 수가 **하루 수십 명 이하**이고, 담당자가 아침에 Cursor를 켤 수 있는 운영  
- Gemini/OpenAI 키·비용을 쓰지 않고 운영을 유지하고 싶을 때  
- 빠르게 판정 결과를 검수·수정한 뒤 슬랙으로 공유하고 싶을 때

### 언제 Gemini 경로(`python -m src.main`)가 좋나

- 지원자 수가 많아 **일관된 자동 판정**이 필요할 때  
- 향후 Railway 크론으로 **완전 자동화**할 계획이 있을 때
