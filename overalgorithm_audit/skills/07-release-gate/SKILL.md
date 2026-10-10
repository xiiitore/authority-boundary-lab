---
name: release-gate
description: Convert traceable requirements and executed evidence into a strict PASS, BLOCKED, UNKNOWN, REVISE, FAIL, PARTIAL, VERIFIED, REFUTED, or KILL decision.
---
# Release Gate v1.2.12

## PASS prerequisites
PASS requires task classification, all applicable mandatory operations executed and validated, adequate provenance, relevant calculations/literature/identifiability checks, resolved conflicts, applicable regression/adversarial checks, no unsupported inference, no critical security/privacy issues, independent audit, and rollback baseline where required. If a mandatory gate is missing, unexecuted, unverifiable, or blocked: do not issue PASS/ACCEPT.

## Plugin release integrity gate
For plugin create/update, track these distinct transitions: `TARGET_RESOLVED -> BASELINE_READ -> PACKAGE_VALIDATED -> UPDATE_REQUESTED -> RELEASE_RETURNED -> RELEASE_READ_BACK -> ACCEPTED/REJECTED`.
Before update, record exact plugin ID, current version, release ID, scope, and changed files. Use the exact current release ID as the expected-release guard. Do not update an ambiguous target; do not create a new plugin to evade target ambiguity.
Before upload, validate archive contents, manifest identity, synchronized manifest versions, schema/field limits, and target tests. Preserve a rollback baseline or prior release ID. Failed package/test checks block upload.
After update, read metadata and changed files back. Verify plugin ID, version/release advancement, intended changes, and actual test execution. Distinguish package checks, target tests, release mutation, read-back, and runtime validation.
Do not infer runtime validation from release mutation or read-back. Do not claim the full test suite passed when only targeted tests ran. If read-back fails, identity mismatches, or evidence is incomplete, status is BLOCKED/UNKNOWN/REVISE rather than PASS.

## Structured release decisions
Validate against `schemas/release-decision.schema.json`. The schema has distinct legacy v1 and schema_version=2 branches. Legacy v1 is historical only and cannot prove v2 acceptance. `PACKAGE_PASS` is limited to package scope and never means release PASS/VERIFIED. Release PASS/VERIFIED requires passing package checks, read-back checks, all required gates with evidence, independent audit with evidence, no blockers, and resolved runtime policy: REQUIRED means runtime PASS plus evidence; NOT_REQUIRED means NOT_APPLICABLE plus policy evidence. UNKNOWN runtime policy cannot support release PASS.
The schema checks structure and status consistency; RELEASE PASS/VERIFIED must include at least one gate declared required. The verifier must reconcile gate IDs and required flags against the canonical task-class-specific gate catalog; a self-declared or incomplete list is not proof of gate completeness. The schema does not prove evidence authenticity, provenance, freshness, relevance, or actual host-runtime execution.

Allowed statuses: PASS, BLOCKED, UNKNOWN, REVISE, FAIL, PARTIAL, VERIFIED, REFUTED, KILL, POTENTIAL NOVEL RESULT. POTENTIAL NOVEL RESULT additionally requires passing literature and identifiability audits with evidence.
