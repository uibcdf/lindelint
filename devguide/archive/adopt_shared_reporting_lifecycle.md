---
summary: Adopt the shared issue-backed reporting lifecycle in LinDelInt.
issue: uibcdf/lindelint#11
status: resolved
opened: 2026-09-27
closed: 2026-09-27
verification: inspected
area: [governance, reporting]
guard: tests/test_reporting_protocol.py
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Adopt the shared reporting lifecycle

**Reported:** 2026-09-27 during the MolSysSuite rollout
`uibcdf/molsyssuite#60`.
**Status:** Resolved on 2026-09-27.

## What

Give LinDelInt's existing issue-backed bug and proposal records the complete
common lifecycle: a report template, archive mapping, generated index,
offline validator and contributor guidance.

## How

Preserve the active Conda artifact bug `uibcdf/lindelint#7`, the Python
ecosystem review `uibcdf/lindelint#9` and the solved wheel bug
`uibcdf/lindelint#6`. Add a narrow local non-pytest guard profile for the
existing wheel-content script. Add an independent hosted governance job, so
the reporting gate is visible even when unrelated scientific tests fail.

## Why

The pre-adoption tree had issue-backed front matter and queue directories,
but manually maintained indexes and no report template or offline validator.
Without a guard, new reports can silently lose their issue identity or
closure evidence.

## What is measured and what is assumed

Inspected `origin/main` on 2026-09-27 after the central `suite_status.py`
fetch. The three existing records name issues #7, #9 and #6. The solved
wheel bug uses `devtools/scripts/check_wheel.py` as its guard; that script
requires a wheel argument and is invoked by the current CI workflow.
No scientific runtime outcome is inferred from this inspection.

## Alternatives and refuted paths

- Rewriting the historical solved bug into a new directory was rejected;
  the common protocol allows an established equivalent archive.
- Accepting every `devtools/scripts/*.py` path as a guard was rejected;
  only the documented wheel-content runner has a verified local profile.

## Scope and exclusions

This is a governance change. The NumPy/Conda defect in #7, ecosystem review
in #9 and scientific behavior stay with their existing owners and outcomes.

## Acceptance criteria

- The queue and archive indexes regenerate deterministically and include
  the existing issue-backed records.
- The offline validator rejects a missing issue, an invalid closure and a
  guard target that does not resolve to a runnable test or the wheel script.
- The contributor routes and independent hosted governance job use the local
  check; local and hosted evidence passes before this issue closes.

## Resolution and verification

Commit `10aa0c8` added the local template, parser, generated queue/archive
indexes, documented wheel-guard profile, contributor routes and independent
governance job. The original issue identities #6, #7 and #9 are preserved.
The archive index includes the resolved wheel bug in `solved_bugs/` without
moving or rewriting that historical record.

Locally, the index check, three reporting tests, eight repository tests,
Ruff lint and Ruff format all passed. On the exact commit, hosted CI run
`36356554719` passed the independent reporting-governance job, including
index validation and reporting tests. The MolSysSuite policy run
`36356555031` passed. The scientific matrix is separate evidence and is not
required to establish the reporting lifecycle. The durable guard is
`tests/test_reporting_protocol.py`; the local rule is
`devguide/reporting_protocol.md`.

## Provenance

Inspection date: 2026-09-27. Source: fetched LinDelInt `origin/main` in the
MolSysSuite Linux development workspace. No runtime dependency versions were
measured for this governance decision.
