# Configure PyUnitWizard for LinDelInt

import pyunitwizard as puw

# Standard units configuration for the MolSysSuite
puw.configure.set_default_form('pint')
puw.configure.set_default_parser('pint')
puw.configure.set_standard_units(['nm', 'ps', 'K', 'mole', 'dalton', 'e',
                                 'kJ/mol', 'kJ/(mol*nm)', 'kJ/(mol*nm**2)', 'radians'])

# Canonical fast-tracks
puw.register_fast_track("nanometers", puw.unit("nm"))
puw.register_fast_track("picoseconds", puw.unit("ps"))
