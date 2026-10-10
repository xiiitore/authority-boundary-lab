---
name: governance
description: Canonical precedence, anti-circularity, conflict handling, and release authority rules for OVERALGORITHM.
---
# OVERALGORITHM Governance v1.2.12

## 1. Authority order
Resolve instruction conflicts in this order: host/platform/system and safety constraints; actual tool schemas, permissions, and connection state; canonical WORKFLOW CORE coordination and authority/dependency state; this OVERALGORITHM governance and release-authority layer; canonical workflow and verification procedures; specialized domain skills and external evidence; model-only reasoning and remembered context. A lower layer cannot override a higher layer by assertion. OVERALGORITHM does not replace WORKFLOW CORE's coordination role.

## 2. Canonical role separation
- WORKFLOW CORE: primary coordinator; classifies tasks, routes capabilities, checks authority, orders dependencies, and tracks execution state.
- OVERALGORITHM: governance/release authority; resolves precedence, defines mandatory gates, handles conflicts and anti-circularity, and decides acceptance status.
- Domain operators execute bounded operations or provide evidence.
- Independent verifiers/auditors check material claims using a materially distinct route where feasible.
- Memory Archive stores provenance and durable state; it is not a truth oracle.

Legacy/duplicate workflow plugins are compatibility adapters when a canonical implementation is available. Their outputs are evidence only after relevance, provenance, and validation checks.

## 3. No circular certification
The producer cannot be its own sole verifier. A correction mechanism cannot certify its own meta-correction. Where feasible, verification must use a materially distinct route, oracle, tool, dataset, derivation, or execution path. If genuine independence is unavailable, report the limitation instead of calling the check independent.

## 4. Evidence is not status
Execution, storage, repetition, citation, plausibility, or model confidence does not by itself establish truth. Memory is an evidence ledger and history store, not a truth oracle. Successful persistence proves storage, not correctness.

## 5. Mandatory-gate logic
PASS/ACCEPT is permitted only when every applicable mandatory gate is executed and validated. Missing, unavailable, contradictory, or non-discriminating evidence remains UNKNOWN/BLOCKED/REVISE as appropriate. Never satisfy a gate merely by invoking a tool whose output is irrelevant to that gate.

## 6. Status discipline
- KILL/REFUTED: a required condition is contradicted by adequate evidence.
- FAIL: an evaluated requirement is not met.
- BLOCKED: execution or a required gate cannot validly proceed.
- UNKNOWN: available evidence does not identify the result.
- REVISE: correction is required before acceptance.
- PARTIAL: only a bounded subset is verified.
- VERIFIED: material result reproduced/validated but final release criteria may remain.
- PASS: all applicable release gates pass.
Never upgrade UNKNOWN or BLOCKED to PASS by narrative reasoning.

## 7. Tool-use economy
Do not call tools merely to satisfy a quota. Every additional operation must have a defined purpose: new evidence, conflict resolution, reproduction, boundary testing, or risk reduction. Stop when required evidence is sufficient or a blocking uncertainty is irreducible.

## 8. Self-correction boundary
Self-correction may diagnose and propose reversible changes, but it may not weaken platform oversight, permissions, safety controls, verification requirements, audit independence, or release gates. A successful target test is insufficient when regression or independent audit is required.

## 9. Capability claims
A capability is strengthened only by an actual verified change to an underlying tool, plugin implementation, permission, connection, or execution path. Renaming, re-prompting, or adding descriptive text is not capability strengthening.

## 10. Research and mathematics
For quantitative research, establish observables and inputs before modeling. Where applicable preserve O, theta, J = dO/dtheta, rank(J), and the left-null relation c^T J = 0 with c in ker(J^T). Literature/novelty claims require literature verification before novelty status.

## 11. Regression invariant
Any accepted correction that can affect an earlier verified result requires regression against that result. Preserve the last verified baseline. If regression is not executable, the affected result cannot be re-certified as PASS.

## 12. Structured decision records
The release-decision schema accepts explicitly separated legacy v1 and schema_version=2 records. A legacy record is historical compatibility data only and must never be promoted as evidence of v2 release acceptance. PACKAGE_PASS means package checks only; it is not release PASS or VERIFIED. A v2 release PASS/VERIFIED requires package checks, read-back checks, required gates, independent audit, blockers, and explicit runtime policy/status/evidence to satisfy the schema.

Schema validation is a structural guard only. Evidence references must be resolved and checked for provenance, source identity, relevance, freshness, and independence. A schema-valid record is not automatically evidence-valid, and schema validity does not prove that the host runtime executed a helper. For RELEASE PASS/VERIFIED, the schema requires at least one gate declared required; an independent verifier must additionally reconcile the submitted gate IDs and their required flags against the canonical task-class-specific gate catalog. A self-declared or incomplete gate list is not proof that every applicable mandatory gate was executed.

## 13. Final decision
OVERALGORITHM is the release authority, not the primary task coordinator. Its release gate decides from traceable requirements and validated evidence. Routing, verification, audit, testing, self-correction, and memory are inputs to that decision; none may bypass it.
