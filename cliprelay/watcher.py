"""The ClipRelay state machine.

IDLE -> (question line matched in session log) -> ARMED
ARMED -> (clipboard changes before the arm window expires) -> CAPTURED
ARMED -> (arm window expires with no clipboard change) -> IDLE
CAPTURED -> sensitive?  -> explicit y/n prompt, no timeout, no auto-send
CAPTURED -> not sensitive -> countdown (cancellable) -> SENT or CANCELLED -> IDLE

"SENT" in this prototype means: the composed message is written to the
event log as what *would* be typed into the real Claude Code terminal. No
keystrokes are actually injected anywhere yet - that's the next phase.
"""
from __future__ import annotations

import re
import time
from typing import List, Optional

from .clipboard import ClipboardMonitor
from .config import Config
from .confirm import ask_yes_no, wait_for_cancel
from .eventlog import EventLogger
from .logtail import LogTailer
from .sensitivity import classify


class ClipRelayWatcher:
    def __init__(self, config: Config):
        self.config = config
        self.logger = EventLogger(config.output_log_path)
        self.tailer = LogTailer(config.session_log_path, poll_interval=config.log_poll_interval)
        self.clipboard = ClipboardMonitor()
        self._question_patterns = [re.compile(p, re.IGNORECASE) for p in config.all_question_patterns()]
        self._armed_until: Optional[float] = None
        self._triggering_question: Optional[str] = None

    def _matches_question(self, line: str) -> bool:
        return any(p.search(line) for p in self._question_patterns)

    def _arm(self, question_line: str) -> None:
        self._armed_until = time.time() + self.config.arm_window_seconds
        self._triggering_question = question_line
        self.clipboard.baseline()
        self.logger.log("QUESTION_DETECTED", f'line="{question_line}"')
        self.logger.log(
            "ARMED",
            f"watching clipboard for the next change (window={self.config.arm_window_seconds}s)",
        )

    def _disarm(self, reason: str) -> None:
        self.logger.log("DISARMED", reason)
        self._armed_until = None
        self._triggering_question = None

    def _handle_capture(self, clipboard_text: str) -> None:
        preview = clipboard_text if len(clipboard_text) <= 60 else clipboard_text[:57] + "..."
        self.logger.log("CLIPBOARD_CHANGED", f"captured new content (len={len(clipboard_text)}, preview=\"{preview}\")")

        is_sensitive, rule = classify(self._triggering_question, clipboard_text, self.config)
        message = self.config.message_template.format(clipboard=clipboard_text)

        if is_sensitive or self.config.always_require_confirmation:
            reason = f"matched rule={rule}" if is_sensitive else "always_require_confirmation=true"
            self.logger.log("SENSITIVE_CHECK", f"{reason} -> manual confirmation required, no auto-send")
            confirmed = ask_yes_no(f"Send this to Claude Code? [y/N]: {message}\n> ")
            if confirmed:
                self.logger.log("SENT", f'message="{message}" (simulated - manual confirm)')
            else:
                self.logger.log("CANCELLED", "user declined manual confirmation")
        else:
            self.logger.log("COMPOSED", f'message="{message}"')
            self.logger.log(
                "COUNTDOWN",
                f"sending in {self.config.confirm_delay_seconds}s - press Enter to cancel",
            )
            cancelled = wait_for_cancel(self.config.confirm_delay_seconds)
            if cancelled:
                self.logger.log("CANCELLED", "user cancelled during countdown")
            else:
                self.logger.log("SENT", f'message="{message}" (simulated - would be typed into terminal)')

        self._disarm("capture handled, returning to idle")

    def run_forever(self) -> None:
        self.logger.log(
            "START",
            f"watching session_log={self.config.session_log_path!r}, "
            f"output_log={self.config.output_log_path!r}",
        )
        while True:
            for line in self.tailer.poll_lines():
                if self._matches_question(line):
                    self._arm(line)

            if self._armed_until is not None:
                if time.time() > self._armed_until:
                    self._disarm("arm window expired with no clipboard change")
                else:
                    new_value = self.clipboard.poll_change()
                    if new_value is not None:
                        self._handle_capture(new_value)

            time.sleep(self.config.clipboard_poll_interval)
