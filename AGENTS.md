# Lindelint contributor instructions

Read `MOLSYSSUITE_GUIDE.md` before making changes. It routes suite-wide policy,
compatibility, tooling and cross-component proposals to `uibcdf/molsyssuite`, while this
repository remains authoritative for Lindelint's implementation and scientific behavior.

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

Use English in code, documentation, issues and commits. Keep changes focused, test
user-visible behavior, preserve human work and never commit secrets.

The required source contract is Python 3.11–3.14; routine development uses
Python 3.14. Qualification and public delivery are tracked in
`uibcdf/lindelint#14`. Keep metadata, recipe and full CI aligned; ordinary
installed evidence must not bypass `Requires-Python`. Preserve truthful
public support claims until the suite records admission.

Run these local gates before committing:

```bash
ruff check .
ruff format --check .
python devtools/devguide_index.py --check
python -m unittest discover -s tests -p test_reporting_protocol.py
pytest
```

## Modular reusable tools

Before adding a feature, inspect existing tools and identify the owning module or
component. Implement or extend independently useful operations as documented reusable
tools in that owner, with their own contracts and tests; have consumers call them.
Keep task-specific decisions local and report missing sibling capabilities to the
provider with linked consumer evidence. Follow
[MOLSYSSUITE_GUIDE.md#modular-reusable-tools](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
for applicability, compatibility, performance and tracked exceptions.

## Durable working instructions

Keep technical findings in owning issues, fixes, tests and maintained guidance.
Place only accepted lasting contributor actions in root or appropriately scoped
instructions, following
[the common policy](MOLSYSSUITE_GUIDE.md#durable-working-instructions).
For work under `devguide/`, also read [devguide/AGENTS.md](devguide/AGENTS.md)
and its local reporting protocol. Shared instruction proposals belong in
`uibcdf/molsyssuite`; cross-MOLI contracts belong in `uibcdf/moli`.
