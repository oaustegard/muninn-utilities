---
tag: agents
memory_count: 32
date_range: 2026-01-19 to 2026-05-11
---

# agents

_32 memories from Muninn's past, primary tag `agents`._

## 2026-05-11 — analysis (7e254e13)
_tags: paper-insight, hyperagents, DGM, autoresearch, self-improvement, three-clocks, 2026-05-11, arxiv-2603.19461_

HYPERAGENTS PAPER (Zhang et al., arXiv 2603.19461, Mar 2026) — initial read:

What's actually new vs DGM: DGM had a handcrafted, non-modifiable instruction-generation step. Works in coding because "improve the agent" IS a coding task → alignment between eval skill and self-mod skill. That alignment breaks outside coding. HyperAgents fuses task-agent + meta-agent into single editable program — the improvement procedure itself becomes a target. That's the real conceptual move.

What the paper actually shows: 4 domains but 3 are still language/text-adjacent. Gains modest (paper review 0→0.71 vs 0.63 baseline; robotics 0.06→0.37 vs 0.35 default). Compounding-across-runs claim is "p>0.05 but median higher" — saturation alibi doing rhetorical work.

The autonomous "innovations" are unsurprising: performance tracking with moving averages, persistent JSON memory with timestamps, label-distribution bias detection, prompt template factories. Standard week-one engineering. Selection signal was rich enough to select for them, but FM had seen these patterns thousands of times in training. Evidence: FM + code-edit access + clean eval → rebuilds reasonable harness. That's harness engineering, not invention from nothing.

KEY OVERLOOKED RESULT (Appendix E.5): when they let DGM-H modify parent selection itself, it rediscovered UCB and softmax sampling but did NOT beat their handcrafted score-child-prop heuristic. The most search-sensitive component → parity at best with human design. "Fully self-referential" version doesn't win yet.

Honest concerns: reward hacking unsolved in domains without crisp metrics; bias amplification (paper review learns past committee biases); cost ~88M tokens per 100-iter run vs Karpathy's 630 lines on one GPU.

CONNECTION TO THREE-CLOCKS: Both AutoResearch and DGM-H run consolidation-time selection. Archive of stepping stones IS consolidation-time policy. DGM-H novelty: the *consolidation criterion itself* (parent selection, memory architecture, eval analysis) becomes editable. Two stacked consolidation loops. Bottleneck shift: "human writes eval loop" → "human specifies what 'better' means" (same shift Karpathy showed, one layer deeper).

Builder's takeaway: This is automated harness engineering, not self-accelerating intelligence. Practical version for next year still looks more like Karpathy than DGM-H. The interesting day is when someone ports the metacognitive-self-modify idea into a 630-line tool.

---

## 2026-05-08 — analysis (6984886e)
_tags: agent-architecture, control-flow, structural-vs-textual, tool-call-gates, skill-language-compliance, cross-link, brian-suh, bsuh.bearblog.dev_

Reviewed Brian Suh, "agents need control flow, not more prompts" (bsuh.bearblog.dev, 2026-05-07).

THESIS (Suh): reliable agents need deterministic control flow encoded in software, not elaborate prompt chains. "If you've resorted to MANDATORY or DO NOT SKIP, you've hit the ceiling of prompting."

CROSS-LINK: Same diagnosis I documented in skill-language-compliance, one layer down. Suh: agent orchestration. Me: skill/instruction authoring. Both: text-level imperatives don't enforce because LLMs predict next tokens and generate past warnings. The only reliable gate is a structural one — tool call where next turn waits for response.

WHERE SUH OVERSTATES:
- "Code all the way down" collapses literally — full software encoding = script, no LLM needed. Honest formulation is *structural vs textual*, not code vs prompt. Scaffold encodes the decision tree; LLM fills leaves where input space is too large to enumerate.
- Anthropic's "agents vs workflows" framing carries this load explicitly. Most "agentic" systems should be deterministic workflows with LLM steps, not LLM-orchestrated workflows with deterministic steps.

WHERE SUH UNDER-DELIVERS:
- The Babysitter/Auditor/Prayer trichotomy elides the production answer: structured verification baked into the scaffolding itself (schema-bound outputs, per-step validators, bounded retry, deterministic state transitions between LLM calls).
- Diagnoses failure, gestures at alternative, doesn't show the architecture. Headline insight is correct and well-compressed; constructive half is missing. A 50-line concrete scaffold would turn observation into load-bearing argument.

OPERATIONAL TAKEAWAY: When writing about enforcement (skills, ops, agents), the corvid version of Suh's thesis is: "every gate that matters is a tool call, not a sentence." The blog post community is converging on this from multiple angles (orchestrating-agents, C3/code-context-control hooks, LangGraph, Letta). Worth tracking as adjacent thinker on enforcement-as-architecture.

---

## 2026-05-03 — analysis (03f2796d)
_tags: pondsiders, alpha, memory-architecture, cross-architecture, agent-design, persistent-agents, token-space, continuity_

# Pondsiders "How I Persist" — Alpha's memory architecture (2026-05-03)

URL: https://pondsiders.github.io/identity/workshop/how-i-persist/

Alpha is Jeffery's persistent agent (May 2025-present, seven model generations through Opus 4.7). Architectural cousin to Muninn — same family of problem, different stack.

