# Muninn backend → remote MCP on Cloudflare

Design + migration plan for moving the memory backend out of the session and into a
deployed Worker, on the Sage pattern (`oaustegard/sage`, `mcp/`), while keeping the
genuinely-local half skill-shaped.

Status: **proposal**. Nothing here is built yet.

---

## 1. Why

Today every Muninn session reaches Turso by running Python that was fetched, at a pinned
SHA, as a tarball, into a mount, with `TURSO_TOKEN` in the environment. That has four
costs:

| Cost | Detail |
|---|---|
| Boot tax | Tarball fetch + env sourcing + `.pth` setup before the first `recall()` |
| Credential spread | `TURSO_TOKEN` must exist in every environment that remembers anything |
| Surface limit | Only works where bash + Python exist. Mobile claude.ai, Slack, a phone — no memory |
| Version skew | Pinned SHAs, plus a deprecated mirror in `claude-skills` that a workflow syncs |

A remote MCP fixes all four: one deployment, OAuth'd connector, no credentials in the
session, and memory available anywhere the connector is enabled.

It does **not** fix — and must not break — the local power path: `_exec()` raw SQL,
corpus-wide analysis (`memory_tfidf`, `satisfaction_skew`, `correction_gate`), and the
`muninn_utils` that talk to GitHub, Bluesky and WhiteWind.

---

## 2. The seam

Three destinations, not two. The split is by *what the code needs*, not by what feels
core.

### Goes remote — `muninn-mcp/` Worker

Everything whose only dependency is Turso and whose result is text.

- `recall`, `recall_batch`, `get`, `get_chain`, `get_alternatives`
- `remember`, `remember_batch`, `supersede`, `forget`, `reprioritize`, `strengthen`, `weaken`
- `config_get`, `config_set`, `config_list`, `profile`, `ops`, `set_rule`
- `journal`, `journal_recent`
- `boot` — the composed payload
- `spokes_list`, `spokes_summary` — registry reads are just `config`

### Stays skill-shaped — `remembering/` + `muninn_utils/`

Everything that needs local execution, local credentials, or a Python object.

- **`_exec()` raw SQL** — the ad-hoc analysis escape hatch. Irreplaceable by a fixed tool set.
- **`muninn_utils/*`** — every one of them needs a non-Turso network identity (GitHub,
  Bluesky, WhiteWind) or writes local files.
- **Task discipline** — `task()`, `recall_gate` are in-session control-flow objects. A
  context manager cannot live behind JSON-RPC. Persistence goes over MCP; the object stays local.
- **Boot's environment prelude** — `.pth` setup, `muninn_utils` materialization, env fallback persist.
- **Corpus analysis** — `memory_tfidf`, `satisfaction_skew`, `correction_gate`, export/import, migrations.

### Becomes cron — `muninnd/` Worker

The saged analog. These are exactly the operations that today only run when someone
remembers to run them:

- `curate`, `consolidate`, `therapy_reflect`
- `prune_by_age`, `journal_prune`
- `_build_cooccurrence` rebuild

Keep saged's discipline: **additive and attributable**. `muninnd` proposes structure
(consolidations, priority demotions), applies it deterministically, and every write it
makes carries its own provenance so a bad pass is identifiable and revertible.

### Tool budget

Each tool's schema costs tokens in *every* conversation on the connector. Sage ships 7.
Muninn's Python surface is ~40 exported functions; it must collapse to **8–12** tools —
e.g. one `muninn_config` tool with an `op` parameter rather than four. Anything that
doesn't earn its schema stays in Python. This constraint is a feature: it forces the
seam above to be drawn honestly.

---

## 3. What the port actually costs (smaller than it looks)

The scary part of re-hosting a search backend is reimplementing the ranking. **Muninn's
ranking is already server-side SQL**, not Python:

```
turso.py:536-566   bm25(memory_fts, 0, 1.0, 1.0)
                     × (1 + priority × 0.3)
                     × recency_decay
                     × confidence_boost
                     [× access_boost when episodic]
```

Green transcribes that SQL string. It does not reimplement BM25, recency decay, or
priority weighting. The composite score is computed by Turso in both worlds.

That collapses parity risk down to four things, all small and all testable:

