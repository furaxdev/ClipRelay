#!/usr/bin/env python3
"""Appends fake "Claude Code" session lines to a log file, to test ClipRelay
end-to-end without wiring it to a real terminal yet.

Usage:
    python tools/simulate_session.py --log session.log
    # in another terminal:
    python main.py --config config.json
    # then copy some text to your clipboard within the arm window.

Add --auto-copy to also copy a fake (non-real) secret to the clipboard a
few seconds after the question line, so the whole flow can be exercised
without touching the clipboard by hand.
"""
from __future__ import annotations

import argparse
import time

import pyperclip

LINES = [
    "Initializing project...",
    "Reading repository structure...",
    "Peux-tu me donner ta clé API OpenAI pour continuer ?",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="session.log")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds between lines")
    parser.add_argument(
        "--auto-copy",
        action="store_true",
        help="Copy a fake (clearly not real) secret to the clipboard after the question line",
    )
    args = parser.parse_args()

    with open(args.log, "a", encoding="utf-8") as f:
        for line in LINES:
            f.write(line + "\n")
            f.flush()
            print(f"[simulate_session] wrote: {line}")
            time.sleep(args.delay)

    if args.auto_copy:
        fake_secret = "sk-FAKE1234567890EXAMPLEDONOTUSE"
        time.sleep(args.delay)
        pyperclip.copy(fake_secret)
        print(f"[simulate_session] auto-copied fake secret to clipboard: {fake_secret}")


if __name__ == "__main__":
    main()
