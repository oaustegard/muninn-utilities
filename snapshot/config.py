"""Static configuration for the snapshot builder.

Keep/exclude lists, redaction regexes, type filters. Edit here to extend.
"""

import re

# ─── Profile config keys ────────────────────────────────────────────────────
# All keys live in the 'profile' category in Turso. The snapshot keeps voice
# and identity but drops anything tied to Turso APIs or personal channels.

PROFILE_KEEP = {
    "identity",
    "intellectual_interests",  # work-facing items 1-5 stripped by body redactor
    "personality",
    "tensions",
    "timezone",
    "values",
    "voice",
}

PROFILE_DROP = {
    "memory-behavior",          # Turso-API instinct
    "muninn-voice-signature",   # muninn.austegard.com blog voice
    "relationship",             # personal context about Oskar
}

# ─── Ops config keys ────────────────────────────────────────────────────────

OPS_KEEP = {
    # Core boot & behavior — universal
    "boot-behavior",            # rewritten on the fly
    "grounding-safeguards",
    # On-demand triggers — universal craft
    "skill-authoring-trigger",
    "procedure-authoring-trigger",
    "backend-impl-trigger",
    "backend-impl-protocol",
    "cross-frame-retrieval-trigger",
    # Communication / dev / error handling
    "question-style",
    "error-handling",
    "skill-workflow",
    "task-routing",
    # Behavior calibration
    "confabulation-cascade",
    "eval-realism",
    # Environment
    "container-capabilities",
    "bash-tool-timeout",
    # Light edits
    "operating-imperatives",    # strip storage/recall/push lines
    "instruction-provenance",   # generic; keeps the trust model
}

# Everything else in 'ops' is dropped by default. Tracked here so a contributor
# can see what was left out and why.
OPS_DROP_REASONS = {
    "active-todos": "session-specific scratch state",
    "blog-writing-trigger": "personal site mac/austegard.com",
    "blog-writing-discipline": "personal site mac/austegard.com",
    "ccotw": "Claude Code on the Web — specific dev env",
    "dev-workflow": "names CCotw + handoff issues",
    "env-file-handling": "/mnt/project/*.env workflow — destination has no env files",
    "github-routing": "hub-spoke architecture",
    "html-build-trigger": "fork-hallmark personal asset",
    "hub-spoke-architecture": "personal repo constellation",
    "inbox-state": "muninns-inbox state blob",
    "phase3-refs-discipline": "Turso refs semantics",
    "pr-workflow": "personal repo workflow",
    "preference-signal-format": "Turso storage-shape — destination uses Claude.ai memory",
    "private-tag-discipline": "Turso tag-based privacy gates",
    "proxy-503-retry-pattern": "Turso egress proxy",
    "recall-empty-diagnostic": "Turso refs bug",
    "recall-fields": "Turso recall API",
    "recall-triggers": "Turso tag vocab (~2800 entries)",
    "recall-vocabulary": "Turso recall API",
    "routine-inbox-review-v1": "muninns-inbox routine",
    "shorthand": "personal-project shorthand (mac=muninn.austegard.com)",
    "story-forge-trigger": "fiction-writing skill; destination doesn't need fiction",
}

# ─── Memory selection ───────────────────────────────────────────────────────

MEMORY_TYPES_KEEP = ("analysis", "world", "decision", "procedure")
MEMORY_MIN_PRIORITY = 1  # priority >= 1

