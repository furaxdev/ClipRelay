"""Real-terminal backend: read a tmux pane's live output and type into it.

This is the phase 2 integration announced in the README roadmap: instead of
tailing a plain text file that simulates a session, we capture the actual
scrollback of a tmux pane running Claude Code, and instead of only logging
what "would" be sent, we can actually type the composed message into that
pane via `tmux send-keys`.

Requires the `tmux` binary on PATH and an existing target session/pane
(we never create or kill sessions here - that's out of scope and would be
a destructive action to take on the user's behalf).
"""
from __future__ import annotations

import subprocess
from typing import Iterator, List, Optional


class TmuxUnavailable(RuntimeError):
    pass


def _run(args: List[str]) -> str:
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=5)
    except FileNotFoundError as exc:
        raise TmuxUnavailable("tmux binary not found on PATH") from exc
    if result.returncode != 0:
        raise TmuxUnavailable(f"tmux command failed: {' '.join(args)}\n{result.stderr}")
    return result.stdout


def session_exists(target: str) -> bool:
    try:
        _run(["tmux", "has-session", "-t", target])
        return True
    except TmuxUnavailable:
        return False


def capture_pane(target: str) -> List[str]:
    """Return the pane's visible lines, with trailing blank padding rows
    (tmux pads the snapshot to the full pane height) stripped off - keeping
    them would make unrelated blank rows collide when diffing two polls.
    """
    text = _run(["tmux", "capture-pane", "-t", target, "-p"])
    lines = text.split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def send_text(target: str, message: str) -> None:
    """Type `message` into the pane as literal text, then press Enter.

    Uses -l (literal) so tmux doesn't try to interpret the message as key
    names (e.g. a message containing the word "Enter" would otherwise be
    parsed as a key, not typed literally).
    """
    _run(["tmux", "send-keys", "-t", target, "-l", message])
    _run(["tmux", "send-keys", "-t", target, "Enter"])


class TmuxPaneTailer:
    """Same polling interface as LogTailer (poll_lines()), backed by a tmux pane."""

    def __init__(self, target: str):
        self.target = target
        self._last_lines: List[str] = []

    def poll_lines(self) -> Iterator[str]:
        current_lines = capture_pane(self.target)

        if not self._last_lines:
            self._last_lines = current_lines
            return

        old = self._last_lines
        new = current_lines
        # Pane content scrolls: find the longest suffix of `old` that is a
        # prefix of `new`, then whatever follows in `new` is genuinely new.
        new_lines = _find_new_suffix(old, new)
        self._last_lines = new
        for line in new_lines:
            if line.strip():
                yield line


def _find_new_suffix(old: List[str], new: List[str]) -> List[str]:
    if old == new:
        return []
    max_check = min(len(old), len(new))
    for i in range(max_check, -1, -1):
        if (old[len(old) - i:] if i else []) == new[:i]:
            return new[i:]
    return new
