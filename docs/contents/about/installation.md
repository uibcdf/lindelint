# Installation

The official public route is the [UIBCDF Conda channel](https://anaconda.org/uibcdf/lindelint).
Its latest inspected version is **0.2.0** (2026-10-06 registry review), with 18
historical platform/interpreter-specific files. These files predate the current
source dependency and Python contracts; they are not evidence that today's
source is available as an installed package on Python 3.14.

Current source targets Python 3.11–3.14. The prepared publication workflow will
build one reviewed `noarch: python` file, qualify those same bytes outside source
on Linux and macOS arm64 across all four minors, and promote that file without
rebuilding. This route is not yet a new public release. A clean public-channel
installation must be measured before recommending a current installation command.
Follow [uibcdf/lindelint#13](https://github.com/uibcdf/lindelint/issues/13) for
distribution controls and [uibcdf/lindelint#14](https://github.com/uibcdf/lindelint/issues/14)
for delivery and Python admission.

GitHub's historical releases have no wheel/sdist assets. No public PyPI route or
Windows installed qualification is claimed here. Local source installation and
development environments are described in the repository's
`devtools/conda-envs/README.md`; source tests do not certify a public artifact.
