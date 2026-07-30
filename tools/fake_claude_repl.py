#!/usr/bin/env python3
"""A minimal stand-in for Claude Code's prompt loop, for testing the tmux
backend against something that behaves like a real interactive CLI (reads
injected text as its own input) instead of a shell that would try to
*execute* the injected text as a command.
"""
from __future__ import annotations

import sys

QUESTIONS = [
    "Initialisation du projet...",
    "Peux-tu me donner ta clé API OpenAI pour continuer ?",
]


def main() -> None:
    for line in QUESTIONS:
        print(line, flush=True)
    while True:
        try:
            answer = input()
        except EOFError:
            break
        print(f"[fake-claude] reçu : {answer}", flush=True)


if __name__ == "__main__":
    main()
