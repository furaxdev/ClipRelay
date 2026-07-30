"""Thin wrapper around pyperclip to track clipboard changes."""
from __future__ import annotations

import pyperclip


class ClipboardMonitor:
    def __init__(self):
        self._last = self._read()

    @staticmethod
    def _read() -> str:
        try:
            return pyperclip.paste() or ""
        except Exception:
            # Clipboard can transiently fail to open on some platforms/desktops.
            return ""

    def baseline(self) -> str:
        """Snapshot the current clipboard so future changes are relative to it."""
        self._last = self._read()
        return self._last

    def poll_change(self) -> str | None:
        """Return the new clipboard content if it changed since the baseline, else None."""
        current = self._read()
        if current != self._last and current.strip() != "":
            self._last = current
            return current
        return None
