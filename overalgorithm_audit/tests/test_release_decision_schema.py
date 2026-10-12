import json
from pathlib import Path
import unittest
import jsonschema
ROOT=Path(__file__).parents[1]
SCHEMA=json.loads((ROOT/"schemas/release-decision.schema.json").read_text())
V1=json.loads((ROOT/"schemas/release-decision-v1.schema.json").read_text())
V2=json.loads((ROOT/"schemas/release-decision-v2.schema.json").read_text())
LEGACY={"decision_id":"D-1","task_class":"plugin-release","required_gates":[{"id":"tests","required":True,"status":"PASS","evidence_ids":["TEST-1"]}],"independent_audit":{"status":"PASS","evidence_ids":["AUDIT-1"]},"blockers":[],"decision":"PASS"}
def release_record():
 return {"schema_version":2,"decision_id":"D2-1","task_class":"plugin-release","decision_scope":"RELEASE","final_status":"PASS","runtime_policy":"REQUIRED","runtime_status":"PASS","runtime_evidence_refs":["RUNTIME-1"],"runtime_policy_evidence_refs":["POLICY-1"],"package_checks":[{"id":"package-tests","status":"PASS","evidence_refs":["PKG-1"]}],"readback_checks":[{"id":"readback","status":"PASS","evidence_refs":["READ-1"]}],"required_gates":[{"id":"tests","required":True,"status":"PASS","evidence_refs":["TEST-1"]}],"independent_audit":{"status":"PASS","evidence_refs":["AUDIT-1"]},"blockers":[]}
def package_record():
 return {"schema_version":2,"decision_id":"D2-PKG","task_class":"plugin-package","decision_scope":"PACKAGE","final_status":"PACKAGE_PASS","runtime_policy":"UNKNOWN","runtime_status":"UNKNOWN","runtime_evidence_refs":[],"runtime_policy_evidence_refs":[],"package_checks":[{"id":"package-tests","status":"PASS","evidence_refs":["PKG-1"]}],"readback_checks":[],"required_gates":[{"id":"package-tests","required":True,"status":"PASS","evidence_refs":["PKG-1"]}],"independent_audit":{"status":"UNKNOWN","evidence_refs":[]},"blockers":[]}
class ReleaseDecisionSchemaTests(unittest.TestCase):
 def test_legacy_v1_validates_as_historical_record(self): jsonschema.validate(LEGACY,V1); jsonschema.validate(LEGACY,SCHEMA)
 def test_valid_release_v2_pass(self): jsonschema.validate(release_record(),SCHEMA)
 def test_wrapper_embedded_schemas_match_versioned_files(self):
  self.assertEqual(SCHEMA["oneOf"][0],V1); self.assertEqual(SCHEMA["oneOf"][1],V2)
 def test_valid_package_pass(self): jsonschema.validate(package_record(),SCHEMA)
 def test_package_scope_cannot_claim_release_pass(self):
  r=package_record(); r["final_status"]="PASS"
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_release_scope_cannot_use_package_pass(self):
  r=release_record(); r["final_status"]="PACKAGE_PASS"
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_v2_cannot_contain_legacy_decision_field(self):
  r=release_record(); r["decision"]="PASS"
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_legacy_record_cannot_mix_v2_fields(self):
  r=dict(LEGACY); r["schema_version"]=2
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_unknown_root_field_rejected(self):
  r=release_record(); r["unexpected_status"]="VERIFIED"
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_required_runtime_without_execution_cannot_pass(self):
  r=release_record(); r["runtime_status"]="NOT_RUN"; r["runtime_evidence_refs"]=[]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_not_required_runtime_requires_policy_evidence(self):
  r=release_record(); r["runtime_policy"]="NOT_REQUIRED"; r["runtime_status"]="NOT_APPLICABLE"; r["runtime_evidence_refs"]=[]; r["runtime_policy_evidence_refs"]=[]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_unknown_runtime_policy_cannot_pass(self):
  r=release_record(); r["runtime_policy"]="UNKNOWN"; r["runtime_status"]="UNKNOWN"; r["runtime_evidence_refs"]=[]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_missing_readback_blocks_release_pass(self):
  r=release_record(); r["readback_checks"]=[]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_unknown_required_gate_blocks_release_pass(self):
  r=release_record(); r["required_gates"][0]["status"]="UNKNOWN"; r["required_gates"][0]["evidence_refs"]=[]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_release_pass_requires_at_least_one_required_gate(self):
  r=release_record(); r["required_gates"]=[{"id":"OPTIONAL-PLACEHOLDER","required":False,"status":"UNKNOWN","evidence_refs":[]}]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_audit_without_evidence_cannot_pass(self):
  r=release_record(); r["independent_audit"]["evidence_refs"]=[]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_blockers_prevent_release_pass(self):
  r=release_record(); r["blockers"]=["unresolved"]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_sentinel_evidence_reference_rejected(self):
  r=release_record(); r["runtime_evidence_refs"]=["UNKNOWN"]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_mixed_case_sentinel_evidence_reference_rejected(self):
  r=release_record(); r["runtime_evidence_refs"]=["UnKnOwN"]
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_whitespace_padded_sentinel_references_are_rejected(self):
  for sentinel in (" UNKNOWN ", "\tN/A", "TBD ", " TODO\t"):
   with self.subTest(sentinel=sentinel):
    r=release_record(); r["runtime_evidence_refs"]=[sentinel]
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,V2)
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
    legacy=dict(LEGACY); legacy["decision_id"]=sentinel
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(legacy,V1)
 def test_whitespace_padded_ordinary_references_are_rejected_across_all_schemas(self):
  # Every field using $defs/ref must reject ordinary identifiers with outer whitespace.
  for value in (" RUNTIME-1 ", "\tEVIDENCE-1", "PACKAGE-ID\t"):
   with self.subTest(value=value):
    r=release_record(); r["decision_id"]=value
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,V2)
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
    r=release_record(); r["runtime_evidence_refs"]=[value]
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,V2)
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
    r=release_record(); r["package_checks"][0]["id"]=value
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,V2)
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
    legacy=dict(LEGACY); legacy["decision_id"]=value
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(legacy,V1)
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(legacy,SCHEMA)
    legacy=dict(LEGACY); legacy["required_gates"][0]["evidence_ids"]=[value]
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(legacy,V1)
    with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(legacy,SCHEMA)
 def test_unknown_nested_field_rejected(self):
  r=release_record(); r["package_checks"][0]["extra"]="mixed-version"
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
 def test_schema_version_must_be_two(self):
  r=release_record(); r["schema_version"]=1
  with self.assertRaises(jsonschema.ValidationError): jsonschema.validate(r,SCHEMA)
if __name__=="__main__": unittest.main()
