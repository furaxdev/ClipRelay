"""Tails a text file (like `tail -f`), yielding new lines as they are appended.

Used to read Claude Code's session log in the prototype. Handles the file
not existing yet and being truncated/rotated (e.g. a new session start).
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Iterator


class LogTailer:
    def __init__(self, path: str, poll_interval: float = 0.3, from_end: bool = True):
        self.path = Path(path)
        self.poll_interval = poll_interval
        self._from_end = from_end
        self._fh = None
        self._pos = 0

    def _open(self) -> bool:
        if not self.path.exists():
            return False
        self._fh = open(self.path, "r", encoding="utf-8", errors="replace")
        if self._from_end:
            self._fh.seek(0, os.SEEK_END)
        self._pos = self._fh.tell()
        return True

    def poll_lines(self) -> Iterator[str]:
        """Non-blocking: yields any new complete lines available right now."""
        if self._fh is None:
            if not self._open():
                return
        try:
            size = self.path.stat().st_size
        except FileNotFoundError:
            return
        if size < self._pos:
            # File was truncated or replaced (new session) - reopen from start.
            self._fh.close()
            self._fh = open(self.path, "r", encoding="utf-8", errors="replace")
            self._pos = 0
        while True:
            line = self._fh.readline()
            if not line:
                break
            self._pos = self._fh.tell()
            if line.endswith("\n"):
                yield line.rstrip("\n")
            else:
                # Partial line written so far; wait for the rest next poll.
                self._fh.seek(self._pos - len(line))
                break

    def wait_for_lines(self) -> Iterator[str]:
        """Blocking generator: sleeps between polls, forever."""
        while True:
            yield from self.poll_lines()
            time.sleep(self.poll_interval)
