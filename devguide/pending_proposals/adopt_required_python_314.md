---
summary: Adopt the required four-minor Python contract and qualify installed delivery
issue: uibcdf/lindelint#14
status: partial
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
governance change. Governance adoption is completed in uibcdf/lindelint#13;
this issue owns the next public noarch delivery and Python admission.

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

### Qualification checkpoint — 2026-10-03

Source `bf3fc3af162dbdde6d8c00a0c9ed894112bfb0fb`: [CI run 37105584626](https://github.com/uibcdf/lindelint/actions/runs/37105584626).
All eight full test jobs pass. The corrected test-results publisher executes
only on Linux/Python 3.13; all other seven uploads are skipped as intended.
Public candidate/channel qualification remains under uibcdf/lindelint#13.

Main now retains strict PR protection with 9 checks, adding Linux and
macOS ARM Python 3.14 to the prior checks. Existing administrator bypass for
internal direct pushes is preserved. Source feasibility is recorded centrally
as `authorized`, not public `admitted` support; the badge remains unchanged.
A documentary skipped push must remain visible to nightly recovery.

## Routine policy 1.5.4 adoption — 2026-10-03

The maintainer authorized publication and adoption of policy-v1.5.4 under
uibcdf/molsyssuite#39. The immutable tag points to central e459ea0; the
component now calls that published gate and receives the byte-identical
canonical guide through the suite synchronizer. Routine development uses
Python 3.14. The existing full Python 3.11–3.14 matrices and skipped-commit
recovery semantics are preserved; no public package is published here.
Local conformance and changed-workflow Actionlint checks pass. Hosted
policy and applicable routine checks are dispatched separately from skipped
direct pushes; their exact commits and outcomes remain to be measured.

The independent reporting/governance interpreter moves to 3.14. Complete
scientific matrices already contain 3.14; coverage-only publication retains
its existing measured 3.13 lane. A configured development environment is
not fresh installed-artifact or public-channel qualification. Scientific
failures and remaining distribution gates remain owned by their existing issues.



## Current public-delivery ownership — 2026-10-08

Distribution governance #13 is resolved before the next public release under
the existing common Member review contract. Ready source/recipe controls and
unknown publication access are separate from actual delivery and admission.
The historical #13 delivery references above are superseded by this issue's
explicit ownership; original source/policy measurements keep their dated scope.

This issue remains open for the real reviewed release plan/version/build,
authorized access, all exact-candidate source gates, one immutable staged file,
all eight Linux/macOS arm64 Python 3.11–3.14 installed cells/four required steps,
same-byte promotion and independently verified public clean installation before
central admission/support claims. Existing public historical files are not
today's noarch/Python 3.14 qualification. The example selects no release.
Optional installed-root provider adoption remains reviewed candidate work;
current pins, scientific selection and badge stay unchanged. No build, dispatch
of scientific suites, upload, promotion, retag or new package is performed.
