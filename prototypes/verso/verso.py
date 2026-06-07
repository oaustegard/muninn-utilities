"""
verso.py — Verso-inspired claim verifier for markdown documents.

Embeds typed claims as HTML comments next to prose:

    PR oaustegard/foo#42 is merged. <!-- claim: pr-state target=oaustegard/foo#42 expected=merged -->

Each claim is resolved against live system state. Verdicts:
    PASS    claim matches reality
    FAIL    claim mismatches reality
    STALE   referenced artifact no longer exists
    ERROR   resolver failed (network, import, bad syntax)

Run:
    python3 verso.py path/to/file.md
    python3 verso.py --json path/to/file.md

Exit 0 if all PASS, 1 otherwise.

Claim types in this prototype:
    pr-state         GitHub PR open / closed / merged
    issue-state      GitHub issue open / closed
    signature        Python callable has expected named parameters
    command-output   subprocess exit code and/or stdout substring

NOTE: v1 had an `eval` resolver and a `memory-exists` resolver. Both were
removed:
    eval was arbitrary-code-execution on attacker-controlled markdown.
    memory-exists was fragile and out of scope for the prototype.
`command-output` replaces eval safely (no shell, no eval, just subprocess).
"""

import re
import sys
import os
import json
import inspect
import importlib
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Callable


# ─── claim parsing ────────────────────────────────────────────────────────────

CLAIM_RE = re.compile(
    r'<!--\s*claim:\s*(?P<type>\S+)\s+(?P<args>[^>]*?)\s*-->',
    re.DOTALL,
)

# key=value, key="quoted value", key='quoted value'
KV_RE = re.compile(r"""(\S+?)=(?:"([^"]*)"|'([^']*)'|(\S+))""")


@dataclass
class Claim:
    type: str
    args: dict
    line: int
    context: str  # surrounding prose (claim comment stripped)


def parse_claims(text: str) -> list[Claim]:
    claims = []
    for m in CLAIM_RE.finditer(text):
        kvs = {}
        for km in KV_RE.finditer(m.group('args')):
            key = km.group(1)
            val = km.group(2) if km.group(2) is not None else \
                  km.group(3) if km.group(3) is not None else \
                  km.group(4)
            kvs[key] = val
        line = text[:m.start()].count('\n') + 1
        line_start = text.rfind('\n', 0, m.start()) + 1
        line_end = text.find('\n', m.end())
        if line_end == -1:
            line_end = len(text)
        line_text = text[line_start:line_end]
        prose = re.sub(r'<!--\s*claim:.*?-->', '', line_text).strip()
        # If the claim sits on a line of its own, the stripped context is
        # empty. Walk back to the nearest non-empty preceding line so the
        # report shows the prose the claim actually describes.
        if not prose:
            cursor = line_start - 1
            while cursor > 0:
                prev_end = cursor
                prev_start = text.rfind('\n', 0, prev_end) + 1
                prev = text[prev_start:prev_end].strip()
                if prev and not prev.startswith('#'):
                    prose = prev
                    break
                cursor = prev_start - 1
        claims.append(Claim(type=m.group('type'), args=kvs, line=line, context=prose))
    return claims


# ─── result type ──────────────────────────────────────────────────────────────

@dataclass
class Result:
    status: str  # 'pass' | 'fail' | 'stale' | 'error'
    expected: str = ''
    actual: str = ''
    detail: str = ''


# ─── resolvers ────────────────────────────────────────────────────────────────

def _gh_headers():
    h = {'User-Agent': 'muninn-verso', 'Accept': 'application/vnd.github+json'}
    if os.environ.get('GH_TOKEN'):
        h['Authorization'] = f'Bearer {os.environ["GH_TOKEN"]}'
    return h


def _gh_get(url: str) -> tuple[dict | None, Result | None]:
    try:
        req = urllib.request.Request(url, headers=_gh_headers())
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, Result('stale', detail=f'{url} → 404')
        return None, Result('error', detail=f'HTTP {e.code}: {e.reason}')
    except Exception as e:
        return None, Result('error', detail=f'{type(e).__name__}: {e}')


