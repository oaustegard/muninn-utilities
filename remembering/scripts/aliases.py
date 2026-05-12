"""Kwarg alias translation and write-id return-shape glue.

Holistic fix for the recurring "wrong kwarg name" failure across the
remembering API surface (issue #15). Three pieces, one module:

1. ``ALIASES`` — per-function mapping of deprecated-or-mistaken kwarg names
   to their canonical counterparts.
2. ``accept_aliases`` — decorator that translates deprecated kwargs to the
   canonical name and emits a ``DeprecationWarning`` so callers (human or
   LLM) actually see the mistake. Raises ``TypeError`` if both the wrong
   and right name are passed.
3. ``MemoryWriteId`` — a ``str`` subclass returned by ``remember()`` and
   ``supersede()``. Behaves as a plain string for back-compat, but exposes
   ``.id`` so the natural ``m.id`` access pattern works without callers
   having to remember that the write path returns a bare string.

Field-name aliases on ``MemoryResult`` (e.g. ``m.content`` → ``m.summary``)
live in ``result.py``, where the actual class definition lives; ``COMMON_MISTAKES``
there is the canonical mapping. The decorator below covers the *kwarg* side
of the same failure class.
"""

from __future__ import annotations

import functools
import warnings
from typing import Callable


# Per-function kwarg aliases. Map structure:
#   function_name -> {wrong_kwarg: canonical_kwarg}
#
# These are kwarg names callers reach for from generic API conventions
# (max_results, content, keywords, ...) that the underlying function does
# not accept. The decorator translates them to the canonical name and
# warns. Keep these conservative — only add an alias when the wrong name
# is plausibly auto-completed from another library's surface, not just any
# typo. If a "deprecated" alias is in fact a long-standing supported alias
# elsewhere in the codebase (e.g. ``recall(query=...)``, ``remember(mem_type=...)``),
# leave it OUT of this table — those are handled inside the function body
# as first-class aliases.
ALIASES: dict[str, dict[str, str]] = {
    # recall family — n is the canonical "count"; tags/type are singular/plural-canonical
    "recall": {
        "max_results": "n",
        "count": "n",
        "k": "n",
        "limit": "n",       # was silently translated in-body; surface it now
        "keywords": "tags",
        "types": "type",
    },
    "recall_since": {
        "max_results": "n",
        "count": "n",
        "k": "n",
        "limit": "n",
        "keywords": "tags",
        "types": "type",
    },
    "recall_between": {
        "max_results": "n",
        "count": "n",
        "k": "n",
        "limit": "n",
        "keywords": "tags",
        "types": "type",
    },
    "recall_batch": {
        "max_results": "n",
        "count": "n",
        "k": "n",
        "limit": "n",
        "keywords": "tags",
        "types": "type",
    },
    # remember family — `what` is the canonical content slot
    "remember": {
        "content": "what",
        "body": "what",
        "text": "what",
        "summary": "what",   # supersede uses `summary`; collision-friendly remap
        "keywords": "tags",
    },
    "remember_bg": {
        "content": "what",
        "body": "what",
        "text": "what",
        "summary": "what",
        "keywords": "tags",
    },
    # supersede uses `summary` as its content slot (yes, it's inconsistent
    # with `remember.what` — preserving back-compat). Translate `content`/`body`.
    "supersede": {
        "content": "summary",
        "body": "summary",
        "text": "summary",
        "what": "summary",   # opposite direction from remember(), matches caller intent
        "keywords": "tags",
    },
    # priority adjustment helpers
    "reprioritize": {
        "prio": "priority",
        "importance": "priority",
    },
    "strengthen": {
        "amount": "boost",
        "by": "boost",
    },
    "weaken": {
        "amount": "drop",
        "by": "drop",
    },
    # decision_trace — uses choice/context/rationale; aliases for the most
    # likely auto-completions
    "decision_trace": {
        "decision": "choice",
        "summary": "choice",
        "reason": "rationale",
        "reasoning": "rationale",
        "keywords": "tags",
    },
    # consolidate / curate / prune — keep minimal
    "consolidate": {
        "min_cluster_size": "min_cluster",
        "cluster_min": "min_cluster",
    },
    "prune_by_age": {
        "days": "older_than_days",
        "age_days": "older_than_days",
    },
    "prune_by_priority": {
        "max_prio": "max_priority",
        "priority_max": "max_priority",
    },
    # config_set — common typo: `value=` is canonical; some callers reach
    # for `val=` from shorter conventions
    "config_set": {
        "val": "value",
        "name": "key",
    },
    "config_get": {
        "name": "key",
    },
    "config_delete": {
        "name": "key",
    },
}


def accept_aliases(func: Callable) -> Callable:
    """Translate deprecated kwarg aliases to canonical names with a warning.

    Wraps ``func`` such that any kwarg listed in ``ALIASES[func.__name__]``
    is renamed to the canonical kwarg before the underlying call. Emits a
    ``DeprecationWarning`` per translated kwarg so the wrong mental model
    surfaces at the call site (silent translation lets the wrong name
    persist forever; hard-failing wastes a turn — warn is the goldilocks).

    Raises:
        TypeError: If both the wrong-name and right-name kwarg are passed.

    Functions without an entry in ``ALIASES`` are pass-through.
    """
    name = func.__name__
    aliases = ALIASES.get(name, {})

    if not aliases:
        # Fast path: no aliases registered for this function. Don't bother
        # wrapping — the decorator is meant to be cheap enough to apply
        # broadly, but we can still skip the kwargs walk entirely.
        return func

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Iterate over a copy of keys since we mutate kwargs in the loop
        for wrong in list(kwargs.keys()):
            if wrong not in aliases:
                continue
            right = aliases[wrong]
            if right in kwargs:
                raise TypeError(
                    f"{name}() got both {wrong!r} and {right!r} — "
                    f"use {right!r} (the canonical name)."
                )
            warnings.warn(
                f"{name}(): {wrong!r} is a deprecated alias for {right!r}. "
                f"Translating, but update the call site.",
                DeprecationWarning,
                stacklevel=2,
            )
            kwargs[right] = kwargs.pop(wrong)
        return func(*args, **kwargs)

    return wrapper


class MemoryWriteId(str):
    """Memory id returned by ``remember()`` / ``supersede()``.

    Subclasses ``str`` so existing callers that treat the return value as a
    bare string keep working (equality, concatenation, ``len()``, ``json.dumps``,
    use as a SQL parameter, …). Adds a single ``.id`` property so the natural
    ``m.id`` access pattern — habitually reached for after writes that *return*
    objects — does not raise ``AttributeError`` on a write that returns the
    id directly.

    Example:
        >>> m = MemoryWriteId("550e8400-e29b-41d4-a716-446655440000")
        >>> m == "550e8400-e29b-41d4-a716-446655440000"
        True
        >>> m.id
        '550e8400-e29b-41d4-a716-446655440000'
        >>> isinstance(m, str)
        True

    Issue #15.
    """

    __slots__ = ()

    @property
    def id(self) -> str:
        return str(self)

    def __repr__(self) -> str:
        return f"MemoryWriteId({str(self)!r})"
