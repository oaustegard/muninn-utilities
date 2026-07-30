"""Tests for muninn_utils.gh_proxy — no live credentials, no network.

Covers the two things that actually broke in production:
  1. the placeholder GH_TOKEN the container injects, which passes a naive
     presence check and then 401s at GitHub
  2. the SECOND Anthropic interception message (GraphQL-specific), which does
     not mention add_repo and so defeated an add_repo-keyed detector
"""
import json
import sys
import unittest
from unittest import mock

sys.path.insert(0, '/home/claude/muninn-utilities')

from muninn_utils import gh_proxy


REPO_SCOPE_403 = json.dumps({
    "message": "GitHub access to this repository is not enabled for this session. "
               "Use add_repo to request access.",
    "documentation_url": "https://docs.anthropic.com/en/docs/claude-code/github-actions",
}).encode()

GRAPHQL_403 = json.dumps({
    "message": "This GraphQL query is not enabled for this session — only the "
               "pinned set of PR-review operations is served. Use REST via "
               "`gh api repos/{owner}/{repo}/...` instead.",
    "documentation_url": "https://docs.anthropic.com/en/docs/claude-code/github-actions",
}).encode()

GITHUB_401 = json.dumps({
    "message": "Bad credentials",
    "documentation_url": "https://docs.github.com/rest",
}).encode()

REAL_PAT = "github_pat_" + "x" * 40


class TestTokenValidation(unittest.TestCase):
    def test_placeholder_rejected(self):
        # The regression that made every presence check lie.
        self.assertFalse(gh_proxy.valid_token("proxy-injected"))

    def test_empty_and_junk_rejected(self):
        for bad in (None, "", "   ", "none", "NULL", "unset", "hunter2"):
            self.assertFalse(gh_proxy.valid_token(bad), bad)

    def test_real_pats_accepted(self):
        for good in (REAL_PAT, "ghp_" + "y" * 36, "ghs_" + "z" * 36):
            self.assertTrue(gh_proxy.valid_token(good), good)

    def test_env_placeholder_falls_through_to_file(self):
        env = {"GH_TOKEN": "proxy-injected"}
        envfile = f"GH_TOKEN={REAL_PAT}\n"
        with mock.patch.dict(gh_proxy.os.environ, env, clear=False), \
             mock.patch("builtins.open", mock.mock_open(read_data=envfile)):
            self.assertEqual(gh_proxy._gh_token(), REAL_PAT)

    def test_no_valid_token_anywhere_raises(self):
        with mock.patch.dict(gh_proxy.os.environ, {"GH_TOKEN": "proxy-injected"}, clear=False), \
             mock.patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(gh_proxy.GitHubTransportError) as cm:
                gh_proxy._gh_token()
            self.assertIn("placeholder", str(cm.exception))


class TestInterceptionDetection(unittest.TestCase):
    def test_repo_scope_403_detected(self):
        self.assertTrue(gh_proxy._intercepted(403, REPO_SCOPE_403))

    def test_graphql_403_detected(self):
        # The one an add_repo-keyed detector misses. This is the whole bug.
        self.assertNotIn(b"add_repo", GRAPHQL_403)
        self.assertTrue(gh_proxy._intercepted(403, GRAPHQL_403))

    def test_github_own_401_not_treated_as_interception(self):
        self.assertFalse(gh_proxy._intercepted(401, GITHUB_401))

    def test_worker_forbidden_not_treated_as_interception(self):
        self.assertFalse(gh_proxy._intercepted(403, b"forbidden"))

    def test_genuine_github_403_not_treated_as_interception(self):
        body = json.dumps({"message": "Resource not accessible by personal access token",
                           "documentation_url": "https://docs.github.com/rest"}).encode()
        self.assertFalse(gh_proxy._intercepted(403, body))


