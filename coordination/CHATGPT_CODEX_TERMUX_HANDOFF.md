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
