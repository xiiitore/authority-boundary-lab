# authority-boundary-lab

A small, dependency-free test harness for application-level authorization boundaries: identity validation, explicit grants, deny-by-default behavior, revocation, and resource isolation.

## Run

Requires Python 3.11 or newer.

```bash
python -m unittest -v
```

## Scope

- `authz.py` contains immutable principals, explicit role/action/resource grants, revocation, and a decision audit snapshot.
- `test_authz.py` tests allow/deny behavior, revocation and restoration, resource separation, input validation, and audit snapshot isolation.
- Policy decisions are deny-by-default and use exact action/resource matches.

## Security limits

This is a model for testing application policy logic, not a production identity provider or a security boundary. It does not authenticate the caller, isolate operating-system resources, sandbox processes, protect audit logs against tampering, or implement distributed revocation. Do not treat a passing unit test as proof of deployment security. Integrate with a real identity source and enforce authorization at every resource boundary before production use.
