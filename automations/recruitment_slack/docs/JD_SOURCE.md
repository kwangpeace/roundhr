# 공고 전문(JD) 확보

## 결론

- 라운드HR MCP의 `vw_jobs`에는 **공고 제목·팀·직군·카운트 등 메타**가 중심이며, **전체 JD 본문**이 뷰에 없을 수 있습니다.
- 추천 품질을 위해 **JD 원문을 이 레포 또는 외부 저장소에 병합**하는 방식을 권장합니다.

## 이 레포에서의 JD 경로

| 우선순위 | 경로 | 설명 |
|----------|------|------|
| 1 | `config/jd/{job_id}.txt` | 한 파일당 하나의 공고. UTF-8 텍스트. |
| 2 | 환경 변수 `JD_FALLBACK` | 모든 공고에 동일한 기본 JD를 쓸 때(비권장, 테스트용). |

`job_id`는 `vw_candidates.job_id`와 동일한 정수 문자열입니다.

## 운영 절차

1. 채용 사이트 또는 라운드HR 관리 화면에서 JD를 복사합니다.
2. `automations/recruitment_slack/config/jd/4664.txt` 형식으로 저장합니다.
3. 배치 실행 시 해당 공고 지원자 그룹에 JD가 자동으로 붙습니다.

JD 파일이 없으면 파이프라인은 **`job_title`, `team_title`, `position_group_title`, `position_title`만** JD 대용으로 LLM에 전달합니다.
