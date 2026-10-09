import unittest

from authz import AuthorizationError, Grant, PolicyEngine, Principal


class PolicyEngineTests(unittest.TestCase):
    def setUp(self):
        self.policy = PolicyEngine([
            Grant("reader", "read", "reports"),
            Grant("admin", "delete", "reports"),
        ])
        self.reader = Principal("alice", frozenset({"reader"}))
        self.admin = Principal("bob", frozenset({"admin"}))

    def test_explicit_grant_allows_exact_action_and_resource(self):
        self.assertTrue(self.policy.authorize(self.reader, "read", "reports"))

    def test_deny_by_default_for_missing_role_action_or_resource(self):
        self.assertFalse(self.policy.authorize(self.reader, "delete", "reports"))
        self.assertFalse(self.policy.authorize(self.reader, "read", "secrets"))
        self.assertFalse(self.policy.authorize(self.admin, "read", "reports"))

    def test_revocation_blocks_previously_allowed_principal(self):
        self.assertTrue(self.policy.authorize(self.reader, "read", "reports"))
        self.policy.revoke_subject("alice")
        self.assertFalse(self.policy.authorize(self.reader, "read", "reports"))
        self.policy.restore_subject("alice")
        self.assertTrue(self.policy.authorize(self.reader, "read", "reports"))

    def test_restore_rejects_invalid_subject(self):
        for subject in ("", " ", None, 42):
            with self.subTest(subject=subject):
                with self.assertRaises(ValueError):
                    self.policy.restore_subject(subject)

    def test_require_raises_without_leaking_policy_details(self):
        with self.assertRaisesRegex(AuthorizationError, "^access denied$"):
            self.policy.require(self.reader, "delete", "reports")

    def test_resource_isolation_and_audit(self):
        self.policy.authorize(self.reader, "read", "reports")
        self.policy.authorize(self.reader, "read", "secrets")
        events = self.policy.audit_snapshot()
        self.assertEqual(len(events), 2)
        self.assertTrue(events[0]["allowed"])
        self.assertFalse(events[1]["allowed"])
        events[0]["allowed"] = False
        self.assertTrue(self.policy.audit_snapshot()[0]["allowed"])

    def test_invalid_identity_and_grants_rejected(self):
        with self.assertRaises(ValueError):
            Principal(" ", frozenset({"reader"}))
        with self.assertRaises(TypeError):
            Principal("alice", {"reader"})
        with self.assertRaises(ValueError):
            self.policy.add_grant(Grant("reader", "", "reports"))

    def test_grants_can_be_added_explicitly(self):
        self.policy.add_grant(Grant("reader", "write", "reports"))
        self.assertTrue(self.policy.authorize(self.reader, "write", "reports"))


if __name__ == "__main__":
    unittest.main()
