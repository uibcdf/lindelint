---
summary: Adopt the distribution policy and a guarded single-file noarch publication route.
issue: uibcdf/lindelint#13
status: partial
opened: 2026-10-01
closed:
verification: measured
area: [governance, distribution, compatibility]
guard: devtools/tests/test_distribution_inputs.py
normative: MOLSYSSUITE_GUIDE.md
blocked_by: []
supersedes: []
---

# Noarch distribution adoption

## What

Adopt the suite distribution contract under uibcdf/molsyssuite#45. The maintainer
authorized adapting this publisher now and using `noarch: python`.

## How

The recipe declares one immutable noarch coordinate, preserves required metadata
constraints, uses host build tools and pip without dependency resolution. Thin
build/promotion wrappers reuse the common implementation at `a44e86a4f6a01dcbfe28fde46d886bc5cd4254c2`.
`devtools/conda-build/resources.toml` inventories the embedded version, package
roots and tracked runtime data. The example plan declares every supported source
CI job and its executed tests. A dedicated administrative reusable check inspects
the recipe/resources and publication controls without importing scientific code.

## Why

The old publisher used a moving action ref, interpreter/platform fan-out and
unrestricted manual public uploads. It did not retain the common exact-candidate
producer evidence. Its recipe did not declare noarch. The new route inspects the
exact built file before upload and promotes tested bytes without rebuilding.

## What is measured and what is assumed

Source inspection found pure Python code/data and no tracked bundled native
extension/executable. This migration is configuration and offline governance
work. It does not prove installed platform compatibility, scientific correctness,
credential access or public package availability. Full source CI remains unchanged;
internal direct/skip pushes remain available to dprada and LMMV.

## Alternatives and refuted paths

- A green recovery probe with skipped tests cannot authorize a candidate.
- Noarch does not prove macOS, Linux or Windows support.
- A second build/upload is not exact-file promotion.
- `release_plan.example.toml` does not authorize or select a public release.

## Scope and exclusions

Distribution governance and packaging identity/resources. Scientific algorithm
repairs and complete scientific execution belong to this component's team.

## Remaining adoption and acceptance criteria

- Inspect hosted evidence for the maintained runtime/source controls documented
  below; retain any scientific failures with the component's team.
- Before a candidate, commit a reviewed actual release plan and immutable build.
- Execute the component-owned installed gate for the actual candidate before
  promotion. The current eight-cell descriptor retains the complete local suite
  and resource/launcher checks; missing, skipped or failed evidence fails closed.
- Confirm publication access only through an authorized maintainer.
- Register actual candidate/build/installed/public evidence only after execution.

The migration implements the common source route; whole-policy adoption remains
partial until these criteria are met. The common policy and module's negative
guards are the durable reference; the owning issue remains open.

## Administrative verification, 2026-10-01

The common early recipe/resource check passes with the example plan; the common
publication-control audit and actionlint pass for all three local wrappers.
Local reporting/index validation passes. No scientific module was imported for
these checks.

An isolated copy was prepared with the common static-version helper and
`pip wheel --no-deps --no-build-isolation`. The illustrative version was 0.0.0;
no release candidate or publication was selected. The wheel is `py3-none-any`,
contains all 3 declared paths and the matching embedded version. This
checks setuptools packaging only; it does not certify a Conda artifact, public
PyPI availability, installed resource use or any scientific/platform claim.

Central common implementation a44e86a passed native governance run 36898671705
and 249 local administrative tests. Its archive guards separately reject missing
resources, stale embedded versions and native payloads before upload.

At that checkpoint the extra runtime recipe requirement scikit-learn still needed
owner classification. The accepted 2026-10-06 decision below supersedes that pending item.

## Installed qualification capability, 2026-10-01

The manual installed wrapper and committed six-cell descriptor are now delivered
through common 42e4de425871c125ef058842075c39e50fc6ac64. No installed scientific gate has been executed.
The workflow verifies the exact downloaded/installed Conda file and resources,
requires ordinary public dependency provenance and runs the whole local test
selection outside source, with import checks inside the pytest interpreter.
It neither uploads nor adds a scientific suite to internal pushes. The real
release plan and actual scientific/installed evidence remain future prerequisites.

## Maintained source controls and public-route review, 2026-10-06

The maintainer accepted removing `scikit-learn` from the Conda runtime recipe and
production environment, retaining it in development/tests/docs. Package code has
no scikit-learn import. The six required metadata dependencies remain unchanged;
no scientific API minimum has been invented. Existing public files are untouched.
ElastNetMT is the registered runtime/documentation consumer and receives notice
under `uibcdf/elastnetmt#18` before this owner rollout.

`devtools/dependency_routes.toml` records all sixteen current routes: one guarded
recipe, seven environment files and eight workflows. It pins the accepted shared
SDK at `38db709ecc07451ff36ea84573d585f9af6b4df7`. Runtime environments follow
metadata Python/dependency constraints, with public uibcdf/conda-forge channels
and strict priority. Development selects Python 3.14. Setup/build are build-only;
the unused historical MolSysMT counterpart fixture is explicitly resolved-package
scope, not source or public LinDelINT qualification. There are no required sibling
source substitutions in current CI. Documentation retains Python 3.13 within
the public interval, with its required administrative dependencies explicit.

The broadcaster generates only the six maintained environments and refuses drift
in check mode; it cannot rewrite the Jinja recipe or frozen version controls.
Create/update helpers reject unsupported Python selections, use strict priority,
propagate failures and remove their temporary input files. The owner preflight
verifies the immutable clean SDK, complete tracked package inventory, generated
environments and shared route contract. Source CI/docs use its default actual
installed public-bound check before consuming source. The independent governance
job uses declaration-only mode and tests `devtools/tests/test_distribution_inputs.py`;
these administrative tests are outside the unchanged installed scientific selection.

The resource inventory now covers all thirteen tracked runtime files plus the
generated version module, including the private SMonitor package and `py.typed`.
Shared artifact tests exercise a complete synthetic file, then reject a missing
private runtime file and stale embedded version; they build no real candidate.
Missing recipe requirements, stale environment floors, below-floor installed or
source versions, incomplete resources and altered/unclassified workflows fail.

Build/promotion first require a real tracked `release_plan.toml`, exact clean
candidate SHA/version and the maintained gate/matrix profile. The example is
onboarding context only. It now names eleven executed native source jobs:
eight complete Linux/macOS arm64 Python 3.11–3.14 cells, independent reporting/
distribution controls, repository/lint/format conformance and Conda governance.
The installed descriptor names all eight cells and all four mandatory steps,
including the provenance recheck after science. Promotion can separately name a
newer `qualification_sha` while retaining the original source and exact digest.

Read-only official registry inspection found public 0.2.0 and eighteen historical
files. GitHub 0.1.0/0.2.0 releases have no assets. Documentation and badge context
now distinguish this historical availability from today's unqualified noarch
delivery. No public PyPI route or current Windows installed claim is made. The
Python badge remains unchanged until admission in `uibcdf/lindelint#14`.

Local evidence: sixteen administrative regression tests pass under
`molsyssuite@uibcdf_3.14` (Python 3.14.7), exercising the actual accepted SDK.
The default sixteen-route preflight also checks the six installed distributions;
this is direct metadata-bound evidence, not transitive closure, joint runtime or
scientific qualification. Existing shared-workspace debt stays in
`uibcdf/molsyssuite#82`. Hosted exact-head results and first real artifact/access/
installed/public evidence remain separate; this report stays partial.
