---
name: designing-html
description: >-
  Router for HTML build requests. Load this BEFORE composing-html or
  fetching Hallmark. Picks composing-html for artifact-shaped briefs
  (reports, decks, reviews, dashboards, flowcharts, postmortems, module
  maps, design-system refs) and Hallmark for greenfield ad-hoc HTML
  (landing pages, marketing pages, audits, redesigns, DNA extraction
  from a screenshot/URL, component-scope work — single button / card /
  modal). Use when a brief involves "build a page", "design a landing
  page", "redesign", "audit", "hallmark", "study this design", or any
  HTML deliverable that isn't an obvious composing-html template
  (status report, slide deck, PR review writeup, postmortem, etc.).
  Knows which target sites bypass Hallmark and stay on their own
  templates.
metadata:
  version: 0.1.0
---

# designing-html

A router. The body below is a decision table; the real work happens in
the selected downstream skill. Don't write HTML from this skill — pick
one and hand off.

## Pick the downstream

| Brief shape | Downstream |
|---|---|
| PR review writeup, status report, incident postmortem | composing-html |
| Slide deck, slides, presentation | composing-html (`deck.slide_deck`) |
| Side-by-side comparison, module map, flowchart | composing-html |
| Design-system reference, token doc, component-variant grid | composing-html (`design.*`) |
| Kanban / triage board, prompt tuner, flag editor | composing-html (`editor.*`) |
| Feature explainer, concept explainer | composing-html (`research.*`) |
| Build a landing page for X | Hallmark |
| Marketing page, product page, pricing page | Hallmark |
| Hero section, pricing section, CTA block in isolation | Hallmark (component-scope) |
| Single button / input / card / modal / dropdown | Hallmark (component-scope) |
| `hallmark audit <target>` — score existing page against anti-patterns | Hallmark (`audit` verb) |
| `hallmark redesign <target>` — keep copy + IA, rebuild visual layer | Hallmark (`redesign` verb) |
| `hallmark study <screenshot \| URL>` — extract design DNA | Hallmark (`study` verb) |

If a brief straddles both — e.g. *"a postmortem styled as a landing
page"* — composing-html wins. Composing-html's chrome is opinionated
but neutral; Hallmark expects to own the page.

If neither fits cleanly (forms, emails, embedded widgets), default to
composing-html `freeform` — the chrome and inventory still earn their
keep over hand-rolled HTML.

## Site exclusions (managed sites)

Do **not** apply Hallmark to:

- `muninn.austegard.com` — established corvid serif voice, type-led
  editorial templates.
- `austegard.com` — Oskar's personal site, established system.

For posts published to either, follow the site's own templates and the
`blog-writing-discipline` / `muninn-voice-signature` configs. Composing-html
may still apply for embedded report artifacts inside a post (e.g. a
PR-review writeup linked from a blog entry).

## Downstream pointers

### composing-html (local)

Already on disk at `/mnt/skills/user/composing-html/`. Read
`/mnt/skills/user/composing-html/SKILL.md` and follow it.

### Hallmark (fetch per session)

Hosted at [`oaustegard/fork-hallmark`](https://github.com/oaustegard/fork-hallmark)
(MIT, fork of `Nutlope/hallmark`; security review 2026-05-21: clean,
no executable hooks, no telemetry, only the public GitHub stars API for
its marketing-site star counter).

Don't vendor — the marketing-site assets push the tree to ~27 MB. Fetch
the tarball when routing here:

```bash
curl -sL "https://codeload.github.com/oaustegard/fork-hallmark/tar.gz/main" \
  -o /tmp/hallmark.tar.gz
mkdir -p /tmp/hallmark
tar -xzf /tmp/hallmark.tar.gz -C /tmp/hallmark --strip-components=1
# Then read /tmp/hallmark/SKILL.md and proceed.
```

The SKILL.md is the entry point; `references/` holds the cookbook
(macrostructures, components, themes, slop-test gates). Load only the
reference files the brief actually needs — loading the cookbook
end-to-end is, per Hallmark's own SKILL.md, *"the single biggest token
waste in the skill."*

## What this skill is not

It's not a place to write HTML. It's not a place to enumerate themes,
template names, or macrostructures — those live in the downstream
skills. If you find yourself drafting markup here, you've taken the
wrong turn; hand off and let the downstream skill own the artifact.
