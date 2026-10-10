import unittest
from pathlib import Path
from algorithms.release_readback_gate import assess_readback

BASE = dict(
    target_plugin_id='plugin-A', returned_plugin_id='plugin-A', readback_plugin_id='plugin-A',
    baseline_release_id='rel-1', returned_release_id='rel-2', readback_release_id='rel-2',
    intended_change_present=True, mandatory_tests_passed=True, runtime_required=False,
    runtime_policy_evidence_refs=['policy-review-01'],
)

class ReleaseReadbackGateBehaviorTests(unittest.TestCase):
    def test_release_gate_skill_documents_runtime_policy_evidence_rule(self):
        skill = (Path(__file__).parents[1] / 'skills' / '07-release-gate' / 'SKILL.md').read_text()
        self.assertIn('# Release Gate v1.2.11', skill)
        self.assertIn('runtime_policy_evidence_refs', skill)
        self.assertIn('yields UNKNOWN, not PASS', skill)

    def test_matching_readback_passes_with_policy_evidence_when_runtime_not_required(self):
        self.assertEqual(assess_readback(**BASE), 'PASS')
    def test_not_required_without_policy_evidence_is_unknown(self):
        self.assertEqual(assess_readback(**{**BASE, 'runtime_policy_evidence_refs': []}), 'UNKNOWN')
    def test_not_required_with_missing_policy_evidence_is_unknown(self):
        args = {k:v for k,v in BASE.items() if k != 'runtime_policy_evidence_refs'}
        self.assertEqual(assess_readback(**args), 'UNKNOWN')
    def test_not_required_with_sentinel_policy_evidence_is_unknown(self):
        self.assertEqual(assess_readback(**{**BASE, 'runtime_policy_evidence_refs': ['UNKNOWN']}), 'UNKNOWN')
    def test_required_but_unexecuted_runtime_is_unknown(self):
        self.assertEqual(assess_readback(**{**BASE, 'runtime_required': True, 'runtime_executed': False}), 'UNKNOWN')
    def test_required_and_executed_runtime_passes_without_not_required_policy_ref(self):
        args = {**BASE, 'runtime_required': True, 'runtime_executed': True}
        args.pop('runtime_policy_evidence_refs')
        self.assertEqual(assess_readback(**args), 'PASS')
    def test_unknown_runtime_applicability_is_unknown(self):
        self.assertEqual(assess_readback(**{**BASE, 'runtime_required': None}), 'UNKNOWN')
    def test_wrong_readback_plugin_id_blocks(self):
        self.assertEqual(assess_readback(**{**BASE, 'readback_plugin_id': 'plugin-B'}), 'BLOCKED')
    def test_stale_or_unchanged_release_requires_revision(self):
        self.assertEqual(assess_readback(**{**BASE, 'returned_release_id':'rel-1', 'readback_release_id':'rel-1'}), 'REVISE')
    def test_readback_release_mismatch_requires_revision(self):
        self.assertEqual(assess_readback(**{**BASE, 'readback_release_id':'rel-1'}), 'REVISE')
    def test_missing_intended_change_requires_revision(self):
        self.assertEqual(assess_readback(**{**BASE, 'intended_change_present':False}), 'REVISE')
    def test_failed_mandatory_tests_block(self):
        self.assertEqual(assess_readback(**{**BASE, 'mandatory_tests_passed':False}), 'BLOCKED')
    def test_sentinel_identifiers_never_pass(self):
        for field in ('target_plugin_id','returned_plugin_id','readback_plugin_id','baseline_release_id','returned_release_id','readback_release_id'):
            for sentinel in ('UNKNOWN','unknown','null','None','N/A','TBD','unset','   '):
                with self.subTest(field=field, sentinel=sentinel):
                    self.assertEqual(assess_readback(**{**BASE, field:sentinel}), 'UNKNOWN')
    def test_non_boolean_runtime_policy_is_unknown(self):
        self.assertEqual(assess_readback(**{**BASE, 'runtime_required':'false'}), 'UNKNOWN')
    def test_missing_release_evidence_is_unknown(self):
        self.assertEqual(assess_readback(**{**BASE, 'readback_release_id':''}), 'UNKNOWN')
    def test_malformed_policy_evidence_is_unknown(self):
        for refs in ([''], ['TBD'], [None], 'policy-review-01', None):
            with self.subTest(refs=refs):
                self.assertEqual(assess_readback(**{**BASE, 'runtime_policy_evidence_refs':refs}), 'UNKNOWN')

if __name__ == '__main__': unittest.main()