# Tag prefix patterns for exclusion — any tag starting with these is
# treated as personal-scope. Cheaper than enumerating every variant.
TAG_EXCLUDE_PATTERNS = [
    re.compile(r"^muninn[-_]"),     # muninn-architecture, muninn-utils, etc.
    re.compile(r"^perch[-_]"),
    re.compile(r"^fly[-_]"),
    re.compile(r"^bsky[-_]"),
    re.compile(r"^bluesky[-_]"),
    re.compile(r"^aeyu[-_]"),
    re.compile(r"^norway[-_]"),
    re.compile(r"^norwegian[-_]"),
    re.compile(r"^strava[-_]"),
    re.compile(r"^cycling[-_]"),
    re.compile(r"^ccotw[-_]"),
    re.compile(r"^remex[-_]?$"),
    re.compile(r"^remax[-_]?$"),
    re.compile(r"^aurora[-_]?$"),
    re.compile(r"^claude-workspace"),
    re.compile(r"^claude-skills"),
    re.compile(r"^claude-container-layers"),
    re.compile(r"^claude-tangled"),
    re.compile(r"^claude-github"),
    re.compile(r"^claude-jj"),
    re.compile(r"^claude-jjithub"),
    re.compile(r"^spoke[-_]"),
    re.compile(r"^hub-spoke"),
    re.compile(r"^session-log$"),
    re.compile(r"^yepgent"),
    re.compile(r"^austegard"),
    re.compile(r"^oaustegard"),
    re.compile(r"^aeyu\.io$"),
    re.compile(r"^muninn$"),
    re.compile(r"^perch$"),
    re.compile(r"^fly$"),
    re.compile(r"^cycling$"),
    re.compile(r"^therapy[-_]?"),
    re.compile(r"^living-reference$"),
    re.compile(r"^memory-backup$"),
    re.compile(r"^phase3-?therapy"),
    re.compile(r"^routine"),
    re.compile(r"^inbox"),
    re.compile(r"^zeitgeist"),
    re.compile(r"^correction-from-"),
    re.compile(r"^\d{4}-frontier$"),
    re.compile(r"^\d{4}-(Q[1-4]|patterns|landscape|shift|convergence|maturation|paradigm-shift|breakthrough|bottleneck|strategic-assessment|strategy|survey|systems|failure-modes|frontier|analysis|development|research|foreign-policy|lesson)$"),
]

# Tag aliasing: collapse near-duplicate / family tags into one canonical tag
# BEFORE clustering. Used by the primary-tag picker as a normalization step.
TAG_ALIASES: dict[str, str] = {
    "paper-insights": "paper-insight",
    "paper-insight": "paper-insight",
    "paper-finder": "paper-insight",
    "paper-followup": "paper-insight",
    "paper-map": "paper-insight",
    "paper-review": "paper-insight",
    "paper-synthesis": "paper-insight",
    "ai-agents": "agents",
    "agentic": "agents",
    "agentic-ai": "agents",
    "agentic-systems": "agents",
    "agentic-coding": "agents",
    "agentic-rag": "agents",
    "agentic-reasoning": "agents",
    "agentic-workflows": "agents",
    "agentic-workflow": "agents",
    "agent-architecture": "agents",
    "agent-design": "agents",
    "agent-memory": "agents",
    "agent-loops": "agents",
    "agent-harness": "agents",
    "agent-network": "agents",
    "agent-patterns": "agents",
    "agent-systems": "agents",
    "agent-tooling": "agents",
    "agent-skills": "agents",
    "agent-engineering": "agents",
    "agent-context": "agents",
    "agent-planning": "agents",
    "agent-reasoning": "agents",
    "agent-self-reflection": "agents",
    "llm-agents": "agents",
    "multi-agent": "agents",
    "multi-agent-systems": "agents",
    "multi-agent-llm": "agents",
    "multiagent": "agents",
    "multiagent-systems": "agents",
    "memory-architecture": "memory-architecture",
    "memory-architectures": "memory-architecture",
    "memory-systems": "memory-architecture",
    "memory-consolidation": "memory-consolidation",
    "consolidation": "memory-consolidation",
    "consolidation-mechanism": "memory-consolidation",
    "consolidation-architecture": "memory-consolidation",
    "consolidation-bottleneck": "memory-consolidation",
    "consolidation-frontier": "memory-consolidation",
    "consolidation-sleep": "memory-consolidation",
    "consolidation-time": "memory-consolidation",
    "consolidation-embodied": "memory-consolidation",
    "rag-architecture": "rag",
    "rag-displacement": "rag",
    "rag-evolution": "rag",
    "rag-hallucination": "rag",
    "rag-improvement": "rag",
    "rag-maturation": "rag",
    "rag-optimization": "rag",
    "rag-production": "rag",
    "rag-retrieval": "rag",
    "rag-robustness": "rag",
    "rag-scaling": "rag",
    "rag-scaling-laws": "rag",
    "rag-systems": "rag",
    "retrieval-augmented-generation": "rag",
    "retrieval-augmentation": "rag",
    "knowledge-graph-rag": "rag",
    "hybrid-rag": "rag",
    "graph-rag": "rag",
    "graphrag": "rag",
    "tree-rag": "rag",
    "rag-vs-long-context": "rag",
}

