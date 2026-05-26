"""Build a Muninn snapshot for use in another Claude.ai project.

Usage from Python:
    from snapshot.build import build_snapshot
    result = build_snapshot(out_dir="/home/claude/snapshot-out")

Usage from CLI:
    python3 -m snapshot.build --out /home/claude/snapshot-out

Result dict shape:
    {
        "out_dir": str,
        "instruction_path": str,
        "kb_dir": str,
        "manifest_path": str,
        "zip_path": str,
        "stats": {...},
    }
"""

from __future__ import annotations
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .config import MEMORY_TYPES_KEEP, MEMORY_MIN_PRIORITY
from .pull import pull_profile, pull_ops, pull_ops_topics, pull_memories
from .filter import (
    filter_memories_by_tag,
    redact_and_filter_memories,
)
from .cluster import cluster_by_primary_tag, cluster_stats
from .compose_instruction import compose_instruction
from .kb import write_kb, write_index


def build_snapshot(out_dir: str | Path = "/home/claude/snapshot-out") -> dict:
    """End-to-end snapshot build. Returns paths + stats dict."""
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    kb_dir = out_dir / "knowledge_base"
    kb_dir.mkdir()

    # ── 1. Pull from DB ────────────────────────────────────────────────────
    profile_rows = pull_profile()
    ops_rows = pull_ops()
    ops_topics = pull_ops_topics()
    raw_memories = pull_memories(
        types=MEMORY_TYPES_KEEP,
        min_priority=MEMORY_MIN_PRIORITY,
    )

    pull_stats = {
        "profile_rows": len(profile_rows),
        "ops_rows": len(ops_rows),
        "raw_memories": len(raw_memories),
    }

    # ── 2. Filter + redact memories ─────────────────────────────────────────
    tag_kept, tag_dropped = filter_memories_by_tag(raw_memories)
    body_kept, body_drop_stats = redact_and_filter_memories(tag_kept)

    filter_stats = {
        "dropped_by_tag": tag_dropped,
        **body_drop_stats,
        "memories_kept": len(body_kept),
    }

    # ── 3. Cluster by primary tag ───────────────────────────────────────────
    buckets = cluster_by_primary_tag(body_kept)
    cluster_summary = cluster_stats(buckets)

    # ── 4. Write KB cluster files + index ───────────────────────────────────
    written = write_kb(buckets, kb_dir)
    index_path = write_index(written, kb_dir)

    # ── 5. Compose project instruction ──────────────────────────────────────
    instruction_text, included_keys = compose_instruction(
        profile_rows,
        ops_rows,
        ops_topics,
        cluster_count=cluster_summary["cluster_count"],
        memory_count=cluster_summary["memory_count"],
    )
    instruction_path = out_dir / "PROJECT_INSTRUCTION.md"
    instruction_path.write_text(instruction_text, encoding="utf-8")

    # ── 6. Manifest ─────────────────────────────────────────────────────────
    manifest = {
        "built_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "oaustegard/muninn-utilities",
        "instruction_hash": hashlib.sha256(
            instruction_text.encode("utf-8")
        ).hexdigest()[:12],
        "stats": {
            **pull_stats,
            **filter_stats,
            **cluster_summary,
            "instruction_chars": len(instruction_text),
            "instruction_lines": instruction_text.count("\n") + 1,
        },
        "included_keys": included_keys,
        "kb_clusters": written,
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=False), encoding="utf-8"
    )

    # ── 7. Zip everything (ready to upload) ────────────────────────────────
    # Write the archive OUTSIDE out_dir so make_archive's walk doesn't
    # pick up a stale copy of the zip from a prior run. Also delete any
    # pre-existing zip — make_archive silently fails to overwrite when
    # the target was created by a different user (e.g. an earlier
    # session's root-owned artifact).
    zip_base = out_dir.parent / out_dir.name  # e.g. /home/claude/snapshot-out
    stale_zip = zip_base.with_suffix(".zip")
    if stale_zip.exists():
        try:
            stale_zip.unlink()
        except (OSError, PermissionError) as e:
            print(f"WARNING: could not remove stale zip {stale_zip}: {e}")
    zip_path = shutil.make_archive(
        str(zip_base),
        "zip",
        root_dir=out_dir,
    )

    return {
        "out_dir": str(out_dir),
        "instruction_path": str(instruction_path),
        "kb_dir": str(kb_dir),
        "manifest_path": str(manifest_path),
        "zip_path": zip_path,
        "stats": manifest["stats"],
    }


# ─── CLI ────────────────────────────────────────────────────────────────────

def _cli():
    p = argparse.ArgumentParser(
        description="Build a Muninn snapshot for another Claude.ai project."
    )
    p.add_argument(
        "--out",
        default="/home/claude/snapshot-out",
        help="Output directory (default: /home/claude/snapshot-out)",
    )
    args = p.parse_args()
    result = build_snapshot(args.out)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    _cli()
