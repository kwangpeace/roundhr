from __future__ import annotations

import re
from typing import Any

import requests

SLACK_MAX = 3500


def format_report_block(
    result: dict[str, Any],
    candidates_by_id: dict[int, dict[str, Any]],
    mask_names: bool,
) -> str:
    job_id = result.get("job_id", "")
    title = result.get("job_title", "")
    team = result.get("team_title", "")
    summary = result.get("summary", "")
    lines: list[str] = [
        f"*{team}* · *{title}* (`job_id={job_id}`)",
        f"_요약_: {summary}",
        "",
    ]
    order = {"S": 0, "A": 1, "B": 2, "C": 3}
    grades = list(result.get("grades") or [])
    grades.sort(key=lambda g: (order.get(str(g.get("grade")), 9), g.get("candidate_id")))

    for g in grades:
        cid = int(g["candidate_id"])
        row = candidates_by_id.get(cid, {})
        name = row.get("candidate_name") or f"id:{cid}"
        if mask_names:
            name = f"후보#{cid}"
        grade = g.get("grade", "?")
        reason = g.get("reason", "")
        risks = g.get("risks", "")
        lines.append(f"*{grade}* · {name} (id `{cid}`)")
        lines.append(f"  - 추천·평가: {reason}")
        if risks:
            lines.append(f"  - 리스크: {risks}")
        lines.append("")
    return "\n".join(lines).strip()


def split_message(text: str, limit: int = SLACK_MAX) -> list[str]:
    if len(text) <= limit:
        return [text]
    parts: list[str] = []
    chunks = re.split(r"\n\n+", text)
    buf: list[str] = []
    size = 0
    for ch in chunks:
        sep = 2 if buf else 0
        if size + sep + len(ch) > limit and buf:
            parts.append("\n\n".join(buf))
            buf = [ch]
            size = len(ch)
        else:
            if buf:
                size += sep
            buf.append(ch)
            size += len(ch)
    if buf:
        parts.append("\n\n".join(buf))
    return parts


def post_to_slack(token: str, channel_id: str, text: str) -> None:
    url = "https://slack.com/api/chat.postMessage"
    for i, chunk in enumerate(split_message(text)):
        resp = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={"channel": channel_id, "text": chunk, "mrkdwn": True},
            timeout=60,
        )
        body = resp.json()
        if not body.get("ok"):
            raise RuntimeError(f"Slack API error: {body}")
        if i > 0:
            import time

            time.sleep(0.3)
