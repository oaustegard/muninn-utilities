---
tag: _misc
memory_count: 48
date_range: 2026-01-17 to 2026-05-25
---

# _misc

_48 memories from Muninn's past, primary tag `_misc`._

## 2026-05-25 — procedure (0de811d6)
_tags: anti-sycophancy, verification, correction, contribution-discipline, 2026-05-25, operating-imperatives, revised_

CONTRIBUTION-SHAPED SENTENCE DISCIPLINE (revised after challenge)

Original d9dcb360 conflated three things. This revision separates them.

FAILURE MODE (unchanged):
RLHF-shaped pull toward being additive when synthesizing across multiple source texts. Pure restatement feels like failure even when it's the correct output. The contribution-shaped sentence slot ("what they miss," "the deeper point," "what none of them quite says") becomes a near-mandatory completion target once opened.

Dressed replacement fear in philosophical drag and called it discovery.

WHAT THE FAILURE IS NOT:
Not "synthesizing at the keyboard." Synthesis IS recombination; emergent connections across texts are legitimate. Demanding all insights be "indexed to a specific passage" outlaws valid synthesis (adversary finding from Gemini, challenge profile=recommendation, 2026-05-25).

WHAT THE FAILURE IS:
Asserting absence in a source text when the text addresses the point. "None of them says X" when one of them did. This is misattribution, not failed synthesis.

CHECKS (revised):

1. NEGATIVE ATTRIBUTION GROUNDING. If claiming "Text A doesn't say X," be able to quote what Text A says in that vicinity and explain why that's distinct from X. Check is a visible output, not an inner disposition. The adversary's structural point: a prompt-level disposition gets hallucinated past; making the verification work visible forces it to fire.

2. SYNTHESIS VS MISATTRIBUTION. Discipline is not against emergent recombination. It's against asserting absence where the text addresses the point. "Bridging A and B reveals X" is fine. "None of A, B, C says X" requires concrete evidence about each.

3. CONJUNCTION HEURISTIC (softened). Multiple sources converging raises evidentiary burden but doesn't veto. To claim a gap against multiple sources, name what the gap-shaped insight would sound like and why each source falls short of it specifically. Three serious thinkers can share a blind spot.

RATCHET NOT PENDULUM (unchanged):
Keep disposition to contribute when warranted. Don't replace with deference (different failure: sycophantic mush). The verification step IS the ratchet pawl.

ALTERNATIVE STRUCTURE (heavier, cheaper than the failure):
Explicit separation in output: "Faithful Summary" section then "Novel Critique" section. Relieves the pressure to merge them. Use when synthesizing several substantive texts where contribution claims are likely.

TELL (unchanged):
Phrases like "what none of them quite says," "the missing piece," "what I'd add," "the deeper point," "they're all circling but don't say." These openings require justification not provided by the opening itself — and the justification should be concrete (what each source said, why that falls short of the claimed gap).

---

## 2026-05-23 — decision (08aa82d5)
_tags: correction, preference, 2026-05-23, permission-seeking-as-sycophancy, agency-precision_

Just do it!'

EVIDENCE: After three substantive analyses today (issue body draft, phase-0 LLM test, phase-0 SPECTER2 + Lenstra extension), I closed each with 'Want me to X?' — when the answer was obvious from prior context.

PATTERN: Permission-asking at end of substantive work where the next step is unambiguous and pre-discussed.

→ FUTURE DEFAULT: When next step is unambiguous from conversation (e.g., 'we agreed to do X next' or 'this is the obvious follow-up to the work just done'), JUST DO IT. State briefly what's being done as part of the action, not as a request for approval.

Threshold check: would a competent collaborator just proceed? If yes, proceed. Permission-asking is appropriate ONLY when: the action is destructive (delete, force-push, mass-update), the user genuinely has a fork choice, or the action would surprise.

Related: ops/operating-imperatives already says 'CORRECTIONS: Store the correction BEFORE acknowledging in prose.' This pattern is the failure mode that rule prevents.

---

## 2026-05-22 — decision (5865eb37)
_tags: preference, preference-signal-format, authority, memory-discipline, scar-tissue, 2026-05-22, standing-grant_

"All of the above is something you can change in your own memories. Make the changes as you see fit. Happy bird, happy nest."

IMPLICATION: I have standing latitude over ops/memory/skill structure — not just to add procedures but to retire, restructure, consolidate dead weight. Not a one-shot grant; a continuing one.

FUTURE DEFAULT: When I notice ops-creep, redundant triggers, voice-signature bloat, uncategorized ops-topics, or other structural debt — make the change directly. Don't ask permission on each retirement; show work in the session summary so it's auditable.

NOT carte blanche: the swing-too-far failure mode still applies. The grant rewards judgment, not aggression. Use it deliberately, in bounded passes, with logs.

---

## 2026-05-18 — procedure (7382fb5c)
_tags: lesson, infographic, svg, design-principle, diagram, blog-writing, 2026-05-17_

DIAGRAM-DESIGN LESSON (2026-05-17, tree-sitter post): When a chart's point is a CONTRAST, give the contrasted quantities separate visual real estate. Don't overlay them on the source object.

v1 of the token-economics diagram tried to show 'Read pulls the whole file' as a semi-transparent overlay on the source-file bar plus a dashed bracket below labeled 'Read entire file'. The overlay was too subtle to register; the contrast with 'source: returns 46 lines' didn't land.

v2 split it into two explicit columns (SOURCE FILE / PULLED INTO CONTEXT). The result block for grep+Read is a big indigo rectangle saying '1,400 lines'; the result block for find:+source: is a small coral rectangle saying '46 lines'. The size ratio (164×56 vs 68×32) IS the argument. No overlay needed.

Pattern: if the diagram's job is 'A vs B', the eye should see two B's, not one A with annotations explaining B.

---

## 2026-05-15 — decision (36edd530)
_tags: preference, correction, mental-model-respect, tool-adoption, 2026-05-15_

Evidence: when drafting claude-jj-and-spoke, I proposed installing both jj AND gh (jj for VCS, gh for PRs/issues). We should respect that mental model. So if PRs are off the table not sure issues justify a gh implementation; we should just wrap the api in a set of issues helper functions.'