def resolve_pr_state(args: dict) -> Result:
    target = args.get('target', '')
    expected = args.get('expected', '').lower()
    m = re.match(r'([\w.-]+)/([\w.-]+)#(\d+)$', target)
    if not m:
        return Result('error', detail=f'bad target {target!r}; want owner/repo#N')
    owner, repo, num = m.groups()
    data, err = _gh_get(f'https://api.github.com/repos/{owner}/{repo}/pulls/{num}')
    if err:
        return err
    actual = 'merged' if data.get('merged') else data.get('state', '?')
    status = 'pass' if actual == expected else 'fail'
    return Result(status, expected=expected, actual=actual)


def resolve_issue_state(args: dict) -> Result:
    target = args.get('target', '')
    expected = args.get('expected', '').lower()
    m = re.match(r'([\w.-]+)/([\w.-]+)#(\d+)$', target)
    if not m:
        return Result('error', detail=f'bad target {target!r}; want owner/repo#N')
    owner, repo, num = m.groups()
    data, err = _gh_get(f'https://api.github.com/repos/{owner}/{repo}/issues/{num}')
    if err:
        return err
    # GitHub issues API returns PRs too; filter
    if 'pull_request' in data:
        return Result('error', detail=f'{target} is a PR, use pr-state')
    actual = data.get('state', '?')
    status = 'pass' if actual == expected else 'fail'
    return Result(status, expected=expected, actual=actual)


def resolve_signature(args: dict) -> Result:
    target = args.get('target', '')
    raw = args.get('has-params', '')
    expected_params = [p.strip() for p in raw.split(',') if p.strip()]
    if '.' not in target:
        return Result('error', detail=f'bad target {target!r}; want module.function')
    mod_path, _, func_name = target.rpartition('.')
    # importlib.import_module executes the target module's top-level code.
    # Only import modules under an allowlisted prefix so a crafted claim
    # can't trigger arbitrary imports. Override via VERSO_IMPORT_ALLOW
    # (comma-separated prefixes).
    allow = os.environ.get('VERSO_IMPORT_ALLOW', 'muninn_utils,scripts,verso')
    prefixes = tuple(p.strip() for p in allow.split(',') if p.strip())
    top = mod_path.split('.', 1)[0]
    if top not in prefixes:
        return Result('error',
                      detail=f'import of {mod_path!r} blocked; '
                             f'allowed prefixes: {list(prefixes)} '
                             f'(set VERSO_IMPORT_ALLOW to extend)')
    try:
        mod = importlib.import_module(mod_path)
        fn = getattr(mod, func_name)
    except (ImportError, AttributeError) as e:
        return Result('stale', detail=f'{target}: {type(e).__name__}: {e}')
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError) as e:
        return Result('error', detail=f'inspect failed on {target}: {e}')
    actual_params = list(sig.parameters.keys())
    missing = [p for p in expected_params if p not in actual_params]
    if missing:
        return Result('fail',
                      expected=f'params include {expected_params}',
                      actual=f'params are {actual_params}',
                      detail=f'missing: {missing}')
    return Result('pass',
                  expected=f'params include {expected_params}',
                  actual=f'params are {actual_params}')


