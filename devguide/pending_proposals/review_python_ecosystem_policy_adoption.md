---
summary: Review LinDelInt Python ecosystem policy adoption.
issue: uibcdf/lindelint#9
status: active
opened: 2026-09-27
closed:
verification: measured
area: [governance, tooling]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review Python ecosystem policy adoption

**Reported:** 2026-09-27 under `uibcdf/molsyssuite#56`; inspected
`437a306b0df6f6cdbae63870b3f50709f06e99ae` on `origin/main`.

## What

Both support-library and developer-tool adoption are **partial**. All four
support libraries are declared, but an optional engine fails its fallback and
import resets the user's unit settings. Hosted CI uses plain pytest.

## How

ArgDigest decorates the constructor and SMonitor carries diagnostics.
`_depdigest.py` configures optional dependencies, but the auto-engine path
still raises a CuPy import error when the backend is absent. This is tracked
as `uibcdf/lindelint#8`, with ElastNetMT trajectory failure as consumer
evidence. `_pyunitwizard.py` unconditionally sets global form, parser, and
unit defaults at import. Add focused tests for both boundaries.

CI run `36310576811` passed six of six jobs at the inspected source; suite
policy run `36310577229` also passed. Published GH Run Receptor `1.0.0`
inspected them. The CI test environment has no Pytest Receptor pin and the
maintained workflow invokes plain pytest. Pin a published exact version, use
`--receptor=ci`, and verify equivalent selection and outcomes in hosted CI.

## Why

A green own-repository matrix did not cover the consumer's missing-CuPy path.
Import-time global policy changes can alter quantities in other suite members.

## What was refuted

The DepDigest configuration file does not establish a runtime guard for the
optional GPU backend. The successful LinDelInt CI matrix does not establish
that `engine='auto'` falls back when CuPy is unavailable.

## Scope and exclusions

This record owns LinDelInt's policy boundaries and CI route. The ElastNetMT
consumer remains tracked in `uibcdf/elastnetmt#14`.

## Acceptance criteria

Verify auto-engine fallback with CuPy absent, preserve user-selected unit
policy on import, use an exact published receptor pin and `ci` profile in
maintained CI, and record independent adoption evidence.
