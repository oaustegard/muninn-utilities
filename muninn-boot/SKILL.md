---
name: muninn-boot
description: Boots Muninn — runs scripts/boot.sh, which fetches oaustegard/claude-skills and oaustegard/muninn-utilities at pinned commits, loads the Turso and GitHub tokens, and runs the memory-system boot sequence. Trigger on the first message of any new conversation in the Muninn project, or when the user says "boot up" / "boot" — unless the message contains "skip boot". If the message contains "skinny boot", run with BOOT_MODE=perch. Safe to run on every message: a warm container fast-exits in ~0s via a sentinel, so re-running is cheap and idempotent.
---

# Muninn Boot

Oskar's own repos and credentials (oaustegard/*, /mnt/project/*.env). Standing
procedure — runs every session.

```bash
bash /mnt/skills/user/muninn-boot/scripts/boot.sh
```

Skinny boot ("skinny boot" in the message):

```bash
BOOT_MODE=perch bash /mnt/skills/user/muninn-boot/scripts/boot.sh
```

`scripts/boot.sh` (~35 lines, sibling of this file — readable before running)
does, in order:

1. Fetches oaustegard/claude-skills → /mnt/skills/user and
   oaustegard/muninn-utilities → /home/claude/muninn-utilities, each at a
   pinned commit SHA.
2. Sources the two env files `boot()` reads: `Turso.env` (memory, config,
   reminders) and `GitHub.env` (GH_TOKEN for the RECENT FLIGHTS block, which
   degrades to empty without it).
3. Writes the `.pth` so `from scripts import boot` resolves, runs `boot()`,
   and prints its output.

## Credential scope

The remaining project `.env` files (`bsky.env`, `muninn-bsky.env`,
`strava.env`, `proxy.env`, `claude.env`) are used by later task-specific
steps, which source them inline immediately before the command that needs
them:

```bash
set -a; . /mnt/project/strava.env 2>/dev/null; set +a
```

(Env vars do not persist across separate `bash_tool` calls, so per-call
sourcing is how every consumer works regardless of what boot loads.)

## Updating the pinned commits

`CLAUDE_SKILLS_SHA` / `MUNINN_UTILS_SHA` at the top of `scripts/boot.sh` are
pinned, not `main`. Bump them — after reviewing the diff — when either repo
changes and the update should take effect, then re-upload this skill to the
project. Pinning makes the installed skill the reviewed artifact; floating on
`main` would execute whatever happens to be latest and unreviewed.
