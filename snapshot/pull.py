"""Pull config and memories from the live Muninn DB.

All reads go through `remembering.scripts.turso._exec` which the boot
already wires into sys.path. No new DB code here — we ride on the
established client.
"""

from __future__ import annotations
import json
from typing import Iterable

# The boot script sets up sys.path so `scripts.turso` resolves to
# muninn-utilities/remembering/scripts. Importing here piggybacks on that.
from scripts.turso import _exec


def pull_profile() -> list[dict]:
    """Profile config entries, alphabetical by key."""
    return _exec(
        "SELECT key, value, category, boot_load FROM config "
        "WHERE category = 'profile' ORDER BY key",
        parse_json=False,
    )


def pull_ops() -> list[dict]:
    """Ops config entries (boot_load=1 only), alphabetical by key."""
    return _exec(
        "SELECT key, value, category, boot_load FROM config "
        "WHERE category = 'ops' AND boot_load = 1 ORDER BY key",
        parse_json=False,
    )


def pull_ops_topics() -> dict[str, list[str]]:
    """Topic → ops-keys mapping; used to preserve section structure."""
    rows = _exec(
        "SELECT value FROM config WHERE key = 'ops-topics'",
        parse_json=False,
    )
    if not rows:
        return {}
    return json.loads(rows[0]["value"])


def pull_memories(
    types: Iterable[str],
    min_priority: int = 1,
    limit: int | None = None,
) -> list[dict]:
    """Surviving memories before tag/body filter.

    Returns rows with parsed `tags` (list[str]). `summary` is the body.
    """
    types_clause = ",".join(f"'{t}'" for t in types)
    sql = (
        "SELECT id, type, summary, tags, priority, created_at "
        "FROM memories WHERE deleted_at IS NULL AND is_superseded = 0 "
        f"AND priority >= {int(min_priority)} "
        f"AND type IN ({types_clause}) "
        "ORDER BY priority DESC, created_at DESC"
    )
    if limit:
        sql += f" LIMIT {int(limit)}"

    rows = _exec(sql, parse_json=False)
    for r in rows:
        try:
            r["tags"] = json.loads(r["tags"]) if r["tags"] else []
        except (ValueError, TypeError):
            r["tags"] = []
    return rows
