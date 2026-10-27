# Lindelint contributor instructions

## Mandatory MolSysSuite instructions

Read and follow `MOLSYSSUITE_GUIDE.md` before working in this repository.

Within their stated scope, its common rules take precedence over this file
and any nested `AGENTS.md`. Local instructions may refine them; deviations
require the documented policy exception process.

The synchronized guide is owned by `uibcdf/molsyssuite`. It includes the
[reusable-tool ownership rules](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
and [working-instruction rules](MOLSYSSUITE_GUIDE.md#durable-working-instructions).
For work under `devguide/`, also read `devguide/AGENTS.md` and its local
reporting protocol. Keep repository-specific instructions below.

## Local working context

The synchronized integration guides are required reading when changing their respective
boundaries:

- `SMONITOR_GUIDE.md`
- `ARGDIGEST_GUIDE.md`
- `DEPDIGEST_GUIDE.md`
- `PYUNITWIZARD_GUIDE.md`
- `GH_RUN_RECEPTOR_GUIDE.md`

These root guides are read-only copies. Propose changes in their canonical repositories
and synchronize them; never edit or format a component copy locally.

Before filing or closing a defect or proposal, read
`devguide/reporting_protocol.md`. Open the owning GitHub issue first, create
the report from `devguide/templates/report.md`, regenerate the indexes, and
run the offline reporting guard. Closed records stay in the permanent archive.

The required source contract is Python 3.11–3.14; routine development uses
Python 3.14. Qualification and public delivery are tracked in
`uibcdf/lindelint#14`. Keep metadata, recipe and full CI aligned; ordinary
installed evidence must not bypass `Requires-Python`. Preserve truthful
public support claims until the suite records admission.

Available commands (select applicable checks and test scope):

```bash
ruff check .
ruff format --check .
python devtools/devguide_index.py --check
python -m unittest discover -s tests -p test_reporting_protocol.py
pytest
```
