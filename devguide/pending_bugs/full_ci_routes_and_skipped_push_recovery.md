---
summary: Complete contributor full-CI routes and skipped-push recovery.
issue: uibcdf/lindelint#12
status: active
opened: 2026-09-30
closed:
severity: medium
verification: inspected
area: [governance, ci]
guard: tests/test_ci_backlog.py
normative:
blocked_by: []
supersedes: []
---

# Full-CI contributor routes and skipped-push recovery

## What

Implement uibcdf/molsyssuite#39 in LinDelINT without changing its scientific
implementation. Baseline main ed588ab had no required PR/checks. Existing
CI covers Python 3.11–3.13 on Linux and macOS with complete distributed pytest,
wheel contents, import, Ruff and reporting gates.

## How

Preserve that matrix and weekly Monday 09:00 UTC route. Add conditional daily
01:43 America/Mexico_City recovery and unconditional manual execution. A manual
`probe_backlog=true` dispatch executes the detector and reporting governance,
but omits the six test jobs. Pin macOS to macos-15 and assert arm64 and each
Python minor before tests. Existing external PRs execute the complete suite.

Main requires strict complete supported checks and a PR with zero required
reviewer approvals; current admins dprada and LMMV retain direct-push bypass.
A documentation commit with `[skip ci]` will verify that route. The detector
accepts only successful main push/schedule/manual runs with every Linux minor
and its actually executed `Run tests` step. Probes, PRs, feature branches,
failed runs and skipped tests cannot clear debt. API/history uncertainty runs
the full matrix. Debt persists across ordinary commits and calendar days until
complete green coverage includes the skipped commits.

## Why

Internal iteration remains lightweight while daily recovery protects the suite.
External contributors use a complete PR matrix. Governance has an independent
job so scientific failures remain visible without obscuring report validation.

## What is measured and what is assumed

On 2026-09-30, GH Run Receptor 1.0.0 inspected baseline weekly run 36457534890:
PASS, seven successful jobs. Native job evidence confirmed six `Run tests`
steps succeeded. Fresh collaborator API listed only dprada/LMMV, both admins.
The updated protection API confirms strict seven supported checks, an explicit
PR requirement with zero approvals, and admin bypass. Local Python 3.13.15,
NumPy 2.4.6, SciPy 1.18.0 and Numba 0.67.0: `pytest` passed 12/12; Ruff,
reporting/index guards and central component conformance passed. New hosted
routes are pending execution evidence.

## Alternatives and refuted paths

Requiring reviewer approvals would add an unrelated review gate. Weekly-only
recovery waits too long. A calendar-day-only detector loses unpaid older debt.
Successful probes cannot stand in for full tests. The existing complete matrix
needs no smoke replacement.

## Scope and exclusions

Only CI routing, architecture evidence, protection and reporting. Existing
scientific/provider issues uibcdf/lindelint#7 and uibcdf/lindelint#8, unit-policy
and tooling adoption uibcdf/lindelint#9, and documentation publication #5 stay
with their respective component work. A green macOS source suite does not prove
the declared Conda platform artifacts install and satisfy published claims.

## Acceptance criteria

- Verify strict supported checks, explicit PR requirement and admin bypass.
- Measure zero-debt probe, one skipped push, debt probe, complete manual matrix
  at the skipped head, and zero debt only after actual full success.
- Observe actual daily schedule and hosted external-PR execution.
- Review claimed distribution platforms independently before claiming adoption.
- Keep tests/test_ci_backlog.py as the durable debt guard.
