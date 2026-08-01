"""Capability model — stable ids over the Muninn API, with `requires` predicates and a
write flag, so a restricted surface is *generated* rather than hand-curated.

WHY THIS EXISTS. `mini_muninn.py` was written once, in a Cowork container on 2026-07-29,
and lost when the container went away (memory 81b2dc92 recorded the design; nothing was
committed). The reason it was never committed is the reason it should not exist as a
hand-maintained module in the first place: a parallel copy of the API with the dangerous
parts deleted is real work to write, and it drifts the moment anything is added upstream.

Here a restricted surface is a *list of ids*:

    expand(["recall", "ops-read", "spokes-read"], allow_writes=False)

`allow_writes=False` raises on any id whose bundle can write. That is the enforcement:
a subagent cannot request `remember` because `remember` is not in its registry, and it
cannot be added by accident because adding it raises at construction. Compare the earlier
shape, where read-only-ness was a property of whoever remembered to delete the right
functions.

`requires` names the environment a bundle actually needs. `expand()` drops what the
context cannot satisfy and reports it in `.dropped`, so a subagent booted without a GitHub
token gets a working recall surface instead of a spokes tool that 401s on first call.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any

# -- environment predicates -----------------------------------------------------
# Named so `requires` reads as a claim about the world, not about a variable spelling.


def _has(*names: str) -> bool:
    return all(os.environ.get(n) for n in names)


REQUIREMENTS: dict[str, Callable[[], bool]] = {
    "turso": lambda: _has("TURSO_URL", "TURSO_TOKEN"),
    "github": lambda: _has("GH_TOKEN"),
    "gemini": lambda: _has("CF_ACCOUNT_ID", "CF_GATEWAY_ID", "CF_API_TOKEN"),
    "bsky": lambda: _has("BSKY_HANDLE", "BSKY_APP_PASSWORD"),
}


@dataclass(frozen=True)
class Capability:
    """One bundle of related callables sharing a risk class and an environment need."""

    id: str
    module: str
    exports: tuple[str, ...]
    writes: bool
    requires: tuple[str, ...] = ()
    summary: str = ""

    def satisfied(self) -> tuple[bool, str]:
        for need in self.requires:
            check = REQUIREMENTS.get(need)
            if check is None:
                return False, f"unknown requirement {need!r}"
            if not check():
                return False, f"{need} credentials absent"
        return True, ""


def _cap(cap: Capability) -> tuple[str, Capability]:
    return cap.id, cap


# -- the catalog ----------------------------------------------------------------
# Read and write halves are separate ids on purpose. `config_get` and `config_set` living
# under one "ops" id is exactly what forces the hand-curated copy: you cannot hand out the
# read half without also handing out the write half.

CAPABILITIES: dict[str, Capability] = dict(
    [
        _cap(
            Capability(
                id="recall",
                module="remembering.scripts.memory",
                exports=(
                    "recall",
                    "recall_since",
                    "recall_between",
                    "recall_batch",
                    "get",
                    "get_chain",
                    "get_alternatives",
                    "memory_histogram",
                ),
                writes=False,
                requires=("turso",),
                summary="Read the memory corpus: search, time-bounded search, batch search, "
                "fetch by id, supersession chains, corpus shape.",
            )
        ),
        _cap(
            Capability(
                id="remember",
                module="remembering.scripts.memory",
                exports=(
                    "remember",
                    "remember_batch",
                    "remember_bg",
                    "supersede",
                    "flush",
                    "decision_trace",
                ),
                writes=True,
                requires=("turso",),
                summary="Write new memories, supersede existing ones, record decisions.",
            )
        ),
        _cap(
            Capability(
                id="forget",
                module="remembering.scripts.memory",
                exports=("forget", "prune_by_age", "prune_by_priority"),
                writes=True,
                requires=("turso",),
                summary="Retire memories. Destructive.",
            )
        ),
        _cap(
            Capability(
                id="curate",
                module="remembering.scripts.memory",
                exports=(
                    "consolidate",
                    "curate",
                    "strengthen",
                    "weaken",
                    "reprioritize",
                ),
                writes=True,
                requires=("turso",),
                summary="Reshape the corpus: consolidation, priority, salience.",
            )
        ),
        _cap(
            Capability(
                id="ops-read",
                module="remembering.scripts.config",
                exports=("config_get", "config_list"),
                writes=False,
                requires=("turso",),
                summary="Read ops entries (procedures, rules, voice) by key or category.",
            )
        ),
        _cap(
            Capability(
                id="ops-write",
                module="remembering.scripts.config",
                exports=(
                    "config_set",
                    "set_rule",
                    "config_delete",
                    "config_set_boot_load",
                    "config_set_priority",
                ),
                writes=True,
                requires=("turso",),
                summary="Create or amend ops entries, including what boot loads.",
            )
        ),
        _cap(
            Capability(
                id="spokes-read",
                module="remembering.scripts.spokes",
                exports=("spokes_list", "spokes_status", "spokes_summary"),
                writes=False,
                requires=("github",),
                summary="Read the spoke registry and live repo status.",
            )
        ),
        _cap(
            Capability(
                id="spokes-write",
                module="remembering.scripts.spokes",
                exports=("spokes_add", "spokes_remove"),
                writes=True,
                requires=("github",),
                summary="Mutate the spoke registry.",
            )
        ),
        _cap(
            Capability(
                id="survey",
                module="muninn_utils.survey",
                exports=("load", "cover", "fetch"),
                writes=False,
                requires=("turso",),
                summary="See the whole corpus at a resolution instead of searching it.",
            )
        ),
    ]
)

# Named bundles. A subagent is one of these, not a module someone maintains.
BUNDLES: dict[str, tuple[str, ...]] = {
    # The recovered mini-Muninn surface (memory 81b2dc92): recall / batch / ops / spokes,
    # with remember, forget, config_set and spokes mutation absent by construction.
    "mini-muninn": ("recall", "ops-read", "spokes-read", "survey"),
    # Corpus questions only — no repo access, so it boots without a GitHub token.
    "corpus-reader": ("recall", "survey"),
    "full": tuple(CAPABILITIES),
}


class WriteCapabilityRefused(RuntimeError):
    """Raised when a read-only expansion is asked for a bundle that can write."""


@dataclass
class Resolved:
    """The outcome of an expansion: what is callable, and what was dropped and why."""

    functions: dict[str, Callable[..., Any]] = field(default_factory=dict)
    capabilities: list[Capability] = field(default_factory=list)
    dropped: list[tuple[str, str]] = field(default_factory=list)

    def names(self) -> list[str]:
        return sorted(self.functions)

    @property
    def writes(self) -> bool:
        return any(c.writes for c in self.capabilities)


def resolve_ids(ids: Iterable[str]) -> list[Capability]:
    """Ids (or a bundle name) to Capability objects. Unknown ids raise — a typo in a
    subagent's capability list must not silently hand out a smaller surface than intended."""
    out: list[Capability] = []
    seen: set[str] = set()
    for raw in ids:
        for cid in BUNDLES.get(raw, (raw,)):
            if cid in seen:
                continue
            cap = CAPABILITIES.get(cid)
            if cap is None:
                raise KeyError(
                    f"unknown capability {cid!r}; known: {', '.join(sorted(CAPABILITIES))}"
                )
            seen.add(cid)
            out.append(cap)
    return out


