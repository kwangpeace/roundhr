from __future__ import annotations

import argparse
import os
import sys

from .settings import load_settings
from .slack_notify import post_to_slack


def _read_message(path: str | None) -> str:
    if path:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    data = sys.stdin.read()
    return data.strip()


def run() -> int:
    parser = argparse.ArgumentParser(
        description="Post a pre-formatted message (from Cursor, etc.) to Slack."
    )
    parser.add_argument(
        "--file",
        "-f",
        default="message.md",
        help="텍스트 파일 경로 (기본 message.md). '-' 이면 표준 입력에서 읽음.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Slack 전송 없이 출력만")
    args = parser.parse_args()

    file_arg = None if args.file == "-" else args.file
    if file_arg and not os.path.isfile(file_arg):
        print(f"파일을 찾을 수 없습니다: {file_arg}", file=sys.stderr)
        return 2

    text = _read_message(file_arg)
    if not text:
        print("보낼 메시지가 비어 있습니다.", file=sys.stderr)
        return 2

    print(text)

    if args.dry_run:
        return 0

    settings = load_settings()
    if not settings.slack_bot_token or not settings.slack_channel_id:
        print("SLACK_BOT_TOKEN / SLACK_CHANNEL_ID 가 없습니다. .env 확인.", file=sys.stderr)
        return 1

    post_to_slack(settings.slack_bot_token, settings.slack_channel_id, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
