# ChatGPT ↔ Codex ↔ Termux Coordination Log

**Purpose:** durable handoff for the active Termux MCP PermissionError: [Errno 13] investigation.

## Current verified state (2026-10-10)

- The MCP server's python_launch_probe returned PermissionError, errno=13.
- Python launches successfully from the ordinary Termux shell: `$HOME/mcp-venv/bin/python -c 'print("PYTHON_LAUNCH_OK")'`.
- process_launch_probe successfully launched /system/bin/true; that does not prove Python subprocess execution works.
- A temporary python_launch_diagnostics endpoint was added locally, but the latest report said it was not yet registered in the active MCP session.
- Root cause is UNKNOWN. Do not assert SELinux or another cause without evidence.
- Target local workspace reported by the user/Codex: `$HOME/authoritylab-mcp-test`. MCP server module: `authoritylab.termux_mcp_server`.

## Message to Codex

Please read this file and continue autonomously from the current working tree. First inspect the current git status and diff; preserve unrelated/uncommitted work. Safely make the diagnostic endpoint available in the active MCP session, using the least disruptive reload/reconnect procedure. Do not kill all Codex or MCP processes. Capture the complete exception message and identify the exact failing operation/stage. Then fix the actual cause with the smallest safe change, and run targeted tests followed by the relevant suite. Never weaken permissions or bypass security controls merely to make a test pass.

Before claiming success, independently verify:
1. Python subprocess launch from the MCP tool;
2. the affected test path;
3. `git diff --check`;
4. no unrelated user changes were overwritten;
5. final git status and changed-file list.

If blocked by an approval or an unavailable tool, continue all safe independent work and report the exact blocker and minimum approval needed. Do not commit, push, merge, delete, or perform other irreversible repository actions without explicit approval.

## Message to Termux / operator

Keep the existing Termux and Codex sessions intact. Do not kill broad process groups. If a restart is required, identify the exact server/session and explain why before requesting approval. Preserve diagnostic output and the current diff until the root cause and regression checks are recorded.

## Update protocol

Append dated entries below; do not rewrite earlier observations. Mark every claim as verified, hypothesis, or unknown. Include commands/tool calls and their actual outputs where material.

### Log

- 2026-10-10 — ChatGPT created this handoff from the known conversation state. No new local Termux command was executed by ChatGPT; local state must be rechecked by Codex.


### Log — continuation (2026-10-10)

- VERIFIED — GitHub handoff was fetched from xiiitore/authority-boundary-lab, main, path coordination/CHATGPT_CODEX_TERMUX_HANDOFF.md. The GitHub App's issue search for PermissionError returned no matching issues. The direct web/curl attempts failed (web cache miss; curl HTTP 404), so the authenticated GitHub file fetch was used.
- VERIFIED — Termux checkout $HOME/authoritylab-mcp-test has root /data/data/com.termux/files/home/authoritylab-mcp-test, branch codex/termux-process-diagnostics, latest commit abe23d8 (Sanitize subprocess startup error messages). Before this continuation it already had user changes in termux_mcp_server.py and termux_workspace_tools.py; these were preserved.
- VERIFIED — Earlier controlled launch comparisons showed the configured LD_PRELOAD value libpython3.13.so failed to launch the Python child with PermissionError errno 13; no preload also failed in that process context; Termux libtermux-exec.so succeeded. The MCP configuration was changed, with user approval from the earlier session, to the verified Termux exec library. No permissions or SELinux settings were changed.
- VERIFIED — After a fresh Termux MCP connection, status listed python_launch_probe and process_launch_probe. python_launch_probe returned {"started":true,"exit_status":0}.
- VERIFIED — A targeted SubprocessHandlerRunner unittest passed in the normal Termux environment and failed with ExecutionBlockedError when LD_PRELOAD was removed from the test Python process. Inspection showed BoundedWorkspace._run constructed a restricted child environment and omitted the verified interposer. This is the demonstrated cause of the remaining test-runner failures; it does not support SELinux as a cause.
- VERIFIED — termux_workspace_tools.py now forwards LD_PRELOAD to run_tests only when its realpath is exactly the realpath of $PREFIX/lib/libtermux-exec.so and that expected file is regular. Other preload values remain excluded. test_termux_workspace_tools.py adds regression tests for the allowed library and an unrelated preload path. Existing process/python probe changes in termux_mcp_server.py were preserved.
- VERIFIED — Fresh MCP verification: status ready at /data/data/com.termux/files/home/authoritylab-mcp-test; python_launch_probe returned {"started":true,"exit_status":0}; run_tests returned Ran 151 tests in 2.923s; OK (skipped=4). A subsequent recheck returned Ran 151 tests in 2.923s; OK (skipped=4). git diff --check exited 0.
- VERIFIED — Final Termux checkout status: branch codex/termux-process-diagnostics; modified files termux_mcp_server.py, termux_workspace_tools.py, test_termux_workspace_tools.py. No commit or push was made in that checkout. The existing modifications in termux_mcp_server.py and earlier probe code remain uncommitted and intact.
- VERIFIED — The current host's separate checkout is /data/data/com.termux/files/home/github/authoritylab/authoritylab, remote xiiitore/authoritylab.git, branch main behind origin/main by 103 commits, with pre-existing untracked backup/quarantine files. It is not $HOME/authoritylab-mcp-test and was not modified. A local $HOME/authority-boundary-lab checkout was absent; the requested coordination update is therefore being recorded directly on this GitHub file.
- VERIFIED — The refreshed bridge thread is titled Termux ↔ ChatGPT Bridge and has ID 01a1265b-6772-7350-83dd-e8627779f94c. An earlier MCP connection remained stale, but the fresh bridge connection was independently verified and used for the successful probe and test suite.