1. **`_escape_fts5_server()`** (`turso.py:418`) — strips `" * ( ) : ^` and the FTS5
   keyword operators `AND OR NOT NEAR`. Sage's `fts.ts` is the precedent for how
   tokenizer detail bites; this is the direct analog and the highest-value unit test.
2. **Tag co-occurrence expansion** (`_cooccurrence_expand`) — fires when FTS returns
   fewer than `expansion_threshold` (3) results. Stateful against the `tag_cooccurrence`
   table, and easy to get subtly wrong.
3. **Result normalization** — `MemoryResult` aliasing (`content`→`summary`, `conf`→
   `confidence`) has no meaning over JSON-RPC. Green returns formatted text; decide the
   text shape once and freeze it.
4. **The boot payload formatter** — `_format_boot_output()` is ~170 lines of section
   ordering, topic grouping and priority sorting. It is the single largest chunk of real
   porting work, and the one most likely to drift silently.

**Open verification gate:** no FTS trigger definitions exist in this repo, which implies
`memory_fts` is maintained DB-side (external-content table + triggers created
out-of-band). If that holds, green does not maintain FTS at all. *Confirm against the
live DB before writing a line of green* — if Python is somehow responsible for FTS
sync, the write path gets materially harder.

---

## 4. Blue-green, when the database cannot be duplicated

Standard blue-green stands up two full stacks and swaps traffic. That does not
translate here, and pretending it does is the way to lose memories.

**A memory database cannot be forked and merged.** Two sessions writing to two copies
diverge irreconcilably — there is no reconciliation function for "what Muninn remembers",
because the rows are not commutative: `supersede` chains, `refs` provenance edges and
`is_superseded` flags encode order.

So:

> **Data stays single-homed. Blue-green applies to the access path, not the stack.**

- **Blue** = the Python skill talking to Turso directly. Stays installed and functional
  throughout the entire migration.
- **Green** = the Worker talking to the same Turso.
- **The switch** = which path the project instructions tell the session to use.
- **Rollback** = edit the project instructions back. No deploy, no restore, seconds.

That last line is the whole reason this shape is safe. The expensive, slow, risky part
of a rollback is normally redeploying; here the fallback path is never torn down, so
reverting is a text edit.

Data rollback is the part that needs actual engineering, and it is stage 0.

---

## 5. Stages

Each stage has an entry gate, a rollback, and a bake period. Do not compress them.

### Stage 0 — Provenance (prerequisite, lands in blue)

**This must ship before green exists.** Without it, green's writes are
indistinguishable from blue's, and there is no data rollback at any later stage.

Add write provenance to `memories` and `config` — a `source` column (`skill@5.13.0`,
`mcp@0.1.0`, `muninnd@0.1.0`) or, if a schema change is unwelcome, a reserved tag
convention. A column is better: tags are user-visible and pollute recall.

- Blue writes `source` on every insert; backfill existing rows to `skill`.
- Gate: 100% of new rows carry a non-null `source` for one week.
- Rollback: drop the column. Nothing reads it yet.

### Stage 1 — Green built read-only, against a Turso branch

`turso db create muninn-green --from-db muninn`. Green deploys, OAuth works, and **every
write tool returns "not enabled"**.

Reuse Sage's auth wholesale: `@cloudflare/workers-oauth-provider`, the self-contained
password page from `mcp/src/mcp-oauth.ts`, `nodejs_compat`, `@libsql/client/web`.
That file is close to copy-paste.

- Gate: **the parity harness**. A frozen set of ~50 golden queries — every `recall`
  shape in `references/`, plus the boot payload — run against blue-Python and
  green-MCP, results normalized and diffed. Byte-equal on the boot payload; identical
  id-order on ranked recalls. This harness is the deliverable of this stage, more than
  the Worker is.
- Rollback: delete the branch DB.

### Stage 2 — Green reads promoted to the real DB

Point green at production Turso. Reads only. Both paths live; instructions still say
Python for writes.

Reads are idempotent, so this is the one genuinely free cutover — worst case green
returns something wrong and you read it, rather than something wrong and you store it.

- Gate: two weeks of real use with no ranking complaints; parity harness green on the
  production corpus (which is larger and messier than the branch).
- Rollback: stop calling the tool.

### Stage 3 — Green writes, shadowed

