from __future__ import annotations

import json
from typing import Any

import requests

DEFAULT_QUERY = (
    "SELECT c.id AS candidate_id, c.job_id, c.job_title, c.team_title, "
    "c.position_group_title, c.position_title, c.candidate_name, c.job_stage_kind, "
    "c.candidate_introduction, c.candidate_recent_education, c.candidate_recent_experience, "
    "c.candidate_skill_titles, c.candidate_from_title, c.candidate_applied_at "
    "FROM vw_candidates c WHERE c.job_stage_kind = 'applied' "
    "ORDER BY c.job_id, c.candidate_applied_at DESC"
)


def fetch_via_http(url: str, token: str, query: str | None) -> list[dict[str, Any]]:
    q = (query or DEFAULT_QUERY).strip()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, headers=headers, json={"query": q}, timeout=120)
    resp.raise_for_status()
    body = resp.json()
    if isinstance(body, list):
        return body
    if isinstance(body, dict) and "data" in body:
        data = body["data"]
        if isinstance(data, list):
            return data
    raise ValueError(f"Unexpected RoundHR API response shape: {type(body)}")
