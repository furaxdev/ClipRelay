"""Clear, append-only log of everything ClipRelay detects and (would) send."""
from __future__ import annotations

import datetime
from pathlib import Path


class EventLogger:
    def __init__(self, path: str):
        self.path = Path(path)

    def log(self, level: str, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{level}] {message}"
        print(line)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
