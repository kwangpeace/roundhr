from __future__ import annotations

import json
import time
from typing import Any

import requests
from openai import OpenAI

SYSTEM_PROMPT = """You are a senior recruiting analyst for document screening.
Grade each applicant who is currently in the applied stage.

Grades:
- S: core talent, strong match to JD, clear impact and depth
- A: strong fit, minor gaps only
- B: average fit, needs more review or missing depth
- C: recommend not advancing document screening (not automatic rejection; hiring manager decides)

Rules:
- Base judgment on JD and candidate fields only; do not penalize or reward by application channel alone.
- Output valid JSON only, no markdown fences.
- Include every candidate_id from the input in grades[].
- grade must be exactly one of: S, A, B, C.

JSON schema:
{
  "job_id": number,
  "job_title": string,
  "team_title": string,
  "summary": string,
  "grades": [
    {
      "candidate_id": number,
      "grade": "S"|"A"|"B"|"C",
      "reason": string,
      "risks": string
    }
  ]
}
"""


def _strip_for_llm(row: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "candidate_id",
        "job_id",
        "job_title",
        "team_title",
        "position_group_title",
        "position_title",
        "candidate_name",
        "candidate_introduction",
        "candidate_recent_education",
        "candidate_recent_experience",
        "candidate_skill_titles",
        "candidate_from_title",
        "candidate_applied_at",
    )
    return {k: row.get(k) for k in keys}


def grade_job_group(
    *,
    job_id: int,
    jd_text: str,
    meta_title: str,
    meta_team: str,
    candidates: list[dict[str, Any]],
    llm_provider: str,
    llm_api_key: str,
    model: str,
    llm_base_url: str | None,
    gemini_fallback_models: list[str],
    mock_llm: bool,
) -> dict[str, Any]:
    if mock_llm:
        return _mock_grades(job_id, meta_title, meta_team, candidates)

    slim = [_strip_for_llm(c) for c in candidates]
    user_payload = {
        "job_id": job_id,
        "job_title": meta_title,
        "team_title": meta_team,
        "job_description": jd_text or "(No full JD text; use job_title/team/position only.)",
        "candidates": slim,
    }
    user_text = json.dumps(user_payload, ensure_ascii=False, indent=2)

    if llm_provider == "gemini":
        models_to_try: list[str] = []
        for m in [model, *gemini_fallback_models]:
            if m and m not in models_to_try:
                models_to_try.append(m)

        last_err: Exception | None = None
        raw = "{}"
        succeeded = False
        for m in models_to_try:
            try:
                raw = _gemini_chat_completion_json(
                    api_key=llm_api_key,
                    model=m,
                    system_prompt=SYSTEM_PROMPT,
                    user_text=user_text,
                    base_url=llm_base_url,
                )
                succeeded = True
                break
            except Exception as e:
                last_err = e
                continue
        if not succeeded:
            if last_err is not None:
                raise last_err
            raise RuntimeError("Gemini grading failed with no models to try.")
    else:
        client = OpenAI(api_key=llm_api_key, base_url=llm_base_url)
        completion = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=0.2,
        )
        raw = completion.choices[0].message.content or "{}"
    parsed = json.loads(raw)
    _validate_result(parsed, candidates, job_id)
    return parsed


def _gemini_chat_completion_json(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    user_text: str,
    base_url: str | None,
) -> str:
    root = (base_url or "https://generativelanguage.googleapis.com/v1beta/openai").rstrip("/")
    url = f"{root}/chat/completions"
    payload = {
        "model": model,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.2,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Gemini occasionally returns 429/503 under load; short exponential backoff helps batch jobs.
    max_attempts = 6
    backoff_s = 1.0
    last_text = ""
    for attempt in range(1, max_attempts + 1):
        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        last_text = resp.text
        if resp.status_code < 400:
            data = resp.json()
            return (
                (((data.get("choices") or [{}])[0].get("message") or {}).get("content")) or "{}"
            )

        retry_after = resp.headers.get("Retry-After")
        if resp.status_code in (408, 409, 425, 429, 500, 502, 503, 504) and attempt < max_attempts:
            sleep_s = backoff_s
            if retry_after:
                try:
                    sleep_s = max(sleep_s, float(retry_after))
                except ValueError:
                    pass
            time.sleep(sleep_s)
            backoff_s = min(backoff_s * 1.8, 30.0)
            continue

        raise RuntimeError(f"Gemini API error {resp.status_code}: {last_text}")

    raise RuntimeError(f"Gemini API error after retries: {last_text}")


def _mock_grades(
    job_id: int,
    meta_title: str,
    meta_team: str,
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    grades = []
    for c in candidates:
        cid = c.get("candidate_id") or c.get("id")
        grades.append(
            {
                "candidate_id": int(cid) if cid is not None else 0,
                "grade": "B",
                "reason": "MOCK_LLM: replace with real LLM grading.",
                "risks": "",
            }
        )
    return {
        "job_id": job_id,
        "job_title": meta_title,
        "team_title": meta_team,
        "summary": "Mock run; set MOCK_LLM=false and LLM_API_KEY for real scores.",
        "grades": grades,
    }


def _validate_result(
    parsed: dict[str, Any],
    candidates: list[dict[str, Any]],
    job_id: int,
) -> None:
    grades = parsed.get("grades")
    if not isinstance(grades, list):
        raise ValueError("LLM output missing grades array")
    ids_in = set()
    for c in candidates:
        cid = c.get("candidate_id")
        if cid is None:
            cid = c.get("id")
        if cid is not None:
            ids_in.add(int(cid))
    ids_out = {int(g["candidate_id"]) for g in grades if "candidate_id" in g}
    missing = ids_in - ids_out
    if missing:
        raise ValueError(f"LLM omitted candidate_ids: {missing}")
    for g in grades:
        if g.get("grade") not in ("S", "A", "B", "C"):
            raise ValueError(f"Invalid grade: {g}")
