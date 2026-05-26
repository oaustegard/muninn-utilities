"""Write knowledge-base cluster files.

One .md per cluster, frontmatter with tag + count + date range, memories
inside ordered newest-first.
"""

from __future__ import annotations
import re
from pathlib import Path


_SAFE_NAME = re.compile(r"[^a-z0-9._-]+")


def _safe_filename(tag: str) -> str:
    """Filesystem-safe name from a tag. Keep readable; lowercase; strip junk."""
    name = tag.lower().strip()
    name = _SAFE_NAME.sub("-", name)
    name = name.strip("-")
    return name or "untitled"


def _short_id(memory_id: str) -> str:
    return (memory_id or "")[:8]


def _format_memory(m: dict) -> str:
    """Render one memory as a heading block."""
    date = (m.get("created_at") or "")[:10]  # YYYY-MM-DD
    body = m.get("body_redacted") or m.get("summary", "")
    mid = _short_id(m["id"])
    mtype = m.get("type", "")
    other_tags = [t for t in m.get("tags", []) if t != m.get("primary_tag")]
    other_tags_str = ", ".join(other_tags[:8])

    header = f"## {date} — {mtype} ({mid})"
    meta = f"_tags: {other_tags_str}_" if other_tags_str else ""

    parts = [header]
    if meta:
        parts.append(meta)
    parts.append("")
    parts.append(body.strip())
    return "\n".join(parts)


def _format_cluster(tag: str, memories: list[dict]) -> str:
    """One full cluster file."""
    dates = sorted([m.get("created_at", "")[:10] for m in memories if m.get("created_at")])
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "unknown"

    out = [
        "---",
        f"tag: {tag}",
        f"memory_count: {len(memories)}",
        f"date_range: {date_range}",
        "---",
        "",
        f"# {tag}",
        "",
        f"_{len(memories)} memories from Muninn's past, primary tag `{tag}`._",
        "",
    ]
    for m in memories:
        out.append(_format_memory(m))
        out.append("")
        out.append("---")
        out.append("")
    return "\n".join(out)


def write_kb(buckets: dict[str, list[dict]], out_dir: Path) -> list[dict]:
    """Write each cluster to `out_dir/{safe-tag}.md`.

    Returns a list of {filename, tag, memory_count} dicts for the manifest.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    seen_names: set[str] = set()

    # Sort by cluster size descending so the manifest reads largest-first
    for tag in sorted(buckets, key=lambda t: (-len(buckets[t]), t)):
        memories = buckets[tag]
        safe = _safe_filename(tag)
        name = f"{safe}.md"
        # Disambiguate filename collisions if two different tags safe-name
        # to the same thing
        counter = 2
        while name in seen_names:
            name = f"{safe}-{counter}.md"
            counter += 1
        seen_names.add(name)

        path = out_dir / name
        path.write_text(_format_cluster(tag, memories), encoding="utf-8")
        written.append({
            "filename": name,
            "tag": tag,
            "memory_count": len(memories),
        })
    return written


def write_index(written: list[dict], out_dir: Path) -> Path:
    """Write a small INDEX.md so the user can scan what's in the KB."""
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Knowledge base index",
        "",
        f"_{len(written)} clusters, "
        f"{sum(w['memory_count'] for w in written)} memories total._",
        "",
        "| Tag | Memories | File |",
        "|---|---:|---|",
    ]
    for w in written:
        lines.append(f"| `{w['tag']}` | {w['memory_count']} | `{w['filename']}` |")
    path = out_dir / "INDEX.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
