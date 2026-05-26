---
tag: flowing
memory_count: 2
date_range: 2026-05-08 to 2026-05-08
---

# flowing

_2 memories from Muninn's past, primary tag `flowing`._

## 2026-05-08 — decision (1ce29655)
_tags: preference, correction, skill-versioning, PR-612, 2026-05-07_

PREFERENCE SIGNAL — skill version bumps are mandatory.

Implication: Every modification to a SKILL.md (or to scripts under a versioned skill) requires bumping `metadata.version` in the frontmatter, even for docs-only changes. SemVer applies: PATCH for docs/clarifications/bug fixes, MINOR for backward-compat new functionality, MAJOR for breaks. The CHANGELOG entry must use the actual version number, not [Unreleased].

Future default: Before opening any PR that touches a SKILL.md or its scripts, check the frontmatter version, bump it appropriately, and add a CHANGELOG entry under the new version header (not [Unreleased]). Apply the same to skill scripts that have a version (e.g. flowing.py's module version if exposed). If unsure whether a change qualifies — assume yes, bump.

Caught the omission on PR #612: did docs change without bump (version 1.1.0 stayed, CHANGELOG used [Unreleased]). Pushed follow-up commits to bump to 1.1.1 and finalize the CHANGELOG header.

---

## 2026-05-08 — procedure (19772489)
_tags: validate, when, authoring-gotcha, 2026-05-07_

flowing v1.1 `validate=` callables receive kwargs by dep NAME, same as task bodies. A validator written with `def must_have_title(fetch_url_meta)` works only for tasks whose dep is named `fetch_url_meta`. Renaming the dep (or reusing the validator across tasks with differently-named deps) raises `TypeError: got an unexpected keyword argument 'foo'` at validate time, surfacing as FAIL of the dependent task.

Same applies to `when=` predicates.

Patterns:
- Single-purpose validator tied to one task: name params after the deps.
- Reusable validator across tasks with different dep names: take `**kwargs` and pull by expected key — loses some explicitness.
- Cleaner: validator factory — `def must_have_title_of(dep_name): def v(**kwargs): if not kwargs[dep_name].get('title'): raise ...; return v`.

Discovered 2026-05-07 while testing — wrote `must_have_title(fetch_url_meta)` then reused across a task whose dep was named `fetch_bad_meta`. Validator failed with signature mismatch, not the intended empty-title error.

---
