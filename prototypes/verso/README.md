# verso-proto

A Verso-inspired claim verifier for markdown documents. Prose makes claims;
the verifier resolves each claim against live state and reports drift.

## The pattern

Documents claim things about the world ("PR #687 is open"; "function `foo`
takes `bar`"; "`verso.py demo.md` exits 0"). Those claims drift the moment
something changes upstream. Verso (Lean's literate framework) prevents this
by sharing one elaboration context across prose and code. This prototype
does the structural minimum: every claim is a typed HTML comment next to its
prose, and a verifier resolves it against the live system.

```
<!-- claim: TYPE key=value key=value ... -->
```

The prose stays human-readable; the claim sits invisibly next to it.

## Verdicts

- **PASS** — claim matches reality
- **FAIL** — claim mismatches (with expected vs actual)
- **STALE** — referenced artifact no longer exists (404, deleted, etc.)
- **ERROR** — resolver couldn't run (network, bad syntax, wrong category)

Exit 0 if all pass, 1 otherwise. `--json` for machine output.

## Claim types

| Type | Checks |
|---|---|
| `pr-state` | GitHub PR is `open`/`closed`/`merged` |
| `issue-state` | GitHub issue is `open`/`closed` |
| `signature` | Python callable has expected named parameters |
| `command-output` | subprocess exit code, stdout-contains, stderr-contains |

## Run

```
GH_TOKEN=... python3 verso.py demo.md
```

The demo is self-referential: `demo.md` is the README *and* the test suite
for `verso.py` — its claims verify `verso.py` itself. One claim deliberately
drifts to demonstrate STALE; everything else passes. Expected exit: 1.

## v1 → v2

v1 had two resolvers that v2 removed:

- **`eval`** — executed arbitrary Python from the markdown. Any document
  could `__import__("os").system("rm -rf /")`. Replaced by `command-output`,
  which uses `subprocess` with `shell=False` and shlex-split args.
- **`memory-exists`** — Muninn-specific and fragile. Deferred until the
  prototype proves out the pattern at all.

Both removals came out of an adversarial review by `challenging(profile=code)`.
The Verso-style win: the v1 demo claimed `resolve_eval` existed; in v2 that
claim now resolves to STALE. The README and the code stayed in sync because
the README *is* the test.

## What this prototype is NOT

- **Not full Verso.** Verso shares one elaboration context across prose and
  code; this is checks-only. The claim is still text — the prose doesn't
  *bind* to the artifact at write time, just gets verified at check time.
- **Not a CI replacement.** It's a verifier, not a test framework. Wire it
  into CI to fail builds on FAIL/STALE; that's the natural use.
- **Not generative.** Doesn't produce views or transform the document.

## What it does demonstrate

A document that **breaks loudly when its claims drift** instead of going
silently stale. The 2026-06-04 GitNexus failure ("PR #687 still open" when
it had merged) is the failure mode this catches in the GitHub axis;
renaming `parse_claims` is the failure mode it catches in the code axis.

## Known limits (carried forward from v2 review)

- `importlib.import_module` in `resolve_signature` executes target module
  top-level code. **Mitigated**: imports are restricted to an allowlist of
  module prefixes (`muninn_utils`, `scripts`, `verso` by default; override
  via `VERSO_IMPORT_ALLOW`). A crafted claim can't `import os` and run it.
- No rate limiting on GitHub claims; a doc with thousands could trip the
  API limit.
- Error detail strings are passed through verbatim; could leak paths in
  shared deployments.
- `KV_RE` doesn't handle escaped quotes inside quoted values.

## High-leverage next steps

- Whitelist for signature imports
- Pre-commit hook for ops/README files that make claims
- `--watch` mode: re-verify on file change
- Cross-claim references: catch drift between two claims that should agree
- A `verso` directive that embeds the live value inline at render time
  (real elaboration, not just verification)
