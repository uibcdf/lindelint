# LinDelINT Conda publication

Owning review: uibcdf/lindelint#13; suite contract: uibcdf/molsyssuite#45.

The recipe prepares one immutable `noarch: python` coordinate. Required runtime
dependencies and Python bounds follow `pyproject.toml`; build tools belong in
host requirements. The shared workflow freezes the reviewed version in an ephemeral
checkout and inspects metadata, embedded version and the complete resource inventory.
scikit-learn is a development/test/docs tool, not a runtime dependency.

Follow the [shared noarch guide](https://github.com/uibcdf/molsyssuite/blob/main/devguide/noarch_conda_workflow.md).
All four shared publication wrappers pin MolSysSuite at
`38db709ecc07451ff36ea84573d585f9af6b4df7`. The existing
`ANACONDA_UIBCDF_TOKEN` mapping is retained; access/validity remains unconfirmed.

## Candidate and executed gates

`release_plan.example.toml` is onboarding context only; it authorizes no release.
Before a candidate, review and commit a real `release_plan.toml`. Build/promotion
first call the local reusable owner review, which requires the exact clean candidate
SHA/version, tracked real plan and the reviewed example's gate/matrix profile.
Changing that profile requires reviewing the example too.

All eleven native source jobs and named steps are required: eight full Linux/macOS
arm64 Python 3.11–3.14 source test cells (including actual installed dependency-bound
preflight), independent reporting/distribution controls, policy/lint/format and Conda
governance. A successful daily probe with omitted science is insufficient.
Declaration-only checks cannot clear scientific debt or authorize publication.

The first noarch file must be staged and qualified outside source across all eight
Linux/macOS arm64 Python 3.11–3.14 cells. Every installed cell requires four executed
successful steps: install the exact artifact, validate installed files, run installed
tests, and recheck provenance after scientific tests. The whole `tests` selection
is retained. The installed wrapper is dispatched explicitly for the original source,
filename and digest; it never runs on pushes. Missing/skipped/failed evidence blocks
promotion. Resource checks include every tracked runtime file and the generated version.

Dispatch build with the full candidate SHA and reviewed version. Promotion also needs
the staged SHA-256 and successful installed run ID. If a newer administrative workflow
commit is needed, supply its full `qualification_sha` separately; retain the original
producer SHA and file digest. Promotion labels those same bytes without rebuilding
or reuploading. Later direct releases still need an eligible reviewed plan, executed
exact-tag gates, public closure and conclusive all-label absence. Never overwrite.

## Maintained inputs and early checks

The sixteen-route inventory is `devtools/dependency_routes.toml`. Use the reviewed
clean SDK clone and resolved consuming interpreter:

```bash
python devtools/check_distribution_inputs.py --suite-root /path/to/molsyssuite --output /tmp/lindelint-inputs.json
LINDELINT_SUITE_ROOT=/path/to/molsyssuite python -m unittest discover -s devtools/tests -p test_distribution_inputs.py
```

Default mode checks actual installed versions against public metadata. Explicit
`--declared-only` is an offline administrative review, not runtime qualification.
Add `--candidate-sha FULL_SHA --version X.Y.Z` to bind the real committed plan.
These commands do not build or publish. Workflow edits require reviewing the
recorded inventory digest and purpose.

Historical public 0.2.0 files do not certify current source delivery. The first real
plan, executed source/installed evidence, credential access and public poststate remain
pending under #13/#14. This configuration alone grants no installed-platform claim.
