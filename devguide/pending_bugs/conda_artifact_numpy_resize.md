---
summary: Published Conda artifact fails NumPy 2.4 ANM resize on Python 3.11.
issue: uibcdf/lindelint#7
status: open
opened: 2026-09-23
closed:
severity: high
verification: measured
area: [packaging, interpolation, integration]
guard:
normative:
blocked_by: []
supersedes: []
---

# Published Conda artifact fails NumPy 2.4 ANM resize

## What

The Lindelint Conda build `0.2.0 py311_1` fails an ANM trajectory
integration test when the solver selects NumPy 2.4.6. Its installed
`interpolator.py:278` calls `bcoords.resize(3)` on an array that NumPy
will not resize in place.

## How

ElastNetMT run 35930639579 installs that Conda build in its Python 3.11
environment. A subsequent pip requirement resolves Lindelint source commit
`3825c74`, but pip's successful-install list omits Lindelint: the existing
package has the same version. The test
`tests/integration/test_anm_trajectory.py::test_anm_trajectory_generation`
then fails in the installed Conda file. Both Linux and macOS Python 3.11
jobs fail; Python 3.12 and 3.13 jobs pass.

## Why

A consumer can appear to install a pinned source revision while still
running an older published artifact. The published package must declare and
support its actual NumPy compatibility, and its release identity should let
consumers verify which implementation was installed.

## What is measured and what is assumed

The hosted Conda package list shows `lindelint 0.2.0 py311_1` and
`numpy 2.4.6`. The pip log resolves the source SHA but does not install
Lindelint. The traceback names `site-packages/lindelint/interpolator.py:278`
and the resize ValueError. Source and Conda distributions have different
code at that path.

## What was refuted

The newer source pin alone did not replace the Conda package. The separate
wheel-content fix in `uibcdf/lindelint#6` resolved a Python 3.13 import
failure but did not update this older Conda artifact.

## Scope and exclusions

The consumer workaround removes Lindelint from the Python 3.11/3.12 Conda
test environment and installs the pinned source revision. This does not
repair an existing published Conda build or establish support for every
NumPy version.

## Acceptance criteria

A published Lindelint build either passes the ANM interpolation path on its
declared Python/NumPy range or constrains unsupported combinations. A clean
installation test identifies the installed implementation and exercises
this regression. ElastNetMT can remove its source-only workaround after a
verified replacement release.

## Dependencies and risks

Consumer: `uibcdf/elastnetmt#12`. The provider should choose the release
and compatibility strategy; the current consumer workaround remains explicit.