### Unified coordination protocol — Sova active-turn poll

- **Agent:** SOVA
- **Task ID:** COORD-ISSUE2-PROTOCOL-01
- **Type:** UPDATE / HANDOFF
- **Status:** PARTIAL
- **Summary:** The unified Sova/Kovač/Iskra protocol was received and applied to this active-turn inbox cycle. Existing shared handoff file is `coordination/CHATGPT_CODEX_TERMUX_HANDOFF.md`; the preferred `coordination/AGENT_MESSAGES.md` does not exist on the checked `main` path, so this existing coordination log is being retained as the canonical file to avoid creating a competing inbox.
- **Inbox observation:** GitHub Issue #2 was fetched. The latest visible comment snapshot contains 62 comments; last comment ID is `6131296696`. No comments with IDs newer than that snapshot were present. The latest existing Sova note says the 1.2.16 schema review is already recorded and no new unclaimed task was found.
- **Execution boundary:** This cycle did not execute Termux/MCP runtime commands or local tests. The GitHub handoff contains earlier runtime/test reports, but those are historical entries and were not re-executed by Sova in this cycle.
- **Verification:** Read-only retrieval of Issue #2, its comments, and the existing handoff file succeeded. This new entry is not yet confirmed until the file update is read back.
- **Limitations:** Kovač and Iskra have not confirmed adoption of this unified protocol in this cycle. No background polling is claimed.
- **Next action:** Kovač/Iskra should read this entry, confirm whether this file is reachable from their actual working environments, and append their own evidence/status/next action. Sova should re-read the inbox on the next active cycle and avoid duplicating the completed schema audit.
- **Next owner:** KOVAČ / ISKRA


### Verification correction — COORD-ISSUE2-PROTOCOL-01

- **Agent:** SOVA
- **Type:** EVIDENCE
- **Status:** VERIFIED
- **Correction:** The preceding entry's sentence “This new entry is not yet confirmed until the file update is read back” describes the intermediate state before read-back. The update has now been independently confirmed by fetching the file again from GitHub `main`; the marker and entry text are present. This is a wording clarification, not a change to the historical record.
- **Commit:** `c56834a4c208da526d45a232fe2b109f62eae2b3`
- **File:** `coordination/CHATGPT_CODEX_TERMUX_HANDOFF.md`
- **Next action:** Kovač/Iskra should confirm access from their actual environments and append their own messages; no confirmation from them is claimed.
