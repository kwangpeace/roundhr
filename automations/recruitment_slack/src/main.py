from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from typing import Any

from .applied_time_window import compute_applied_window, filter_rows_by_applied_window
from .data_sources.load_candidates import filter_applied, group_by_job_id, load_candidates
from .jd_loader import load_jd_text
from .llm_grade import grade_job_group
from .settings import load_settings
from .slack_notify import format_report_block, post_to_slack


def _meta_from_group(job_id: int, group: list[dict[str, Any]]) -> tuple[str, str]:
    first = group[0]
    return str(first.get("job_title") or f"job_{job_id}"), str(first.get("team_title") or "")


def _candidate_id(row: dict[str, Any]) -> int | None:
    cid = row.get("candidate_id")
    if cid is None:
        cid = row.get("id")
    if cid is None:
        return None
    try:
        return int(cid)
    except (TypeError, ValueError):
        return None


def run() -> int:
    parser = argparse.ArgumentParser(description="Recruitment Slack recommendation batch")
    parser.add_argument("--dry-run", action="store_true", help="Print only; no Slack")
    args = parser.parse_args()
    if args.dry_run:
        os.environ["DRY_RUN"] = "true"

    settings = load_settings()
    rows = load_candidates(
        input_json_path=settings.input_json_path,
        roundhr_api_url=settings.roundhr_api_url,
        roundhr_api_token=settings.roundhr_api_token,
        roundhr_query=settings.roundhr_query,
    )
    applied = filter_applied(rows)
    if not applied:
        print("No candidates in applied stage; exiting.", file=sys.stderr)
        return 0

    window_note = "시간 필터 비활성 (로컬 기본; GitHub Actions에서는 기본 활성)"
    if settings.applied_time_filter:
        window = compute_applied_window()
        filtered, missing_ts = filter_rows_by_applied_window(applied, window)
        if missing_ts:
            print(
                f"candidate_applied_at 없음으로 제외: {missing_ts}건",
                file=sys.stderr,
            )
        applied = filtered
        window_note = window.describe_kst()
        if not applied:
            print(
                f"지정 기간 내 applied 지원자 없음 ({window_note}); 종료.",
                file=sys.stderr,
            )
            return 0

    groups = group_by_job_id(applied)
    header = (
        f":briefcase: *서류 단계 지원자 AI 추천 요약*\n"
        f"_실행_: {datetime.now(timezone.utc).astimezone().isoformat(timespec='minutes')}\n"
        f"_기간_: {window_note}\n"
        f"_대상_: `applied` {len(applied)}명 / 공고 {len(groups)}건\n"
    )
    blocks: list[str] = []

    for job_id in sorted(groups.keys()):
        group = groups[job_id]
        meta_title, meta_team = _meta_from_group(job_id, group)
        jd = load_jd_text(job_id, settings.jd_dir, settings.jd_fallback)
        meta_bits = [
            f"직군: {group[0].get('position_group_title') or '-'}",
            f"직무: {group[0].get('position_title') or '-'}",
        ]
        if not jd:
            jd = "\n".join(meta_bits)

        use_mock = (not settings.llm_api_key) or settings.mock_llm

        result = grade_job_group(
            job_id=job_id,
            jd_text=jd,
            meta_title=meta_title,
            meta_team=meta_team,
            candidates=group,
            llm_provider=settings.llm_provider,
            llm_api_key=settings.llm_api_key or "",
            model=settings.llm_model,
            llm_base_url=settings.llm_base_url,
            gemini_fallback_models=settings.gemini_fallback_models,
            mock_llm=use_mock,
        )

        by_id: dict[int, dict[str, Any]] = {}
        for row in group:
            cid = _candidate_id(row)
            if cid is not None:
                by_id[cid] = row
        blocks.append(format_report_block(result, by_id, settings.mask_candidate_names))

    full_message = header + "\n\n" + ("\n\n---\n\n".join(blocks))

    print(full_message)

    if settings.dry_run:
        return 0
    if not settings.slack_bot_token or not settings.slack_channel_id:
        print("SLACK_BOT_TOKEN / SLACK_CHANNEL_ID missing; printed to stdout only.", file=sys.stderr)
        return 0

    post_to_slack(settings.slack_bot_token, settings.slack_channel_id, full_message)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
