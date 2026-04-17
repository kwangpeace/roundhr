from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Any

# 한국은 일광절약이 없어 고정 UTC+9 (Windows 등 tzdata 미설치 환경에서도 동작)
KST = timezone(timedelta(hours=9))


@dataclass(frozen=True)
class AppliedWindow:
    """Inclusive start, exclusive end (KST, tz-aware datetimes)."""

    start: datetime
    end: datetime

    def describe_kst(self) -> str:
        s = self.start.astimezone(KST).strftime("%Y-%m-%d %H:%M")
        e = self.end.astimezone(KST).strftime("%Y-%m-%d %H:%M")
        return f"{s} ~ {e} KST (시작 포함, 종료 시각 제외)"


def compute_applied_window(now: datetime | None = None) -> AppliedWindow:
    """
    - 화~금: 전날 09:50 KST 이상 ~ 배치 시작 시각(미만).
    - 월요일: 직전 금요일 10:00 KST 이상 ~ 배치 시작 시각(미만).
    """
    end = (now or datetime.now(KST)).astimezone(KST)
    today: date = end.date()
    if today.weekday() == 0:  # Monday
        friday = today - timedelta(days=3)
        start = datetime.combine(friday, time(10, 0), tzinfo=KST)
    else:
        prev = today - timedelta(days=1)
        start = datetime.combine(prev, time(9, 50), tzinfo=KST)
    return AppliedWindow(start=start, end=end)


def parse_candidate_applied_at(row: dict[str, Any]) -> datetime | None:
    raw = row.get("candidate_applied_at")
    if raw is None or raw == "":
        return None
    if isinstance(raw, datetime):
        dt = raw
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=KST)
        return dt.astimezone(KST)
    if not isinstance(raw, str):
        return None
    s = raw.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=KST)
    return dt.astimezone(KST)


def filter_rows_by_applied_window(
    rows: list[dict[str, Any]], window: AppliedWindow
) -> tuple[list[dict[str, Any]], int]:
    kept: list[dict[str, Any]] = []
    missing_ts = 0
    for row in rows:
        at = parse_candidate_applied_at(row)
        if at is None:
            missing_ts += 1
            continue
        if window.start <= at < window.end:
            kept.append(row)
    return kept, missing_ts
