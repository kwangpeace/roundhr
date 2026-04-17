from __future__ import annotations

import os


def load_jd_text(job_id: int, jd_dir: str, jd_fallback: str | None) -> str:
    path = os.path.join(jd_dir, f"{job_id}.txt")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            text = f.read().strip()
            if text:
                return text
    return (jd_fallback or "").strip()
