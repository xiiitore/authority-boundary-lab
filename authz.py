"""Small, deterministic authorization model for testing policy boundaries.

This module models application-level authorization only. It does not enforce OS,
container, process, or network isolation.
"""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    roles: frozenset[str]

    def __post_init__(self) -> None:
        if not isinstance(self.subject, str) or not self.subject.strip():
            raise ValueError("subject must be a non-empty string")
        if not isinstance(self.roles, frozenset) or any(
            not isinstance(role, str) or not role.strip() for role in self.roles
        ):
            raise TypeError("roles must be a frozenset of non-empty strings")


@dataclass(frozen=True, slots=True)
class Grant:
    role: str
    action: str
    resource: str


class AuthorizationError(PermissionError):
    """Raised when a request is denied by the authorization policy."""


class PolicyEngine:
    """Deny-by-default RBAC policy with explicit revocation and audit decisions."""

    def __init__(self, grants=()) -> None:
        self._lock = RLock()
        self._grants: set[Grant] = set()
        self._revoked_subjects: set[str] = set()
        self._audit: list[dict[str, str | bool]] = []
        for grant in grants:
            self.add_grant(grant)

    def add_grant(self, grant: Grant) -> None:
        if not isinstance(grant, Grant):
            raise TypeError("grant must be a Grant")
        if not all(isinstance(value, str) and value.strip() for value in
                   (grant.role, grant.action, grant.resource)):
            raise ValueError("grant fields must be non-empty strings")
        with self._lock:
            self._grants.add(grant)

    def revoke_subject(self, subject: str) -> None:
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError("subject must be a non-empty string")
        with self._lock:
            self._revoked_subjects.add(subject)

    def restore_subject(self, subject: str) -> None:
        with self._lock:
            self._revoked_subjects.discard(subject)

    def authorize(self, principal: Principal, action: str, resource: str) -> bool:
        if not isinstance(principal, Principal):
            raise TypeError("principal must be a Principal")
        if not isinstance(action, str) or not action.strip():
            raise ValueError("action must be a non-empty string")
        if not isinstance(resource, str) or not resource.strip():
            raise ValueError("resource must be a non-empty string")
        with self._lock:
            allowed = (
                principal.subject not in self._revoked_subjects
                and any(
                    grant.role in principal.roles
                    and grant.action == action
                    and grant.resource == resource
                    for grant in self._grants
                )
            )
            self._audit.append({
                "subject": principal.subject,
                "action": action,
                "resource": resource,
                "allowed": allowed,
            })
            return allowed

    def require(self, principal: Principal, action: str, resource: str) -> None:
        if not self.authorize(principal, action, resource):
            raise AuthorizationError("access denied")

    def audit_snapshot(self) -> tuple[dict[str, str | bool], ...]:
        with self._lock:
            return tuple(dict(entry) for entry in self._audit)