def resolve_command_output(args: dict) -> Result:
    """Run a command via subprocess (NOT shell=True). Assert exit code and/or
    stdout substring. Replaces v1's `eval` resolver, which executed arbitrary
    Python from the markdown — a critical RCE surface.

    Args:
        cmd               required; shlex-split, run with shell=False
        exit              expected exit code
        stdout-contains   expected substring of stdout
        timeout           seconds, default 10
    """
    import shlex
    import subprocess

    cmd_str = args.get('cmd')
    if not cmd_str:
        return Result('error', detail='no cmd given')
    try:
        argv = shlex.split(cmd_str)
    except ValueError as e:
        return Result('error', detail=f'cmd parse: {e}')
    try:
        timeout = int(args.get('timeout', '10'))
    except ValueError:
        return Result('error', detail=f'bad timeout {args.get("timeout")!r}')

    cwd = args.get('_cwd')  # injected by driver from the markdown file's dir
    try:
        proc = subprocess.run(
            argv, cwd=cwd, capture_output=True, text=True,
            timeout=timeout, check=False,
        )
    except FileNotFoundError as e:
        return Result('stale', detail=f'command not found: {e}')
    except subprocess.TimeoutExpired:
        return Result('error', detail=f'timed out after {timeout}s')
    except Exception as e:
        return Result('error', detail=f'{type(e).__name__}: {e}')

    failures = []
    if 'exit' in args:
        try:
            want = int(args['exit'])
        except ValueError:
            return Result('error', detail=f'bad exit {args["exit"]!r}')
        if proc.returncode != want:
            failures.append(f'exit={proc.returncode} want={want}')
    if 'stdout-contains' in args:
        needle = args['stdout-contains']
        if needle not in proc.stdout:
            failures.append(f'stdout missing {needle!r}')
    if 'stderr-contains' in args:
        needle = args['stderr-contains']
        if needle not in proc.stderr:
            failures.append(f'stderr missing {needle!r}')

    assertion_keys = ('exit', 'stdout-contains', 'stderr-contains')
    if not any(k in args for k in assertion_keys):
        return Result('error',
                      detail='no assertions (need exit / stdout-contains / stderr-contains)')

    actual = f'exit={proc.returncode} stdout={len(proc.stdout)}B stderr={len(proc.stderr)}B'
    if failures:
        expected = '; '.join(f'{k}={v}' for k, v in args.items()
                             if k in assertion_keys)
        return Result('fail', expected=expected, actual=actual,
                      detail='; '.join(failures))
    return Result('pass', expected='assertions met', actual=actual)


RESOLVERS: dict[str, Callable[[dict], Result]] = {
    'pr-state':        resolve_pr_state,
    'issue-state':     resolve_issue_state,
    'signature':       resolve_signature,
    'command-output':  resolve_command_output,
}


# ─── driver ───────────────────────────────────────────────────────────────────

SYMBOL = {'pass': '✓', 'fail': '✗', 'stale': '⚠', 'error': '!'}
COLOR  = {'pass': '\033[32m', 'fail': '\033[31m',
          'stale': '\033[33m', 'error': '\033[35m'}
RESET  = '\033[0m'


def verify_file(path: str, json_out: bool = False) -> int:
    with open(path, encoding='utf-8') as f:
        text = f.read()
    file_dir = os.path.dirname(os.path.abspath(path))
    claims = parse_claims(text)
    results = []
    for c in claims:
        # Inject cwd for command-output so relative paths in cmd resolve from
        # the directory containing the markdown file.
        if c.type == 'command-output':
            c.args.setdefault('_cwd', file_dir)
        resolver = RESOLVERS.get(c.type)
        r = resolver(c.args) if resolver else \
            Result('error', detail=f'unknown claim type {c.type!r}')
        results.append((c, r))

    if json_out:
        print(json.dumps([{
            'line': c.line, 'type': c.type, 'args': c.args,
            'context': c.context, 'status': r.status,
            'expected': r.expected, 'actual': r.actual, 'detail': r.detail,
        } for c, r in results], indent=2))
    else:
        use_color = sys.stdout.isatty()
        for c, r in results:
            sym = SYMBOL[r.status]
            if use_color:
                head = f'{COLOR[r.status]}{sym} {r.status.upper():<5}{RESET}'
            else:
                head = f'{sym} {r.status.upper():<5}'
            ctx = c.context[:75] + ('…' if len(c.context) > 75 else '')
            print(f'{head} L{c.line:<3} [{c.type}] {ctx}')
            if r.status != 'pass':
                if r.expected: print(f'         expected: {r.expected}')
                if r.actual:   print(f'         actual:   {r.actual}')
                if r.detail:   print(f'         {r.detail}')
        counts: dict[str, int] = {}
        for _, r in results:
            counts[r.status] = counts.get(r.status, 0) + 1
        print()
        print(f'Summary: {len(results)} claim(s) — ' +
              ', '.join(f'{n} {s}' for s, n in sorted(counts.items())))

    return 0 if all(r.status == 'pass' for _, r in results) else 1


def main():
    args = sys.argv[1:]
    json_out = False
    if '--json' in args:
        json_out = True
        args.remove('--json')
    if len(args) != 1:
        print('usage: verso.py [--json] path/to/file.md', file=sys.stderr)
        return 2
    return verify_file(args[0], json_out=json_out)


if __name__ == '__main__':
    sys.exit(main())
