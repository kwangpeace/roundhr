# 라운드HR 배치(자동화) 데이터 접근

## 결론

- Cursor용 **라운드HR MCP**(`query_data`)는 대화형 분석에 맞춰져 있으며, **GitHub Actions 등 배치 러너에서 동일하게 호출하는 공개 HTTP 스펙은 이 레포에 포함되어 있지 않습니다.**
- **라운드HR 고객지원(support@roundhr.com)** 또는 관리 콘솔 문서에서 **자동화용 API·쿼리 엔드포인트** 제공 여부를 확인해야 합니다.

## 권장 확인 사항

1. MCP와 동일한 읽기 전용 SQL을 **서비스 계정 토큰**으로 호출할 수 있는지.
2. 없을 경우 **정기 데이터보내기**(CSV/JSON) 또는 **웹훅** 지원 여부.

## 이 레포에서의 대응

| 방식 | 설명 |
|------|------|
| `ROUNDHR_API_URL` + `ROUNDHR_API_TOKEN` | 지원팀에서 URL·인증 방식을 받은 뒤 `.env`에 설정. `src/data_sources/roundhr_http.py`가 `POST {"query":"..."}` 형태를 가정(실제 페이로드는 받은 스펙에 맞게 수정). |
| `INPUT_JSON_PATH` | MCP/수동 SQL로 뽑은 결과를 JSON 파일로 저장해 배치가 읽도록 함(운영 전 단계에 실용적). |

## 수동 추출용 SQL 예시 (MCP `query_data`에서 실행)

지원 슬롯(`applied`) 지원자와 공고 메타만 가져오는 예시입니다. SQL 주석은 라운드HR MCP 규칙상 사용하지 마세요.

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

결과를 JSON 배열로 저장한 뒤 `INPUT_JSON_PATH`로 지정하면 파이프라인이 동작합니다.
