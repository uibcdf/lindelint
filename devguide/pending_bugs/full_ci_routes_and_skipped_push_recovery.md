---
summary: Complete contributor full-CI routes and skipped-push recovery.
issue: uibcdf/lindelint#12
status: partial
opened: 2026-09-30
closed:
severity: medium
verification: measured
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
reporting/index guards and central component conformance passed. Hosted route verification is recorded below; actual daily schedule,
external-PR execution and publication-platform review remain pending.

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

## Hosted verification

Implementation 78ddc30 was pushed directly to main; GitHub reported bypass
of the explicit PR rule and seven required checks. Suite policy 36700140495
passed. Initial probe 36700190976 found zero skipped commits since baseline
ed588ab and omitted all six matrix jobs; independent reporting still passed.

Documentation-only skipped push 81c45be deliberately exercised recovery,
with GitHub bypass notices for the PR rule and seven checks. Debt probe
36700480542 found exactly one skipped commit since successful full CI at
78ddc30 and omitted the six heavy jobs. Complete manual CI 36700581051 at
81c45be passed reporting and all six supported Linux/macOS cells. Native
step evidence confirmed `Run tests` and the interpreter/architecture assertion
succeeded in every cell; the decision job was intentionally skipped for
unconditional manual execution. GH Run Receptor 1.0.0 preserved success.
Recovery probe 36700906324 recognized 81c45be as the full watermark, found
zero debt and omitted the six heavy jobs. No intermediate full push could
clear the debt: the manual run executed at the deliberately skipped head.

Routine full CI 36700139663 at 78ddc30 also passed reporting and all six cells
with both required steps executed. These observed routes establish the
implementation and recovery control, not actual daily or external-PR execution.
Those acceptance items and publication-platform claims keep #12 partial/open.

Evidence URLs:
- https://github.com/uibcdf/lindelint/actions/runs/36700139663
- https://github.com/uibcdf/lindelint/actions/runs/36700140495
- https://github.com/uibcdf/lindelint/actions/runs/36700190976
- https://github.com/uibcdf/lindelint/actions/runs/36700480542
- https://github.com/uibcdf/lindelint/actions/runs/36700581051
- https://github.com/uibcdf/lindelint/actions/runs/36700906324