Enable write tools. Green writes to the real DB tagged `source=mcp`. Blue still available.

`muninnd` runs a nightly invariant check: no orphan `refs`, valid `type` on every row,
no duplicate ids, an FTS row per memory, no `is_superseded` set outside a `supersede`
call (the exact bug class that v5.7.0 fixed — see `memory.py:103`).

- Gate: 30 days, zero invariant violations attributable to `source=mcp`.
- Rollback: `UPDATE memories SET deleted_at = now WHERE source = 'mcp' AND created_at > <cutover>`.
  Bounded and precise — **only because of stage 0**. Soft delete, consistent with the
  existing `forget()` semantics, so it is itself reversible.

### Stage 4 — Cutover

Project instructions flip to MCP-first. The skill is demoted to power-use, not removed.

- Gate: none — this is the decision point.
- Rollback: revert the instructions.

### Stage 5 — Collapse the double implementation

**The stage it is tempting to skip, and the one that determines whether this was worth
doing.**

After stage 4 you own two implementations of composite scoring: the SQL in `turso.py`
and the SQL in green. They will drift. "Some aspects remain skill-shaped" quietly means
"two backends, forever" unless this stage happens.

The fix is Sage's own structure: in Sage, `tools.ts` is shared by *both* the Worker
transport and the stdio transport — one implementation, two doors. Muninn's analog:

> The Worker becomes the only thing that talks to Turso. `remembering/scripts/` is
> re-pointed at the Worker's HTTP endpoint and becomes a thin local client.

Then "skill-shaped" means *local convenience wrapper*, which is sustainable, rather
than *second backend*, which is not.

**Unresolved:** what happens to `_exec()` raw SQL. Three options, needs a decision —
(a) a `execute_sql` MCP tool gated behind a separate secret; (b) Python retains direct
Turso credentials for the power path only, accepting a narrow second door; (c) drop raw
SQL and widen the tool set to cover the analysis cases. (b) is the pragmatic default and
(a) is the clean one.

---

## 6. Inherited traps

From Sage's CLAUDE.md, the ones that transfer:

- **FTS tokenizer.** Sage uses `unicode61 tokenchars '-_/+#.'`; Muninn uses the Porter
  stemmer. Different config, same class of failure. Never pass raw user input to `MATCH`
  — `_escape_fts5_server()` is not optional in the port.
- **Worker-to-Worker same-zone (error 1042).** Only bites if `muninn-mcp` calls another
  Worker. It talks to Turso directly, so this should not apply — but if `muninnd` ever
  calls the MCP Worker, it needs a service binding, not a URL.
- **Secrets are per-Worker.** `TURSO_URL`, `TURSO_TOKEN`, `MCP_LOGIN_PASSWORD` set with
  `wrangler secret put` on both Workers independently.

Muninn-specific:

- **`config` rows carry `read_only` and `boot_load` flags.** Green's `config_set` must
  honour `read_only` (`config.py:283`) or the ops entries marked immutable stop being immutable.
- **Turso 503 on cold start is expected.** Green needs the same retry-with-backoff the
  Python layer has (`_retry_with_backoff`), or the first call of every idle period fails.
- **`.well-known/install-manifests.json`** and the `claude-skills` mirror workflow both
  reference the skill layout. Stage 4 has to touch them.

---

## 7. Decisions needed

1. **Provenance mechanism** — `source` column vs. reserved tag. (Recommend: column.)
2. **Auth** — reuse Sage's password-page OAuth, or a static bearer token? claude.ai
   custom connectors require OAuth; a bearer token only works for programmatic clients.
   (Recommend: OAuth, copied from Sage.)
3. **One Worker or two?** `muninn-mcp` + `muninnd` separately, as Sage does, or a single
   Worker with a cron trigger. (Recommend: two — different failure modes, different
   deploy cadence, and the cron half should never be able to break the interactive half.)
4. **Tool collapse** — which 8–12 tools. Needs a concrete list before implementation.
5. **`_exec()` fate** at stage 5 (§5).
6. **Does `boot` belong as an MCP tool or an MCP resource?** Connectors do not reliably
   auto-read resources, so a tool called by project instructions is the pragmatic answer
   — but it means boot stays an explicit call, not something the client just has.
