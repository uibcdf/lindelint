---
summary: Include private package in installed Lindelint wheel.
issue: uibcdf/lindelint#6
status: resolved
opened: 2026-09-23
closed: 2026-09-23
severity: high
verification: reproduced
area: [packaging, integration]
guard: devtools/scripts/check_wheel.py
normative:
blocked_by: []
supersedes: []
---

# Installed wheel omits private package

## What

The built wheel omits `lindelint/_private/smonitor`, but `lindelint/__init__.py` imports it. A clean Python 3.13 installation fails to import the package.

## How

Setuptools package discovery uses `namespaces = false`, while `lindelint/_private` has no `__init__.py`. The built wheel has no `lindelint/_private/` entries. A wheel-content guard will inspect the distributable artifact independently of source-tree imports.

## Why

`uibcdf/elastnetmt#12` CI run 35923676969 failed in both Python 3.13 cells with `ModuleNotFoundError: No module named 'lindelint._private'`. This masks the true source behavior during integration tests.

## What is measured and what is assumed

`python -m pip wheel --no-build-isolation --no-deps .` produced a wheel with zero private package entries. Hosted ElastNetMT CI reproduced the installed import failure.

## What was refuted

Source-tree import success is insufficient: Python can see the unbundled `_private` directory there, and older Conda installations can leave stale files in site-packages.

## Scope and exclusions

The interpolation algorithm is unaffected; this report concerns wheel package contents.

## Acceptance criteria

The built wheel includes `lindelint/_private/smonitor/__init__.py`, and an installed import works without a prior Conda overlay. The wheel-content check is run in CI.

## Dependencies and risks

None.

## Resolution

Setuptools now discovers the `lindelint*` namespace tree, so the built wheel includes the private SMonitor package. The CI wheel-content guard directly checks that artifact. It failed against the former wheel and passed after the fix; an installation into `/tmp/lindelint-clean-import` imported successfully from that target. The local suite passed with pytest-receptor: 5 passed.