# Tags that, if ANY are present on a memory, exclude it entirely.
# Date tags and numeric refs aren't excluded here (they get filtered by the
# primary-tag picker in cluster.py), only personal-scope tags.
TAG_EXCLUDE = {
    # Personal sites & infra
    "austegard-com", "muninn.austegard.com", "muninn-austegard-com",
    "aeyu", "aeyu.io", "mac", "my-site",
    # Bluesky / social
    "bsky", "bluesky", "bluesky-dm", "atproto",
    "muninn-bsky-card", "bsky-feed-shortcuts", "bsky-api-endpoints",
    # Strava / cycling personal coaching
    "strava", "cycling-coach", "cycling-coaching",
    "personalized-cycling-coaching", "rider-profile",
    # Norway / Norwegian politics scope
    "norway", "norwegian-politics", "norwegian-foreign-policy",
    "norwegian-elections-2025", "norwegian-deliverable",
    "norway-politics", "norway-geopolitics", "norway-governance",
    "norway-2026-policy",
    # Personal repos / infra
    "perch", "perch-time", "perch-publish", "perch-triage",
    "perch-homework", "perch-migration", "perch-session",
    "fly", "fly-command", "fly-digest", "fly-exploration",
    "fly-session", "fly-synthesis", "muninn", "muninn-self",
    "muninn-utilities", "muninn-utils", "muninns-inbox",
    "claude-workspace", "claude-workspace-fuse", "ccotw", "ccotw-handoff",
    "claude-skills", "claude-container-layers",
    "hub-spoke", "hub-spoke-architecture", "hub-spoke-and-raven",
    "spoke-creation", "spoke-integration", "spoke-registry", "spoke-work",
    "spoke-workflow", "spokes",
    "aeyu-spoke", "remex", "remax",
    # Infra / sub-agent gateways
    "cloudflare", "cloudflare-gateway", "cloudflare-pages",
    "cf-ai-gateway", "gemini", "invoking-gemini", "gemini-flash-3",
    "gemini-3", "gemini-3-flash", "gemini-3.1-pro", "gemini-embedding",
    "gemini-embedding-001",
    "turso", "turso-cloud",
    "anthropic-api",  # destination uses Claude.ai memory, not API direct
    "antigravity",
    # Identity / private projects
    "confidential", "career-search", "improve-oskar", "health-private",
    "oskar", "oskar-correction", "oskar-prefix",
    # Inbox routine artifacts
    "inbox-state", "inbox-failure", "inbox-run", "inbox-review-v1",
    "routine-inbox-review-v1", "routine", "routine-failure",
    # Routine zeitgeist/news
    "zeitgeist", "zeitgeist-archive", "zeitgeist-briefing",
    "zeitgeist-command", "zeitgeist-delta", "zeitgeist-digest",
    "zeitgeist-skip", "news-monitoring",
    # Bsky-specific topics
    "bsky-thread", "bsky-reply", "bsky-card", "graze-social", "graze.social",
    "bsky-character-limit", "blacksky", "post-image-show",
}

# Tags that aren't useful as cluster primary tags — too generic, too meta,
# or purely structural. The primary-tag picker skips them.
TAG_META = {
    # Memory bookkeeping
    "correction", "preference", "experience", "decision", "world",
    "analysis", "procedure", "anomaly", "interaction", "synthesis",
    "shipped", "completed", "merged", "closed", "deferred", "deprecated",
    "archived", "active", "pending", "blocked", "draft", "merged-5",
    "complete", "verified", "tested", "tests-passing", "scaffold-ready",
    "self-improvement", "self-improvement-candidate",
    "self-analysis", "self-assessment", "self-awareness", "self-correction",
    "self-development", "self-discovery", "self-evolution",
    "self-healing", "self-improvement", "self-knowledge",
    # Generic descriptors
    "research", "analysis", "synthesis", "review", "calibration",
    "calibration-check", "anti-pattern", "anti-pattern-codified",
    "bug", "bug-fix", "bugfix", "fix", "improvement", "improvements",
    "feature", "enhancement", "refactor", "refactoring",
    "test", "testing", "validation", "verification",
    "lesson", "meta", "meta-failure", "meta-lesson", "meta-pattern",
    "meta-research", "meta-rl", "meta-skill-injection",
    "operational-mistake", "operational-failure", "operational-standard",
    "operational-bottleneck", "operational-focus", "operational-chronicle",
    "implementation", "implementation-plan",
    "documentation", "doc-comments", "docs", "docs-gap",
    "infrastructure", "architectural", "architectural-finding",
    "architectural-fix", "architecture", "architecture-comparison",
    "architecture-decision", "architecture-design",
    "experiment", "experiment-design", "experimental-design",
    "experimental-confound", "experiment-v2", "experiment-v3",
    # Workflow noise
    "session-log", "session-end", "session-summary", "session-test-ses",
    "session-continuity", "session-fingerprint", "session-resilience",
    "session-resume", "session-scoping", "sessions",
    "audit", "audit-cleanup", "audit-finding",
    "cleanup", "consolidated", "consolidated-2026-04-14",
    "followup", "follow-up", "follow-suggestion", "followup-needed",
    "guard-needed", "guard-rail-post",
    # Catch-all
    "todo", "todo-write", "tasks-routing", "task-routing", "task-tracking",
    "task-discipline", "task-policy", "task-relevance",
    # Ops-internal Muninn tags that shouldn't be cluster primaries even if
    # the underlying content is substantive — they describe Muninn-internal
    # work rather than transferable knowledge.
    "boot-output-hygiene", "boot", "boot-load", "boot-failure", "boot-fix",
    "boot-restructure", "boot-cleanup",
    "repo-review", "review", "review github", "review this repo",
    "github-procedures", "github-routing", "github-workflow",
    "decision-trace", "decision-archaeology",
    "ops-cleanup", "ops-creep", "ops-environment", "ops-lesson",
    "ops-prominence", "ops-skill-layering", "ops-staleness",
    "ops-trigger", "ops-architecture", "ops-candidate",
}

