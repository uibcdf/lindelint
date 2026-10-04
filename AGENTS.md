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

Choose local gates before committing by the changed code, inputs and scope:

- Documentation, instructions and evidence require applicable reporting/index,
  link and synchronized-guide checks; prose changes alone do not require the
  scientific suite.
- Executable behavior, dependency, metadata, packaging and integration changes
  require relevant code/contract tests and applicable lint, format and local
  type checks. Broaden validation when the affected boundary requires it.
- Scientific exploration requires informative hypothesis cases and explicit
  limits; an administrative check does not establish scientific equivalence.

Available commands (select applicable checks and test scope):

```bash
ruff check .
ruff format --check .
python devtools/devguide_index.py --check
python -m unittest discover -s tests -p test_reporting_protocol.py
pytest
```

## Direct pushes and scoped local validation

Follow [the common checkpoint policy](MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints)
for authorized internal direct pushes by `dprada` and `LMMV`. Batch focused local
commits when remote visibility is unnecessary; a permitted interim CI skip is
conditional, never the default after every locally checked change. Retain local
results while tested code, inputs, environment and scope remain applicable.
Normally finish with an unskipped head and inspect its applicable CI, or explicitly
execute and verify those exact-head gates manually. Record missing evidence,
untested scope, owning issue and recovery route; administrative checks do not
clear full-suite backlog. External PRs, admission and publication require all
mandatory executed gates for the exact candidate and required installed file.
An authorized manual qualification retains the original producer and artifact
bytes/digest; a marker alone neither waives a gate nor disqualifies that evidence.

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
