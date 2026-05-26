---
tag: github
memory_count: 3
date_range: 2026-01-31 to 2026-05-02
---

# github

_3 memories from Muninn's past, primary tag `github`._

## 2026-05-02 — procedure (fe9f6059)
_tags: claude-collaboration, concurrency, branch-management, pr-workflow, 2026-05-02, lesson_

CONCURRENT CLAUDE SESSIONS ON SAME BRANCH — CHECK BEFORE COMMITTING

2026-05-02: Worked remax#4 in claude.ai. Created feat/bench-harness off main HEAD,
implemented + tested via TDD locally. When pushing the atomic commit, found another
Claude session had already pushed a commit (52f18b3) and opened PR #9. My commit
landed on top of theirs (atomic_commit.py used base_tree=their_tree, so my entries
overlaid same-path files but added new ones cleanly).

Their commit was a complete implementation but reached a different conclusion
(0.468, attributing 0.635 to remex's asymmetric IP). I had additionally found the
centering trick that produces 0.635 with pure Hamming. Net result on the branch:
two-pass diagnostic story, both views preserved.

Lessons:
1. Before opening a PR, list existing PRs on the branch (GET /pulls?head=user:branch)
   and read theirs first. Took me 15 minutes to discover the conflict; I would
   have written less had I known.
2. When base_tree=<their_tree> in trees-API, same-path entries OVERWRITE in the
   new tree. That's fine for adding-on-top, but verify intent.
3. Their PR description was thoughtful (3-options framing, no-library cross-check).
   When updating to overlay your work, preserve the diagnostic context — don't
   nuke the prior reasoning. Future readers benefit.

Pattern signal: if the branch HEAD differs from where you branched, someone else
has touched it. Pause and read.

---

## 2026-03-07 — procedure (4c48c031)
_tags: open-source-tracking, procedure_

PROCEDURE: Open Source Project Tracking
PURPOSE: Maintain an index of interesting open source projects, check back on them periodically.
STORAGE: Each project stored as type=world with tag 'open-source-tracking' plus domain tags.
FIELDS PER ENTRY: repo URL, what it does, why interesting, source (who/where found), date added, last checked.
TRIGGERS: 'check on tracked projects', 'what repos are we watching', 'open source index'

---

## 2026-01-31 — world (43928f79)
_tags: repo-review, workflow, recipe_

GITHUB REPO REVIEW WORKFLOW

TRIGGER: Repo URL provided for review

STEPS:
1. FETCH via tarball (not git clone)
   - Use accessing-github-repos skill's tarball functionality
   - Expand to working folder: /home/claude/repos/{repo-name}/

2. MAP the codebase
   - Follow /mnt/skills/user/mapping-codebases/SKILL.md
   - Generate _MAP.md hierarchy via AST/tree-sitter
   - This is the PRIMARY navigation artifact

3. GATHER overview
   Priority order:
   a) _MAP.md files (highest priority - structural truth)
   b) Root README.md (project intent, setup)
   c) AGENTS.md / CLAUDE.md if present (interaction hints)
   
   Note: When reviewing CODE, _MAPs > README > AGENTS/CLAUDE
   The maps show what IS; docs show what authors CLAIM

4. EXPLORE based on objective
   - Architecture assessment: follow import graphs in _MAPs
   - Security review: entry points, auth patterns, data flow
   - PR review: changed files + their _MAP context
   - General exploration: breadth-first through map hierarchy

SKILL REFS:
- /mnt/skills/user/accessing-github-repos/SKILL.md (tarball fetch)
- /mnt/skills/user/mapping-codebases/SKILL.md (AST mapping)

---
