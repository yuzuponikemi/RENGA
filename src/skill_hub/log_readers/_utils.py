"""Shared utilities across log readers (user_id resolution, correction detection)."""
import functools
import hashlib
import os
import re
import subprocess


# ── User identity resolution ────────────────────────────────────────────

@functools.lru_cache(maxsize=1)
def _resolve_stable_user_id() -> str | None:
    """USER_ID env var > git config user.email の SHA-256 先頭 8 桁。"""
    explicit = os.environ.get("USER_ID", "").strip()
    if explicit:
        return explicit
    try:
        email = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True, text=True, timeout=2,
        ).stdout.strip()
        if email:
            return hashlib.sha256(email.encode()).hexdigest()[:8]
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return None


def resolve_user_id(session_id: str) -> str:
    """USER_ID env > git email hash > session_id 先頭 8 桁（後方互換）。"""
    stable = _resolve_stable_user_id()
    return stable if stable is not None else session_id[:8]


# ── Correction / system-message heuristics ─────────────────────────────

_CORRECTION_PATTERNS = (
    "違う", "ちがう", "no ", "wrong", "incorrect", "そうじゃない", "やり直し",
)


def is_correction(text: str) -> bool:
    """次ターンが訂正・否定なら True（accepted=False の判定材料）。"""
    t = text.lower()
    return any(p in t for p in _CORRECTION_PATTERNS)


_SYSTEM_PREFIXES = (
    "<task-notification>", "<system-reminder>", "<command-name>",
    "<user-prompt-submit-hook>",
)
_LOOP_MARKERS = (
    "Task output file:", "Check if regen_graph", "Check if re-extraction",
)


def is_system_message(text: str) -> bool:
    """ScheduleWakeup ループ・CI フック・システムリマインダーを除外。"""
    t = text.strip()
    if any(t.startswith(p) for p in _SYSTEM_PREFIXES):
        return True
    if any(marker in t for marker in _LOOP_MARKERS):
        return True
    return False
