"""Filter retained memories and redact body content.

Two passes:
1. TAG FILTER — drop memories whose tags intersect TAG_EXCLUDE.
2. BODY REDACTOR — within retained memories AND within retained config values,
   remove sentences/lines that hit personal-scope tokens. Memories that lose
   too much content are dropped entirely.
"""

from __future__ import annotations
import re

from .config import (
    TAG_EXCLUDE,
    TAG_EXCLUDE_PATTERNS,
    REDACT_TOKEN_PATTERNS,
    LINE_DROP_PATTERNS,
    HARD_DROP_PATTERNS,
    MIN_LINES_AFTER_REDACT,
)


# ─── Memory tag filter ──────────────────────────────────────────────────────

def _tag_excluded(tag: str) -> bool:
    if tag in TAG_EXCLUDE:
        return True
    for pat in TAG_EXCLUDE_PATTERNS:
        if pat.match(tag):
            return True
    return False


def filter_memories_by_tag(memories: list[dict]) -> tuple[list[dict], int]:
    """Drop memories with any excluded-tag intersection.

    Returns (kept, dropped_count).
    """
    kept = []
    dropped = 0
    for m in memories:
        if any(_tag_excluded(t) for t in m.get("tags", [])):
            dropped += 1
            continue
        kept.append(m)
    return kept, dropped


# ─── Hard-drop check ────────────────────────────────────────────────────────

def _hard_drop_body(text: str) -> bool:
    """True if any HARD_DROP_PATTERNS hits the body."""
    for pat in HARD_DROP_PATTERNS:
        if pat.search(text):
            return True
    return False


# ─── Body redactor ──────────────────────────────────────────────────────────

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def _line_should_drop(line: str) -> bool:
    """True if the line matches a Turso-storage idiom we don't want to ship."""
    for pat in LINE_DROP_PATTERNS:
        if pat.search(line):
            return True
    return False


def _sentence_should_drop(sentence: str) -> bool:
    """True if the sentence contains a personal-scope token."""
    for pat in REDACT_TOKEN_PATTERNS:
        if pat.search(sentence):
            return True
    return False


def redact_body(text: str) -> str:
    """Sweep `text` for personal-scope tokens.

    Strategy:
    - Walk line by line. Drop lines matching LINE_DROP_PATTERNS outright.
    - For each remaining line, split into sentences; drop sentences hitting
      REDACT_TOKEN_PATTERNS; rejoin.
    - Drop lines that become empty after sentence pruning.

    Returns the redacted text.
    """
    if not text:
        return text

    out_lines: list[str] = []
    for line in text.splitlines():
        if _line_should_drop(line):
            continue

        stripped = line.strip()
        if not stripped:
            out_lines.append(line)
            continue

        sentences = _SENTENCE_SPLIT.split(stripped)
        kept_sentences = [s for s in sentences if not _sentence_should_drop(s)]
        if not kept_sentences:
            continue

        # Preserve leading whitespace from the original line
        leading_ws = line[: len(line) - len(line.lstrip())]
        out_lines.append(leading_ws + " ".join(kept_sentences))

    # Collapse runs of 3+ blank lines
    result = "\n".join(out_lines)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def redact_and_filter_memories(memories: list[dict]) -> tuple[list[dict], dict]:
    """Apply hard-drop and body redactor.

    - Drop memories whose raw body hits HARD_DROP_PATTERNS.
    - Run sentence redactor on the rest.
    - Drop memories gutted below MIN_LINES_AFTER_REDACT.

    Mutates `memories` in place (sets `body_redacted` on kept entries).
    Returns (kept, drop_stats).
    """
    kept = []
    hard_dropped = 0
    gutted = 0
    for m in memories:
        raw = m.get("summary", "")
        if _hard_drop_body(raw):
            hard_dropped += 1
            continue

        redacted = redact_body(raw)
        non_empty = sum(1 for line in redacted.splitlines() if line.strip())
        if non_empty < MIN_LINES_AFTER_REDACT:
            gutted += 1
            continue
        m["body_redacted"] = redacted
        kept.append(m)
    return kept, {"hard_dropped": hard_dropped, "gutted_by_redact": gutted}


def redact_config_value(value: str) -> str:
    """Sweep a config value (ops or profile entry body)."""
    return redact_body(value)
