"""Decide whether a captured clipboard value should be treated as sensitive.

Two independent checks, either one is enough to flag as sensitive:
1. Shape-based: the clipboard text itself looks like a known secret format
   (AWS key, GitHub token, private key block, JWT, ...).
2. Context-based: the question that armed the watcher mentions a sensitive
   keyword (password, api key, token, ...), regardless of the answer's shape.

Neither check requires storing an actual secret value in config - the
"denylist" the user configures is a list of *keywords/patterns*, not values.
"""
from __future__ import annotations

import re
from typing import Optional, Tuple

from .config import Config


def classify(question_line: Optional[str], clipboard_text: str, config: Config) -> Tuple[bool, Optional[str]]:
    for name, pattern in config.secret_patterns.items():
        if re.search(pattern, clipboard_text):
            return True, f"shape:{name}"

    lower_q = (question_line or "").lower()
    for keyword in config.sensitive_context_keywords:
        if keyword.lower() in lower_q:
            return True, f"context:{keyword}"

    return False, None
