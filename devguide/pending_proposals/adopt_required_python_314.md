---
summary: Adopt the required four-minor Python contract and qualify installed delivery
issue: uibcdf/lindelint#14
status: active
opened: 2026-10-03
closed:
verification: inspected
area: [compatibility, packaging, ci, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Required Python 3.14 adoption

## What

MolSysSuite requires every Python member to adopt `>=3.11,<3.15` under
uibcdf/molsyssuite#51 and immutable `policy-v1.5.3`. Source `0420400a` still
excluded 3.14. LinDelINT is also the required provider of ElastNetMT under
uibcdf/elastnetmt#19, so its interpreter contract must not block that closure.

## How

Align package metadata, the noarch recipe, installed-candidate resource and
release-plan matrices, full Linux/macOS arm64 CI and contributor instructions.
The existing test environment has an unconstrained interpreter and is reused
without changing scientific test selection or older-minor dependencies.
Routine development stays on 3.13. The CI recovery detector now requires
actual successful full Linux execution on 3.14 before advancing its watermark.

## Why

The previous cap and three-minor watermark contradict the current ecosystem
requirement. Source edits and noarch packaging do not qualify an interpreter
or a public artifact by themselves.

## What is measured and what is assumed

The prior source range, recipe bounds and six configured CI cells were
inspected in an isolated published-source clone. New local/hosted evidence is
recorded when obtained; no 3.14 or public-channel result is assumed.

## Alternatives and refuted paths

Ignoring Requires-Python or promoting the support badge from a metadata edit
would hide incomplete qualification. An executed three-minor matrix cannot
clear the new four-minor recovery debt.

## Scope and exclusions

Interpreter and ecosystem contract only. Scientific numerical defects remain
with the component team and must not be suppressed or repaired through this
governance change. Public package delivery remains under uibcdf/lindelint#13.

## Acceptance criteria

- Metadata, recipe, full CI and installed-artifact gates cover 3.11–3.14.
- Normal installation, import and full relevant tests execute on 3.14, with
  failures retained and concrete owned blockers if qualification cannot pass.
- Recovery rejects historical three-minor success as a full watermark.
- Candidate/channel and independent public clean-install evidence precede
  central admission or a delivered-support badge.

The recovery regression is
`tests/test_ci_backlog.py::test_a_previous_three_minor_matrix_cannot_clear_314_debt`.
This issue remains open while scientific/public qualification is incomplete.

### Test-results publisher condition inspected on 2026-10-03

Expanding the matrix exposed an existing malformed mixed expression in the
test-results upload condition. Actionlint reported that surrounding text made the
condition always true. The complete condition is now one GitHub expression,
retaining test-results publication only from Linux/Python 3.13 after failed tests
as well as successful tests, unless the run is cancelled. Python 3.14 cells
run the suite without publishing additional test-results uploads. The separate
coverage report publisher was already correctly scoped to Linux/Python 3.13.

### Hosted source qualification on 2026-10-03

Source `1fab05063af49697324343bc1df97d9672b2bf5c` passed
[CI run 37104544799](https://github.com/uibcdf/lindelint/actions/runs/37104544799):
all eight Linux/macOS ARM jobs executed installation, wheel resource
validation, import, interpreter/architecture verification and full tests.
The policy and Conda publication-governance runs also passed. This qualifies
the tested source matrix; candidate/channel and independent public
clean-install evidence remain pending under uibcdf/lindelint#13. The malformed
test-results condition was reproduced in this run as uploads from non-routine
cells; the correction is checked by actionlint before publication.
