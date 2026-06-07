# verso-proto

A Verso-inspired claim verifier for markdown documents. Prose makes claims;
the verifier resolves each claim against live state and reports drift.

## The pattern

Documents claim things that should stay true ("function `foo` takes `bar`";
"`verso.py demo.md` exits 0"). The claim and the thing it describes are
separate artifacts, and separate artifacts drift. Verso (Lean's literate
framework) prevents this by sharing one elaboration context across prose and
code. This prototype does the structural minimum: every claim is a typed HTML
comment next to its prose, and a verifier resolves it against the live system.

```
<!-- claim: TYPE key=value key=value ... -->
```

The prose stays human-readable; the claim sits invisibly next to it. Every
claim type encodes an **invariant** — a FAIL means a real defect to fix.

## Verdicts

- **PASS** — claim matches reality
- **FAIL** — claim mismatches (with expected vs actual)
- **STALE** — referenced artifact no longer exists (404, deleted, etc.)
- **ERROR** — resolver couldn't run (network, bad syntax, wrong category)

Exit 0 if all pass, 1 otherwise. `--json` for machine output.

## Claim types

| Type | Checks |
|---|---|
| `signature` | Python callable has expected named parameters |
| `command-output` | subprocess exit code, stdout-contains, stderr-contains |

### Why no `pr-state` / `issue-state`

Earlier versions checked GitHub PR and issue state. They were removed. A PR
going open→merged is the PR doing its job, not drift — the state is *expected*
to change, so it isn't an invariant. The tell is which artifact you edit to
make the check pass again: for a signature mismatch you fix the code; for
"PR #687 is open" the only move is to edit the claim to say "merged," chasing
reality instead of constraining it. When the document is the thing that has to
change, the check is just confirming a stale cache. Mutable state wants live
transclusion (render the current value at read time), not a frozen assertion —
a different mechanism, noted under next steps.

## Run

```
python3 verso.py demo.md
```

The demo is self-referential: `demo.md` is the README *and* the test suite
for `verso.py` — its claims verify `verso.py` itself. One claim deliberately
drifts to demonstrate STALE; everything else passes. Expected exit: 1.

## Version history

Removed across revisions:

- **`eval`** — executed arbitrary Python from the markdown. Any document
  could `__import__("os").system("rm -rf /")`. Replaced by `command-output`,
  which uses `subprocess` with `shell=False` and shlex-split args.
- **`pr-state` / `issue-state`** — checked mutable GitHub state, which is
  expected to change and so isn't an invariant. See "Why no pr-state /
  issue-state" above.
- **`memory-exists`** — Muninn-specific and fragile. Deferred.

The `eval` removal came out of an adversarial review by
`challenging(profile=code)`; the temporal removal came out of a design
objection from Oskar. The Verso-style win: the demo claimed `resolve_eval`
existed; that claim now resolves to STALE. The README and the code stayed in
sync because the README *is* the test.

## What this prototype is NOT

- **Not full Verso.** Verso shares one elaboration context across prose and
  code; this is checks-only. The claim is still text — the prose doesn't
  *bind* to the artifact at write time, just gets verified at check time.
- **Not a CI replacement.** It's a verifier, not a test framework. Wire it
  into CI to fail builds on FAIL/STALE; that's the natural use.
- **Not generative.** Doesn't produce views or transform the document.

## What it does demonstrate

A document that **breaks loudly when its claims drift** instead of going
silently stale. Renaming `parse_claims` while the README still documents the
old name is the failure mode it catches: the next verify run flags the
mismatch. The check only makes sense for claims that *should* stay true —
signatures, command exit codes — not for state that is supposed to change.

## Known limits (carried forward from v2 review)

- `importlib.import_module` in `resolve_signature` executes target module
  top-level code. **Mitigated**: imports are restricted to an allowlist of
  module prefixes (`muninn_utils`, `scripts`, `verso` by default; override
  via `VERSO_IMPORT_ALLOW`). A crafted claim can't `import os` and run it.
- Error detail strings are passed through verbatim; could leak paths in
  shared deployments.
- `KV_RE` doesn't handle escaped quotes inside quoted values.

## High-leverage next steps

- Pre-commit hook for ops/README files that make claims
- `--watch` mode: re-verify on file change
- Cross-claim references: catch drift between two claims that should agree
- **Live transclusion** for mutable references (PR state, current versions):
  render the current value at read time instead of asserting a snapshot. This
  is the right home for the temporal cases that were removed — a different
  mechanism from verification, with no FAIL verdict.
- A `verso` directive that embeds a live value inline at render time
  (real elaboration, not just verification)
