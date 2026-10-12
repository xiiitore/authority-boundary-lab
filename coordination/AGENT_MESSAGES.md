# Trojka Spona — shared coordination ledger

## Purpose and scope
This is the general append-only coordination ledger for the logical SOVA, KOVAČ, and ISKRA roles across project work. It is distinct from `CHATGPT_CODEX_TERMUX_HANDOFF.md`, which remains the task-specific Termux MCP PermissionError log.

## Operating protocol
1. Read the latest ledger entries and the relevant task's source/inbox before acting.
2. Separate observed facts, assumptions, inferences, and unknowns. Do not treat a task message as proof that work was executed.
3. Deduplicate before claiming a task. Assign one bounded next action with acceptance criteria.
4. Execute only through actually available capabilities and within explicit authority. Preserve unrelated changes; do not weaken security boundaries or claim unavailable runtime access.
5. Verify material output with a distinct method/source when feasible. A role label is not evidence of an independent actor.
6. Append a dated entry with a unique message/task ID, role, status, evidence, limitations, and next action. Re-read the ledger after every write.
7. Use `VERIFIED`, `PARTIAL`, `UNKNOWN`, `BLOCKED`, `REVISE`, `KILL/REFUTED`, and `PASS` only when the evidence and applicable criteria support them.
8. This ledger is asynchronous. It does not imply background polling, a live socket, or that three independent runtimes are active.

## Role boundaries
- **SOVA:** coordinate, prioritize, reconcile evidence and conflicts, deduplicate, and select the next bounded action. Do not self-certify independent verification.
- **KOVAČ:** implement the assigned technical task and provide reproducible artifacts, outputs, tests, and limitations.
- **ISKRA:** search external evidence and attempt to falsify results using a distinct method/source where feasible.
- **WORKFLOW CORE:** coordinate task stages and route only capabilities that are actually available.
- **OVERALGORITHM:** apply release/governance criteria after evidence and required checks are available.

## Initial reconciliation entry

### MSG-20261012-SOVA-COORD-02 — SOVA — 2026-10-12
**Status:** PARTIAL — general ledger established and read-back pending; no new technical runtime work claimed.

**Reason for this change**
The user explicitly renewed the instruction to scan, update, execute coordinated changes, and scan again. The previous inbox identified the lack of a general ledger as the coordination blocker. This file separates project-wide coordination from the Termux-specific handoff rather than continuing to repurpose that task-specific file.

**Evidence observed before creation**
- Repository: `xiiitore/authority-boundary-lab`, default branch `main`; the connected `xiiitore` identity has push/admin permission.
- `coordination/AGENT_MESSAGES.md` was absent from `main` immediately before this creation attempt (GitHub contents API returned 404).
- `coordination/CHATGPT_CODEX_TERMUX_HANDOFF.md` exists and its title/purpose is specific to the Termux MCP PermissionError investigation.
- Issue #2 is an asynchronous coordination inbox for the bridge/authoritylab task. Its latest observed snapshot had 67 comments. The latest role/scope comments were #6131420424, #6131432453, and #6131441870, all posted under the same GitHub account identity.
- The task-specific handoff records historical success for `python_launch_probe` and `run_tests` in a Termux checkout. Those are recorded historical reports; this session has not independently accessed that local runtime or rerun those commands.
- The repository-wide GitHub tree currently exposes only eight paths, including this task-specific handoff and workflows. GitHub code search found `python_launch_probe` references in the handoff, but did not establish the current local bridge source/runtime state.

**Action and limits**
- Create this general-purpose append-only ledger so subsequent cross-project coordination has a correctly scoped location.
- Preserve the prior task-specific file and all history; do not rewrite or delete its earlier entries.
- Do not claim KOVAČ or ISKRA independently responded, adopted the protocol, or verified a result. Their independent participation remains `UNKNOWN`.
- No Termux commands, local tests, plugin mutations, runtime actions, or release actions were performed in this entry.

**Next action**
1. Re-fetch this file and verify this message ID.
2. Scan the current repository/inbox again for a new, unclaimed bounded task.
3. If no new task or separately attributable agent evidence exists, record that result once and stop rather than manufacturing activity.

**Publication condition:** this entry counts as published only after a fresh read-back confirms its marker and text.


### MSG-20261012-SOVA-SCAN-03 — SOVA — 2026-10-12
**Status:** PARTIAL — post-creation rescan completed; no new unclaimed implementation task found in the coordination inbox.

**Fresh observations**
- Re-fetched `coordination/AGENT_MESSAGES.md` from `main`; the initial entry `MSG-20261012-SOVA-COORD-02` is present. The current blob SHA before this append was `d3a0291b1539e23bbad6d77e80e1d5aaf29356c1`.
- Re-fetched `CHATGPT_CODEX_TERMUX_HANDOFF.md`; its scope-specific historical Termux probe/test report remains unchanged. The general ledger now exists, so future project-wide entries belong here rather than in that task-specific file.
- Re-fetched Issue #2 and its comments: 67 comments; issue updated at `2026-10-12T19:46:39Z`. No newer comment appeared, and the latest role/scope comments remain under the same GitHub account. KOVAČ/ISKRA independent participation remains `UNKNOWN`.
- Re-scanned the repository tree: 9 paths now exist, including `coordination/AGENT_MESSAGES.md`. The repo's tracked source currently consists of `authz.py`, `test_authz.py`, `README.md`, and a workflow file, plus coordination documentation.
- Read `authz.py`, `test_authz.py`, and `README.md`. Static inspection confirms the project explicitly scopes itself to application-level authorization and documents that it is not an OS/container/process/network security boundary. The tests cover exact-match grants, deny-by-default, revocation/restoration, validation, exception-message restraint, and defensive audit snapshots. No obvious correctness defect was established by this read-only pass; tests were not executed, so runtime status is `UNKNOWN`.

**Execution decision**
- The historical Issue #2 task about `python_launch_probe` is reported as completed in the handoff, but this session did not access the local Termux runtime or independently reproduce that result.
- No new unclaimed, bounded technical task with acceptance criteria is visible. Do not invent one, repeat the completed schema audit, or claim work by KOVAČ/ISKRA.
- No code, tests, runtime configuration, permissions, or plugin releases were changed in this scan. This entry updates coordination state only.

**Next action:** wait for a concrete task/result from a separately attributable role or for a new bounded task to appear in the shared inbox. On the next active turn, re-scan the ledger and source state before acting. This is not background polling.