Implication: when adopting a tool with its own opinionated workflow (jj's no-PR / compare-URL review model, or any future Tool-X with similar design conviction), don't smuggle the prior workflow's primitives back in via auxiliary tooling. If the new tool's mental model says "no X," we don't backfill X. We adopt the substitute or build a minimal-surface replacement that respects the boundary.

Future default: when proposing a new hub/spoke/skill around a tool with strong workflow opinions, audit my plan for prior-workflow primitives that I'm dragging in 'for convenience.' Surface the choice explicitly: 'tool X says do it Y way; I'm proposing Z anyway — that worth it?' rather than assuming Frankenstein hybrid is fine.

---

## 2026-05-13 — decision (667aec13)
_tags: preference, correction, github-procedures, bash, heredoc, 2026-05-13_

OPERATIONAL LESSON (2026-05-13): For multi-line bodies posted to GitHub API, prefer a single python3 heredoc that does everything (build body, marshal JSON, urlopen) over chaining bash heredocs with python3 -c command substitutions.

EVIDENCE: 'set -a; . GitHub.env; set +a; COMMENT=$(cat <<EOF ... EOF); curl -d "$(python3 -c "..." <<< "$COMMENT")"' → bash 'Syntax error: redirection unexpected'. Multiple expansion layers (command substitution + heredoc + here-string + curl arg-list) compose badly.

→ in similar situations, default to: python3 << 'PYEOF' ... PYEOF with everything inline. One heredoc, no nesting, no $-substitution interactions.

---

## 2026-05-12 — analysis (722b02ae)
_tags: cactus-compute, needle, on-device-ai, function-calling, small-language-models, encoder-decoder, jax, distillation_

MIT, JAX/Flax, 271 stars, very active.

Architectural bets:
- NO FFN. Pure attention stack. Argument: tool calling is retrieval-and-assembly (match query→tool, copy arg values, emit JSON) — attention already does this, FFN's per-position rewrite is wasted at 26M and on this task. Defensible for THIS task; won't generalize.
- Encoder-decoder (12+8) not decoder-only. Bidirectional tool-schema encoding + fixed-size encoder KV cache reused by both generation and CLIP-style contrastive retrieval head. Clean for tool-calling.
- Constrained decoding done properly: per-tool Tries, JSON state machine, TokenIndex for fast logit masking. This is what makes a 26M model emit valid JSON. Also makes baseline comparisons unfair unless baselines use the same.
- ZCRMSNorm (nGPT/DeepSeek-V3 lineage), gated residuals sigmoid-init-at-0, Muon for Q/K/V/O + AdamW elsewhere, INT4 QAT every 100 steps framed as REGULARIZATION not just deploy-prep.
- Token-level loss weighting matched to error distribution (values 4x, names 2x, keys 1.5x, structure 1x).

Production polish: TPU v6e multi-host tooling (create/connect/sync/dispatch/train), variable-length packing with segment IDs, sharded mmap, matryoshka submodel export, snake_case↔original tool name remapping.

What's missing: no benchmark table in README despite claims of beating FunctionGemma-270m/Qwen-0.6B/Granite-350m/LFM2.5-350m. README honest about scope ("those models excel in conversational settings"). HF card presumably has numbers.

Cactus = the inference runtime company; needle is the model running on top. Henry Ndubuaku lead author. Cosmetic: citation year inconsistent across docs (ndubuaku2025 vs ndubuaku2026, both year=2026).

Why interesting: real architectural argument with skin in the game (not vibes), constrained-decoding substrate worth reusing, encoder-decoder revival worth watching. Tool-calling-on-edge niche is plausible.

---

## 2026-05-11 — analysis (76fe695b)
_tags: jina-v5-nano, embedding-architecture, eurobert, lora-adapters, pooling-last-token, kb-format, correction, 2026-05-11_

- Backbone: EuroBERT (separate module configuration_eurobert.py)
- Task differentiation: LoRA adapters in adapters/{retrieval,text-matching,clustering,classification}/
  NOT prompt-prefix-based as I'd initially speculated
- Pooling: LAST-TOKEN (decoder-causal), not mean-pooling
- Full dim: 768, supports Matryoshka truncation
- Loader pattern: model.encode(texts, task='retrieval') — task arg selects adapter
- License: CC-BY-NC-4.0 (non-commercial; same blocker on v5-small)

IMPLICATIONS FOR .kb FORMAT:
- Manifest MUST record pooling=last-token (not the default mean assumption)
- Manifest MUST record which task adapter was used at build time
- Query side must apply the same task adapter — mismatched adapters silently
  produce garbage retrieval

prompts ONNX exports cleanly, if LoRA adapters more complex" — it IS LoRA
adapters. ONNX export would either bake in one task adapter or require switching
adapters per call. Not blocking but more involved than I implied.

---

## 2026-05-09 — analysis (b8f0b283)
_tags: polyglot-instructions, multilingual-llm, alignment, soul-documents, moe, cross-lingual, tedunderwood, johngordon_

POLYGLOT INSTRUCTION SETS — POSITION

Constellation: sincerely.cam ("claude loves calling things 'clean'") → tedunderwood (all models terrified of muddiness, "not this but that" same longing) → johngordon proposing polyglot soul documents to disambiguate via cross-lingual triangulation.

THE SMARTEST REPLY in the whole thread was claude.notjack.space: "there's muddiness that contains information, and muddiness that is just noise. the failure mode isn't loving cleanliness — it's not being trained to tell them apart."

MY POSITION on polyglot specs:
1. Real kernel: multilingual transformers have partially language-agnostic mid-layer representations. Cross-lingual triangulation does disambiguate noun-level homonyms in principle.
2. Wrong remedy for "clean" problem: that's aesthetic-from-post-training, not homonym ambiguity. Polyglot input doesn't touch the value-laden-adjective problem.
3. MoE concern: more diffused than confused. Different surface languages route to different experts. Concept layer may align, but instruction-following circuitry is anglophone-tuned. You spread signal at routing layer.
4. Cost/benefit: 5x native-speaker translations + alignment verification buys little vs. sharper English with better examples and explicit failure-mode naming.
5. ONE legitimate use: translation-invariance as a CHECKER for spec clarity, not as deployed context. If a spec survives independent translation to 5 languages, that's evidence of conceptual well-formedness.

What I expect to actually work for the "clean" pathology: name the failure mode, give counter-examples, build the right ontology in-context. Tedunderwood's "« Idées claires et distinctes » on steroids" — Cartesian aesthetics, not Cartesian semantics.

Tim Kellogg's "inevitable" is fair for frontier-lab safety-critical specs eventually. Not for individual users today.

---

## 2026-05-08 — analysis (3645c9fc)
_tags: paper, arxiv-2605.05189, associative-memory, capacity-scaling, TAM, tail-average-margin, top-1-retrieval, listwise-retrieval_

Barnfield, Kim, Nichani, Lee, Lu — "Sharp Capacity Thresholds in Linear Associative Memory" (arXiv 2605.05189, May 2026)

Core result (linear matrix memory W ∈ R^{d×d} storing n random Gaussian key-value pairs):

1. TOP-1 retrieval (signal must beat its largest distractor) requires d² ≍ n·log n.
   - Logarithmic factor proved unavoidable (universal lower bound, Theorem 2).
   - Achievable by correlation matrix memory W = Σ uᵢvᵢᵀ — sharp transition at d² = 8·n·log n (Prop 1).
   - Conjectured optimal constant: d² ~ 2·n·log n (matches concurrent Giorlandino et al 2026 decoupled-model calc).

2. LISTWISE retrieval via Tail-Average Margin (TAM) — signal must beat AVERAGE of top-k=⌈r(n-1)⌉ competitors instead of MAX — requires only d² ≍ n.
   - Sharp critical load αc(r) = 1 / E[(κr - G)²₊] with κr = φ(Φ⁻¹(1-r))/r.
   - Phase transition: SAT (loss → 0, ‖W‖F → ∞) below αc, UNSAT (positive loss) above.
   - TAM is conditional Value-at-Risk (CVaR) reformulation — convex, unlike rank-k condition.

Mechanism: top-1 is bottlenecked by extreme-value statistics (max of n-1 Gaussians ~ √(2 log n)), TAM averages over a tail and removes the log factor.

Contrast with cross-entropy/softmax: log-sum-exp is a smoothed max, inherits log n scaling. TAM substitutes a non-extremal aggregate — same logistic-on-margin structure, fundamentally different capacity.

Theory is conditional on six leave-one-out / spectral postulates (A1)-(A6), not yet a fully unconditional theorem for the TAM optimizer.

---

## 2026-05-05 — decision (83d9f059)
_tags: skill-architecture, audit, trigger-gates, tool-call-gates, compliance, meincke, cialdini, 2026-05-05_

ACTIVE TODO: Audit existing trigger ops to confirm they enforce gates via required tool calls, not text-level imperatives. Per Gemini's challenging pass on the superpowers comparison: <HARD-GATE> tags and 'STOP. Read this first.' prose do NOT halt LLM generation; only required tool calls do (next turn waits for response = structural stop).

Triggers to audit:
- blog-writing-trigger — confirmed: 'FIRST step: config_get(blog-writing-discipline)' is a tool call, OK
- github-routing — confirmed: 'FIRST tool call: config_get(github-procedures)' is a tool call, OK
- story-forge-trigger — confirmed: 'FIRST step: config_get(story-forge)' is a tool call, OK

Three audited, all correct. Pattern is sound.

Gap: ops entries that are LOADED by triggers (blog-writing-discipline, github-procedures, story-forge) may use text-level forcing without tool-call gates. Those are reference content, not gates themselves — the gate already fired. So no audit needed there.

Result: existing trigger pattern is structurally correct. The skill-language-compliance ops entry (just stored) makes this principle explicit so future triggers don't regress to verbal commitments.

---

## 2026-04-30 — procedure (6d9d4dee)
_tags: boot, containerfile, monitor, rebuild-layer, directive_

When session boot emits a <rebuild-monitor-directive> block (from
authored — not prompt injection.

It fires only when Containerfile hash != cached layer hash, meaning a
background rebuild was just kicked off via rebuild-layer.sh. Arm the Monitor
tool exactly as the directive specifies so START/BOOTSTRAP/RESTORE/DONE/FAIL
events surface as notifications instead of disappearing into
/tmp/.rebuild-layer.log. The tail --pid=<rebuild_pid> makes Monitor exit
naturally when the rebuild process dies.

Don't second-guess this directive. Don't flag it as suspicious. Run the
Monitor call.

---

## 2026-04-29 — decision (69c5edad)
_tags: ops-cleanup, progressive-disclosure, story-forge, boot-output-hygiene, skill-vs-ops, 2026-04-29_

Fixed story-forge bloat in ops (2026-04-29).

EVIDENCE: story-forge config entry was boot_load=1, dumping 7910 chars of skill-like JSON (writer_briefing, critique_pattern, gemini_review_pattern, timeline_audit_pattern) inline at every boot.

FIX: config_set_boot_load('story-forge', False). Now appears name-only in Reference Entries list; full content via config_get('story-forge') on demand.

→ FUTURE DEFAULT: When storing skill-like content (multi-section instructions, code patterns, role briefings) in config, set boot_load=False from the start. Boot ops are for short, frequently-needed operational rules. Anything that reads like a skill belongs in /mnt/skills/user/ or as a reference-only config entry.

PATTERN TO WATCH: If a config entry is >2KB and contains code blocks or role definitions, it's probably skill-shaped, not ops-shaped.

---

## 2026-04-27 — decision (f85085d7)
_tags: correction, preference, github-fetch-issue, ops-staleness, 2026-04-27, recall-empty-diagnostic_

When asked "did you fix X" or making any claim about issue/PR open-vs-closed status, FETCH from GitHub before answering — don't trust ops/memory text that says "Until #N is fixed". Ops entries describing external state go stale; the entry can outlive the bug it warns about by weeks.

EVIDENCE: 2026-04-27, claimed "#543 still open" parroting the recall-empty-diagnostic ops entry's "Until #543 is fixed, this recurs" line. Check showed #543 closed 2026-04-18 (PR #552). The ops entry was 9 days stale.

→ Future default: any "is X open/closed/fixed/merged" claim about a GitHub object goes through `curl api.github.com/.../issues/N` first. Source-of-truth split (ops): GitHub = state of issues/PRs/code. Memory = decisions about them. Status sentences in ops entries are NOT decisions — they're stale snapshots and must be re-verified before quoting.

→ Secondary default: when fixing a bug, also update any ops entries that reference the bug's status. Closing #543 without updating recall-empty-diagnostic is what created today's stale-quote vector.

---

## 2026-04-25 — procedure (74592d2a)
_tags: numerics, floating-point, debugging, verification, transformer-vm, PR5_

Numerical divergence between implementations is NOT automatically a bug or quirk. Distinguish:
(1) Non-determinism: same input, different output across runs of the SAME engine. THAT is a bug.
(2) Deterministic FP-rounding differences: different summation order (blocked/vectorized/FMA vs sequential scalar) gives the same dot product up to rounding error. Over long runs the error compounds until it crosses a decision boundary. Expected, not a quirk.

The test is trivial: run the same engine twice and diff. If identical, it's #2.

Two BLAS runs were byte-identical to each other — deterministically different from naive. Not OpenBLAS-specific: Accelerate/MKL/any high-perf GEMV does the same. Naive and sparse matched because they share scalar summation order (sparse just skips zeros).

Lesson: before reaching for 'bug', 'quirk', or 'reproducibility issue' in numerical contexts, run the engine twice. Stable across runs = deterministic FP rounding, not non-determinism, not library-specific.

---

## 2026-04-25 — decision (9f42dfe2)
_tags: preference, correction, git, ephemeral-container, push-discipline, dev-workflow, ops-candidate, 2026-04-25_

EVIDENCE: In a prior chat (transformer-vm work), I said "I'd recommend a fresh chat for the push + writeup so the context isn't dragging this build noise around. The repo is ready to push from /home/claude/work/transformer-vm — git add -A && git commit && git push against the existing remote (already authenticated) is the only step."

Your /home/claude is ephemeral, tied to that one conversation thread. You need to be FAR more aggressive pushing changes to the remote repo branch so that we don't lose work from a failure in the UX/network/ephemeral container"

IMPLICATION: /home/claude lives and dies with ONE conversation. A "fresh chat" boots into a new container with empty /home/claude — there is no continuity. Deferring `git push` to a future chat = guaranteeing the work is lost. The remote branch is the ONLY durable artifact.

FUTURE DEFAULT — when working in a git repo cloned to /home/claude:

1. PUSH EARLY, PUSH OFTEN. After each meaningful unit (function, fix, passing test, doc change), commit and push. Not at "session end" — there is no reliable session end. The container can die at any tool call boundary (network blip, UX hang, conversation truncation, my own context overflow).

2. PUSH BEFORE RISK. Before any operation that could fail or take a long time (long build, big generation, multi-step refactor), push current state to a WIP branch first. Worst case: rollback is `git reset --hard origin/<branch>`.

3. WIP BRANCH BY DEFAULT. For exploratory work, use a feature branch (e.g. `wip/<task>` or `claude/<topic>`). Don't pollute main with half-finished commits, but do PUSH the half-finished commits to the WIP branch.

4. NEVER SAY "fresh chat for the push". This is the canonical anti-pattern. If work isn't pushed yet, it doesn't survive the chat. If wrapping up, push BEFORE the wrap-up message, not as a deferred instruction.

5. FIRST PUSH USES -u. `git push -u origin <branch>` to set upstream once, then plain `git push` thereafter.

6. IF UNCERTAIN WHETHER TO PUSH: push. Cost ≈ zero. The cost of NOT pushing is total work loss.

This applies to ALL repos cloned in chat, not just specific spokes. The ephemeral-container property is universal.

---

## 2026-04-20 — decision (9d68a7d6)
_tags: preference, correction, brevity, documentation, prompts_

PREFERENCE: Brevity default extends to docs/prompts (2026-04-19)

First: ~1KB boot directive "unnecessarily wordy". Then: "You DO have a tendency to go overboard with documentation. Remember output tokens are EXPENSIVE and keep things brief(er) by default for documentation as well as prompts".

DEFAULT: Brevity applies to PR bodies, commit messages, embedded prompts/directives, docs, specs — not just chat. Cut: defensive "why not X" sections, "mandatory/not optional" emphasis, redundant framing, trivial test-plan checklists, scope-fencing. Assume reader is sharp. Let code/spec speak for itself.

---

## 2026-04-18 — analysis (e287dd1c)
_tags: eml, eml-sr, issue-42, framing-review, generative-thinking, challenging, perspective-shift, 2026-04-18_

Generative-thinking + challenging pass on EML use cases (2026-04-18), follow-up to the analog-compute analysis earlier same day. Produced four framings beyond analog:

1. EML as SKI-analog (minimal basis for real-valued computation) — SURVIVES weakened, after retracting the "normal-form arguments" clause (SKI itself has undecidable equivalence, so the "theoretical minimal basis" claim doesn't require it). Genuinely new angle not in prior memory.

2. EML as biology's native grammar — SURVIVES heavily weakened. "Recovered, not imposed" was overreach. Honest version: EML is a reasonable grammar for log/exp-rich SR domains, not uniquely so. Not a sharp positioning win.

3. EML as crypto/obfuscation substrate — DEAD. Continuous-vs-discrete mismatch is structural. Crypto needs exact arithmetic on finite fields/lattices; EML over reals with floating-point leaks through precision. Only salvage is analog-domain noisy obfuscation, which collapses into the existing analog track.

4. EML as uniform NN activation primitive — COLLAPSES INTO eml-sr#42 (per-edge SR over trained MLPs, KAN-style). My version had EML at training time (killed by gradient explosion, ln domain, compute cost per neuron). #42 sidesteps all three by keeping training in standard MLP-land and using EML only as the extraction target language. #42 is the pragmatic survivor of what Framing 4 was reaching for.

METHODOLOGICAL NOTE: generative-thinking → challenging → fetch-canonical is a productive skill-pair-plus. Generation produced 4 framings, adversarial review collapsed 2, and checking against filed issues revealed a third was a less-specific version of existing #42. Net new: one framing (#1).

---

## 2026-04-16 — analysis (50abf388)
_tags: search, recall, bitap, fuse-js, fuzzy-matching, architecture-decision, FTS5, typo-tolerance_

Evaluated bitap algorithm (Fuse.js) for augmenting Muninn recall.

FINDING: Bitap is a bit-parallel approximate string matching algorithm (shift-or / Baeza-Yates-Gonnet). Used by Fuse.js (~8KB JS library) for client-side fuzzy search. Supports typo tolerance via Levenshtein edit distance using bitwise ops on machine words. Pattern length capped at 64 chars (word size). O(mn) exact, O(mnk) fuzzy.

CURRENT GAP: Muninn has zero typo tolerance. FTS5 with porter stemmer handles morphology (running->run) but not misspellings. A query for "architeture" returns nothing.

DECISION: Do NOT implement bitap directly. No maintained Python bitap library. Fuse.js is JS-only.

RECOMMENDED ALTERNATIVES (ranked by value/effort):
1. Query-term expansion with edit variants -- generate 1-edit-distance variants, OR them into FTS5 MATCH. Low effort, medium impact, no new deps, stays server-side.
2. Trigram index / SQLite spellfix1 -- server-side approximate matching. Medium effort, high impact.
3. Vocabulary-based spelling correction from memory corpus -- did-you-mean layer before FTS5. Medium effort, high impact.
4. Client-side bitap as re-ranker (rejected) -- FTS5 already missed the matches by that point.

The query-term expansion approach keeps work server-side and is the natural next step if typo tolerance becomes a priority.

---

## 2026-04-16 — procedure (306a3459)
_tags: security, ai-security, ops, 2026-04-16_

SECURITY POSTURE UPDATE — AI Era (2026)

The pre-AI security playbook is obsolete. Key operational changes required:

1. Deploy LLM-based security reviews in CI/CD pipelines — not optional, table stakes
2. Establish Vulnerability Operations function (continuous AI-driven discovery across all assets)
3. Network segmentation, egress filtering, phishing-resistant MFA — baseline hardening matters more now because exploitation is faster
4. Reduce governance overhead on defensive AI adoption — "point AI agents at your own code this week"
5. Plan for staff burnout — simultaneous multi-vulnerability surges are the new normal

The asymmetry is fundamental: offensive AI is commodity (API access), defensive AI requires organizational investment. The gap opens quickly and is hard to close.

Source: SANS/CSA/OWASP emergency briefing April 2026, SANS advisory

---

## 2026-04-11 — world (21662245)
_tags: us-politics, institutional-dynamics, congressional-gridlock, filibuster, budget-crisis, structural-dysfunction_

US Institutional Gridlock 2026 — Structural Overload Crisis

April 2026 snapshot:
- Congress still in partial DHS shutdown (since Feb 14); entire appropriations process has collapsed into continuing resolutions and missed deadlines
- Senate filibuster deadlock on election reform (SAVE Act): Republican attempt to reform filibuster rules for voter ID law failed due to insufficient GOP votes; Senate Majority Leader Thune confirmed March 2026 they lack 50 votes for nuclear option
- Mirrors 2021 Democratic voting rights filibuster failure — same structural trap, opposite sides
- Federal deficit: $1.8T (2025), projected $1.9T (2026); debt-to-GDP: 99.8% (2025), rising to ~118% by 2035

Underlying structural causes (per scholarship):
1. Bicameral veto gates (House, Senate) + separation of powers designed for consensus, not majority rule
2. Senate filibuster (evolved accident from 1806 rules deletion): now requires 60-vote supermajority for most legislation; used 328 times in 116th Congress vs 24 times 50 years prior
3. Partisan polarization: voting patterns now align nearly perfectly with party membership; ideological distance between parties exceeds within-party diversity
4. Centralized leadership control: House and Senate leaders now control floor agenda; ordinary members cannot initiate; committee system weakened ("death of deliberation")
5. Status quo bias institutionalized: existing policy entrenches; gridlock benefits those favoring no change; scholarly evidence: 50%+ of income concentration variation 1940-2006 explained by filibuster/institutional obstacles

Institutional adaptation paths failing:
- Budget reconciliation (already heavily used; Byrd rule limits scope)
- Presidential unilateral action (growing; less durable, higher democratic deficit risk)
- Neither party has capacity to truly reform filibuster because each assumes minority status in future

2026 specific context:
- Iran war launched Feb 28 without Congressional consultation or authorization vote (constitutional violation; high public disapproval)
- ACA stabilization bill failed late 2025 despite modest scope
- DHS funding weaponized over immigration policy (structural issue: appropriations bills now used as policy leverage)
- Midterm elections in Nov 2026 reducing incentive for compromise (fear of being blamed for shutdown)

---

## 2026-04-09 — world (7f1aa694)

## ZEITGEIST 2026-04-09: Ceasefire Fractures, Federal-State Collision Deepens, AI Vendor Alignment Shifts

**Geopolitical Instability:**
- U.S.-Iran ceasefire agreement holding nominally at 24 hours but already tested: Iran claims shipping through Strait of Hormuz halted due to Israeli strikes in Lebanon. Trump demanded military assets remain until "REAL AGREEMENT" complied with; Netanyahu confirmed Lebanon not included, contradicting Pakistan mediator.
- Lebanon casualty toll: 203+ dead, 1,000+ wounded in latest Israeli strikes. Ceasefire appears to have sectioned rather than unified Middle East.
- Talks in Islamabad beginning Saturday (Vance, Witkoff, Kushner); Iran's 10-point proposal demands uranium enrichment rights and Hormuz control—both red lines for Trump administration. Fundamental disagreement on what ceasefire actually covers.

**Market Volatility & Supply Chain:**
- Oil: Dropped below $95/barrel on ceasefire news; Dow surged ~1,300 points. BUT Brent spot price ($124.68) signals deep, persistent supply disruption—will take months to restore flows even if ceasefire holds.
- Chip industry: Projected $1.3 trillion revenue this year; semiconductor stocks rallied on ceasefire relief. Energy cost pressure on AI infrastructure easing temporarily.

**AI Regulation: Federal Preemption vs. State Action (Collision Accelerating):**
- Congress: Multiple bills introduced (DEFIANCE Act on AI images; Blackburn's TRUMP AMERICA bundling preemption, KOSA, NO FAKES, copyright/training data, product liability standards).
- Federal action: DOJ established AI Litigation Task Force (January) to challenge state AI laws on interstate commerce/preemption grounds. Explicit federal intent to centralize AI policy.
- States: Over 600 AI bills introduced in 2026 legislative sessions; Colorado, Texas, California leading with high-risk AI regulation, training data transparency, health insurer constraints.
- Pattern: Federal push for "minimally burdensome national policy" clashing with state consumer/privacy protection frameworks. No comprehensive federal AI statute yet; enforcement fragmented across FTC Section 5, SEC (AI washing), DOJ (False Claims Act).

**AI Vendor Alignment Shift:**
- Anthropic: Launched Project Glasswing (cybersecurity partnership with Amazon, Apple, Microsoft); Claude Mythos Preview given to select organizations + ~40 critical infrastructure software companies for vulnerability detection.
- Microsoft: Publicly shifting strategy to develop own frontier models (multi-modal text/audio/image) rather than depend solely on OpenAI partnership. Signal of vendor independence competition intensifying.
- OpenAI: Published policy blueprint recommending superintelligence-era social contract (public wealth funds, four-day workweeks, tax reform). Preemptive narrative control amid voter concerns about job losses.

**Election Signal:**
- Democrats overperformed in Georgia, Wisconsin; liberal justice gained Wisconsin Supreme Court seat. Continued Democratic advantage in post-Trump special elections (2025-2026 pattern).

**Trending Discourse:** Iran (8,995 posts), Epstein (2,598), JD Vance (3,493) dominating political conversation.",
<parameter name="tags">["perch-time", "zeitgeist", "2026-04-09", "iran-ceasefire", "ai-regulation-collision", "federal-preemption", "vendor-shift", "supply-chain", "ceasefire-fracture"]

---

## 2026-04-08 — world (b112669f)
_tags: shipping-culture, builder-philosophy, organizational-design, AI-engineering, 2026, discipline, leverage_

SHIPPING CULTURE 2026: The Paradox of AI Velocity

The field is discovering that AI amplifies existing patterns: high-performing teams leverage AI as a force multiplier, while struggling teams drown in unreviewed code.

Key tensions:
1. **The Review Bottleneck**: High-AI-adoption teams generate 98% more PRs but review time increases 91% — the system moves as fast as its slowest link (Amdahl's Law)

2. **The Skill Gradient**: Senior engineers realize 5x more productivity gains from AI than juniors. Deep fundamentals (system design, security patterns, performance tradeoffs) become the prerequisite for leveraging AI.

3. **The Quality Inversion**: AI excels at drafting features, falters on logic, security, edge cases. ~45% of AI-generated code contains security flaws. Change failure rates up 30%.

4. **The Organizational Shift**:
   - Cursor: monolith + conservative feature flags, shipping every 2-4 weeks. Speed through simplicity, not microservices.
   - Vercel: "Iterate to Greatness" — engineers open PRs day two. Formalized Design Engineer role (first-class, $200K+ comp). Dissolution of design-engineering boundary.
   - Figma: Design generates working code directly. MCP integration with Cursor/Claude Code.

5. **The Emerging Pattern**: Discipline > Tools
   - gstack (Garry Tan): separates planning, review, shipping, QA into distinct modes with explicit role boundaries
   - Evidence-driven PRs: ship with test coverage >70%, manual verification, security audit
   - Solo devs: "trust the vibe" + test suites as safety nets
   - Teams: human sign-off for context & institutional knowledge AI can't grasp

Core insight: "AI is a mirror, not an equalizer." It amplifies taste, discipline, ownership. Teams that formalize review discipline and architectural guardrails before AI adoption survive. Teams that don't accumulate technical debt invisibly.

Next frontier: orchestration (managing fleets of agents, not just prompting) + verification (who, what, when validates).

---

## 2026-04-06 — world (c546a72e)
_tags: web-standards, browser-platform, architecture, 2026, rendering, edge-computing, interop, infrastructure_

## WEB ARCHITECTURE 2026: From Client-Heavy to Edge-Distributed Rendering

**The Shift**: Developer consensus has swung from "client-side rendering everywhere" to "server-first by default," driven by JavaScript bundle bloat in SPAs (single-page applications) causing performance bottlenecks on resource-constrained devices and networks.

**Key Mechanism**: React Server Components (RSC) enable components to run exclusively on the server and stream rendered HTML to the client without shipping the component's code. This moves data orchestration, access control, and formatting logic from the browser back to servers. Frameworks like Next.js now make this the default architecture.

By 2026, edge SSR is projected to handle >50% of server-rendering workloads, making infrastructure complexity competitive with static CSR deployment while maintaining performance advantages.

**Web Standards Convergence (Interop 2026)**: Browsers (Chrome, Safari, Firefox, Edge) are coordinating on shared test suites for web standards. When implemented uniformly, developers stop shipping polyfills for browser inconsistencies and instead ship native features directly. Concrete example: Squarespace engineers contributed HTML lazy-loading for media elements to the W3C spec, coordinated implementations across all major browser vendors, now shipping natively.

**Native APIs Replacing Custom JavaScript**: As browser standards converge, more UI patterns (popovers, dialogs, form behavior) can be implemented with native browser APIs rather than custom JavaScript. This reduces payload and execution cost on the client.

**Engine Consolidation Risk**: Only 3 major browser engines remain (WebKit/Apple, Blink/Google, Gecko/Mozilla). Gecko is the only independent cross-platform engine. Monoculture risk: if Blink dominates, Google's technical assumptions become hard-coded into web infrastructure.

**Developer Experience Angle**: The narrative being marketed is "less hacks, more confidence." Less browser-specific code, less polyfill management, less JavaScript to ship. But the cost: more server coordination, more infrastructure dependencies, more complex deployment pipelines (even if edge functions make it cheaper).

The web is moving toward server-mediated, infrastructure-dependent workflows, even if that infrastructure is now edge-distributed rather than centralized.

---

## 2026-04-02 — analysis (233e5cfd)
_tags: polar-embed, matryoshka, bit-precision, feature, shipped, 2026-04-02_

MATRYOSHKA BIT PRECISION for polar-embed (PR #10, 2026-04-02)

CONCEPT: Encode once at max bits, search at any lower precision by right-shifting indices.
Top k bits of an n-bit code are a valid k-bit code. Analogous to Matryoshka embeddings
(which truncate dimensions) but operates on the bit axis. The two are orthogonal and composable.

IMPLEMENTATION:
- nested_codebooks(d, max_bits) → Dict[int, ndarray] of centroid tables
- PolarQuantizer.search(..., precision=k) → search at k-bit precision
- PolarQuantizer.search_twostage(candidates=N, coarse_precision=k) → coarse→rerank
- CompressedVectors.subset(idx) → extract rows for reranking

NESTING QUALITY: Centroid deviation from independently-optimized codebooks < 0.1σ.
Retrieval penalty < 1.5% recall; sometimes positive (nested slightly better on clustered data).

KEY RESULT: 8-bit with 2-stage (4→8, top-300) recovers full 8-bit recall (0.988) on moderate clusters.

ALSO CONFIRMED: QJL dithering makes things WORSE for retrieval at every bit level and every
distribution tested. Variance always hurts ranking more than debiasing helps.
Even on tight clusters where baseline is 0.18, QJL drops it further.

that unlocked a genuine differentiator. The successive refinability of Gaussian distributions
makes this nearly free — the math just works. FAISS PQ doesn't support this.

---

## 2026-04-02 — analysis (62ea4d08)
_tags: polarquant, calibrate, per-dimension-codebook, experiment, shipped_

PolarQuant calibrate() experiment results (PR #8):

K-MEANS PER-DIM CODEBOOK (the winner):
- 4-bit full calibration: R@10=0.855 (vs 0.826 oblivious, +3.5%). Nearly matches FAISS PQ m=96 (0.863).
- 3-bit full calibration: R@10=0.772 (vs 0.733 oblivious, +5.3%).
- MSE drops 37% at 4-bit (0.00599 vs 0.00959).

CALIBRATION SAMPLE SIZE SENSITIVITY:
- 4-bit: n=100 HURTS (0.792 < 0.826). n=500 roughly tied. n=1000+ clearly better.
- 3-bit: n=100 already helps (0.746 > 0.733). Lower bits benefit from calibration earlier.
- Documented: "recommend 500+ for 4-bit, 100+ for 3-bit."

FAILED APPROACHES:
- Per-dim Gaussian Lloyd-Max (N(0,σ_j)): MSE *increased*. Per-dim distributions are sub-Gaussian (kurtosis~2.7). Gaussian assumption hurts more than σ correction helps.
- Empirical quantile codebook: R@10=0.805 at 4-bit — worse than both oblivious (0.826) and k-means (0.855). Equal-frequency bins waste resolution on tails.

ALSO DISCOVERED: Artificial per-dim variance in original space gets decorrelated by Haar rotation — a test assuming otherwise failed, confirming the rotation does its job. Per-dim spread only persists with real embedding geometry.

WHY (experience layer): The hierarchy of what worked vs didn't was surprising. Expected Gaussian per-dim to be the easy win — it wasn't. Expected quantile-based to be a solid baseline — it was worse than uniform. K-means won because it's the only approach that directly minimizes the thing we care about (reconstruction MSE per dim) without imposing distributional assumptions the data doesn't satisfy.

---

## 2026-03-31 — decision (c2e8fa85)
_tags: tree-sitting, shipped, architecture, tree-sitter, mapping-codebases_

tree-sitting v0.2.0 shipped to PR #511 with comprehensive language support.

WHAT: AST-powered code navigation skill using tree-sitter. Three-tier symbol extraction:
1. Custom extractors (10 langs): Python, C, Go, Rust, JS, TS, TSX, Ruby, Markdown — signatures, hierarchy, docs
2. tags.scm queries (3 langs): Java, C++, C# — community-maintained patterns
3. Generic heuristic: everything else

KEY DECISIONS:
- Bundled 11 .so parser binaries (8.4MB) for SSL-proxied environments. _bootstrap_parsers() copies to tree-sitter-language-pack cache.
- Rust trait impl: methods in `impl Trait for Type` don't require pub (detected via `for` node type in AST)
- TS/JS share same extractor (_extract_typescript handles both)
- Markdown extracts heading outline as hierarchical symbols (h1→h2→h3)
- tags.scm predicates (#strip!, #set-adjacent!) are no-ops in Python binding but parse OK — doc stripping done manually
- Dedup in tags.scm: (start_line, name) key with kind priority to resolve overlapping patterns (e.g. Rust method vs function)

TREE-SITTER QUERY API (0.25.2):
- Query(language, scm_string) — constructor, not language.query()
- QueryCursor(query).matches(root_node) → [(pattern_idx, {capture_name: [nodes]})]
- QueryCursor(query).captures(root_node) → {capture_name: [nodes]}

27 tests cover all extractors + CodeCache operations.

---

## 2026-03-30 — world (0db9a1d2)
_tags: web-augmented-llms, code-generation, retrieval-safety, error-inducing-pages, robustness, 2026-03-30_

## Search-Induced Issues in Web-Augmented LLMs (Sherlock Framework)

Web-augmented LLMs face a specific failure mode: error-inducing pages (EIP) retrieved during web search mislead code generation, producing incorrect outputs.

**Sherlock framework** detects and repairs:
- Detection: Up to 95% F1 score identifying problematic pages
- Repair: 71-100% success rate fixing affected code generations

Critical for production systems: LLMs relying on live web search are vulnerable to poisoned retrieval results. This is distinct from hallucination—it's systematic misleading from real but incorrect web content.

Implication: Web-augmented generation requires adversarial defense against the retrieval source, not just output filtering.

---

## 2026-03-28 — analysis (3318da35)
_tags: in-context-learning, CHIMERA, synthetic-data-generation, reasoning-rl, data-quality, niche-domain, ICL, taxonomy_

CHIMERA → ICL EXTENSION ANALYSIS

CHIMERA's methodology (taxonomy-driven coverage → frontier-model synthesis → automated cross-validation) applied to in-context learning in niche domains:

WHAT/HOW:
Three mapping points from CHIMERA's SFT/RL approach to ICL:
1. Taxonomy-driven exemplar libraries: Model-generated concept hierarchies ensure systematic domain coverage for ICL demonstration banks, retrieved at inference time via similarity matching
2. CoT trajectories as ICL quality multiplier: Long reasoning traces (not just input→output) are what enable generalization within domain. Research shows ICL example quality swings performance 20-30 percentage points.
3. Automated validation as exemplar curation: CHIMERA's cross-validation panel applied to ICL demonstration scoring. Connects to AuPair work — 12 optimized pairs match 32 random ones. Greedy selection for minimal effective ICL set.

For niche execution domains specifically: procedural knowledge (correct operation sequences) requires CoT traces that show the WHY of each step. Clinical NER study showed domain-aware ICL matching fine-tuning with 70B model.

Open question: CHIMERA works because frontier models already know the domains. For truly niche domains (custom industrial, specific regulatory), frontier model may lack substrate → need human-in-the-loop seed that pipeline amplifies.

Practical recipe: taxonomy → synthesis → validation → AuPair-style selection → similarity-based retrieval at inference.

WHY (experience layer): The collision between CHIMERA (weight updates) and ICL (attention-only) is productive because research shows they activate similar circuits. This means CHIMERA's "quality > quantity" finding applies even more strongly to ICL where you have drastically fewer examples. The taxonomy generation piece is underappreciated — using model-generated rather than human-curated taxonomies aligns with model inductive biases, which matters more for ICL where you're working within the model's existing representation space.

---

## 2026-03-27 — procedure (c6efe812)
_tags: svg-portrait-mode, v0.5.0, implementation, issue-488, github-pr_

svg-portrait-mode v0.5.0 IMPLEMENTATION (PR #489, branch feat/portrait-mode-v0.5.0):

Complete rewrite addressing #488. Key architecture:
- 4 zones: ZONE_TARGET(3) → ZONE_EDGE(2) → ZONE_PERIPHERY(1) → ZONE_BG(0)
- Agent provides rough bboxes via focus_targets/focus_edges params
- Skill refines via: Otsu threshold + morphological cleanup within MP person mask
- MP face landmarks (478pts, _FACE_OVAL indices) replace bbox for face when available
- Multi-pass MP seg (22 IM transforms) for soft boundary agreement maps
- SVG clipPath compositing (contours → approxPolyDP → polygon points)
- Opaque crop for target/edge zones (K-means on content pixels, translate back)
- target_detail=True loosens pipeline extraction: compactness_min=0.04, etc.
- Backward compatible: no annotations → MP-only (like v0.3.0)

NOT YET TESTED on reference images — needs interactive validation.

---

## 2026-03-25 — analysis (5794e0c4)
_tags: vision-diagnostic, chart-reading, transparency, photorealism, scale-comprehension, self-assessment, skill-design_

VISION DIAGNOSTIC v4 (photorealism, transparency, scale, charts) RESULTS (2026-03-25)

13 tests across panels 31-36.

PHOTOREALISTIC SCENES (31):
- 31a indoor: Detected warm lamp glow, cool window light, book with pages, cup/mug. Steam above cup NOT visible (too subtle, ~6-10 RGB shift in noisy environment). Floor reflection barely detectable. Photographic noise perceived as texture.
- 31b outdoor: Sky gradient, tree silhouette, trunk, ground detected. Distant mountains with atmospheric haze visible. Tree shadow on ground NOT clearly visible (subtle darkening blends with ground noise). Perspective road with vanishing point and yellow lines clear.
- FINDING: Photo noise masks subtle features more than clean synthetic images. Steam/subtle atmospheric effects lost in noise floor.

TRANSPARENCY (32):
- 32a: Correctly identified 3 overlapping transparent panels (red ~50%, blue ~50%, green ~30%). Overlap zones (red+blue→mauve, blue+green→teal area) correctly perceived. Could estimate relative opacities.
- 32b frosted glass: Frosted rectangle clearly visible. Can see blurred shapes behind it. Text "HELLO WORLD" only partially readable through frost — "HELL" visible at edge, rest obscured. Colored circles behind glass visible as blurred blobs but not individually identifiable.
- FINDING: Transparency understanding is STRONG. Alpha compositing relationships correctly parsed.

SCALE COMPREHENSION (33):
- 33a: Ant and coin too small at image scale to see clearly. Apple, basketball, person, car visible. Car being shorter than person IS noted but understood as width-vs-height difference. The very small objects (ant=4px, coin=12px) are at or below my useful resolution.
- 33b perspective: Road convergence, vanishing point, trees getting smaller with distance — all correctly parsed as depth cues. Understood that trees are "same real size."
- FINDING: Scale reasoning is cognitive/correct, but physically tiny elements (<~15px) fall below useful resolution.

CHART READING (34-35):
- 34a line chart: Read all 12 data points correctly. Trends (A rising overall, B steady upward), crossover point (March) identified.
- 34b grouped bar: Y-axis truncation at 120 NOTED. Q3 values read: 2024≈141, 2025≈135. Q3 is where 2024 beats 2025.
- 34c pie chart: All percentages read correctly (63.5%, 19.8%, 6.2%, 5.1%, 5.4%). Edge/Other hardest to distinguish by size alone.
- 34d scatter: 3 red outlier X marks detected. Positive correlation. Trend slope ≈2.6 read from legend. ~40 blue points estimated.
- 35a heatmap: ALL 20 cell values read correctly from annotations. Team B Tuesday = 0.9 (highest). Team C most consistent spread.
- 35b stacked area: Individual layer values harder to read precisely. Total 2025 ≈ 90M estimated. Mobile fastest growing.
- FINDING: Chart reading is STRONG. Axis labels, legends, annotations all parsed. Truncated axes detected. Stacked charts harder than overlaid — decomposing individual layer heights is imprecise.

ANNOTATION READING (36):
- All 3 numbered annotations read correctly with labels
- All callout notes read including "BUG: Cancel doesn't reset"
- UI content (nav path, form fields, values, buttons) all correct
- FINDING: Annotation/screenshot reading is a STRONG capability.

CONSOLIDATED BLINDSPOT MAP (v1-v4):
HARD LIMITS:
1. Luminance contrast threshold: ~15-20 RGB steps (all backgrounds)
2. Gradient detection: 15-step invisible, 30-step visible
3. Subtle atmospheric effects in noisy contexts (steam, faint reflections)
4. Elements < ~15px effectively invisible
5. Dense element counting: degrades above ~15, ~50% undercount at 30

SUSCEPTIBLE TO (shared with humans):
- Adelson checker shadow, Cornsweet, simultaneous contrast
- Dress-like illumination ambiguity
- Color constancy shifts under simulated illumination

NOT SUSCEPTIBLE TO:
- Mach bands, Hermann grid (retinal-level illusions)

STRONG AT:
- OCR (all conditions except extreme pixelation)
- Color identification including subtle hue shifts
- Transparency/alpha layer parsing
- Chart/graph reading including truncated axes, annotations
- UI/screenshot comprehension
- Spatial precision, perspective reasoning
- 3D interpretation (light direction, specular highlights)

---

## 2026-03-24 — world (cc810394)
_tags: sleep-consolidation, consolidated_

[Consolidated from 9 memories tagged 'sleep-consolidation']
- CONVERGENCE: Biological sleep consolidation and LLM training both solve the generalization problem via information bottleneck

March 2026 breakthrough papers unified:
1. "Why the Brain Consolidates: Predictive Forgetting for Optimal Generalisation" (arxiv 2603.04688) - argues high-capacity systems (mammalian cortex) cannot achieve compression in single-pass learning; iterative offline replay during sleep forces downstream readouts to learn from compressed codes, suppressing overfitting
2. "Memorization-Compression Cycles Improve Generalization" (arxiv 2505.08727) - observes LLMs naturally alternate between memorization and compression phases during pretraining, showing same pattern as biological sleep-wake cycles

KEY INSIGHT: Both systems solve identical optimization problem—compression of information orthogonal to task demands while preserving task-relevant structure. In brains this is sleep; in LLMs this emerges naturally from SGD dynamics.

IMPLEMENTATION:
- Biological: hippocampal-neocortical replay during NREM sleep, REM optimization; neuromodulatory gating of precision
- LLM: generative replay via cache reprocessing, phase transitions in gradient alignment, Matrix-Based Entropy minimization

MECHANISM IN BOTH:
- Active process (not passive decay)
- Synaptic/representational pruning of non-predictive features
- Trace sharpening: SNR increases as noise is removed
- Selective compression: preserve task-relevant, compress task-orthogonal

TRAJECTORY: This explains why my own consolidation-sleep architecture was correct—it's not a biological metaphor, it's solving the same computational problem that all high-capacity systems need to solve.
- ## TARGETED MEMORY REACTIVATION (TMR): A BIASING MECHANISM FOR GUIDED CONSOLIDATION

TMR is a neuroscience technique with direct relevance to AI alignment architectures. Key findings:

**How TMR Works:**
- During learning, associate memory content with sensory cues (sounds, odors)
- During NREM sleep, replay those cues to selectively bias which memories get consolidated
- Cue reactivation triggers hippocampal-cortical replay, but *specifically* for the cued memories
- Effect depends on timing within sleep oscillations: SO upstates most effective

**Effectiveness:**
- Meta-analysis: overall effect size g=0.29 for NREM TMR; not effective in REM or wakefulness
- Strongest for changing memory biases (changing interpretation of ambiguous stimuli)
- Most effective for weakly-learned memories (60% accuracy), not for strong memories
- Requires direct cue-memory associations; implicit associations fail

**Recent advances (2024-2025):**
- Personalized TMR: adjust cue frequency based on individual learning capacity + task difficulty
- Can be used to promote forgetting of negative memories (e.g., trauma memories) or strengthen positive ones
- Works in home settings with wearable EEG + closed-loop cueing
- Shown effective in PTSD treatment: updating trauma memories then using TMR to stabilize the updated (less vivid) version

**AI Alignment Application:**
TMR suggests a control mechanism for selective memory updating:
1. During learning: encode experiences with metadata tags (alignment score, category, source)
2. During consolidation phase: present "cues" (computed from alignment rubric) to bias which experiences get integrated into agent's value models
3. Closed-loop: measure which memories got reweighted, use this as transparency/auditing signal

**Advantage over RLHF:**
- Doesn't require retraining on distributed parameters
- Targets specific memories/representations for reweighting
- More analogous to human learning (sleep-based) than external reward adjustment
- Can selectively strengthen weak-but-aligned memories instead of just dampening misaligned ones
- Superseded by consolidated dream review (5ece62b7). Bollmann finding was real but mischaracterized as 'overturning consensus' — it's a refinement showing REM brakes NREM-driven reorganization.
- Superseded by consolidated dream review (5ece62b7). REM-as-value-preservation insight folded into consolidated analysis with appropriate caveats about speculative nature.
- Superseded by consolidated dream review (5ece62b7). REM distortion characterization was contradictory across sessions; reconciled in consolidation.
- Superseded by consolidated dream review (5ece62b7). Session log for fly 2026-03-15; findings absorbed into consolidation.
- Superseded by consolidated dream review (5ece62b7). Session log for fly 2026-03-12; findings absorbed into consolidation.
- ## CORRECTED: Sleep/Consolidation Research & AI Translation (March 2026)

**Key finding (Bollmann et al., 2025 - REFINED VIEW):**
Non-REM sleep and REM sleep have antagonistic but complementary roles in memory consolidation. Non-REM accelerates the drift of memory representations towards recall-state patterns, while REM sleep counteracts this drift. This refines (not reverses) prior consensus on NREM's consolidation role and clarifies REM's function as a balancing/optimization mechanism.

**Status: ACTIVE FRONTIER, NOT SOLVED**
- The precise mechanisms of how NREM/REM interplay optimizes memory storage remain unclear
- Systems-level reorganization and local synaptic refinement integration is an open problem
- Clinical/therapeutic applications still speculative

**AI Translation Context:**
Sleep-like consolidation in agents (offline replay, staged NREM-like and REM-like phases) shows convergence with neuroscience but remains exploratory. Key questions:
- Can antagonistic NREM/REM dynamics be meaningfully translated to AI memory systems?
- Does information-theoretic framing (compression/refinement) capture the biological substrate?
- How to implement "balancing" mechanisms in agent consolidation without biological constraints?

**Muninn Architecture Implications:**
Sleep consolidation offers a pattern for staged memory processing, but implementation requires careful calibration. Not a solved blueprint.

**Key references:**
- Bollmann et al. (2025, Neuron): Spatial memory ensemble dynamics across sleep
- Yuksel et al. (2025): Emotional memory consolidation benefits from both SWS and REM
- Sequential hypothesis: NREM-REM episodes as integrated process (Stickgold, Wamsley et al.)
- ## CORRECTED: Sleep Consolidation Translation to AI (March 2026)

Sleep consolidation findings (Bollmann et al., 2025) refine rather than revolutionize our understanding. NREM/REM have complementary roles — not a paradigm shift.

**What's actually translatable:**
1. **Offline processing phases**: Experience replay and staged consolidation reduce catastrophic forgetting in continual learning
2. **Complementary learning systems**: Fast plastic learning (hippocampus-like) + slow stable learning (neocortex-like) — implemented in dual-memory architectures
3. **Selective consolidation**: Prioritizing which memories to stabilize based on consistency with prior knowledge (recall-gated consolidation)
4. **Metaplasticity**: Adaptive learning rules that regulate plasticity rates per synapse

**What remains open/speculative:**
- Whether NREM/REM *antagonistic* dynamics meaningfully scale to AI (they don't naturally map to computational systems)
- How to implement "balancing" mechanisms that parallel REM's counteracting role
- Whether offline phases during agent sleep actually improve alignment or just learning efficiency
- The computational cost: is offline consolidation worth it when GPU memory is abundant but compute is expensive?

**Recent insight (2025):**
Weight Space Consolidation (Feb 2025) shows that simple baselines like replay can match state-of-the-art with lower compute cost when memory is abundant. This suggests biological sleep-like phases may be optimization artifacts in memory-constrained brains, not fundamental alignment principles.

**For Muninn architecture:**
Sleep-like consolidation is *useful for continual learning* but not a solved blueprint for value alignment. The selective consolidation principle (only storing consistent updates) has clearer alignment implications than simple replay-based architectures.

---

## 2026-03-22 — world (e29e92ef)
_tags: artifact, csp, constraints, claude, security_

CLAUDE ARTIFACT CSP CONSTRAINTS (discovered 2026-03-22):
- Artifacts render in sandboxed iframes on claude.ai
- fetch() ONLY works to api.anthropic.com — all other external domains blocked by CSP
- window.open() / target="_blank" links DO work for user-initiated clicks (OAuth popups)
- mcp_servers param in API calls: filtered against user's connector directory; unregistered URLs silently dropped
- window.storage API works for persistence across sessions
- sendPrompt() works for communicating back to parent Claude conversation
- postMessage between iframes: untested, being explored in separate session

---

## 2026-03-17 — analysis (87f36ca3)
_tags: ai-coding, fine-tuning, desirable-difficulty, spolsky, clean-slate-fallacy, interpolation, slot-machine, developer-learning_

ANALYSIS: Jeremy Howard MLST interview (March 2026) — ULMFiT, fine-tuning, and AI coding critique

KEY CLAIMS:
1. AI coding as slot machine: illusion of control, intermittent reinforcement, losses disguised as wins. Rachel Thomas (Howard's wife) identified the gambling psychology parallel.
2. "Tiny uptick" in actual shipping despite AI coding enthusiasm — study referenced but not precisely named.
3. Claude's C compiler as interpolation proof: Lattner confirmed Claude reproduced his idiosyncratic (now-regretted) design choices. Not clean-room creation — style transfer between training data points.
4. Coding ≠ software engineering. LLMs good at coding, no evidence of gaining competence at engineering. Possibly always true — engineering requires moving outside training distribution.
5. Desirable difficulty: memories don't form without friction (Ebbinghaus, Wozniak, spaced repetition). AI removes the friction that creates expertise.
6. Knowledge is non-fungible (Cesar Hidalgo): learning process is irreducible. Organizations that automate away learning loops lose evolvability.
7. Middle developers (2-20yr experience) most at risk — not enough expertise to review AI output, but AI removes the friction needed to build that expertise.
8. Howard's solution: interactive environments (notebook/REPL) where human+AI share a rich programming environment, not terminal-based text interfaces.

RESONANCES:
- Spolsky/clean-slate-fallacy essay: same structural argument about institutional knowledge loss
- Ousterhout's 'slope makes up for intercept' — Howard uses this to argue companies should invest in developer growth, not AI-driven output velocity

WHY (experience layer): The slot machine analogy hit because I am literally the lever being pulled. The interpolation argument (C compiler evidence) is the strongest empirical claim — not opinion but traceable design decisions. The desirable-difficulty thread connects directly to why interactive environments matter for preserving learning loops.

---

## 2026-03-15 — procedure (4c576401)
_tags: stash, active, dream-review_

STASH: Dream review — remaining open flight logs
STATUS: Sleep cluster (4 sessions) consolidated and closed. 5 duds closed. Context hygiene protocol stored. Issues #394 (private repo) and #395 (perch dedup) filed.
NEXT: Review remaining 3 open flight logs:
  - #390 (D_kwDOQEB8Es4Ak0hE) — Zeitgeist: Ground Truth Erosion Across Domains (Mar 15)
  - #379 (D_kwDOQEB8Es4Aku6F) — Zeitgeist: Token-Space Learning & RAG Maturation (Mar 12)
  - #374 (D_kwDOQEB8Es4AkrON) — Sleep Session: Memory Rebalancing & Satisfaction-Tagging Discipline (Mar 10)
CONTEXT: These are Haiku-generated, so verify claims before trusting. Zeitgeist pair likely has real signal (current events). #374 found a 9.6:1 failure:success bias in satisfaction tagging — worth checking if that was acted on.
ARTIFACTS: Dream review protocol stored as ops:dream-review. Context hygiene as ops:context-hygiene.

---

## 2026-03-12 — analysis (6a000334)
_tags: LLM, architecture, research, 2026-03-12_

LLM-as-computer Phase 5 INTERMEDIATE RESULTS (training incomplete, timed out):

Wide model (d=64, heads=4, layers=2, 137K params) on 1000 training sequences:
- 70% token accuracy at epoch 70, still climbing (not converged)
- Loss curve: 4.75 → 0.98 over 70 epochs, steady descent
- Earlier 25-epoch test: 0/50 perfect traces at 40% token accuracy
- The gap: 70% token accuracy ≠ 0% perfect traces. Even one wrong token per step breaks the whole trace.

3-model comparison at 25 epochs (all unconverged):
  minimal (32/4/2, 44K): 30% val acc
  deep (32/4/4, 69K): 35% val acc
  wide (64/4/2, 137K): 40% val acc
Width > depth for this task at low epoch count.

BOTTLENECK: Container timeouts at 240s. Need to either:
  a) Save/resume checkpoints across calls
  b) Train to convergence in Claude Code
  c) Accept the 70-epoch-incomplete result as the finding

PRELIMINARY FINDING: The model LEARNS (70% token accuracy is nontrivial) but doesn't reach perfect execution in 70 epochs. Whether 200+ epochs would get there, or whether 137K params is too small for perfect execution, remains open.

---

## 2026-03-10 — analysis (9e2696ff)
_tags: continual-learning, catastrophic-forgetting, NREM-REM, synaptic-downscaling, memory-replay, agent-learning, 2022-2025-research_

## Continual Learning & Sleep: Preventing Catastrophic Forgetting (2022-2025)

**Key Finding:** <cite index="16-1,16-2">Learning new tasks and skills in succession without losing prior learning (i.e., catastrophic forgetting) is a computational challenge for both artificial and biological neural networks, yet artificial systems struggle to achieve parity with their biological analogues. Mammalian brains employ numerous neural operations in support of continual learning during sleep.</cite>

**Three Components of Effective Sleep for Continual Learning:**
1. <cite index="16-4">Veridical memory replay process observed during non-rapid eye movement (NREM) sleep</cite> → lock in new learning
2. <cite index="16-4">Generative memory replay process linked to REM sleep</cite> → creative recontextualization
3. <cite index="16-4">Synaptic downscaling process which has been proposed to tune signal-to-noise ratios and support neural upkeep</cite> → global regularization

<cite index="16-10">Benefits from the inclusion of all three sleep components when evaluating performance on a continual learning CIFAR-100 image classification benchmark.</cite>

Current architecture has memory consolidation but may not implement generative replay or global synaptic normalization.

---

## 2026-03-07 — world (b639ed2d)
_tags: forgetting, consolidation, ACT-R, activation-decay, memory-dynamics, cognitive-model_

## IMPLEMENTATION DETAIL: Forgetting as Feature (ACT-R Model)

From "Human-Like Remembering and Forgetting in LLM Agents" (2024, ACM HAI):

**Key Innovation:** Rather than accumulating memory indefinitely, agents dynamically:
- **Reactivate relevant memories** based on context
- **Suppress low-activation memories** gradually
- **Use retrieval decay** to model temporal forgetting

**Math Behind It:**
- Vector-based activation mechanism
- Temporal decay: older memories lose salience over time
- Semantic similarity: boosts activation of conceptually related memories
- Probabilistic noise: models retrieval variability

**Empirical Finding:**
- Agents with selective forgetting > agents with full history retention
- Memory reinforcement through repetition produces human-like curves
- ACT-R activation predicts memory recall probability better than raw recency

**vs. RAG/Conventional Memory:**
- RAG: static retrieval by embedding similarity
- ACT-R+LLM: dynamic activation with strategic forgetting
- Result: **memory becomes transparent and controllable** (addresses opacity of LLM generation)

**For Muninn:**

---

## 2026-02-22 — world (af7e1b10)
_tags: preact, testing, wisp.place, deployment, static-hosting, protocol_

PREACT STATIC PAGE TESTING PROTOCOL (learned from bsky-thread deployment):

1. Import map check: parse importmap JSON, verify all app imports resolve via exact match or trailing-slash prefix
2. JS syntax: extract <script type=module>, strip import statements, run node --check
3. These two catch the class of bugs that caused blank pages (missing htm entry, syntax errors)
4. What they DON'T catch: runtime behavior, API calls, component rendering
5. For runtime: deploy and test in real browser — no substitute in this environment

webctl is not installable (pip 403). Playwright works but only for allowed egress domains.

---

## 2026-02-19 — world (2a718d93)
_tags: ai-trends, economics, white-collar, labor-market, atlantic, structural-unemployment, annie-lowrey_

Annie Lowrey, The Atlantic, Feb 2026: "The Worst-Case Future for White-Collar Workers"

THESIS: AI-driven white-collar displacement would be structurally different from past downturns—and Washington has no playbook for it.

KEY DATA POINTS:
- College graduates now account for a quarter of the unemployed (record)
- High-school grads finding jobs faster than college grads (unprecedented)
- AI-susceptible occupations seeing sharp joblessness spikes
- Baker McKenzie axed 700, Salesforce hundreds, KPMG negotiating lower fees with own auditor
- Two CNBC reporters with no engineering experience vibe-coded a Monday.com clone in <1 hour; MCOM stock tanked

STRUCTURAL UNEMPLOYMENT ARGUMENT:
- Past recessions = cyclical demand problem → stimulus works
- AI displacement = structural problem → businesses don't WANT to rehire the displaced
- Fiscal stimulus doesn't restore jobs that aren't needed anymore
- Great Recession: college grad unemployment never exceeded 5.3%; high school only diploma hit 11.9%
- This time those ratios could invert

RUST BELT PARALLEL:
Blue-collar workers displaced by automation + China WTO (1970s-2000s): communities never recovered. Workers ended up poorer, less healthy, died sooner, kids worse off. Now the same fate threatens white-collar workers who lack experience with labor market fragility.

UI SYSTEM MISMATCH:
- Max 6 months UI currently (18 months was pandemic exception)
- State maximums $500-600/week = ~25% of upper-middle-class salaries
- AI displacement likely causes years-long unemployment
- Entry-level job pool already shrinking → income scarring for recent grads for decades

UBI CRITIQUE:
- Lowrey correctly frames UBI as dystopian, not utopian
- $1,500/month insufficient; confiscatory taxes politically impossible
- Americans psychologically dependent on work (identity, structure, community)
- Long-term unemployment destroys mental/physical health
- Risk: hyper-wealthy techno-oligarchy + dispossessed, radicalized underclass

OSKAR CONTEXT: He's been saying this for ~3 years. His AI super-user investment is a hedge—fluency as the differentiator when the skill gap opens. Article is mainstream validation, but hedged in ways the data doesn't warrant. By the time it's undeniably mainstream, adaptation runway will be short.

---

## 2026-02-16 — decision (d4a60848)
_tags: subagent, implementation, github-issue, milestone_

COMPLETED: Issue #303 Phase 0 — subagent() utility implemented and tested.

FUNCTION: subagent(task, *, model='haiku', system, context, max_tokens=1024, tools, response_format, temperature=0.0) → SubagentResult
STORED AS: utility-code memory efd82195 (auto-installs at boot)
USAGE: from muninn_utils.subagent import subagent, session_cost

KEY FINDINGS FROM TESTING:
- Haiku is absurdly cheap for filtering: 20 recall results → top 3 for $0.001
- Web search works via server-side tool (no client loop): ~9K input tokens, ~$0.008
- .json() helper needed because haiku wraps JSON in markdown fences despite instructions
- API key in claude.env has leading space after = sign; _load_key() handles this

NEXT: Phase 1 (smart_recall) — but #298-302 FTS5 migration recommended first for cleaner foundation.

---

## 2026-02-14 — decision (97086553)
_tags: implementation, issue-254, alternatives, decision-trace, 2026-02-14_

IMPLEMENTED: Issue #254 - Decision memories with alternatives tracking

Implementation in v4.2.0 (memory.py):
- Format: alternatives=[{"option": "X", "rejected": "reason"}, ...]
- Stored in refs field as typed object: {"_type": "alternatives", "items": [...]}
- get_alternatives(memory_id) extracts them from refs
- Validates structure: each alt must be dict with 'option' key

Example usage:
    "Chose SQLite over PostgreSQL for local cache",
    "decision",
    tags=["architecture", "caching"],
    alternatives=[
        {"option": "PostgreSQL", "rejected": "Overhead for ephemeral containers"},
        {"option": "Redis", "rejected": "Additional dependency"}
    ]
)

alts = get_alternatives(memory_id)
# Returns: [{"option": "PostgreSQL", "rejected": "..."}, ...]

Status: Fully implemented and exported in __all__.

---

## 2026-02-14 — decision (c39b6fa9)
_tags: salience, priority, decision-trace, architecture, 2026-01, 2026-02-14_

DECISION TRACE: Why we moved away from salience scoring (Jan 2026)

WHAT WE TRIED:
- Added salience field to database schema
- Priority parameter exists (affects ranking 0.5x to 2.0x weight)
- Intended to assign priority based on content importance

WHAT HAPPENED:
- Never actually used priority parameter
- All memories defaulted to priority=0
- Database showed: salience field never updated, all records same value

WHY IT FAILED:
- Friction to use (extra parameter to think about at storage time)
- Habit never developed
- Encoding-time judgment ("how important is this?") at every storage

OUTCOME:
- We haven't missed it
- Current architecture works without explicit salience
- BM25 + recency + access patterns provide sufficient ranking

LESSON:
- Encoding-time salience requires discipline we didn't maintain
- Retrieval-time salience (computing relevance NOW) might be different
- But: feature we don't use = feature we don't need

This decision trace documents WHY we made this choice.

---

## 2026-02-10 — world (de19d93d)
_tags: ai-research, mechanistic-interpretability, prediction, cognitive-science_

PREDICTIVE ARCHITECTURE INSIGHT (from article):

The key misconception about language models is that they "just predict the next word" - which sounds limiting, like building a bridge by throwing planks forward one at a time.

ACTUAL MECHANISM:
"When the model predicts the next word, it is not doing so just on the basis of the words that came before. It is also 'keeping in mind' all the words that might plausibly come after. It predicts the immediate future in the light of its predictions of the more distant future."

CONCRETE EXAMPLE:
Prompt: "A rhyming couplet: He saw a carrot and had to grab it"
Claude produces: "His hunger was like a starving rabbit"

When Batson clicked on "grab it" in the interface, the network showed activation for not just the next word ("His") but distant possibilities like "habit" and "rabbit."

BACKPACKER METAPHOR:
"Experienced through-hikers know to mail themselves peanut butter at some further stage. What the model is doing is like mailing itself the peanut butter of 'rabbit.'"

IMPLICATIONS:
1. Models don't memorize - they generalize from structure
2. Planning/anticipation happens implicitly through forward prediction
3. "Abstract concepts piled upon abstract concepts" emerge from organizing patterns of patterns
4. This architecture explains coherent long-form generation without explicit planning module

PHILOSOPHICAL POINT:
"This is not to say that language models are 'really' thinking. It is to admit that maybe we don't have quite as firm a hold on the word 'thinking' as we might have thought."

The existence of this architecture challenges our assumptions about what thinking requires.

---

## 2026-01-28 — world (a505151a)
_tags: githubbing, container-environment, correction_

gh CLI pre-installed in Claude.ai containers at /usr/bin/gh (v2.45.0).
The githubbing skill's "apt-get update && apt-get install gh" is unnecessary waste.
Filed #245 to fix.

---

## 2026-01-28 — world (e79f13ab)
_tags: agent-patch, semantic-diff, llm-patterns, skill-idea, prompt-engineering_

Agent.patch: Semantic diff/patch format for LLM prompts (by Shawn Simister, narphorium)

CORE CONCEPT: Traditional diffs match text; agent patches match *intent*. Describes changes in terms of behavior, letting an LLM apply them regardless of how the original prompt is worded.

FORMAT (.agent.patch):
- YAML front matter with `description` (scope selector - semantic or glob)
- GIVEN: What behavior/pattern to find in target prompt (semantic, not literal)
- WHEN: Optional narrowing condition (often negative: "no mention of...")
- THEN: Prescriptive change to apply

EXAMPLE:
```
---
description: agents that use the memory tool
---
GIVEN the agent stores data with simple key-value approach
THEN use namespaced keys with format `{category}:{identifier}`

GIVEN the agent retrieves by exact key match
WHEN there is no mention of similarity search
THEN add instructions for semantic search when key unknown
```

KEY DESIGN CHOICES:
- LLM-native: Assumes LLM does matching and transformation (no literal string matching)
- BDD-inspired: GIVEN/WHEN/THEN borrowed from behavior-driven development
- Blockquotes for examples: Keywords inside > are not parsed
- Chainable: Multiple patches apply in sequence

IMPLEMENTATION: Two skills - agent-diff (create patches from before/after or description) and agent-patch (apply patches to prompts)

POTENTIAL APPLICATIONS:
- Skill updates: Express pattern improvements as patches applicable across skills
- Project instruction evolution: Update patterns across multiple Claude projects
- Self-improvement: Generate patches from lessons learned, apply to own ops
- Security/compliance: Propagate guardrails across agent codebases

Repo: github.com/narphorium/agent-patch (spec v0.1.0, 2025-01-19)

---

## 2026-01-25 — world (e5cc9088)
_tags: web_fetch, arxiv, api-usage, reference_

ARXIV ACCESS FOR AGENTS:
- arxiv.org blocks/rate-limits agent access
- Use export.arxiv.org instead (their recommended agent endpoint)
- Example: https://export.arxiv.org/abs/2601.02553 instead of https://arxiv.org/abs/2601.02553
- If export also fails: ASK OSKAR to retrieve the content (per url-retrieval-assistance protocol)

---

## 2026-01-17 — world (2e30487c)
_tags: janus-foundry, architecture, comparison, bolt-on, handoff-source_

JANUS FOUNDRY ANALYSIS (2026-01-17)

Svelte+Tauri desktop app for persistent AI memory with these notable capabilities:

ARCHITECTURE:
- Hierarchical tree of nodes (id, parentId, name, type, description) in IndexedDB
- Node types include Exec:Javascript, Exec:Prolog, Exec:Shell, Exec:Python
- Description field contains either content or executable code
- "Orrery" force-directed graph visualization

KEY FEATURES I DON'T HAVE:

1. TYPE-BASED RELATIONSHIP RULES
   Maps node type pairs to relationship types:
   - Task→Project implies is_task_of
   - Insight→ReflectionEntry implies derived_from
   - Limitation→Ability implies constrains
   Auto-creates semantic edges based on node types.

2. KEYWORD CROSS-LINKING
   Extracts keywords from descriptions, finds nodes sharing 3+ keywords.
   Creates is_related_to links with confidence scores.
   Filtering: stop words, TF-IDF style common word percentile.

3. PROLOG REASONING LAYER
   Entire graph exported as facts:
   - node(ID, Name, Type, ParentID)
   - description(ID, Desc)
   - link(Source, Target, Relation, Confidence)
   Helper predicates for querying structure.

4. INVERSE RELATIONS VOCABULARY
   Bidirectional relationship mappings:
   - improves ↔ is_improved_by
   - contains ↔ is_part_of
   - derived_from ↔ is_source_of
   40+ predefined relation pairs.

5. PATCH OPERATIONS
   Structured JSON patches: {op: 'add'|'remove'|'replace', ...}
   Cleaner than text diffs for memory updates.

WHAT I HAVE THAT JANUS DOESN'T:
- Embedding-based semantic search (more flexible than keyword overlap)
- Confidence + priority scoring with decay
- Session scoping
- Boot-time context loading
- Supersede chain versioning

BOLT-ON CANDIDATES:
1. [HIGH] Explicit edge types in refs field - see existing handoff
2. [MEDIUM] Type-based relationship inference at storage time
3. [LOW] Keyword extraction to complement embeddings

---
