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

Use English in code, documentation, issues and commits. Keep changes focused, test
user-visible behavior, preserve human work and never commit secrets.

Run these local gates before committing:

```bash
ruff check .
ruff format --check .
pytest
```
