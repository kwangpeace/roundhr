"""
Slack으로 마크다운 메시지 전송만 담당합니다.
라운드HR 조회는 Cursor 채팅 + MCP로 하세요 (터미널 스크립트는 MCP를 호출할 수 없음).

사용법 (토큰을 파일에 저장하지 않음):
  .\\.venv\\Scripts\\python send_slack.py "xoxb-...|C0123456789"

  또는 파일 경로 지정:
  .\\.venv\\Scripts\\python send_slack.py "xoxb-...|C0123456789" -f message.md

  미리보기만 (전송 안 함):
  .\\.venv\\Scripts\\python send_slack.py "xoxb-...|C0123456789" --dry-run

구분자는 파이프(|) 하나입니다. 토큰과 채널 ID 사이에 공백 없이 붙이세요.
"""
from __future__ import annotations

import argparse
import re
import sys
import time

import requests

SLACK_MAX = 3500


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
            time.sleep(0.3)


def parse_cred(s: str) -> tuple[str, str]:
    s = s.strip()
    if "|" not in s:
        raise ValueError(
            '인자 형식: "xoxb-...토큰|C...채널ID" (가운데 파이프 하나, 공백 없음)'
        )
    token, _, channel = s.partition("|")
    token, channel = token.strip(), channel.strip()
    if not token or not channel:
        raise ValueError("토큰과 채널 ID가 모두 필요합니다.")
    return token, channel


def main() -> int:
    parser = argparse.ArgumentParser(description="Send message.md to Slack (no .env).")
    parser.add_argument(
        "credential",
        nargs="?",
        help='한 덩어리: "xoxb-...|C..."',
    )
    parser.add_argument(
        "-f",
        "--file",
        default="message.md",
        help="전송할 마크다운 파일 (기본 message.md)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Slack 전송 없이 출력만")
    args = parser.parse_args()

    if not args.credential:
        print(__doc__, file=sys.stderr)
        return 2

    try:
        token, channel = parse_cred(args.credential)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2

    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read().strip()
    except OSError as e:
        print(f"파일을 읽을 수 없습니다: {args.file} ({e})", file=sys.stderr)
        return 2

    if not text:
        print("메시지가 비어 있습니다.", file=sys.stderr)
        return 2

    print(text)
    if args.dry_run:
        return 0

    post_to_slack(token, channel, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
