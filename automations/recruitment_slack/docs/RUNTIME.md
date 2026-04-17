# 실행 환경: 스케줄 + KST 기간 규칙

## 선택

이 레포는 **GitHub Actions** 또는 **Railway Cron Job**으로 같은 배치(`python -m src.main`)를 돌릴 수 있습니다. Railway는 [docs/RAILWAY.md](RAILWAY.md)를 참고하세요.

## Asia/Seoul 시각 ↔ UTC

GitHub Actions `schedule`은 **UTC**만 지원합니다.

| 요구 시각 (KST) | 요일 | UTC `cron` | 비고 |
|-----------------|------|------------|------|
| 09:50 | 월~금 | `50 0 * * 1-5` | `1-5` = 월요일~금요일(UTC 기준 weekday) |

정의 위치: [`.github/workflows/recruitment-recommend.yml`](../../../.github/workflows/recruitment-recommend.yml)

## 지원 접수 기간(배치가 평가하는 구간)

- **화~금 트리거**: 전날 09:50 KST 이상 ~ **이번 실행이 시작된 시각** 미만, `applied` 단계 지원만.
- **월요일 트리거**: 직전 **금요일 10:00** KST 이상 ~ **이번 실행이 시작된 시각** 미만, `applied` 단계 지원만.

로컬에서 샘플 JSON을 쓸 때는 `APPLIED_TIME_FILTER=false`로 끄는 것을 권장합니다. GitHub Actions에서는 `GITHUB_ACTIONS=true`일 때 기본으로 시간 필터가 켜지며, 워크플로에서 `APPLIED_TIME_FILTER=true`로 명시합니다.

## 수동 실행

저장소 **Actions** 탭에서 `Recruitment Slack recommendations` 워크플로를 선택한 뒤 **Run workflow**로 즉시 실행할 수 있습니다.

## 다른 런타임

온프레미스나 다른 클라우드에서는 동일 디렉터리에서 `python -m src.main`을 **cron** 또는 **작업 스케줄러**로 같은 시각에 호출하면 됩니다.
