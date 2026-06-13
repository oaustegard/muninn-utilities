## Task: Job Search (Target Board Scan)

Narrow, repetitive, reliable — the opposite of fly. Scan the target companies' ATS boards for NEW senior roles and post a digest. Runs every morning **in the same session as fly** (two task steps, one routine).

### Phase 0: Read live policy
```python
from muninn_utils.task_policy import load
policy = load('jobsearch')
# instructions: jobsearch-command ops entry (target repo, role filters, digest format, open_issues)
# preferences:  recent jobsearch preference memories (per-company overrides, target add/drop)
# last_run:     most recent scan
```

### Phase 1: Load targets
Read `targets/companies.csv` from `oaustegard/career-search` via `github_rw.get_file`.
For each row with a real ats+slug, build the poll URL:
- greenhouse: `https://boards-api.greenhouse.io/v1/boards/{slug}/jobs`
- lever:      `https://api.lever.co/v0/postings/{slug}?mode=json`
- ashby:      `https://api.ashbyhq.com/posting-api/job-board/{slug}`
Skip rows with `ats=TBD` (not yet verified).

### Phase 2: Poll + diff
- Fetch each board (urllib). **These domains must be on the project allowlist or the fetch fails.**
- Load prior seen-set from `targets/_seen.json` in career-search (`{}` if absent).
- New = posting ids not in the seen-set.

### Phase 3: Filter
- Keep senior AI / Data / Analytics / VP / Chief / Head / Director-level roles.
- Apply per-company overrides from the CSV notes / policy (e.g. POLITICO: Data/AI or VP/CTO only).
- Drop anything requiring a clearance above public trust.

### Phase 4: Write digest (MANDATORY)
`create_discussion` in `oaustegard/career-search`:
- Title: `Job scan {YYYY-MM-DD} — {N} new roles`
- Body: grouped by company, each new role as `[title](url)` + location + why-flagged. Zero new → one-line log.

### Phase 5: Persist
- Overwrite `targets/_seen.json` with the full current posting-id set (`github_rw.commit_file`, branch=main).
- If `policy['instructions']` enables open_issues: open one issue per strong match (feeds the pipeline tracker).
- `remember()` a one-line session log: tags `['session-log','jobsearch','perch-time']`.
