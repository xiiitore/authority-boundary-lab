import json
from pathlib import Path
import unittest
ROOT=Path(__file__).parents[1]
class PluginReleaseIntegrityContractTests(unittest.TestCase):
 def test_manifests_match_release_version(self):
  root=json.loads((ROOT/'plugin.json').read_text()); codex=json.loads((ROOT/'.codex-plugin'/'plugin.json').read_text())
  self.assertEqual(root['name'],'overalgorithm-engine'); self.assertEqual(root['version'],codex['version']); self.assertEqual(root['version'],'1.2.14')
 def test_release_transitions_are_explicit(self):
  s=(ROOT/'skills'/'07-release-gate'/'SKILL.md').read_text()
  for token in ['TARGET_RESOLVED','BASELINE_READ','PACKAGE_VALIDATED','RELEASE_RETURNED','RELEASE_READ_BACK']: self.assertIn(token,s)
 def test_release_mutation_is_not_runtime_validation(self):
  s=(ROOT/'skills'/'07-release-gate'/'SKILL.md').read_text(); self.assertIn('Do not infer runtime validation from release mutation or read-back',s); self.assertIn('Do not claim the full test suite passed when only targeted tests ran',s); self.assertIn('canonical task-class-specific gate catalog',s)
 def test_ambiguous_target_and_missing_readback_block_acceptance(self):
  s=(ROOT/'skills'/'07-release-gate'/'SKILL.md').read_text(); self.assertIn('do not create a new plugin to evade target ambiguity',s); self.assertIn('status is BLOCKED/UNKNOWN/REVISE rather than PASS',s)
 def test_loop_and_execution_claims_are_release_gated(self):
  s=(ROOT/'skills'/'07-release-gate'/'SKILL.md').read_text(); self.assertIn('trace completeness is not established, use UNKNOWN',s); self.assertIn('Loop detection coverage is UNKNOWN',s)
if __name__=='__main__': unittest.main()
