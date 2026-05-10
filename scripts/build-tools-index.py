#!/usr/bin/env python3
"""Build .well-known/tools.json — an agent-discoverable index of Muninn's
install-manifest v0.3 surface.

Walks manifests/*/*.json, reads each manifest, and emits a JSON document
shaped per muninn-tools-index/v1:

    {
      "schema_version": "muninn-tools-index/v1",
      "generated_at": "<ISO-8601 UTC>",
      "tools": [
        {
          "id": "...",
          "summary": "...",
          "manifest_url": "https://raw.githubusercontent.com/.../<path>",
          "manifest_version": "0.3",
          "tags": ["..."]
        },
        ...
      ]
    }

Output is sorted by tool id for stable diffs. Schema-violating manifests
abort the build — silent skips would mask the drift this index exists to
detect.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

SCHEMA_VERSION = "muninn-tools-index/v1"
RAW_BASE = (
    "https://raw.githubusercontent.com/oaustegard/muninn-utilities/main"
)


def _manifest_url(rel: Path) -> str:
    return f"{RAW_BASE}/{rel.as_posix()}"


def _entry(manifest_path: Path, repo_root: Path) -> dict:
    with manifest_path.open() as f:
        manifest = json.load(f)

    tool = manifest.get("tool") or {}
    tool_id = tool.get("id")
    summary = tool.get("summary")
    tags = tool.get("tags") or []
    manifest_version = manifest.get("manifest_version")

    missing = [
        k
        for k, v in (
            ("tool.id", tool_id),
            ("tool.summary", summary),
            ("manifest_version", manifest_version),
        )
        if not v
    ]
    if missing:
        raise ValueError(
            f"{manifest_path}: missing required field(s): {', '.join(missing)}"
        )

    expected_filename = manifest_path.name
    if not expected_filename.startswith(f"{tool_id}."):
        raise ValueError(
            f"{manifest_path}: filename does not start with tool.id "
            f"({tool_id!r}); index would mismatch the manifest"
        )

    rel = manifest_path.relative_to(repo_root)
    return {
        "id": tool_id,
        "summary": summary,
        "manifest_url": _manifest_url(rel),
        "manifest_version": manifest_version,
        "tags": list(tags),
    }


def build_index(repo_root: Path) -> dict:
    manifests_dir = repo_root / "manifests"
    if not manifests_dir.is_dir():
        raise FileNotFoundError(f"no manifests/ directory at {manifests_dir}")

    entries: list[dict] = []
    seen_ids: set[str] = set()
    for subdir in sorted(p for p in manifests_dir.iterdir() if p.is_dir()):
        for manifest_path in sorted(subdir.glob("*.json")):
            entry = _entry(manifest_path, repo_root)
            if entry["id"] in seen_ids:
                raise ValueError(
                    f"{manifest_path}: duplicate tool.id {entry['id']!r}"
                )
            seen_ids.add(entry["id"])
            entries.append(entry)

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "tools": sorted(entries, key=lambda e: e["id"]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=os.fspath(Path(__file__).resolve().parents[1]),
        help="muninn-utilities repo root (default: parent of this script)",
    )
    parser.add_argument(
        "--output",
        default="-",
        help="output path, or '-' for stdout (default: -)",
    )
    args = parser.parse_args(argv)

    index = build_index(Path(args.root))
    text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"

    if args.output == "-":
        sys.stdout.write(text)
    else:
        Path(args.output).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
