# LinDelINT development and Conda inputs

Routine development uses Python 3.14; source compatibility remains Python
3.11–3.14. Bootstrap with Conda/Mamba and PyYAML/packaging available to the helper
interpreter. Commands below run from the repository root:

```bash
python devtools/conda-envs/create_conda_env.py -n lindelint_3.14 -p 3.14 devtools/conda-envs/development_env.yaml
conda activate lindelint_3.14
python -m pip install --no-deps --editable .
```

To update an already active environment explicitly:

```bash
python devtools/conda-envs/update_conda_env.py devtools/conda-envs/development_env.yaml
```

Helpers retain selected requirements and set strict channel priority. Unsupported
Python minors are rejected; the development environment requires 3.14. The old
create helper delegates to the same implementation. Failures propagate and temporary
YAML is removed. Updating prunes packages, so use the owner's development environment;
do not update a shared ecosystem environment with this component file.

## Maintained generated files

`pyproject.toml` owns required runtime names and Python/dependency bounds;
`devtools/requirements.yaml` owns development/test/docs/build tools. The six
generated environment files use uibcdf then conda-forge; current CI/docs and helper
consumers enforce strict priority. scikit-learn is retained in development/tests/
docs only. Setup/build are build-only. The unused `importable_env.yaml` is an
explicitly inventoried historical MolSysMT resolved-package fixture, with its old
channels; it is not current LinDelINT source/public qualification. New use needs
owner review under `uibcdf/lindelint#9`.

After reviewing metadata/tool changes:

```bash
python devtools/broadcast_requirements.py
python devtools/broadcast_requirements.py --check
```

The broadcaster never writes the guarded Conda recipe. Update that recipe after
owner review and run the shared checks in [the publication guide](../conda-build/README.md).
Default preflight verifies actual installed bounds before source tests/docs;
declaration-only checks have no runtime or scientific qualification value.
Any workflow change also requires reviewing its recorded inventory digest and purpose.
