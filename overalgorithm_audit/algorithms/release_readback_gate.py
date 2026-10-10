"""Reference decision helper for validating a plugin release read-back.

This helper is testable policy logic, not evidence that ChatGPT host runtime
uses or executes it. Callers must supply observed identifiers and test results.
"""
from typing import Optional, Sequence

_SENTINEL_IDENTIFIERS = {"unknown", "null", "none", "n/a", "na", "tbd", "todo", "unset"}


def _is_real_identifier(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value.strip().casefold() not in _SENTINEL_IDENTIFIERS
    )


def assess_readback(
    *,
    target_plugin_id: str,
    returned_plugin_id: str,
    readback_plugin_id: str,
    baseline_release_id: str,
    returned_release_id: str,
    readback_release_id: str,
    intended_change_present: bool,
    mandatory_tests_passed: bool,
    runtime_required: Optional[bool],
    runtime_executed: bool = False,
    runtime_policy_evidence_refs: Optional[Sequence[str]] = None,
) -> str:
    """Return a conservative status for the supplied release-readback evidence.

    If runtime testing is declared unnecessary, at least one concrete reference
    supporting that policy decision is required. An empty, sentinel, or malformed
    reference must never be treated as evidence.
    """
    identifiers = (
        target_plugin_id,
        returned_plugin_id,
        readback_plugin_id,
        baseline_release_id,
        returned_release_id,
        readback_release_id,
    )
    if not all(_is_real_identifier(value) for value in identifiers):
        return "UNKNOWN"
    if (
        type(runtime_required) is not bool
        or type(runtime_executed) is not bool
        or type(intended_change_present) is not bool
        or type(mandatory_tests_passed) is not bool
    ):
        return "UNKNOWN"
    if target_plugin_id != returned_plugin_id or target_plugin_id != readback_plugin_id:
        return "BLOCKED"
    if returned_release_id == baseline_release_id or readback_release_id != returned_release_id or not intended_change_present:
        return "REVISE"
    if not mandatory_tests_passed:
        return "BLOCKED"
    if runtime_required:
        if not runtime_executed:
            return "UNKNOWN"
    else:
        if not isinstance(runtime_policy_evidence_refs, (list, tuple)) or not runtime_policy_evidence_refs:
            return "UNKNOWN"
        if not all(_is_real_identifier(ref) for ref in runtime_policy_evidence_refs):
            return "UNKNOWN"
    return "PASS"
