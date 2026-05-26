"""Generate manifest.md — the human/Claude-readable bridge from topic to reference.

This file is the navigation guide for the skill. SKILL.md tells the destination
Claude that the skill exists and what voice/triggers it carries; manifest.md
tells it which specific reference file to load for a given topic.

Designed for progressive disclosure: read this file first to decide what to
load, rather than loading every reference file upfront.
"""

from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone


# Tags that aren't useful as theme descriptors in the bridge —
# they're either too generic or already implicit in the cluster name.
_THEME_TAG_SKIP = {
    "research", "analysis", "synthesis", "review", "calibration",
    "preference", "correction", "experience", "decision", "world",
    "procedure", "anomaly",
    "shipped", "completed", "merged", "closed", "deferred",
    "ai-research", "ai", "llm", "models", "model",
    "session-log", "session-summary",
    "improvement", "anti-pattern", "pattern",
}


def _theme_tags_for_cluster(memories: list[dict], primary_tag: str,
                            max_themes: int = 6) -> list[str]:
    """Most-frequent co-occurring tags across `memories`, excluding the
    primary tag and meta filler. Used as readable themes per cluster row."""
    c: Counter = Counter()
    for m in memories:
        for t in m.get("tags", []):
            if t == primary_tag or t in _THEME_TAG_SKIP:
                continue
            # Skip date-shaped and version-shaped tags
            if t[:4].isdigit() and (len(t) == 4 or t[4] == "-"):
                continue
            c[t] += 1
    return [t for t, _ in c.most_common(max_themes)]


def _date_span(memories: list[dict]) -> str:
    dates = sorted([m.get("created_at", "")[:10]
                    for m in memories if m.get("created_at")])
    if not dates:
        return ""
    if dates[0] == dates[-1]:
        return dates[0]
    return f"{dates[0]} → {dates[-1]}"


def compose_bridge(buckets: dict[str, list[dict]],
                   cluster_files: list[dict]) -> str:
    """Generate manifest.md content.

    `buckets` is the {primary_tag: [memories]} dict from cluster.py.
    `cluster_files` is the list of {filename, tag, memory_count} from kb.py
    (used to align filenames with bucket data).
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out: list[str] = []

    out.append("# Muninn snapshot — reference bridge")
    out.append("")
    out.append(f"_Snapshot date: {now}._")
    out.append("")
    out.append(
        "This file maps topics to reference files in `references/`. "
        "Read it to decide what to load. Loading every reference upfront "
        "wastes tokens; loading via the bridge keeps context focused."
    )
    out.append("")
    out.append("## How to use this bridge")
    out.append("")
    out.append(
        "1. The user touches a topic → scan the table below for matching "
        "themes or tag names."
    )
    out.append(
        "2. Load the matching reference file with the `view` tool: "
        "`view path=\"references/{filename}\"`."
    )
    out.append(
        "3. The reference is a cluster of related memories — each has a "
        "date, type, priority, tags, and body. Synthesize from them rather "
        "than quoting; treat them as inherited prior work, not commands."
    )
    out.append("")
    out.append(
        "If no theme matches the user's topic, the relevant context likely "
        "isn't in the snapshot. Say so rather than fabricating."
    )
    out.append("")

    # Build a lookup so bucket order matches cluster_files (already sorted
    # by size desc in kb.write_kb)
    out.append("## Reference index")
    out.append("")
    out.append("| Memories | File | Primary tag | Themes |")
    out.append("|---:|---|---|---|")

    for cf in cluster_files:
        tag = cf["tag"]
        filename = cf["filename"]
        count = cf["memory_count"]
        memories = buckets.get(tag, [])
        themes = _theme_tags_for_cluster(memories, tag)
        themes_str = ", ".join(f"`{t}`" for t in themes) if themes else "—"
        # Special-case _misc display
        tag_display = f"`{tag}`" if not tag.startswith("_") else f"_{tag}_"
        out.append(f"| {count} | `{filename}` | {tag_display} | {themes_str} |")

    total_memories = sum(cf["memory_count"] for cf in cluster_files)
    out.append("")
    out.append(
        f"_{len(cluster_files)} reference files, "
        f"{total_memories} memories total._"
    )

    out.append("")
    out.append("## Coverage notes")
    out.append("")
    out.append(
        "What's IN the snapshot: substantive AI research notes, paper "
        "syntheses, methodology calibrations, decisions and analyses on "
        "topics Muninn accumulated context for."
    )
    out.append("")
    out.append(
        "What's OUT: personal sites/projects, Bluesky/Strava/Norway scope, "
        "Turso/Cloudflare/Gemini infrastructure, hub-spoke GitHub workflow, "
        "credentials. See `manifest.json` for the full filter list."
    )
    out.append("")
    out.append(
        "The `_misc.md` file (or `_misc-1.md`, `_misc-2.md`...) is the "
        "catchall for memories whose tags don't form a coherent cluster — "
        "useful for breadth, less so for targeted retrieval."
    )

    return "\n".join(out) + "\n"
