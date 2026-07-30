"""Configuration loading for ClipRelay.

Config is a plain JSON file so the prototype has zero extra dependencies
beyond pyperclip. Any field omitted from the user's config file falls back
to the defaults below.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from .patterns import (
    DEFAULT_QUESTION_PATTERNS,
    DEFAULT_SECRET_PATTERNS,
    DEFAULT_SENSITIVE_CONTEXT_KEYWORDS,
    LOOSE_QUESTION_FALLBACK,
)

DEFAULTS = {
    "session_log_path": "session.log",
    "output_log_path": "cliprelay_events.log",
    "clipboard_poll_interval": 0.5,
    "log_poll_interval": 0.3,
    "arm_window_seconds": 60,
    "confirm_delay_seconds": 3,
    "message_template": "Voici la valeur demandée : {clipboard}",
    "question_patterns": DEFAULT_QUESTION_PATTERNS,
    "enable_loose_question_fallback": False,
    "secret_patterns": DEFAULT_SECRET_PATTERNS,
    "sensitive_context_keywords": DEFAULT_SENSITIVE_CONTEXT_KEYWORDS,
    "always_require_confirmation": False,
    "backend": "logfile",  # "logfile" (safe default, log-only) or "tmux" (real send-keys)
    "tmux_target": "",  # tmux session/window/pane, e.g. "claude-code" or "claude-code:0.0"
}


@dataclass
class Config:
    session_log_path: str
    output_log_path: str
    clipboard_poll_interval: float
    log_poll_interval: float
    arm_window_seconds: float
    confirm_delay_seconds: float
    message_template: str
    question_patterns: List[str]
    enable_loose_question_fallback: bool
    secret_patterns: Dict[str, str]
    sensitive_context_keywords: List[str]
    always_require_confirmation: bool
    backend: str
    tmux_target: str

    def all_question_patterns(self) -> List[str]:
        patterns = list(self.question_patterns)
        if self.enable_loose_question_fallback:
            patterns.append(LOOSE_QUESTION_FALLBACK)
        return patterns


def load_config(path: str | None) -> Config:
    data = dict(DEFAULTS)
    if path and Path(path).exists():
        with open(path, "r", encoding="utf-8") as f:
            user_data = json.load(f)
        data.update(user_data)
    return Config(**data)