class TestFallback(unittest.TestCase):
    def setUp(self):
        gh_proxy._state["force_proxy"] = False
        gh_proxy._state["proxy_key"] = "test-key"
        self.env = mock.patch.dict(gh_proxy.os.environ,
                                   {"GH_TOKEN": REAL_PAT}, clear=False)
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_direct_success_skips_proxy(self):
        with mock.patch.object(gh_proxy, "_request",
                               return_value=(200, b'{"ok":true}')) as req:
            status, raw = gh_proxy.call("/rate_limit")
        self.assertEqual(status, 200)
        self.assertEqual(req.call_count, 1)
        self.assertIn(gh_proxy.API, req.call_args[0][0])
        self.assertFalse(gh_proxy._state["force_proxy"])

    def test_graphql_interception_falls_back_and_latches(self):
        calls = []

        def fake(url, **kw):
            calls.append(url)
            if url.startswith(gh_proxy.API):
                return 403, GRAPHQL_403
            return 200, b'{"data":{"viewer":{"login":"oaustegard"}}}'

        with mock.patch.object(gh_proxy, "_request", side_effect=fake):
            data = gh_proxy.graphql("{ viewer { login } }")
            self.assertEqual(data["viewer"]["login"], "oaustegard")
            self.assertTrue(gh_proxy._state["force_proxy"])
            # Latched: the next call must not retry the dead direct path.
            gh_proxy.graphql("{ viewer { login } }")

        self.assertEqual(sum(u.startswith(gh_proxy.API) for u in calls), 1)
        self.assertEqual(sum(u.startswith(gh_proxy.PROXY) for u in calls), 2)

    def test_proxy_key_rejection_raises_clearly(self):
        def fake(url, **kw):
            if url.startswith(gh_proxy.API):
                return 403, REPO_SCOPE_403
            return 403, b"forbidden\n"

        with mock.patch.object(gh_proxy, "_request", side_effect=fake):
            with self.assertRaises(gh_proxy.GitHubTransportError) as cm:
                gh_proxy.rest("/repos/oaustegard/muninns-inbox")
        self.assertIn("X-Proxy-Key", str(cm.exception))

    def test_graphql_query_errors_raise(self):
        with mock.patch.object(gh_proxy, "_request",
                               return_value=(200, b'{"errors":[{"message":"nope"}]}')):
            with self.assertRaises(gh_proxy.GitHubTransportError) as cm:
                gh_proxy.graphql("{ bad }")
        self.assertIn("nope", str(cm.exception))

    def test_proxy_call_carries_both_auth_headers(self):
        seen = {}

        def fake(url, **kw):
            if url.startswith(gh_proxy.API):
                return 403, REPO_SCOPE_403
            seen.update(kw["headers"])
            return 200, b"{}"

        with mock.patch.object(gh_proxy, "_request", side_effect=fake):
            gh_proxy.rest("/repos/oaustegard/muninns-inbox")

        self.assertEqual(seen["X-Proxy-Key"], "test-key")
        self.assertEqual(seen["Authorization"], f"Bearer {REAL_PAT}")
        self.assertEqual(seen["User-Agent"], gh_proxy.UA)



class TestProxyKeyParsing(unittest.TestCase):
    """The ops config value carries usage docs after the key. Passing the whole
    thing as a header raises UnicodeEncodeError on the first em-dash, because
    HTTP headers are latin-1. Regression from expanding the ops entry."""

    DOCUMENTED = (
        "p1o6mUPSeQCNmkVYUmFrPYp0nupAqOrNSY5o8uyoxnk\n"
        "\n"
        "GH-API-PROXY \u2014 X-Proxy-Key above.\n"
        "FULL PASSTHROUGH \u2014 any method, ANY PATH \u2014 including /graphql.\n"
    )

    def test_extracts_key_from_documented_value(self):
        self.assertEqual(gh_proxy.parse_proxy_key(self.DOCUMENTED),
                         "p1o6mUPSeQCNmkVYUmFrPYp0nupAqOrNSY5o8uyoxnk")

    def test_extracted_key_is_header_safe(self):
        key = gh_proxy.parse_proxy_key(self.DOCUMENTED)
        key.encode("latin-1")  # would raise before the fix

    def test_bare_key_still_works(self):
        self.assertEqual(gh_proxy.parse_proxy_key("  abcdefghij0123456789  "),
                         "abcdefghij0123456789")

    def test_prose_only_value_raises_clearly(self):
        with self.assertRaises(gh_proxy.GitHubTransportError) as cm:
            gh_proxy.parse_proxy_key("see the worker source \u2014 no key here")
        self.assertIn("no line that looks like a key", str(cm.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
