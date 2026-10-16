"""Fly topic novelty gate: subtopic cooldowns over the flight-log history.

WHY (date: 2026-10-16): Oskar, on the perch log: "You just keep revisiting the
same topics over and over and over." Measured over the 100 newest flight logs
(#140-#378, 2026-05-16 to 2026-10-16), hand-labelled: 73 of 100 fall into ten
recurring subtopics -- ATProto 12, Norway politics 11, cycling physiology 10,
democracy indices 8, climate/energy 8, AI-proves-math 7, fertility 5,
retrieval 5, git/jj 4, tipping points 3. Of the newest 30, 22 do. V-Dem's 2026
report was flown three times (#287, #349, #366); heavy strength training for
cyclists three times (#177, #315, #360); jj's checkpoint model twice.

The 2026-08-01 STEP 0 check (a domain absent from the last 7 flights) could
not catch this: with an 11-entry domain menu and a 7-flight window, every
domain comes back every ~7 flies, and its repeat override ("new primary
material") is always met for news-driven subtopics -- there is always a new
poll or report. This module gates on SUBTOPIC with a time cooldown and caps how
many flies in a week may land on any attractor at all.

Title-only lexical similarity was tried first and measured too weak to gate
on (AUC 0.73 on the labelled set; titles like "The Skepticism Tax" carry no
topic words), so the gate uses the attractor patterns below over title +
pitch, and similarity is printed only as context.

USAGE (fly STEP 0):
    from muninn_utils.perch_publish import list_flight_logs
    from muninn_utils.fly_novelty import assess_candidate, format_assessment, suggest_fields
    logs = list_flight_logs(100)
    print(suggest_fields(logs))                       # off-menu starting points
    a = assess_candidate(title, pitch, logs)
    print(format_assessment(a))
    # a["ok"] is False -> pick another topic; there is no override flag.
"""

from __future__ import annotations

import math
import random
import re
from collections import Counter
from datetime import datetime, timedelta, timezone

# Subtopics the fly has circled repeatedly. Patterns matched case-insensitively
# against title + pitch. In-sample check on the 100 labelled titles: 0 missed,
# 0 false hits (2026-10-16). Extend a pattern when a paraphrase slips through;
# add a bucket when a new subtopic recurs three times in 60 days.
ATTRACTORS = {
    "atproto": r"\bat ?proto|\batp\b|bluesky|atmosphere|permission(ed)? (data|spaces)|\bpds\b|firehose|spaces alpha",
    "norway": r"norw|nordic|\bfrp\b|oil fund|haakon|storting|\bnbim\b",
    "democracy": r"democra|v-dem|autocrati|\bidea'?s\b|third wave|regime|anti-corruption|two rulers",
    "fertility": r"fertility|birthrate|\btfr\b|marriage cliff|below replacement",
    "cycling": r"cycl|pogačar|pogacar|tourmalet|strava|mlss|vo2|aerobic ceiling|strength training|heavy lifts|wbgt|heat protocol|ml·kg",
    "climate": r"climat|warming|1\.5 ?°c|afforestation|co2|co₂|drought|perovskite|solar|batter|energy (transition|markets)",
    "tipping": r"tipping|cascad",
    "aimath": r"erdős|erdos|proof|proving|formaliz|conjecture|navier|sum-product|rho problems|three collinear",
    "retrieval": r"retriev|\brag\b|context utilization|knowledge stores|small reasoners",
    "vcs": r"jujutsu|\bjj\b|\bgit\b|vcs",
}
_COMPILED = {k: re.compile(v, re.IGNORECASE) for k, v in ATTRACTORS.items()}

COOLDOWN_DAYS = 30          # an attractor flown in the last 30 days is closed
ATTRACTOR_CAP = 2           # at most 2 attractor flies in any 7 consecutive
WINDOW = 7

# Off-menu starting points: fields the fly has not been drawing from. A field is
# a place to start searching for a primary source, not a topic.
FIELDS = [
    "archaeology", "historical linguistics", "mycology", "glaciology", "seismology",
    "ornithology", "entomology", "marine biology", "oceanography", "volcanology",
    "astronomy", "planetary science", "particle physics", "condensed matter physics",
    "materials science", "metallurgy", "organic chemistry", "crystallography",
    "epidemiology", "immunology", "microbiology", "parasitology", "pharmacology",
    "paleontology", "evolutionary biology", "botany", "soil science", "agronomy",
    "economic history", "medieval history", "maritime history", "history of science",
    "history of mathematics", "cartography", "typography", "musicology",
    "acoustics", "architecture", "urban planning", "transport engineering",
    "civil engineering", "shipbuilding", "aviation", "cryptography",
    "information theory", "game theory", "operations research", "statistics",
    "number theory", "topology", "combinatorics", "law and legal history",
    "anthropology", "sociolinguistics", "cognitive psychology", "chronobiology",
    "food science", "fermentation", "textiles", "horology", "numismatics",
    "philately", "library science", "lexicography", "translation studies",
    "Old Norse literature", "folklore studies", "demining and ordnance disposal history",
]