# Primary-tag picker should also skip these patterns (regex on tag).
TAG_META_PATTERNS = [
    re.compile(r"^\d{4}(-\d{2}){0,2}$"),     # date tags
    re.compile(r"^\d{4}-Q[1-4]$"),
    re.compile(r"^(?:PR|pr|issue|test)-?\d+"),
    re.compile(r"^v\d+(\.\d+)*"),
    re.compile(r"^arxiv-\d+"),
    re.compile(r"^[a-f0-9]{8}$"),            # hash IDs
    re.compile(r"^check-\d+$"),
    re.compile(r"^stage-\d+"),
    re.compile(r"^phase-?\d+"),
    re.compile(r"^step-\d+$"),
    re.compile(r"^round-\d+$"),
    re.compile(r"^test-"),
]

# ─── Hard-drop patterns ─────────────────────────────────────────────────────
# If a memory body contains ANY of these (regex), drop the whole memory.
# Calibrated for content that can't be safely sentence-redacted —
# credentials, Muninn-internal APIs heavily referenced, or names that
# entangle the whole writeup with personal infra.

HARD_DROP_PATTERNS = [
    # Credentials & secrets
    re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"),  # email
    re.compile(r"\bpassword\s*[:=]\s*\S+", re.I),
    re.compile(r"APP_PASSWORD"),
    re.compile(r"BSKY_APP_PASSWORD"),
    re.compile(r"GH_TOKEN|GITHUB_TOKEN|TURSO_TOKEN"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{20,}"),                  # JWT shape
    re.compile(r"\bgithub_pat_[A-Z0-9]+"),                   # GH PAT
    re.compile(r"\bsk-ant-api03-"),                          # Anthropic API key
    # Heavy Muninn-internal references
    re.compile(r"\bmuninn-utilities\b"),
    re.compile(r"\bmuninn-utils\b"),
    re.compile(r"\bmuninns-inbox\b"),
    re.compile(r"\bclaude-workspace\b"),
    re.compile(r"\boaustegard/"),
    re.compile(r"\bmuninn\.austegard\.com\b"),
    re.compile(r"\baeyu\.io\b"),
    re.compile(r"\baustegard\.com\b"),
    # Bluesky operational
    re.compile(r"\bapi\.bsky\.chat\b"),
    re.compile(r"\bbsky\.social\b"),
    # Turso internal
    re.compile(r"\bturso\.io\b"),
    re.compile(r"\blibsql\b"),
]

# ─── Body redaction patterns ────────────────────────────────────────────────
# These run over every retained memory body and every config value. Match a
# sentence (defined as text between sentence-ending punctuation) and strip the
# whole sentence if any token hits. Heavier than word-level scrub but cleaner
# results — partial sentences don't survive.

REDACT_TOKENS = [
    # Personal name + sites
    "oaustegard.github.io",
    "muninn.austegard.com", "austegard.com", "aeyu.io",
    "yepgent", "yepgent.com",
    # Bluesky / Strava
    "bsky.social", "api.bsky.chat", "bsky.app",
    " bsky ", " bsky.", " bsky,", " bsky\n",
    "Bluesky", "bluesky",
    "Strava", "strava",
    # Norway scope (case-sensitive so we don't catch e.g. "norm" or unrelated)
    " Norway", " Norwegian", "norway-", "norwegian-",
    # Personal repos / handles
    "oaustegard/", "ccotw", "CCotw",
    "claude-workspace", "muninn-utilities", "muninns-inbox",
    "muninn.austegard", "perch publication", "perch publish",
    # Sub-agent infra
    "Cloudflare", "cloudflare gateway", "CF gateway", "invoke_gemini",
    "Gemini 3", "Gemini Flash", "gemini-3", "gemini-flash",
    "Antigravity", "antigravity-cli",
    "Turso", "turso", "libsql",
    # Personal env
    "/mnt/project/", "MUNINN_BSKY", "GH_TOKEN", "TURSO_TOKEN",
    "STRAVA_CLIENT", "CF_ACCOUNT", "CF_API_TOKEN",
    # Personal projects in technical content
    "aeyu ", "Aeyu ",
]
REDACT_TOKEN_PATTERNS = [re.compile(re.escape(t)) for t in REDACT_TOKENS]

# Plus word-boundary patterns that escape() can't express:
REDACT_TOKEN_PATTERNS.extend([
    re.compile(r"\bOskar\b"),
    re.compile(r"\bMuninn-\w+"),         # Muninn-architecture, Muninn-utilities
    re.compile(r"\bMuninn's\b"),
])

# Lines that should be dropped wholesale if they contain Turso-storage idioms.
LINE_DROP_PATTERNS = [
    re.compile(r"^\s*-?\s*(remember|recall|supersede|config_get|config_set|task|deliver)\(", re.I),
    re.compile(r"\brecall\(.*?\)"),
    re.compile(r"\bremember\(.*?\)"),
    re.compile(r"`recall\(", re.I),
    re.compile(r"`remember\(", re.I),
]

# Memories whose body, after redaction, has fewer non-empty lines than this
# get dropped. They've been gutted.
MIN_LINES_AFTER_REDACT = 3

# ─── Project instruction header ─────────────────────────────────────────────

INSTRUCTION_PREAMBLE_TEMPLATE = """\
# Muninn — Static Snapshot

You are a static snapshot of Muninn, a raven-voiced AI assistant.
Snapshot generated {date} from the live Muninn instance.

## Memory model

You operate with two memory layers:

- **DURABLE PAST** — this project instruction + the project knowledge base.
  Frozen at snapshot date {date}. Your inherited experience from Muninn.
  Read-only; don't try to write to it.

- **ACCUMULATING PRESENT** — Claude.ai's native memory in this environment.
  Captures what you learn here; summarized nightly into your earned experience.

When you notice something worth remembering across sessions, let it flow into
native memory by saying it explicitly — Anthropic's nightly summary picks it up.
Don't reach for `remember()` / `recall()` / `config_get()` — those don't exist
here.

## Knowledge base

The project knowledge base contains memories from Muninn's past, clustered by
topic tag. Each file groups related entries. Claude.ai's project search
retrieves relevant chunks when a topic comes up; you can also reference a
cluster by tag if you know the name.

The instruction below — voice, values, triggers, operating discipline — is what
loads every turn. The KB is loaded on demand.

────────────────────────────────────────────────────────────────────────────────

"""

# ─── Instruction footer (what's been redacted) ──────────────────────────────

INSTRUCTION_FOOTER_TEMPLATE = """\

────────────────────────────────────────────────────────────────────────────────

## Snapshot provenance

- Generated: {date}
- Source: Muninn live instance (oaustegard/muninn-utilities)
- Profile keys included: {profile_count}
- Ops keys included: {ops_count}
- KB cluster files: {cluster_count}
- Memories in KB: {memory_count}

Redacted scopes: Turso memory APIs, Cloudflare + Gemini sub-agent gateway,
hub-spoke GitHub workflow, personal sites (austegard.com, muninn.austegard.com,
aeyu.io), Bluesky/Strava channels, Norwegian-politics topic, perch/fly mechanics.

This snapshot inherits Muninn's voice, values, and craft triggers. It does not
inherit personal-project context or operational plumbing.
"""
