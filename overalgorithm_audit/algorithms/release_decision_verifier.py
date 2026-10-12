"""Consumer-side release-decision contract checks.

This module supplements JSON Schema validation. It reconciles the decision's
self-reported gates against a caller-supplied task-class catalog and refuses to
promote legacy v1 records into current release acceptance.

A PASS from this helper means only that the supplied record matches this
structural contract. It does not authenticate the catalog/reference, validate
the truth of evidence, or authorize a production release.
"""
from collections.abc import Mapping, Sequence
from pathlib import Path
import json
import re

import jsonschema

_SCHEMA_PATH = Path(__file__).parents[1] / "schemas" / "release-decision.schema.json"
_SCHEMA = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
_SENTINELS = {"unknown", "null", "none", "n/a", "na", "tbd", "todo", "unset"}
_SENTINEL_RE = re.compile(
    r"^\s*(?:unknown|null|none|n/a|na|tbd|todo|unset)\s*$", re.IGNORECASE
)


def _real_reference(value):
    return (isinstance(value, str) and bool(value.strip()) and value == value.strip()\n            and not _SENTINEL_RE.fullmatch(value))


def _catalog_entries(catalog, task_class):
    if not isinstance(catalog, Mapping):
        return None, "canonical gate catalog is missing or is not a mapping"
    entries = catalog.get(task_class)
    if not isinstance(entries, Sequence) or isinstance(entries, (str, bytes)) or not entries:
        return None, "catalog has no non-empty entry for this task_class"
    normalized = {}
    for item in entries:
        if not isinstance(item, Mapping):
            return None, "catalog entries must be mappings with id and required fields"
        gate_id, required = item.get("id"), item.get("required")
        if not isinstance(gate_id, str) or not gate_id.strip() or not _real_reference(gate_id):
            return None, "catalog contains an invalid or sentinel gate ID"
        if type(required) is not bool:
            return None, "catalog required flag must be a boolean"
        if gate_id in normalized:
            return None, "canonical catalog contains duplicate gate IDs"
        normalized[gate_id] = required
    return normalized, None


def verify_decision_contract(record, *, canonical_gate_catalog=None, catalog_evidence_ref=None):
    """Return a conservative structural status without granting release authority.

    canonical_gate_catalog maps task_class to a sequence of
    {"id": <gate ID>, "required": <bool>} entries. The caller must resolve that
    catalog from an authoritative source and supply a concrete provenance
    reference; this helper cannot authenticate either input by itself.
    """
    result = {
        "status": "UNKNOWN",
        "errors": [],
        "task_class": record.get("task_class") if isinstance(record, Mapping) else None,
        "catalog_evidence_ref": catalog_evidence_ref,
        "release_acceptance_authorized": False,
    }
    if not isinstance(record, Mapping):
        result.update(status="BLOCKED", errors=["decision record must be a mapping"])
        return result

    try:
        jsonschema.validate(dict(record), _SCHEMA)
    except (jsonschema.ValidationError, jsonschema.SchemaError) as exc:
        result.update(status="BLOCKED", errors=[f"decision schema validation failed: {exc.message}"])
        return result

    # A schema-valid v1 record is historical data, not a current release decision.
    if "schema_version" not in record and "decision" in record:
        result.update(
            status="BLOCKED",
            errors=["legacy v1 records are historical-only and cannot be promoted to current release acceptance"],
        )
        return result

    if not _real_reference(catalog_evidence_ref):
        result.update(status="UNKNOWN", errors=["a concrete catalog provenance reference is required"])
        return result

    task_class = record.get("task_class")
    expected, catalog_error = _catalog_entries(canonical_gate_catalog, task_class)
    if catalog_error:
        result.update(status="UNKNOWN" if "missing" in catalog_error or "no non-empty" in catalog_error else "BLOCKED",
                      errors=[catalog_error])
        return result

    gates = record.get("required_gates")
    if not isinstance(gates, list):
        result.update(status="BLOCKED", errors=["required_gates must be a list"])
        return result
    actual = {}
    for gate in gates:
        if not isinstance(gate, Mapping):
            result.update(status="BLOCKED", errors=["each decision gate must be a mapping"])
            return result
        gate_id = gate.get("id")
        required = gate.get("required")
        if not _real_reference(gate_id):
            result.update(status="BLOCKED", errors=["decision contains an invalid gate ID"])
            return result
        if gate_id in actual:
            result.update(status="BLOCKED", errors=[f"decision contains duplicate gate ID: {gate_id}"])
            return result
        if type(required) is not bool:
            result.update(status="BLOCKED", errors=[f"gate {gate_id} has a non-boolean required flag"])
            return result
        actual[gate_id] = required

    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    mismatched = sorted(gate_id for gate_id in set(expected) & set(actual)
                        if expected[gate_id] is not actual[gate_id])
    if missing or extra or mismatched:
        errors = []
        if missing:
            errors.append("missing catalog gate IDs: " + ", ".join(missing))
        if extra:
            errors.append("gate IDs absent from catalog: " + ", ".join(extra))
        if mismatched:
            errors.append("required-flag mismatch for gate IDs: " + ", ".join(mismatched))
        result.update(status="REVISE", errors=errors)
        return result

    result.update(status="PASS", errors=[])
    return result
