import json
from pathlib import Path
import unittest
ROOT=Path(__file__).parents[1]
class GovernanceVersionContractTests(unittest.TestCase):
 def test_governance_heading_matches_both_manifests(self):
  root=json.loads((ROOT/'plugin.json').read_text()); codex=json.loads((ROOT/'.codex-plugin'/'plugin.json').read_text()); skill=(ROOT/'skills'/'00-governance'/'SKILL.md').read_text()
  self.assertEqual(root['version'],codex['version']); self.assertIn(f"OVERALGORITHM Governance v{root['version']}",skill)
if __name__=='__main__': unittest.main()
