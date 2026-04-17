from __future__ import annotations

import json
import os
from typing import Any

from .roundhr_http import fetch_via_http


def _read_json_file(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "data" in data:
        data = data["data"]
    if not isinstance(data, list):
        raise ValueError(f"JSON root must be a list or object with 'data' array: {path}")
    return data


def normalize_candidate_ids(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for r in rows:
        if r.get("candidate_id") is None and r.get("id") is not None:
            r["candidate_id"] = r["id"]
    return rows


def load_candidates(
    *,
    input_json_path: str | None,
    roundhr_api_url: str | None,
    roundhr_api_token: str | None,
    roundhr_query: str | None,
) -> list[dict[str, Any]]:
    if roundhr_api_url and roundhr_api_token:
        return normalize_candidate_ids(
            fetch_via_http(roundhr_api_url, roundhr_api_token, roundhr_query)
        )
    if input_json_path and os.path.isfile(input_json_path):
        return normalize_candidate_ids(_read_json_file(input_json_path))
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sample = os.path.join(root, "examples", "sample_candidates.json")
    if os.path.isfile(sample):
        return normalize_candidate_ids(_read_json_file(sample))
    raise FileNotFoundError(
        "No data source: set ROUNDHR_API_URL+ROUNDHR_API_TOKEN or INPUT_JSON_PATH, "
        "or add examples/sample_candidates.json"
    )


def filter_applied(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        if str(row.get("job_stage_kind", "")).lower() != "applied":
            continue
        out.append(row)
    return out


def group_by_job_id(rows: list[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    groups: dict[int, list[dict[str, Any]]] = {}
    for row in rows:
        jid = row.get("job_id")
        if jid is None:
            continue
        try:
            key = int(jid)
        except (TypeError, ValueError):
            continue
        groups.setdefault(key, []).append(row)
    return groups
