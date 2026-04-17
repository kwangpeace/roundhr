# 라운드HR 데이터 접근

## MCP 연동·401 대응

플랜·**조직 사전 승인**·MCP URL·OAuth 절차는 공식 가이드를 요약한 [`ROUNDHR_MCP.md`](ROUNDHR_MCP.md) 를 보세요. (원문: [guide.roundhr.com — MCP 연동](https://guide.roundhr.com/round-ai/mcp))

## 결론

- **지원자 조회·선별은 Cursor에서 라운드HR MCP**로만 합니다. MCP는 IDE(Cursor) 세션 안에서 동작하며, 이 폴더의 Python 스크립트가 라운드HR에 대신 로그인하거나 API를 부를 수는 없습니다.
- 운영 절차는 [`../PROMPT_ROUNDHR.md`](../PROMPT_ROUNDHR.md)를 따르세요.

## MCP에서 쓸 SQL 예시

지원 슬롯(`applied`)과 **게재·진행 중인 공고**만 포함합니다. `vw_jobs` 기준으로 `deleted = 0` 이고 `application_form_status = 'in_progress'` 인 공고만 조인합니다. SQL 주석은 라운드HR MCP 규칙에 맞게 사용하지 마세요.

```sql
SELECT c.id AS candidate_id,
       c.job_id,
       c.job_title,
       c.team_title,
       c.position_group_title,
       c.position_title,
       c.candidate_name,
       c.job_stage_kind,
       c.candidate_introduction,
       c.candidate_recent_education,
       c.candidate_recent_experience,
       c.candidate_skill_titles,
       c.candidate_from_title,
       c.candidate_applied_at
FROM vw_candidates c
INNER JOIN vw_jobs j ON j.id = c.job_id
WHERE c.job_stage_kind = 'applied'
  AND j.deleted = 0
  AND j.application_form_status = 'in_progress'
ORDER BY c.job_id, c.candidate_applied_at DESC
```

- **지원일시**로 범위를 두지 않습니다.  
- **지원서 접수 창만 열린 공고**로 더 좁히려면 `AND j.application_form_open_status = 1` 을 추가할 수 있습니다. 조직 설정에 따라 0건일 수 있으니, 그때는 해당 조건을 빼고 위 쿼리만 쓰면 됩니다.

자세한 지시는 [`../PROMPT_ROUNDHR.md`](../PROMPT_ROUNDHR.md) 를 따르세요.
