from __future__ import annotations

import os
import re
from dataclasses import dataclass

from dotenv import load_dotenv


def _truthy(name: str, default: bool = False) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


def _applied_time_filter_from_env() -> bool:
    v = os.environ.get("APPLIED_TIME_FILTER")
    if v is None:
        # GitHub Actions / Railway 프로덕션에서는 기본으로 기간 필터 사용
        if os.environ.get("GITHUB_ACTIONS") == "true":
            return True
        if any(
            os.environ.get(k)
            for k in ("RAILWAY_ENVIRONMENT", "RAILWAY_ENVIRONMENT_NAME", "RAILWAY_PROJECT_ID")
        ):
            return True
        return False
    return _truthy("APPLIED_TIME_FILTER", False)


@dataclass
class Settings:
    input_json_path: str | None
    roundhr_api_url: str | None
    roundhr_api_token: str | None
    roundhr_query: str | None
    llm_provider: str
    llm_api_key: str | None
    llm_model: str
    llm_base_url: str | None
    gemini_fallback_models: list[str]
    slack_bot_token: str | None
    slack_channel_id: str | None
    jd_dir: str
    jd_fallback: str | None
    mask_candidate_names: bool
    dry_run: bool
    mock_llm: bool
    applied_time_filter: bool


def load_settings() -> Settings:
    load_dotenv()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_jd = os.path.join(root, "config", "jd")
    llm_provider = (os.environ.get("LLM_PROVIDER") or "openai").strip().lower()
    if llm_provider == "gemini":
        llm_api_key = os.environ.get("LLM_API_KEY") or os.environ.get("GEMINI_API_KEY")
    else:
        llm_api_key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    llm_model = (
        os.environ.get("LLM_MODEL")
        or os.environ.get("OPENAI_MODEL")
        or ("gemini-2.0-flash" if llm_provider == "gemini" else "gpt-4o-mini")
    )

    gemini_fallback_models: list[str] = []
    raw_fallback = os.environ.get("GEMINI_FALLBACK_MODELS")
    if raw_fallback:
        gemini_fallback_models = [p.strip() for p in re.split(r"[,\s]+", raw_fallback.strip()) if p.strip()]
    elif llm_provider == "gemini":
        gemini_fallback_models = ["gemini-flash-latest", "gemini-2.5-flash-lite"]
    return Settings(
        input_json_path=os.environ.get("INPUT_JSON_PATH"),
        roundhr_api_url=os.environ.get("ROUNDHR_API_URL"),
        roundhr_api_token=os.environ.get("ROUNDHR_API_TOKEN"),
        roundhr_query=os.environ.get("ROUNDHR_QUERY"),
        llm_provider=llm_provider,
        llm_api_key=llm_api_key,
        llm_model=llm_model,
        llm_base_url=os.environ.get("LLM_BASE_URL"),
        gemini_fallback_models=gemini_fallback_models,
        slack_bot_token=os.environ.get("SLACK_BOT_TOKEN"),
        slack_channel_id=os.environ.get("SLACK_CHANNEL_ID"),
        jd_dir=os.environ.get("JD_DIR", default_jd),
        jd_fallback=os.environ.get("JD_FALLBACK") or None,
        mask_candidate_names=_truthy("MASK_CANDIDATE_NAMES", False),
        dry_run=_truthy("DRY_RUN", False),
        mock_llm=_truthy("MOCK_LLM", False),
        applied_time_filter=_applied_time_filter_from_env(),
    )