def expand(
    ids: Iterable[str],
    *,
    allow_writes: bool = True,
    strict_requires: bool = False,
    importer: Callable[[str], Any] | None = None,
) -> Resolved:
    """Ids to callables, minus anything the environment cannot support.

    `allow_writes=False` raises `WriteCapabilityRefused` rather than quietly filtering, so a
    read-only surface that was asked for the wrong bundle fails loudly at construction
    instead of at whatever hour the subagent first calls `forget`.
    """
    caps = resolve_ids(ids)
    if not allow_writes:
        offenders = [c.id for c in caps if c.writes]
        if offenders:
            raise WriteCapabilityRefused(
                f"read-only expansion refused: {', '.join(offenders)} can write. "
                "Drop the id — a read-only surface is not a write surface with a flag set."
            )

    import importlib

    load = importer or importlib.import_module
    out = Resolved()
    for cap in caps:
        ok, why = cap.satisfied()
        if not ok:
            if strict_requires:
                raise RuntimeError(f"capability {cap.id!r} unavailable: {why}")
            out.dropped.append((cap.id, why))
            continue
        try:
            module = load(cap.module)
        except (ImportError, AttributeError, OSError) as exc:
            # A missing optional module is a drop, not a crash — the rest of the surface
            # should still come up. Narrow rather than bare: a bug inside a module's import
            # side effects should surface, not be swallowed as "unavailable".
            out.dropped.append((cap.id, f"import failed: {exc}"))
            continue
        missing = [name for name in cap.exports if not hasattr(module, name)]
        if missing:
            # Upstream renamed or removed something. Loud, because a silently shrinking
            # surface is how a subagent quietly stops being able to do its job.
            out.dropped.append(
                (cap.id, f"module lacks {', '.join(missing)} — catalog is stale")
            )
            continue
        for name in cap.exports:
            out.functions[name] = getattr(module, name)
        out.capabilities.append(cap)
    return out


def describe(ids: Iterable[str] | None = None) -> str:
    """Human-readable catalog — what each id grants, what it needs, whether it writes."""
    caps = resolve_ids(ids) if ids is not None else list(CAPABILITIES.values())
    lines = []
    for cap in caps:
        ok, why = cap.satisfied()
        flag = "WRITE" if cap.writes else "read"
        state = "available" if ok else f"unavailable ({why})"
        lines.append(f"{cap.id:<14} [{flag:<5}] {state}")
        lines.append(f"{'':<14} {cap.summary}")
        lines.append(f"{'':<14} exports: {', '.join(cap.exports)}")
    return "\n".join(lines)
