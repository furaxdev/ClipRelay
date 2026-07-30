"""Cross-platform "cancel window" for the confirmation countdown.

Gives the user a few seconds to cancel an auto-send before it's logged as
sent. On a real TTY: Enter cancels (Unix) / any key cancels (Windows). When
not attached to a TTY (e.g. running as a background service), the countdown
just runs to completion since there's no way to interrupt it.
"""
from __future__ import annotations

import os
import sys
import time


def wait_for_cancel(seconds: float) -> bool:
    """Sleep up to `seconds`, returning True if the user cancelled early."""
    if not sys.stdin.isatty():
        time.sleep(seconds)
        return False

    if os.name == "nt":
        return _wait_windows(seconds)
    return _wait_unix(seconds)


def _wait_windows(seconds: float) -> bool:
    import msvcrt

    end = time.time() + seconds
    while time.time() < end:
        if msvcrt.kbhit():
            msvcrt.getch()
            return True
        time.sleep(0.05)
    return False


def _wait_unix(seconds: float) -> bool:
    import select

    end = time.time() + seconds
    while True:
        remaining = end - time.time()
        if remaining <= 0:
            return False
        ready, _, _ = select.select([sys.stdin], [], [], min(remaining, 0.2))
        if ready:
            sys.stdin.readline()
            return True


def ask_yes_no(prompt: str) -> bool:
    """Blocking, explicit confirmation for sensitive content (no timeout, no auto-proceed)."""
    if not sys.stdin.isatty():
        return False
    try:
        answer = input(prompt).strip().lower()
    except EOFError:
        return False
    return answer in ("y", "yes", "o", "oui")