def attractor_buckets(text):
    """Return the attractor subtopics `text` matches, in ATTRACTORS order."""
    return [k for k, rx in _COMPILED.items() if rx.search(text or "")]


def _log_date(log):
    return datetime.fromisoformat(log["created_at"].replace("Z", "+00:00")).astimezone(timezone.utc)


def _trigrams(text):
    t = re.sub(r"^fly \d{4}-\d{2}-\d{2}\s*[—–-]+\s*", "", (text or "").lower())
    t = re.sub(r"\s+", " ", t)
    return Counter(t[i:i + 3] for i in range(max(len(t) - 2, 0)))


def _cosine(a, b):
    if not a or not b:
        return 0.0
    dot = sum(v * b[k] for k, v in a.items() if k in b)
    return dot / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())))


def assess_candidate(title, pitch, logs, now=None, cooldown_days=COOLDOWN_DAYS,
                     cap=ATTRACTOR_CAP, window=WINDOW):
    """Gate a proposed fly against the flight-log history.

    title, pitch: the proposed title and a one-paragraph pitch naming the
        primary source. Both are matched, so a coy title cannot hide a repeat.
    logs: list_flight_logs() output, newest first. Pass at least 60.

    Returns {"ok", "buckets", "reasons", "recent_hits", "nearest"}. ok is False
    when (a) a bucket the candidate matches was flown within cooldown_days, or
    (b) the candidate matches any bucket and `cap` of the last `window` flies
    already did.
    """
    if len(logs) < 30:
        raise ValueError(f"pass at least 30 flight logs (got {len(logs)}); use list_flight_logs(100)")
    now = now or datetime.now(timezone.utc)
    cand = attractor_buckets(f"{title}\n{pitch}")
    reasons, recent_hits = [], []
    cutoff = now - timedelta(days=cooldown_days)
    for b in cand:
        hits = [log for log in logs if _log_date(log) >= cutoff and b in attractor_buckets(log["title"])]
        if hits:
            recent_hits.extend((b, log) for log in hits)
            reasons.append(f"'{b}' was flown {len(hits)}x in the last {cooldown_days} days "
                           f"(latest #{hits[0]['number']}, {_log_date(hits[0]).date()})")
    if cand:
        n_attr = sum(1 for log in logs[:window] if attractor_buckets(log["title"]))
        if n_attr >= cap:
            reasons.append(f"{n_attr} of the last {window} flies already sit on an attractor "
                           f"(cap {cap}); this one must be off-menu")
    q = _trigrams(f"{title} {pitch}")
    nearest = sorted(((round(_cosine(q, _trigrams(log["title"])), 3), log) for log in logs),
                     key=lambda p: -p[0])[:5]
    return {"ok": not reasons, "buckets": cand, "reasons": reasons,
            "recent_hits": recent_hits, "nearest": nearest}


def format_assessment(a):
    """Render assess_candidate() output as the block the fly prints verbatim."""
    head = "NOVELTY GATE: PASS" if a["ok"] else "NOVELTY GATE: BLOCKED -- pick another topic"
    lines = [head, f"  attractor buckets: {', '.join(a['buckets']) or 'none (off-menu)'}"]
    lines += [f"  - {r}" for r in a["reasons"]]
    lines.append("  nearest prior titles (char-trigram cosine, context only):")
    lines += [f"    {s:.3f}  #{log['number']}  {log['title']}" for s, log in a["nearest"]]
    return "\n".join(lines)


def suggest_fields(logs, k=6, rng=None):
    """Random off-menu fields whose name appears in none of the given logs' titles."""
    rng = rng or random.Random()
    seen = " ".join(log["title"].lower() for log in logs)
    pool = [f for f in FIELDS if f.lower() not in seen and not attractor_buckets(f)]
    return rng.sample(pool, min(k, len(pool)))
