import json
from pathlib import Path
import unittest

from algorithms.release_decision_verifier import verify_decision_contract

ROOT = Path(__file__).parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "release-decision-v2.schema.json").read_text())
LEGACY = {
    "decision_id": "D-1",
    "task_class": "plugin-release",
    "required_gates": [{"id": "tests", "required": True, "status": "PASS", "evidence_ids": ["TEST-1"]}],
    "independent_audit": {"status": "PASS", "evidence_ids": ["AUDIT-1"]},
    "blockers": [],
    "decision": "PASS",
}


def release_record():
    return {
        "schema_version": 2, "decision_id": "D2-1", "task_class": "plugin-release",
        "decision_scope": "RELEASE", "final_status": "PASS", "runtime_policy": "REQUIRED",
        "runtime_status": "PASS", "runtime_evidence_refs": ["RUNTIME-1"],
        "runtime_policy_evidence_refs": ["POLICY-1"],
        "package_checks": [{"id": "package-tests", "status": "PASS", "evidence_refs": ["PKG-1"]}],
        "readback_checks": [{"id": "readback", "status": "PASS", "evidence_refs": ["READ-1"]}],
        "required_gates": [{"id": "tests", "required": True, "status": "PASS", "evidence_refs": ["TEST-1"]}],
        "independent_audit": {"status": "PASS", "evidence_refs": ["AUDIT-1"]},
        "blockers": [],
    }


CATALOG = {"plugin-release": [{"id": "tests", "required": True}]}
REF = "catalog-review-2026-10-12"


class ReleaseDecisionVerifierTests(unittest.TestCase):
    def verify(self, record=None, catalog=CATALOG, ref=REF):
        return verify_decision_contract(record or release_record(),
                                       canonical_gate_catalog=catalog,
                                       catalog_evidence_ref=ref)

    def test_exact_catalog_match_passes_contract_only(self):
        result = self.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["release_acceptance_authorized"])

    def test_missing_catalog_is_unknown(self):
        result = self.verify(catalog=None)
        self.assertEqual(result["status"], "UNKNOWN")

    def test_missing_catalog_provenance_is_unknown(self):
        result = self.verify(ref=" UNKNOWN ")
        self.assertEqual(result["status"], "UNKNOWN")

    def test_whitespace_padded_catalog_gate_id_is_blocked(self):
        catalog = {"plugin-release": [{"id": " tests ", "required": True}]}
        self.assertEqual(self.verify(catalog=catalog)["status"], "BLOCKED")

    def test_whitespace_padded_decision_gate_id_is_blocked(self):
        record = release_record()
        record["required_gates"][0]["id"] = " tests "
        self.assertEqual(self.verify(record)["status"], "BLOCKED")

    def test_whitespace_padded_catalog_provenance_is_unknown(self):
        result = self.verify(ref=" catalog-review-2026-10-12 ")
        self.assertEqual(result["status"], "UNKNOWN")

    def test_missing_required_gate_is_revise(self):
        result = self.verify(catalog={"plugin-release": [
            {"id": "tests", "required": True}, {"id": "independent-audit", "required": True}]})
        self.assertEqual(result["status"], "REVISE")
        self.assertTrue(any("missing catalog gate IDs" in e for e in result["errors"]))

    def test_extra_gate_not_in_catalog_is_revise(self):
        record = release_record()
        record["required_gates"].append({"id": "unlisted", "required": False, "status": "UNKNOWN", "evidence_refs": []})
        self.assertEqual(self.verify(record)["status"], "REVISE")

    def test_duplicate_decision_gate_id_is_blocked(self):
        record = release_record()
        record["required_gates"].append(dict(record["required_gates"][0]))
        self.assertEqual(self.verify(record)["status"], "BLOCKED")

    def test_duplicate_catalog_gate_id_is_blocked(self):
        catalog = {"plugin-release": [{"id": "tests", "required": True},
                                      {"id": "tests", "required": True}]}
        self.assertEqual(self.verify(catalog=catalog)["status"], "BLOCKED")

    def test_required_flag_mismatch_is_revise(self):
        catalog = {"plugin-release": [{"id": "tests", "required": False}]}
        self.assertEqual(self.verify(catalog=catalog)["status"], "REVISE")

    def test_unknown_task_class_is_unknown(self):
        self.assertEqual(self.verify(catalog={"other-task": [{"id": "tests", "required": True}]})["status"], "UNKNOWN")

    def test_legacy_v1_pass_cannot_be_promoted(self):
        result = self.verify(LEGACY)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["release_acceptance_authorized"])
        self.assertTrue(any("historical-only" in e for e in result["errors"]))

    def test_invalid_schema_record_is_blocked(self):
        record = release_record()
        record["unexpected"] = "PASS"
        self.assertEqual(self.verify(record)["status"], "BLOCKED")

    def test_catalog_must_use_boolean_required_flags(self):
        catalog = {"plugin-release": [{"id": "tests", "required": "true"}]}
        self.assertEqual(self.verify(catalog=catalog)["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
