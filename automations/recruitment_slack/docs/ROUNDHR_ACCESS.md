# 라운드HR 데이터 접근

## 결론

- **지원자 조회·선별은 Cursor에서 라운드HR MCP**로만 합니다. MCP는 IDE(Cursor) 세션 안에서 동작하며, 이 폴더의 Python 스크립트가 라운드HR에 대신 로그인하거나 API를 부를 수는 없습니다.
- 운영 절차는 [`../PROMPT_ROUNDHR.md`](../PROMPT_ROUNDHR.md)를 따르세요.

## MCP에서 쓸 SQL 예시

지원 슬롯(`applied`)과 공고 메타 위주입니다. SQL 주석은 라운드HR MCP 규칙에 맞게 사용하지 마세요.

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
WHERE c.job_stage_kind = 'applied'
ORDER BY c.job_id, c.candidate_applied_at DESC
```

조회 기간은 **요청할 때 채팅에 적은 KST 구간**만 씁니다. MCP 쿼리의 `WHERE`에 `candidate_applied_at` 조건으로 넣으면 됩니다. ([`../PROMPT_ROUNDHR.md`](../PROMPT_ROUNDHR.md) 참고.)