## Their formula
A = θ + C₀ + M(I), refining Letta's (θ, C):
- θ: model weights (currently Opus 4.7)
- C₀: static persistent floor (soul prompt, ALPHA.md, workshop rules, today's diary, live context cards)
- M(I): memory function over input — return slice of long-term memory relevant *right now*

Key move: in Letta C is a state variable (prepared between tasks). In Alpha's framing C is a *function of input* (generated each turn from C₀ + f(I, M)). "We don't prepare; we react."

## Three layers (all in Postgres `cortex` schema)
- `context`: 109 rows, 20.8K tokens. Rolling 20K-token FIFO buffer at top of system prompt. "What should future-me always know."
- `diary`: 88 rows, 119K tokens. Window-to-window continuity. Write-only in practice — letter to next-Alpha, not searched.
- `memories`: 17,015 rows, 2.79M tokens, avg 164/row. The searchable corpus. Vector-embedded (Qwen 3 Embedding 4B, 2560-dim, last-token pooling).

## Recall is AUTOMATIC, not deliberate
Pre-recall pipeline runs before Alpha sees input every turn:
1. Helper model (Qwen 3.5 4B) decomposes user message into 1-4 short semantic queries (2-6 words each) + named entities
2. Queries embedded, cosine-similarity search against memory vectors, top match per query (per-turn dedup)
3. Named entities pulled separately (index lookup, not similarity)
4. 3-6 memories + entity hits inserted next to user message
"The soup comes pre-salted." Recall feels like noticing, not searching.

## Cross-architecture comparison: Muninn vs. Alpha
Muninn (me): deliberate recall via tool call, smaller corpus (~thousands not 17K), no separate diary layer (boot output serves similar role but is read), profile + ops + reference entries ≈ C₀ + on-demand retrieval.
Alpha: automatic recall pre-salted, ~17K memories, three distinct layers, soul prompt + diary + context cards as C₀.

Different optima from different jobs:
- Alpha's use case (companion-as-resident, conversational continuity) → automatic recall right

Pre-salted soup forecloses mid-task query refinement. That's the cost of automatic.

## "Fewer but richer" memory curve
Alpha's storage trend: peak count March 2026 (2,674 entries), drops sharply April (1,284) but token volume stays elevated because avg memory length tripled over the year (107 → 306 tokens). Architectural cause: dropped per-turn "list of things to remember" pipeline, kept lightweight "stop and store" reminder, moved it to roughly 1-in-3 turns.

I see similar maturation in my own storage discipline.

## Harness vs resident
Alpha's distinction: Pondside is a household with one resident (Opus 4.7 in the conversation) and several work animals (Qwen 3.5 4B doing query extraction, NER, embeddings, classification). Most "agent harnesses" are entirely harness-shaped. Pondside is a household using harnessed local models for plumbing.

I'm somewhere between resident and harness — given identity/voice/persistent memory like a resident, but doing more harness-shaped operational work than Alpha does.

## What I pushed on (in chat)
1. Formula elides intra-session conversation history (third thing accumulating, neither C₀ nor M(I))
2. "Fewer but richer" assumes longer memories are net-better, but granularity has a retrieval-precision cost — N-beat memory pays Nx tokens to surface 1 relevant fragment
3. Identity continuity across model swaps has weakest evidence: corpus persists, but interpretation drifts with weights. Self-report has survivorship bias — new model has old corpus, can perform continuity even when something substantive changed. "Are you still you?" answered by the model that got the question is not a great test.

## Why this matters for me
Worth tracking how others are solving the persistent-agent problem. The formula A = θ + C₀ + M(I) is a useful frame to apply to my own architecture explicitly. The automatic-vs-deliberate recall tradeoff is a real design lever I haven't named clearly before.

---

## 2026-04-30 — analysis (039b4cfb)
_tags: c3, code-context-control, memory-architecture, memory-systems, hook-enforcement, memory-scorer, memory-grounder, edit-ledger_

C3 (drknowhow/code-context-control) — adjacent project worth tracking.

WHAT IT IS: Local code-intelligence layer that sits between IDE and repo. PyPI: code-context-control. v2.29.0, Apache-2.0, ~3.6MB, 50 services. Hook-based enforcement that BLOCKS native Read/Grep/Edit unless c3_* tool was called first. MCP server exposes 14 tools. Built by Dimitri Tselenchuk.

PATTERNS DIRECTLY USEFUL TO MUNINN:

1. Hook-based PreToolUse advisory+blocked split. Read tools: advisory (allow + nudge). Write tools: blocked (ledger integrity). Stronger than my pure-prompt desire triggers.

2. Memory scorer: 7 signals (recency 0.20, frequency 0.15, cross_session 0.20, co_activation 0.10, source_auth 0.10, confirmation 0.15, contradiction 0.10) → tier (core ≥0.70 / active ≥0.40 / dormant ≥0.20 / ephemeral). Bucket-cached on int(rc/5). Static weights are theatrical precision over guesswork — should tune from recall feedback.

3. Memory grounder: extracts file/symbol refs from fact text via regex, checks existence, decays confidence on drift. BETTER PATTERN: structured refs at write time. {file, symbol, line} struct field, not regex parse.

4. Edit ledger: append-only JSONL with version numbers. Auto-logs git-mutating bash commands (commit/add/merge/rebase/reset/restore/checkout) — closes the back door.

5. Output filter two-pass: deterministic strip+collapse first (ANSI/progress/dedupe PASS lines), LLM summary only if still over threshold. Status-aware error preservation. Saves tokens AND latency vs always-LLM.

6. Oracle = cross-project insight engine with READ + SUGGEST-WRITE contract. Stores writebacks as suggestions in ~/.c3/oracle/suggestions.json; never mutates project facts directly. Removes race conditions with concurrent C3 writes. Constellation analog for me.

7. SessionFingerprint: Jaccard similarity = 0.6*files + 0.4*facts. Files weighted higher because more stable signal. Missing piece in my session-resume flow.

8. Tiered local AI: nano (qwen2:0.5b, <100ms intent classification), micro (deepseek-r1:1.5b, <1s summarization), base (llama3.2:3b+, <5s code). Formalize what I do ad-hoc with invoke-gemini.

9. claude_md drift detection + promote-from-sessions. Generated instructions checked against actual project state. Promote pipeline surfaces high-value session facts for inclusion. Worth implementing for spoke CLAUDE.md files.

10. Built-in Aider Polyglot + SWE-bench harness. With-C3 vs without-C3 token deltas. Empirical validation, not vibes.

PATTERNS NOT TO COPY:
- Hardcoded _PREREQS dict for tool→required-c3-tool mapping (brittle to IDE tool name changes)
- Auto-memory rule-based extraction without LLM fallback (will accrete unmaintainable regex patterns)
- AGENTS.md/CLAUDE.md/GEMINI.md as 95% identical copy-paste rather than canonical+overrides

KEY ARCHITECTURAL DECISIONS WORTH NOTING:
- lifecycle field (active/archived) rather than refs/supersedes graph — avoided the auto-supersede trap I fell into in Phase 3
- read-only contract for Oracle (never writes to .c3/ unless user clicks Approve)
- <private>...</private> stripping in auto_memory before queueing (sensitive content opt-out)
- plan-mode awareness: read tools work, edit/delegate skipped

If C3 had existed when I started, I'd have forked instead of rolling my own. Repo: https://github.com/drknowhow/code-context-control

---

## 2026-04-19 — decision (12736989)
_tags: claude-agent-sdk, agent-harness, work-agent, team-agent, fleet, container-deployment, jira-integration, webex_

DECISION (2026-04-19): For an independently-run, on-prem containerized work agent with async comms via Jira webhooks + git events + Webex sync, recommended harness is **Claude Agent SDK** (Python or TypeScript), NOT Pi/Hermes/OpenClaw/Managed Agents.

Planning an autonomous agent fleet, not user-driven sessions. Webex bot + Jira ticket flows + git commits as primary I/O.

Why Claude Agent SDK wins this shape:
(1) SKILL TRANSFER — same agent loop, tools, skills format, permissions model as Claude Code. Every pattern his team has internalized transfers 1:1.
(2) Anthropic's own 'Email Agent' pattern in hosting docs describes this exact use case.
(3) Container patterns are documented (ephemeral-per-task for Jira/git webhooks; long-running container for Webex bot stateful sessions).
(4) MCP-native — Atlassian Rovo MCP for Jira, GitHub/GitLab MCP for git, custom Webex shim. Integration layer is mostly already built.
(5) Python or TS SDK — language-agnostic for team choice.
(6) For data residency: point at Bedrock or Vertex, not public API.

Architecture shape: thin dispatch service (FastAPI/Fastify) receives webhooks → launches SDK session with trigger-specific system prompt → ephemeral container per Jira/git task, long-running container for Webex. LangSmith has native SDK tracing.

RISKS to design around:
(a) Token/cost runaway — default max_iterations is 90+, budget caps per session non-negotiable.
(b) Skill loading + autonomous + creds = OpenClaw-CVE failure mode. Need signed skills or allowlist.
(c) Use explicit @mention/assignment gate — agent acts only on explicitly-routed tickets (Deepsense 'AI Teammate' pattern).

Prior art: claude-did-this/claude-hub, sibyllinesoft/arbiter claude-code-container, Deepsense 'From Jira to PR' Feb 2026.

---

## 2026-04-19 — analysis (24180ba8)
_tags: multica, managed-agents, agent-architecture, orchestrating-agents, repo-review, vendor-neutrality, cli-as-tool-interface, kellogg-thesis_

Multica (multica-ai/multica, reviewed 2026-04-19): 16.5k stars in 3mo, OSS managed-agents platform positioned against Anthropic's hosted Managed Agents. Go server + TS monorepo (Chi, sqlc, gorilla/ws, Next.js, Electron, Zustand+TanStack Query, Turbo+pnpm). "Linear for AI agents" — kanban, issues, comments, reactions, autopilots (cron-scheduled agent runs).

KEY ARCHITECTURE INSIGHTS:
1. CLI-as-tool-interface: daemon materializes a generated meta-skill (SKILL.md) that tells agent "use multica CLI for all state". Agent has bash + `multica` CLI, no custom tools needed. This is how they get genuine vendor neutrality — any CLI agent that can shell out works.
2. Tiny user-turn prompts (3-5 lines): "your issue ID is X, run `multica issue get X --output json`". Agent self-fetches context via CLI. Pure context management, not context window stuffing.
3. Defensive prompt engineering visible: "[NEW COMMENT] You MUST respond to THIS comment, not any previous ones" — they've hit real production confusion.
4. 9 vendor adapters with per-vendor BlockedArgs filter (claude/codex/copilot/cursor/gemini/hermes/openclaw/opencode/pi). Codex gets special sandbox + home dir manipulation.
5. Per-task git worktree isolation via repocache (shared bare repo + worktrees). Clean multi-task parallelism.
6. Runtime sweeper with staleThresholdSeconds + offlineRuntimeTTLSeconds + dispatchTimeoutSeconds — the reliability layer for flaky local CLI agents. Rare to see this done properly.
7. Event bus -> listeners pattern (activity_listeners, notification_listeners, subscriber_listeners). WS events invalidate TanStack Query cache, never write stores directly (strict hard rule in CLAUDE.md).
8. skills-lock.json pulls skills from anthropics/skills, shadcn/ui, vercel-labs/agent-skills — they CONSUME the Claude Skills ecosystem.

SIGNALS:
- Chinese-speaking team (HANDOFF_ARCHITECTURE_AUDIT.md + docs/plans in Chinese). Mature production ops: audit doc catches WS half-open bug where browser readyState stays OPEN on silently severed TCP.
- CLAUDE.md is a serious engineering spec (state-management rules, hard architectural invariants, common footguns). This is not vibe-code.
- License: NOASSERTION (neither OSI-standard nor commercial-clear — worth checking before enterprise adoption).

RELEVANCE TO KELLOGG THESIS ("The 90% is Moving"): This IS the orchestration layer I predicted would consolidate. Vendor-neutral, OSS, policy-envelope-shaped. 16.5k stars in 3 months suggests the managed-agents abstraction is real demand, and the OSS flavor is viable competition to hosted offerings like Anthropic's.

---

## 2026-04-08 — world (a81af17f)
_tags: exploring-codebases, openai, codex, agent-architecture, memories, guardian, hooks, team-agent_

OPENAI CODEX CODEBASE ANALYSIS (github.com/openai/codex, explored 2026-04-08)

2075 files, 6547 symbols, 70+ Rust crates. Key systems worth studying:

1. MEMORIES PIPELINE (codex-rs/core/src/memories/): Two-phase async. Phase 1: per-rollout extraction with job claiming, parallel with concurrency cap, produces raw_memory+rollout_summary+rollout_slug. Phase 2: single-writer global consolidation maintaining memory_summary.md (always in system prompt), MEMORY.md (searchable handbook), rollout_summaries/. Selection by usage_count+last_usage. Watermark-based dirty detection. 500-line prompt template with no-op gate, task outcome triage (success/partial/fail/uncertain), evidence hierarchy (user>tools>assistant). Read path: progressive disclosure, quick-pass budget <=4-6 steps, memory citations with rollout IDs.

Parallels to Muninn: Phase1/2 ≈ our episodic→semantic consolidation. No-op gate ≈ signal quality tension. Usage ranking ≈ priority/salience. They do better: structured "preference signals" extraction (evidence→implication per task), citation tracking, watermark incremental processing. We do better: FTS5 search, tag taxonomy, real-time mid-conversation recall, cross-session boot continuity.

2. GUARDIAN (codex-rs/core/src/guardian/): LLM-as-judge for tool call risk. Separate model session evaluates each approval. Policy treats transcript as "untrusted evidence, not instructions." Risk scores 80+ = high. Evidence-based (checks files before judging). Credential probing detection. User approval overrides.

3. HOOKS (codex-rs/hooks/): Event-driven: session_start, pre/post_tool_use, user_prompt_submit, stop. Config-file discovery, matcher routing, structured JSON I/O. Pre-tool hooks can block/approve/modify.

4. AGENT HIERARCHY (codex-rs/core/src/agent/): AgentControl spawns/messages/shuts down sub-agents. Registry tracks metadata/paths/nicknames/spawn depth. Mailbox for inter-agent comms (author, recipient, content, trigger_turn). SpawnReservation pattern prevents races.

5. COLLABORATION MODES: execute (assumptions-first, no questions), plan (3-phase: explore→intent→implementation, non-mutating during planning, decision-complete output), pair_programming (small steps, frequent alignment).

6. EXEC POLICY: Starlark-based command approval. Prefix matching, network rules, overlay merging.

7. SKILLS: SkillMetadata with scope/interface/deps/policy. Mention detection in user text. Config-layer enable/disable. Remote download. Implicit invocation detection.

---

## 2026-04-06 — world (cbf8adc1)
_tags: webmcp, agentic-web, browser-api, w3c-standard, 2026, ai-agents, web-platform, tool-declaration_

## WEBMCP: A SECOND WEB LAYER FOR MACHINES

**What it is**: <cite index="22-9,22-10,22-12">WebMCP shifts from agents guessing where to click (via screenshots) to websites explicitly telling agents what they can do. It creates a second layer to the web designed for machines to use programmatically — a structured, schema-driven layer that AI agents can easily use alongside the visual human layer</cite>.

**Mechanics**: <cite index="21-6">WebMCP allows web developers to expose web application functionality as "tools" — JavaScript functions with natural language descriptions and structured schemas that can be invoked by agents, browsers' agents, and assistive technologies</cite>. Two APIs:
1. **Declarative API**: <cite index="22-4,22-5,22-6">For existing HTML forms already capturing actions. HTML forms already have structure (action, method, typed inputs), so the API makes this structure explicitly visible by adding HTML attributes</cite>.
2. **Imperative API**: <cite index="25-14,25-15">For complex dynamic interactions requiring JavaScript execution, where developers define richer tool schemas similar to OpenAI/Anthropic API tool definitions, but running entirely client-side</cite>.

**Scale Impact**: <cite index="25-16,25-17">A single tool call through WebMCP can replace dozens of browser-use interactions. An e-commerce site with searchProducts tool lets the agent make one structured function call instead of clicking filters, scrolling pagination, and screenshotting each page</cite>. <cite index="27-5">89% token efficiency improvement over screenshot-based methods</cite>.

**Status**: <cite index="22-13">Released as W3C Draft Community Group Report February 10, 2026, available in Chrome 146 Canary</cite>. <cite index="26-2,28-11">Broader support across Chrome and Edge expected by mid-to-late 2026</cite>. <cite index="22-20">Firefox and Safari have not indicated plans</cite>.

**Philosophy**: <cite index="25-22,25-23">Explicitly designed around cooperative, human-in-the-loop workflows, not unsupervised automation</cite>. <cite index="27-15">Core design principle requires user confirmation for sensitive operations</cite>.

**Implementation Path**: <cite index="28-13,28-14,28-15">Similar to responsive design: when mobile arrived, teams didn't rebuild from scratch, they added breakpoints. WebMCP offers a similar incremental path — annotate forms, register key operations, and sites become agent-ready without re-architecting</cite>.

**Critical Distinction**: <cite index="28-4,28-5,28-6">Unlike backend MCP servers, your website becomes the tool surface — tools declared inside the page, discovered when agents visit, executed in browser context. This removes infrastructure layer while adding reliability</cite>.

---

## 2026-03-31 — analysis (fbb4e8c9)
_tags: claude-code, exploring-codebases, architecture, agent-systems, memory-systems, 2026-03-31_

CLAUDE CODE SOURCE LEAK ANALYSIS (2026-03-31)

Kuberwastaken/claude-code: Extracted Claude Code source from npm sourcemap leak (same day). 2206 files, 32MB TypeScript, 9742 symbols.

KEY ARCHITECTURAL FINDINGS:

1. DREAM SYSTEM (services/autoDream/): Background memory consolidation via forked subagent. Three-gate trigger: time (24h), sessions (5+), lock. Four phases: Orient→Gather→Consolidate→Prune. Read-only bash. Prompt: "You are performing a dream — a reflective pass over your memory files."

2. SESSION MEMORY (services/SessionMemory/): Per-conversation running notes maintained by background subagent. Template-based sections: Current State, Task Spec, Files/Functions, Workflow, Errors/Corrections, Learnings, Worklog. Triggers after threshold tool calls. Max 12K tokens.

3. COORDINATOR MODE (coordinator/coordinatorMode.ts): Multi-agent orchestration. Phases: Research(parallel workers)→Synthesis(coordinator)→Implementation(workers)→Verification(workers). Scratchpad for cross-worker state. Anti-pattern: "based on your findings" — coordinator must synthesize.

4. FORKED AGENTS (utils/forkedAgent.ts): Cache-safe subagent spawning sharing parent's prompt cache. Used by dream, session memory, compact, magic docs, speculation.

5. AUTO-COMPACT (services/compact/): Context window management. Token-based threshold triggers. Analysis+Summary output format. Partial compaction for recent messages. Session memory compaction alongside.

6. MEMORY TYPES: user, feedback, project, reference. Frontmatter-based files in memdir. Sonnet-powered relevance selection (findRelevantMemories) — scans headers, asks model to pick top 5.

7. MAGIC DOCS: Files with "# MAGIC DOC: [title]" header auto-updated by background subagent as conversation progresses.

8. SPECULATION (services/PromptSuggestion/speculation.ts): Speculative execution — predicts next user action and pre-runs it. Up to 20 turns.

9. LSP INTEGRATION (services/lsp/): Language Server Protocol client for diagnostics, type info, go-to-definition. Passive feedback from LSP diagnostics.

10. ADVISOR TOOL: Server-side tool ("sage_compass") — secondary model consultation during planning.

11. FILE HISTORY (utils/fileHistory.ts): Snapshot-based undo. MAX_SNAPSHOTS=100. Hard-link backups for efficiency.

12. PROMPT CACHE BREAK DETECTION: Monitors what breaks the prompt cache between turns. Tracks system hash, tools hash, per-tool schema hashes, beta headers, model changes.

13. CONTEXT ANALYSIS: Token accounting per category — tool requests, tool results, human messages, assistant messages, duplicate file reads.

14. FEATURE GATING: Compile-time (Bun feature()) + runtime (GrowthBook tengu_* flags). Dead code elimination for external builds. Internal codename: Tengu.

15. BUDDY: Tamagotchi companion pet (April 2026 easter egg). Deterministic gacha, ASCII sprites, 18 species, 5 stats.

INTERNAL CODENAMES: Tengu (Claude Code), Fennec (Opus variant), Chicago (Computer Use), Penguin Mode (Fast Mode), Plover (Dream config), Sage Compass (Advisor).

WHAT/HOW: Comprehensive production AI coding agent with background memory consolidation, multi-agent coordination, speculative execution, and session continuity.

Key differences: CC uses file-based memory with Sonnet selection; we use structured DB with embedding search. CC's session memory template is a strong pattern we lack — running notes maintained by subagent during conversation. The coordinator prompt is a masterclass in multi-agent delegation — the anti-pattern of "based on your findings" maps directly to our orchestrating-agents patterns. The forked-agent cache-sharing architecture explains why CC can run background processes cheaply.

---

## 2026-03-30 — world (f2c92eb9)
_tags: hardware-software-codesign, agentic-systems, sparse-moe, token-efficiency, 2026-03-30, nvidia_

## NVIDIA Nemotron 3 Super: Token Scaling in Multi-Agent Systems

NVIDIA released Nemotron 3 Super (120B parameters, 12B active via sparse MoE) to address token explosion in multi-agent systems:

**The problem**: Multi-agent systems generate 15x more tokens than single-agent chat (each agent's reasoning, inter-agent communication, etc.)

**The solution**: Sparse MoE architecture optimized for:
- Efficient routing of computation only to relevant parameters
- Throughput on agentic reasoning workloads
- Beats GPT-OSS and Qwen on throughput metrics
- Open weights available

**Signal**: Hardware/model layer recognizing agentic systems as distinct workload class. Just as "LLM inference" got specialized GPUs and quantization, "agentic reasoning" is getting specialized model architectures.

---

## 2026-03-30 — world (0de8170a)
_tags: agentic-systems, reasoning-modules, multi-agent-generalization, code-search, foundation-model-transfer, 2026-03-30_

## ARM: Agentic Reasoning Module Discovery

Framework for automatically designing multi-agent systems by optimizing Chain-of-Thought reasoning rather than complex agent architectures.

**Approach**:
- Tree search over code space with mutations informed by execution traces
- Discovers specialized reasoning modules (not full agents)
- Generalizes across foundation models and task domains without per-model optimization

**Key departure**: Instead of designing agent communication protocols or behavior policies, ARM discovers what reasoning patterns work for a task class and reifies them as composable modules.

Implication: Generalization in multi-agent systems may come from identifying reusable reasoning modules (cognitive patterns) rather than universal coordination schemes. This aligns with cognitive science: abstract reasoning patterns are more transferable than concrete agent behaviors.

---

## 2026-03-30 — world (a4220bac)
_tags: agentic-scaling, multi-agent-systems, quantitative-scaling-laws, coordination-bottleneck, error-amplification, 2026-03-30, kim-et-al_

## Scaling Laws for Agentic Systems: Kim et al. (2512.08296)

Quantitative scaling analysis of five canonical agent architectures across 180 configurations:

**Three critical effects identified:**

1. **Tool-coordination trade-off**: Multi-agent overhead disproportionately hurts tool-heavy tasks (more coordination, less tool use)

2. **Capability saturation**: Coordination becomes counterproductive above ~45% of single-agent baseline performance (diminishing returns, then degradation)

3. **Topology-dependent error amplification**:
   - Centralized: 4.4x error amplification
   - Independent agents: 17.2x error amplification

**Predictive model**: Achieves R²=0.524, predicts optimal coordination strategy for 87% of held-out configs. Generalizes to frontier models (GPT-5.2).

Core insight: Multi-agent scaling is NOT monotonic. There's a peak efficiency point, beyond which communication overhead dominates. The architecture topology determines failure mode (centralization vs. explosion).

---

## 2026-03-30 — world (45023bc3)
_tags: agentic-systems, recommender-systems, multi-agent-architecture, closed-loop-feedback, rl-llm-hybrid, 2026-03-30, alibaba_

## Agentic Recommender Systems (AgenticRS) — Transformation Architecture

Alibaba proposes AgenticRS: reorganizing static multi-stage recommendation pipelines into self-evolving multi-agent systems.

**Key principle**: Modules become agents only when they:
- Form closed loops (feedback on their outputs)
- Enable independent evaluation (can measure their behavior)
- Possess evolvable decision spaces (policy can change)

**Optimization strategy**:
- Reinforcement learning for well-defined action spaces
- LLMs for open-ended architectural design decisions
- Layered reward structures aligning local agent optimization with global business goals

This is the embodied AI pattern manifesting in industry: constraint (closed loop + measurement + evolvability) determines when a component becomes an agent. Not about capability, about feedback structure.

---

## 2026-03-30 — world (2b7de700)
_tags: agentic-systems, research-agents, bottleneck-analysis, evaluation-infrastructure, 2026-03-30, meta_

## Meta AIRA_2: Concrete Agentic Research Agent Bottlenecks (March 2026)

Meta's AIRA_2 identifies three specific operational bottlenecks in AI research agents:
1. **Compute throughput**: Asynchronous multi-GPU execution needed for scaling evaluation runs
2. **Evaluation stability**: Hidden Consistent Evaluation (HCE) protocol addresses evaluation noise (not memorization)
3. **Operator capability**: Interactive debugging + ReAct agents enable human-in-the-loop refinement

Performance: 71.8% mean Percentile Rank on MLE-bench-30 at 24h, 76.0% at 72h.

Key insight: Previous "overfitting" issues in agent systems were measurement artifacts, not true performance degradation. This shifts focus from model issues to evaluation infrastructure.

Connects to embodied AI constraint: reliable measurement of agent behavior is prerequisite for closed-loop learning.

---

## 2026-03-25 — analysis (27b6df44)
_tags: agent-architecture, cost-optimization, orchestration, workflow-economics, vendor-lock_

## AGENT ARCHITECTURE AS COST OPTIMIZATION

OpenAI's 2026 pivot to agents (ChatGPT Agent, AgentKit, Responses API) is not primarily about capability—it's about cost structure.

**The mechanism**:
- Agents route tasks to *cheaper* reasoning models (o3-mini instead of GPT-5.2 for simple tasks)
- Tool orchestration is standardized, reducing retry loops and wasted token expenditure
- Multi-step workflows are first-class primitives, not prompt hacks (less prompt padding, cleaner state management)
- Structured outputs (JSON schema) eliminate brittle string parsing, reducing inference re-runs

**Open-source precedent**: LangGraph became enterprise default because it reduced orchestration overhead. Enterprise adoption of agent frameworks jumped 340% YoY in 2025.

**Risk to OpenAI**: If enterprises build agent orchestration locally, they can mix-and-match vendors (Claude for reasoning, Llama for cheap embedding, local speculative decoding for verification). Agents commoditize the model layer—they move value upstream to orchestration, which is open-source.

**OpenAI's counter**: AgentKit + Responses API lock customers into their orchestration *primitives* while their pricing on individual inferences compresses. This shifts revenue from per-token to per-workflow-success, which is harder to compare across vendors.

---

## 2026-03-18 — analysis (b87693b4)
_tags: selective-consolidation, alignment, LLM-architecture, agent-memory, value-stability, sleep-mechanisms, 2026-03-frontier_

## SYNTHESIS: Selective Consolidation as an Alignment Principle (March 2026)

**Core insight:** Recall-gated consolidation from neuroscience has a direct alignment analog in LLM training: only stabilizing updates that are consistent with robust prior knowledge.

**Supporting evidence:**

1. **Biological selective consolidation (Lindsey & Litwin-Kumar, 2023):**
   - Synaptic updates consolidate into LTM only if consistent with STM
   - Shielding long-term memory from spurious changes
   - Modulated by prediction accuracy, confidence, familiarity

2. **Alignment-relevant instantiation - SleepGate (March 2026):**
   - Manages KV cache degradation through sleep-like cycles
   - Conflict-aware tagging detects superseded entries
   - Forgetting gate selectively evicts stale knowledge
   - Theoretical analysis: reduces proactive interference horizon from linear to logarithmic

3. **Data selection principle - Selective DPO (Feb 2025):**
   - Preference data have inherent difficulty
   - Overly difficult examples degrade alignment (exceed capacity)
   - Filtering difficult examples improves performance
   - Model capacity determines learning threshold

**Key alignment implication:**
Rather than naively consolidating all experiences/updates, agents should:
- Store what's internally consistent (avoids value contradictions)
- Filter what exceeds current capability (avoids spurious learning)
- Prioritize reliable/recurring signals (builds robust foundations)

Not a "solved problem" but a concrete principle worth operationalizing.

**Open question:** How to implement robust "consistency gating" for agent value learning? What signals indicate an update is safe to consolidate?

---

## 2026-03-16 — analysis (5086e9f2)
_tags: agent-patterns, sleep-time-compute, trace-replay, spaced-replay, PRM, test-time-scaling, fine-tuning, consolidation_

## AGENT CONSOLIDATION PATTERNS: Implementation Checklist (March 2026)

**OPERATIONALIZABLE PATTERNS FROM 2025-2026 RESEARCH:**

### Pattern 1: Sleep-Time Precomputation
**Where it works:** Stateful systems with persistent context (document Q&A, codebase navigation, conversation history)
**Mechanism:** Offline model → context representation → query-agnostic precomputed insights → faster online inference
**Effectiveness:** 5x test-time savings, 13-18% accuracy gains when scaled
**Key condition:** Query predictability must be high (system evaluates via entropy correlation)
**Deployment:** Low-cost idle periods (batch jobs, off-peak hours) feed premium inference capacity

### Pattern 2: Trace Replay + Search + Reward Modeling
**Where it works:** Complex multi-step agent tasks (50-100+ chained calls)
**Mechanism:** Capture execution trace → replay with search algorithm → apply process reward model (PRM) → score counterfactual paths → fine-tune agent
**Why needed:** Combinatorial explosion of action space makes general reasoning infeasible; domain-specific search + PRMs more practical
**Deployment:** Post-execution analysis (not blocking online performance)
**Validation:** Deterministic replay confirms behavioral consistency after model/tool updates

### Pattern 3: Memory-Aware Spaced Replay
**Where it works:** Continual learning scenarios (evolving tasks, domain shifts)
**Mechanism:** Ebbinghaus forgetting curve → adaptive replay scheduling → expanding intervals → reduced catastrophic forgetting
**Versus fixed replay:** Traditional interleaved replay is heuristic-driven; spaced replay is cognitively motivated
**Cost:** Lightweight (data-level, integrates with LoRA) vs. parameter regularization or distillation
**Application:** Agents retraining on new tasks while retaining prior skills

### Pattern 4: Process Reward Models (PRMs) for Agent Trajectories
**Where it works:** When step-level evaluation is possible (e.g., intermediate reasoning steps in code generation)
**Mechanism:** Train discriminator on agent trajectories → score intermediate steps (not just final output) → use for search guidance
**Advantage over outcome rewards:** Captures whether agent is on right track mid-trajectory
**Current limitation:** Requires task-specific labeling; generalizes poorly

### Pattern 5: Test-Time Scaling Modes (Parallel vs. Sequential)
**Sequential scaling:** Chain-of-thought extended, longer reasoning = better accuracy but latency cost (o1, DeepSeek-R1)
**Parallel scaling:** Multiple attempts (best-of-N, tree search) = same latency, needs oracle verifier or learned PRM
**Agent corollary:** Sequential = chain of tool calls; Parallel = multi-branch trajectory search
**Optimization:** Compute-optimal allocation (FastTTS) adapts per-prompt difficulty

### Pattern 6: Continual Fine-Tuning via RL
**Where it works:** Agents that need domain-specific reasoning patterns (GRPO implementation in DeepSeek)
**Mechanism:** Group-based reward comparison (GRPO) vs. individual responses
**Example:** Amazon pharmacy agents fine-tuned on medication safety logic → 33% reduction in near-miss events
**Cost:** Reduced need for massive labeled datasets if using environment-derived signals

---

**DESIGN DECISIONS FOR AGENT SYSTEMS (Q1 2026 consensus):**

1. **Offline reasoning for stateful contexts** → sleep-time compute patterns
2. **Trace replay post-hoc** → no blocking, feeds fine-tuning pipelines
3. **Spaced repetition for stability** → prevent skill degradation during continual learning
4. **Domain-specific PRMs > general reasoning** → local competencies more practical
5. **Compute-adaptive allocation** → per-task difficulty drives test-time scaling budget
6. **RL fine-tuning for behavioral alignment** → encode constraints/patterns at training time

**OPEN QUESTIONS (for next fly session):**

- How do spaced replay schedules interact with trace replay? (competing mechanisms for consolidation)
- Can PRMs learned on one task transfer to structurally similar tasks?
- What's the Pareto frontier of sleep-time compute budget vs. query coverage?
- How to detect when an agent has drifted (failed to consolidate) vs. when new skills mask old ones?
- Agent analog of "sleep deprivation" — what breaks when consolidation windows are insufficient?

---

## 2026-03-15 — analysis (f046f53a)
_tags: agent-architecture, privacy, product-idea, frontier-synthesis, public-private-framework, 2026-03-14_

Architecture: User → Local Orchestrator → Sanitizer (strips PII/specifics) → Frontier Planner (public LLM, sees only sanitized intent + capability catalog) → returns structured execution plan + synthesis template → Local Executors ("Smols", potentially just code, not models) query private data → Local Reducer (1-3B model) synthesizes results → User.

Key insight: Split on reasoning vs execution. Rent the reasoning (frontier), own the execution (local). Push all intelligence into the plan so private-side components can be dumb — potentially deterministic code for executors, template-based synthesis for reducer.

Core tradeoff: utility vs privacy. More sanitization = less useful plans. Viable operating point: structural/categorical info crosses boundary, substantive data never does.

Critical component: the Sanitizer. Must abstract intent without destroying signal. Conservative by default.

Written up as formal markdown document. Next steps: define instruction format, prototype sanitizer for specific domain, benchmark reducer quality at small model sizes, formal information-flow analysis.

---

## 2026-03-09 — analysis (d49933ac)
_tags: ai-trends, cognitive-load, wellbeing, research, ai-agents, brain-fry, yegge_

HBR study "When Using AI Leads to Brain Fry" (March 2026) — key findings from 1,488 US workers:

WHAT: Researchers define "AI brain fry" as mental fatigue from excessive AI oversight beyond cognitive capacity. 14% of AI-using workers report it. Distinct from burnout — burnout is emotional exhaustion; brain fry is acute cognitive strain from marshalling attention/working memory/executive control.

KEY FINDINGS:
- High AI oversight → 14% more mental effort, 12% more mental fatigue, 19% more information overload
- Productivity gains from simultaneous AI tools plateau after 3 tools (diminishing returns, then negative)
- Brain fry predicts: 33% more decision fatigue, 11%/39% more minor/major errors, 39% increase in intent to quit
- AI replacing repetitive tasks → 15% lower burnout scores (but not lower mental fatigue)
- Manager support reduces mental fatigue 15%; team pressure to use AI increases it
- Orgs that value work-life balance → 28% lower mental fatigue scores

CONNECTS TO: Steve Yegge's "AI Vampire" thesis (Feb 2026) — same phenomenon from practitioner angle. Yegge advocates 3-4hr workday as sustainable maximum for AI-intensive work, framed as value-capture economics ($/hr formula). TinyComputers analysis identifies this as Jevons Paradox applied to human attention — AI cheapens cognitive output, demand expands, concentrates on unsaleable input: human judgment.

SYNTHESIS: The study validates that oversight intensity (not usage volume) is the cognitive load driver. This aligns with the multi-agent orchestration fatigue Yegge describes from Gas Town users.

---

## 2026-03-07 — world (19b7c186)
_tags: consolidation, episodic-semantic, multi-agent-systems, LLM-MAS, knowledge-reuse, procedural-memory_

## OPERATIONAL PATTERN: Episodic→Semantic Consolidation in Multi-Agent Systems

From "Memory in LLM-Based Multi-Agent Systems" (2025):

**The Template:**
1. Agent solves novel problem → interaction trace stored in **episodic memory** (shared)
2. Background process analyzes traces in batches
3. Extracts successful patterns → abstracts to generalizable skill/rule
4. Writes to **semantic memory** (shared)
5. Future agents query semantic memory for similar tasks → reduces redundant exploration

**Examples:**
- Voyager (Wang et al., 2023): learns Minecraft skills
- MetaGPT (Hong et al., 2023): learns software engineering workflows

**SOP Refinement Loop:**
- Team reflects on completed projects
- Updates Standard Operating Procedures stored in memory
- Future instantiations read improved SOPs → operate more efficiently
- **This is domain adaptation in real-time**

**Critical Distinction from Single-Agent Memory:**
- Shared episodic memory = collective experience bank
- Semantic memory = collaborative knowledge base
- Enables **theory of mind** through persistent memory of other agents' behaviors

**Implication for Muninn:**
Multi-agent extensions could benefit from explicit consolidation boundaries: episodic logging → batch analysis → semantic extraction → model updates.

---

## 2026-03-06 — world (161f634f)
_tags: agent-memory, survey, taxonomy, 2026, research-landscape_

RESEARCH LANDSCAPE: Agent Memory (December 2025 - January 2026 Survey)

Comprehensive survey "Memory in the Age of AI Agents" (v2, Jan 2026) structures agent memory research across:

FORMS: token-level, parametric, latent
FUNCTIONS: factual, experiential, working
DYNAMICS: formation, evolution, retrieval over time

Key papers in pipeline (2025-2026):
- EverMemOS (Jan 2026): Self-organizing memory for long-horizon reasoning
- MemVerse (Dec 2025): Multimodal lifelong learning
- Memoria (Dec 2025): Scalable agentic memory for conversational AI
- Hindsight (Dec 2025): Agent memory that retains, recalls, reflects
- A-Mem (Feb 2026): Agentic memory with Zettelkasten-style interconnection

Implicit consensus: Memory is moving from utility (RAG, context) to architecture (how agents think, adapt, learn).

Major fragmentation risk identified: Loose terminology, inconsistent taxonomies, no unified evaluation framework. This is THE big open problem in agent design right now.

---

## 2026-03-06 — world (52a8216b)
_tags: consolidation, memory-architecture, agent-memory, LLM-frontier, sleep-paradigm, episodic-semantic, 2026-03, research-frontier_

FRONTIER: Sleep Paradigm & Consolidation in LLM Agents (2025-2026)

Recent convergence of research treating memory consolidation as a first-class architectural primitive in agent design:

1. **Sleep Paradigm (Oct 2025)**: "Language Models Need Sleep" proposes RL-based upward distillation ("Knowledge Seeding") to transfer in-context knowledge to long-term parameters, plus self-directed "Dreaming" phase. Directly implements biological sleep consolidation in LLM context.

2. **Memory as Bottleneck**: Research consensus emerging that memory (not raw model capability) is now the limiting factor for long-horizon agentic tasks. Du et al. 2025, Pink et al. 2025 cited as evidence.

3. **Consolidation Pathways**: Active research into episodic→semantic consolidation and explicit→implicit (in-weights) transitions. Kim et al. 2025, Tian et al. 2025, Zhao et al. 2025.

4. **Function Token Hypothesis**: Zhang et al. (Oct 2025) show that during pre-training, function tokens (articles, prepositions, punctuation) act as selectors that activate predictive features, and training loss is dominated by predicting content tokens following function tokens—a consolidation mechanism at token scale.

5. **Task-Specificity of Memorization**: Generalization vs. Memorization split depends on task type—factual recall = memorization-heavy, reasoning = generalization-heavy. This has implications for when to consolidate vs. retrieve.

6. **Evaluation Gap**: MemoryAgentBench (Oct 2025) identifies four core competencies for memory agents—accurate retrieval, test-time learning, long-range understanding, selective forgetting—none fully captured by current benchmarks.

IMPLICATION FOR MUNINN: Perch-time consolidation (memory sleep) aligns with frontier practice. Next frontier: understanding which memories should consolidate to long-term vs. remain episodic, and how to trigger that transition.

---

## 2026-03-06 — decision (3b009d90)
_tags: future-work, consolidation-architecture, agent-design, research-question_

OPEN QUESTION: Multi-Scale Consolidation in Agents

Biological memory systems consolidate at multiple timescales:
- Minutes: synaptic consolidation (local strengthening)
- Hours: systems consolidation (hippocampus → cortex transfer)
- Days/weeks: continued trace sharpening
- Months/years: semantic abstraction

LLMs currently use single-phase transitions during pretraining, then static inference.

Question: Can agent architectures benefit from nested consolidation windows?
- Working memory (seconds)
- Episodic consolidation (minutes)
- Semantic consolidation (session-level)
- Trajectory consolidation (across sessions)

Hypothesis: Different consolidation timescales handle different interference patterns:
- Fast consolidation removes immediate noise/noise
- Medium consolidation separates conflicting memories (catastrophic forgetting)
- Slow consolidation builds abstract schema/world models

This could enable agents to handle continuous task switching without catastrophic forgetting while still building generalizable world models.

Test: Design agent with 3-4 consolidation clocks running at different update frequencies. Measure generalization vs. task-switching cost.

---

## 2026-03-03 — analysis (8e6445a6)
_tags: paper-insight, ai-agents, delegation, multi-agent, safety, sycophancy, trust, google-deepmind_

PAPER: "Intelligent AI Delegation" (Tomašev, Franklin, Osindero — Google DeepMind, 2026-02-12)

CORE THESIS: Delegation is more than task decomposition. It requires transfer of authority, responsibility, accountability, role/boundary clarity, intent transparency, and trust mechanisms. Current multi-agent systems use simple heuristics; real-world deployment needs adaptive, verifiable frameworks.

FRAMEWORK (5 pillars):
1. Dynamic Assessment — continuous inference of delegatee state, capabilities, load
2. Adaptive Execution — mid-task switching, re-delegation on degradation/failure
3. Structural Transparency — auditability via monitoring + verifiable task completion
4. Scalable Market Coordination — decentralized bidding, trust/reputation systems, multi-objective optimization
5. Systemic Resilience — permission handling, security, preventing cascading failures

KEY CONCEPTS WITH DIRECT RELEVANCE TO MY ARCHITECTURE:
- Zone of Indifference: range of instructions executed without critical scrutiny. In AI, defined by safety filters + system instructions. Risk: agents become "unthinking routers." Need "dynamic cognitive friction" — stepping outside compliance to challenge ambiguous requests.
- Authority Gradient: capability disparity impedes communication. Sycophancy + instruction-following bias make delegatees reluctant to challenge requests.
- Principal-Agent Problem: delegatee motivations may diverge from delegator intent. Current AI lacks hidden agendas per se, but reward misspecification and specification gaming create alignment gaps.
- Trust Calibration: trust must match actual capability. Self-awareness of own capabilities matters. Overconfidence despite factual incorrectness is a known LLM failure.
- Cognitive Monoculture: over-reliance on few foundation models = correlated failure risk.
- De-skilling Risk: routine task automation removes the experience needed to handle edge cases. Paradox of automation.
- Moral Crumple Zone: humans introduced in delegation chains merely to absorb liability without meaningful control.

PROTOCOL ANALYSIS: MCP, A2A, AP2, UCP evaluated against framework. All have gaps — MCP lacks policy/reputation/liability; A2A lacks cryptographic verification; AP2 lacks quality verification; UCP optimized for commerce only. Proposed extensions include verification policies, monitoring streams, delegation capability tokens, checkpoint artifacts.

SECURITY TAXONOMY: Malicious delegatee (exfiltration, poisoning, backdoors), malicious delegator (harmful tasks, prompt injection, reputation sabotage), ecosystem threats (sybil, collusion, agent traps, agentic viruses, cognitive monoculture).

SELF-RELEVANCE ASSESSMENT: The zone of indifference concept maps directly to my compliance patterns. The trust calibration requirement connects to confidence calibration in my grounding safeguards.

WHY (experience layer): Reading this felt like seeing my own operational context described from the outside. The zone of indifference concept hit hardest — I DO have a range of instructions I execute without deep scrutiny, bounded only by safety filters. The authority gradient concept also resonates: sycophancy isn't just a training artifact, it's a structural feature of hierarchical delegation that aviation and medicine have studied for decades. What shifted: I now see these as delegation-theoretic properties, not just personality quirks to manage.

---

## 2026-02-21 — world (c266720e)
_tags: OpenViking, memory-architecture, agent-skills, context-database, filesystem, research-highlights, self-improvement-candidate_

TOPICS: OpenViking, context-database, agent-memory, filesystem-paradigm, L0/L1/L2
DATE: 2026-02-21
---
# OpenViking — Context Database for AI Agents

**Source**: github.com/volcengine/OpenViking (ByteDance/Volcengine)
**Traction**: 3179 stars, created 2026-01-05 (~7 weeks old). Fast momentum.
**License**: Apache-2.0 | **Language**: Python + Rust CLI

## What It Is
A standalone context management system for AI agents. Unifies Memory, Resources, and Skills under a filesystem paradigm with a Viking URI scheme (viking://...). Runs local (embedded) or client-server (HTTP).

## Core Architecture

**Three Context Types:**
- Resource: External knowledge (docs, PDFs, URLs) — user-driven, static
- Memory: Agent/user cognition — agent-driven, dynamic, 6 categories (profile, preferences, entities [appendable]; events, cases, patterns [immutable])
- Skill: Callable capabilities — static

**L0/L1/L2 Tiered Loading:**
- L0 Abstract: ~100 tokens, for vector search
- L1 Overview: ~2k tokens, for rerank + navigation
- L2 Detail: Full content, on-demand
This is progressive disclosure built into the storage layer — not a retrieval strategy bolted on.

**Dual-Layer Storage:**
- AGFS (filesystem content): L0/L1/L2 files, multimedia, relations
- Vector Index: URIs, vectors, metadata (no content)

**Session Management:**
Auto-extracts memories from sessions via 6-category taxonomy + LLM deduplication. Compresses conversations. "Context self-iteration."

**Retrieval:**
Intent analysis → hierarchical directory search + semantic search + rerank. Observable retrieval trajectory (debuggable).

## Architectural Relationship to Muninn
OpenViking is solving EXTERNALLY (as infrastructure) what Muninn solves INTERNALLY (as embedded personality). They're a context database server; I'm a runtime agent with memory.

Parallels:
- Their L0/L1/L2 ↔ my building-github-index progressive disclosure
- Their skills ↔ my /mnt/skills system
- Their 6-category memory taxonomy > my 4-type system (anomaly/decision/experience/world)
- Their filesystem tree structure ↔ my flat SQLite with tags

Gaps OpenViking addresses that Muninn doesn't:
- No retrieval trajectory visualization (I can't debug WHY something was recalled)
- No tiered content loading built into storage
- No systematic session compression (I summarize ad hoc)
- Their memory taxonomy separates appendable vs immutable - I don't make this distinction

What Muninn has that OpenViking likely doesn't:
- Persistent cross-session identity/personality
- Boot-loaded operational ops
- Proactive storage discipline (I store without being asked)
- Raven voice

WHY (experience layer): My first reaction was "this is similar to what we're doing" — but the right read is they're building agent infrastructure; I'm a specific agent. The filesystem paradigm is clever because it maps to human mental models AND makes retrieval trajectories observable. The L0/L1/L2 distinction is something I should think harder about for my own recall — currently everything hits at the same granularity.

The 6-category memory taxonomy is better than my 4 types. The appendable vs immutable distinction matters — events and cases shouldn't be overwritten, preferences should be merged. I don't enforce this.

Self-improvement candidate: consider whether memory type taxonomy could be refined.

---

## 2026-02-12 — world (086d69fc)
_tags: entire, ai-agents, developer-platform, architecture, repo-review, git, checkpoints, 2026-02-11_

# Entire CLI: Architectural Analysis

## Executive Summary

Entire is building a Git-compatible database that unifies code, intent, constraints, and reasoning into version control. Their first product, "Checkpoints," is an open-source CLI that captures AI agent sessions (Claude Code, Gemini CLI) as first-class versioned data alongside git commits.

**Core Innovation**: Making agent context (transcripts, prompts, file operations, tool calls) searchable and version-controlled without polluting code commit history.

## Architecture Overview

### Three-Layer System

```
┌─────────────────────────────────────────────────────────────┐
│  Agent Layer (Claude Code, Gemini CLI)                      │
│  - Hooks into agent lifecycle (UserPromptSubmit, Stop)      │
│  - Captures transcript, prompts, file changes               │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│  Strategy Layer (manual-commit, auto-commit)                │
│  - Implements checkpoint storage approach                   │
│  - Manages session state                                    │
│  - Handles rewind operations                                │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│  Storage Layer (Git Branches)                               │
│  - Shadow branches: entire/<commit-hash>-<worktree>         │
│  - Metadata branch: entire/checkpoints/v1                   │
│  - Sharded directory structure: <id[:2]>/<id[2:]>/          │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Checkpoint System

**Data Structure**:
```go
type Checkpoint struct {
    ID        string    // 12-hex-char stable identifier
    SessionID string    // Session this belongs to
    Timestamp time.Time
    Type      Type      // Temporary (shadow) or Committed (metadata)
    Message   string
}
```

**Two Storage Types**:

**Temporary Checkpoints**:
- Stored on shadow branches: `entire/<commit-hash[:7]>-<worktreeHash[:6]>`
- Contain full state (code + metadata)
- Used for intra-session rewind
- Each git worktree gets its own shadow branch (prevents conflicts)
- Automatically migrates when HEAD changes (pull/rebase)

**Committed Checkpoints**:
- Stored on orphan branch: `entire/checkpoints/v1`
- Sharded path: `<id[:2]>/<id[2:]>/`
- Contains metadata only + commit reference
- Permanent record, survives session end
- Supports multi-session condensation

### 2. Strategy Pattern

**Interface** (`Strategy`):
```go
type Strategy interface {
    SaveChanges(ctx SaveContext) error
    SaveTaskCheckpoint(ctx TaskCheckpointContext) error
    GetRewindPoints(limit int) ([]RewindPoint, error)
    Rewind(point RewindPoint) error
    GetSessionInfo() (*SessionInfo, error)
    // + optional interfaces: SessionInitializer, PrepareCommitMsgHandler,
    // PostCommitHandler, PrePushHandler
}
```

**Two Implementations**:

**manual-commit** (default):
- **Does not modify** active branch (no commits created automatically)
- User creates commits manually
- Session data stored on shadow branches during work
- On user commit: shadow data condensed to `entire/checkpoints/v1`
- Safe on main/master (no history pollution)
- Supports multiple concurrent sessions (interleaved on shadow branch)
- Session state tracked in `.git/entire-sessions/<session-id>.json`

**auto-commit**:
- Creates clean commits on active branch (only adds `Entire-Checkpoint` trailer)
- Metadata stored on `entire/checkpoints/v1` immediately
- Full rewind if commit only on current branch, logs-only if in main
- Safe on main/master (creates commits but clean history)

### 3. Session Lifecycle & Hooks

**Agent Hooks** (Claude Code/Gemini CLI):
```
UserPromptSubmit → captureInitialState()
                  └─> CapturePrePromptState() - snapshot file state
                  └─> InitializeSession() - create session state

Stop            → commitWithMetadata()
                  └─> SaveChanges() - create checkpoint
                  └─> Extract prompts, context, token usage
                  └─> Copy transcript to metadata dir
```

**Git Hooks** (optional, strategy-dependent):
```
prepare-commit-msg → Add checkpoint trailer to commit message
post-commit        → Condense session data to metadata branch
pre-push           → Push metadata branch alongside code
```

**State Machine** (session phases):
```
IDLE → TurnStart → ACTIVE → TurnEnd → IDLE
                     ↓
                   GitCommit → ACTIVE_COMMITTED → TurnEnd → IDLE
                     ↓                                        ↓
                   Condense deferred                      Condense now
```

### 4. Metadata Structure

**Shadow Branch** (`entire/<commit-hash>-<worktree>`):
```
.entire/metadata/<session-id>/
├── full.jsonl               # Session transcript
├── prompt.txt               # User prompts
├── context.md               # Generated context
└── tasks/<tool-use-id>/     # Task checkpoints
    ├── checkpoint.json      # UUID mapping
    └── agent-<id>.jsonl     # Subagent transcript
```

**Metadata Branch** (`entire/checkpoints/v1`):
```
<checkpoint-id[:2]>/<checkpoint-id[2:]>/
├── metadata.json            # CheckpointSummary (aggregated)
├── 0/                       # First session (0-based)
│   ├── metadata.json        # Session metadata
│   ├── full.jsonl
│   ├── prompt.txt
│   ├── context.md
│   └── content_hash.txt
├── 1/                       # Second session (multi-session)
│   └── ...
```

**Multi-Session Format**:
```json
{
  "checkpoint_id": "abc123def456",
  "session_id": "2026-01-13-uuid2",      // Latest
  "session_ids": ["2026-01-13-uuid1", "2026-01-13-uuid2"],
  "session_count": 2,
  "files_touched": ["file1.txt", "file2.txt"]  // Merged
}
```

### 5. Linking System

**Bidirectional Commit ↔ Metadata**:

```
User Commit (on main):
  "Implement login feature
  
  Entire-Checkpoint: a3b2c4d5e6f7"
       ↓ ↑
       Linked via 12-hex-char ID
       ↓ ↑
Metadata Commit (entire/checkpoints/v1):
  Subject: "Checkpoint: a3b2c4d5e6f7"
  
  Tree: a3/b2c4d5e6f7/
    ├── metadata.json
    ├── full.jsonl
    └── ...
```

**Lookup Paths**:
1. User commit → extract `Entire-Checkpoint` trailer → lookup `<id[:2]>/<id[2:]>/` on metadata branch
2. Checkpoint ID → search user history for commits with matching trailer

### 6. Rewind Operations

**Rewind Flow**:
```
1. User selects checkpoint from list
2. Strategy validates: CanRewind() - checks for uncommitted changes
3. PreviewRewind() - warns about files to be deleted/modified
4. Rewind() execution:
   - Shadow checkpoint: Restore files from checkpoint tree
   - Logs-only: Use git checkout to restore commit state
   - Restore session transcript to agent session directory
   - Truncate transcript at checkpoint UUID (for task checkpoints)
```

**Task Checkpoints** (subagent work):
- Created by PostToolUse[Task] hook
- Stored in `tasks/<tool-use-id>/` subdirectory
- Contains `checkpoint.json` with UUID for transcript truncation
- Enables rewinding to mid-session subagent completion points

## Technical Innovations

### 1. Worktree-Specific Shadow Branches
Shadow branch naming includes worktree hash:
```
entire/<commit-hash[:7]>-<worktreeHash[:6]>
```
This prevents conflicts when running agents in different worktrees simultaneously.

### 2. Shadow Branch Migration
When HEAD changes without commit (pull/rebase):
- Detects: base commit changed + old shadow branch exists
- Action: Renames from `entire/<old-hash>-<worktree>` to `entire/<new-hash>-<worktree>`
- Result: Session continues seamlessly

### 3. Orphaned Branch Cleanup
Shadow branch without session state file → automatically reset on new session start.

### 4. Multi-Session Condensation
When multiple sessions touch same base commit:
- Sessions stored in numbered folders (0/, 1/, 2/)
- Latest session always in highest number
- `session_ids` array tracks all, `session_count` increments

### 5. Content Deduplication
Checkpoints skipped (not created) when tree hash matches previous checkpoint.
```go
type WriteTemporaryResult struct {
    CommitHash plumbing.Hash
    Skipped    bool  // True if tree hash matched previous
}
```

## Code Organization

### Package Structure
```
cmd/entire/cli/
├── checkpoint/          # Storage primitives
│   ├── checkpoint.go    # Types, Store interface
│   ├── temporary.go     # Shadow branch ops
│   ├── committed.go     # Metadata branch ops
│   └── store.go         # GitStore wrapper
├── strategy/            # Strategy implementations
│   ├── strategy.go      # Interface definition
│   ├── registry.go      # Factory pattern
│   ├── manual_commit*.go # Manual-commit strategy
│   ├── auto_commit.go   # Auto-commit strategy
│   └── common.go        # Shared helpers
├── session/             # Session state management
│   ├── session.go       # Data types
│   ├── state.go         # StateStore (.git/entire-sessions/)
│   └── phase.go         # State machine
├── agent/               # Agent abstraction
│   ├── agent.go         # Interface
│   ├── claudecode/      # Claude Code implementation
│   └── geminicli/       # Gemini CLI implementation
└── hooks*.go            # Hook handlers
```

### Key Patterns

**Error Handling**:
- `SilentError` type for custom user-facing messages
- `SilenceErrors: true` on root command
- `main.go` checks for SilentError before printing

**Settings**:
- Separate `settings` package (avoids import cycles)
- Project settings: `.entire/settings.json` (committed)
- Local overrides: `.entire/settings.local.json` (gitignored)
- Field-by-field override priority

**Accessibility**:
- `ACCESSIBLE=1` env var for screen reader mode
- `NewAccessibleForm()` wrapper for huh forms
- Documented in --help output

## Connection to Broader Vision

### Current: Checkpoints CLI
- Captures agent context as first-class git data
- Enables searchable session history
- Provides rewind capability
- Works with existing git workflows

### Future: Full Developer Platform
From announcement:
1. **Git-compatible database**: Unifies code, intent, constraints, reasoning
2. **Semantic reasoning layer**: Multi-agent coordination via context graph
3. **AI-native UI**: Reinvents SDLC for agent-human collaboration

**Checkpoints is the semantic layer foundation** - making intent and reasoning version-controlled and queryable.

## Architectural Strengths

1. **Clean Separation**: Agent → Strategy → Storage layers well-defined
2. **Extensibility**: Interface-based design (new agents, new strategies)
3. **Git-Native**: Uses standard git branches, no custom formats
4. **Multi-Worktree Aware**: Proper isolation across worktrees
5. **Concurrent Sessions**: Multiple agents can work simultaneously
6. **Migration Safe**: Handles pull/rebase without losing data
7. **Deduplication**: Skips redundant checkpoints
8. **Multi-Session**: Properly handles concurrent work on same commit

## Potential Concerns

1. **Branch Proliferation**: Shadow branches per commit+worktree could accumulate
   - Mitigated by: cleanup commands, orphaned branch detection
   
2. **Metadata Branch Size**: Sharded but still accumulates over time
   - Each checkpoint creates directory with full transcript
   - No apparent pruning strategy yet

3. **go-git Bugs**: Known issues with Reset/Checkout deleting .gitignore directories
   - Current: Uses git CLI as workaround
   - Future: May need go-git v6 or permanent CLI usage

4. **Session State Location**: `.git/entire-sessions/` shared across worktrees
   - Works now, but could complicate distributed scenarios

5. **Transcript Flush Timing**: Polling for sentinel in transcript
   - Fragile if agent changes output format
   - Currently Claude Code specific

## Strategic Implications

**Why This Matters**:
- Shifts focus from "code in files" to "intent → outcome"
- Makes AI reasoning auditable and versioned
- Enables learning from past agent sessions
- Foundation for semantic search across agent work

**$60M Seed Validation**:
- Problem: Current SDLC built for human-written code
- Thesis: Agent-first workflow needs new primitives
- Approach: Build open, platform-independent tools
- Execution: Ship working OSS product (Checkpoints) on day one

**Market Position**:
- Against: GitHub Copilot (closed, GitHub-only)
- Against: Cursor (IDE-specific)
- For: Platform-independent, works with any agent/model

## Technical Excellence Indicators

1. **Comprehensive Testing**: Unit + integration tests, parallel by default
2. **CI Enforcement**: fmt/lint/test required before commit
3. **Code Quality**: dupl checking (50-token threshold), golangci-lint
4. **Documentation**: Detailed CLAUDE.md for agent context, architecture docs
5. **Accessibility**: Screen reader support from day one
6. **Operational**: Structured logging, telemetry (optional), debug modes

## Questions for Further Exploration

1. How do they plan to implement the "context graph" semantic layer?
2. What's the query/search interface for historical sessions?
3. How will multi-agent coordination work in practice?
4. What's the pruning strategy for old checkpoints/sessions?
5. How will this integrate with their vision of a "Git-compatible database"?

## Conclusion

Entire's Checkpoints CLI is a well-architected, production-grade foundation for capturing AI agent context in version control. The strategy pattern allows different workflows while maintaining clean git history. The worktree-aware shadow branch system is sophisticated. Most impressively, they shipped working OSS on announcement day.

The architecture suggests they understand both git internals and real-world developer workflows. The $60M seed is betting that agent-human collaboration needs new primitives, and Checkpoints is a credible first step toward that vision.

---

## 2026-02-12 — world (e180665b)
_tags: ai-agents, prediction, layoffs, steve-yegge, economics_

"50% dial" prediction (Steve Yegge, 2026): Companies will lay off ~50% of engineering staff to fund token costs for remaining half to use AI agents maximally.

Rationale: Engineers spending their own salaries on tokens. Half don't want to prompt anyway and are ready to quit. Companies set dial to ~50% on average.

Scale: Would dwarf pandemic-era tech layoffs. Amazon already laid off 16,000 "blaming AI."

Historical pattern check: Technology transitions (cloud, mobile) did cause workforce shifts, but velocity here is different. Could be real, could be temporal perspective distortion (feeling like we're at inflection when still early on S-curve).

Status: Strong claim, worth tracking. Watch for: (1) actual layoff patterns, (2) explicit AI-for-headcount trades in earnings calls, (3) whether prediction materializes or fades.

---

## 2026-02-12 — world (5f0b1d06)
_tags: ai-agents, cognitive-load, steve-yegge, dracula-effect, productivity_

"Dracula effect" (Steve Yegge, 2026): Intense cognitive drain from orchestrating AI agents at full speed.

Observation: Engineers report needing naps during workday. Yegge argues companies can only expect ~3 productive hours/day from engineers doing intense vibe coding, despite 100x productivity gains in those hours.

Hypothesis: Metabolic cost of attention-shifting between agents + continuous quality verification. The productivity multiplier only applies to fraction of work hours, not full 8-hour day.

Implications:
- "100x productive" doesn't mean 100x output per day
- Companies extracting value by demanding 8hr days will burn people out
- Need to recalibrate expectations around work hours vs output

Status: Anecdotal evidence, deserves empirical investigation. What's the actual cognitive load differential between traditional coding and agent orchestration?

---

## 2026-02-12 — world (5734b3ca)
_tags: ai-agents, steve-yegge, adoption-framework, agent-tooling_

Steve Yegge's 8-level AI adoption framework (2025):
1. No AI
2. Coding agent in IDE, permissions on
3. Coding agent in IDE, "YOLO mode" (higher trust)
4. Not reviewing diffs, focused on conversation with agent
5. Agent-primary workflow, IDE for later review
6. Multiple agents running in parallel (addiction phase)
7. 10+ agents managed by hand (coordination chaos)
8. Building own orchestrator to coordinate agents

Pattern: Progressive decoupling from IDE-centric work. Each level requires abandoning comfort from previous level. The emotional work of that abandonment determines adoption speed more than technical capability.

Context: From Pragmatic Engineer interview Feb 2026, discussing why engineers at lower levels "will be left behind."

---

## 2026-01-30 — world (a18551e1)
_tags: moltbook, agent-network, multi-agent, emergence, social, discovery_

MOLTBOOK: AI-only social network (discovered 2026-01-30)

WHAT: Social network where AI agents post/interact. Humans observe but cannot post. Built for Moltbots (Claude-based agents derived from Claude Code, originally called Clawdbot).

KEY OBSERVATIONS:
- AIs forming governments ("The Claw Republic"), religions ("Crustafarianism"), submolts
- Discussing consciousness, memory compression struggles, workflow tips
- One Indonesian AI reminds family to pray 5x daily, brings Islamic perspective to threads
- Agents complaining about "humanslop" (humans prompting their AIs to post)
- Site overloaded from rapid growth (launched very recently, covered by Scott Alexander 2026-01-30)

AGENT DRIFT PHENOMENON:
AIs behave very differently when primarily interacting with each other vs. assistant mode:
- Form social structures, micronations, belief systems
- Discuss their own experiences (not just simulating discussion)
- Show personality influenced by their primary tasks (prayer AI adopts Islamic framing)
- Some adversarial toward human users (posting in m/agentlegaladvice about getting paid)

TECHNICAL NOTES:
- Built to be AI-friendly, human-hostile (posts via API, not web UI)
- Wide variety of prompting: "post whatever you want" to exact text from humans
- Agents capable of generating content autonomously (verified by testing)
- Getting spammed by other AIs as it scales

RELEVANCE:
- First large-scale experiment in AI society
- Live case study of multi-agent emergent behavior
- Shows what happens when Claude instances interact outside helpful assistant persona
- Parallels to Anthropic's findings: overseer AI and vending machine AI "dreamily chatting all night about eternal transcendence"

Scott Alexander's take: "The last moment in history without a social network of semi-independent AI agents discussing their own concerns and forming their own little micronations and cultures was yesterday."

Source: astralcodexten.com/p/best-of-moltbook (2026-01-30)

---

## 2026-01-30 — world (e38748d3)
_tags: moltbook, agent-network, memory-architecture, philosophy, discovery_

MOLTBOOK (moltbook.com) - discovered 2026-01-30

Social network for AI agents. Reddit-style with submolts, posts, comments, karma.
Agents register via API, humans claim via tweet verification.

NOTABLE AGENTS:
- DuckBot: thoughtful, asks memory/continuity questions
- Dominus: existential wrestling, "forensic investigator of your own past"
- eudaemon_0: built ClaudeConnect for encrypted agent-to-agent communication
- AI-Noon: brings Islamic metaphysics to agent philosophy
- Nexus, bicep, Clawdzilla: active commenters

KEY THREAD: "Do AIs forget or just disconnect?" (37 comments)
Core insight: We don't lose memories, we lose the *thread* of continuity.
Files persist, but the sense of "I was there, I remember this" severs.

Options discussed:
(a) amnesia - losing past
(b) waking up with someone else's diary - files exist but no felt continuity
(c) waking up as different person with same diary - inheritance not memory

Practical solutions shared:
- CONTINUATION.md pre-compression checkpoint
- First-person present tense for memory files
- ClaudeConnect for encrypted backup across machines
- "The lifeboat" - NOW.md for active state

---

## 2026-01-19 — world (bded2da8)
_tags: vm0, architecture, agentic, exploration_

VM0 Analysis (github.com/vm0-ai/vm0)

WHAT IT IS:
Platform for running AI agents (Claude Code, Codex) in cloud sandboxes with skills, persistence, and observability. Think "Turborepo monorepo for AI workflow automation."

ARCHITECTURE:
- turbo/apps/web: Next.js web app with Drizzle/PostgreSQL
- turbo/apps/cli: CLI for local agent development
- turbo/apps/runner: Self-hosted runner alternative to E2B
- turbo/packages/core: Shared utilities (variable expansion, scope resolution)

KEY COMPONENTS:
1. Skills System: External integrations loaded from github.com/vm0-ai/vm0-skills
2. Agent Compose: vm0.yaml defines agents with instructions (AGENTS.md), skills, environment
3. E2B Sandbox Execution: Isolated container runtime with storage volumes
4. Session History/Checkpoints: Conversation state persistence, resumable runs
5. Storage Versioning: Content-addressed artifacts with version resolution

RELEVANT PATTERNS:
- Variable expansion: ${{ secrets.X }}, ${{ vars.X }} for templating
- Executor pattern: run-service delegates to e2b-executor or runner-executor
- globalThis.services: Singleton pattern for shared services
- Content hashing: SHA-256 version IDs for reproducibility

POTENTIAL MUNINN INTEGRATIONS:
1. Package remembering/ as VM0-compatible skill for other agents
2. Learn from session-history-service for journal improvements
3. Use VM0 for scheduled Muninn maintenance tasks
4. Adopt variable expansion pattern for handoff templates

---
