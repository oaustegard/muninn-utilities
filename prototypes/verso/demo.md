# verso.py — self-verifying README

This document is the README *and* the test suite for `verso.py`. Every prose
claim about verso.py carries an embedded check that verso.py itself can run.
The recursion is the point: a document whose claims are verified by the
artifact it documents.

Run:

```
python3 verso.py demo.md
```

If verso.py drifts from this README — a renamed function, a removed claim
type, a broken CLI — this document stops verifying. The drift surfaces
loudly instead of waiting to be noticed.

## What verso.py is

A claim verifier for markdown. Prose makes claims via HTML comments; the
verifier resolves each claim against live state and reports PASS, FAIL,
STALE, or ERROR. Exit 0 if all pass, 1 otherwise.

## Functions verso.py defines

The parser walks markdown, extracts claim comments, and returns `Claim`
objects. <!-- claim: signature target=verso.parse_claims has-params=text -->

The driver opens a file, resolves every claim, and prints results.
<!-- claim: signature target=verso.verify_file has-params=path,json_out -->

The CLI entry point reads `sys.argv` and dispatches. <!-- claim: signature target=verso.main has-params= -->

## Resolvers it ships with

GitHub PR state — open, closed, merged. <!-- claim: signature target=verso.resolve_pr_state has-params=args -->

GitHub issue state — open, closed. <!-- claim: signature target=verso.resolve_issue_state has-params=args -->

Python callable signature — does the named function accept the listed
parameters? <!-- claim: signature target=verso.resolve_signature has-params=args -->

Command output — run a subprocess and assert exit code or stdout substring.
This resolver replaced v1's `eval` resolver, which was arbitrary-code-
execution on attacker-controlled markdown. <!-- claim: signature target=verso.resolve_command_output has-params=args -->

## Self-test via command-output

verso.py exits 0 on a fixture whose only claim passes:
<!-- claim: command-output cmd='python3 verso.py fixtures/all_pass.md' exit=0 -->

verso.py exits 1 on a fixture with a known-failing claim:
<!-- claim: command-output cmd='python3 verso.py fixtures/has_fail.md' exit=1 -->

The CLI prints usage to stderr when called with no arguments:
<!-- claim: command-output cmd='python3 verso.py' exit=2 stderr-contains=usage -->

## Drift demonstration

v1 of verso.py had a `resolve_eval` resolver. v2 removed it because eval()
on markdown-controlled input was a critical RCE. If a stale document still
claims `resolve_eval` exists, the verifier flags it as drift:

<!-- claim: signature target=verso.resolve_eval has-params=args -->

That FAIL is intentional — it's the demonstration. Every other claim in
this document should PASS. The expected outcome is exit code 1, with a
summary like "10 pass, 1 stale".

## What this demonstrates

The Verso-DNS-RFC pattern at the smallest possible scale: a single document
whose prose and the artifact it describes are bound together by a verifier
that runs against both. Rename `parse_claims` → `extract_claims` and the
documentation breaks loudly the next time anyone runs `python3 verso.py
demo.md`. There is no path where the README silently drifts.
