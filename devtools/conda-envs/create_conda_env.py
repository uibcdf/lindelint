import argparse
import os
import re
import glob
import shutil
import subprocess as sp
from tempfile import TemporaryDirectory
from contextlib import contextmanager

# YAML imports
try:
    import yaml  # PyYAML
    loader = yaml.safe_load
except ImportError:
    try:
        import ruamel_yaml as yaml  # Ruamel YAML
    except ImportError:
        try:
            from importlib import util as import_util
            CONDA_BIN = os.path.dirname(os.environ['CONDA_EXE'])
            ruamel_yaml_path = glob.glob(os.path.join(CONDA_BIN, '..',
                                                      'lib', 'python*.*', 'site-packages',
                                                      'ruamel_yaml', '__init__.py'))[0]
            spec = import_util.spec_from_file_location('ruamel_yaml', ruamel_yaml_path)
            yaml = spec.loader.load_module()
        except (KeyError, ImportError, IndexError):
            raise ImportError("No YAML parser could be found. Please install PyYAML or Ruamel YAML.")
    loader = yaml.YAML(typ="safe").load


@contextmanager
def temp_cd():
    """Temporary working directory context."""
    cwd = os.getcwd()
    with TemporaryDirectory() as td:
        try:
            os.chdir(td)
            yield
        finally:
            os.chdir(cwd)


# Argument parsing
parser = argparse.ArgumentParser(description='Creates a conda environment from file for a given Python version.')
parser.add_argument('-n', '--name', type=str, required=True, help='The name of the created Python environment')
parser.add_argument('-p', '--python', type=str, required=True, help='The version of the created Python environment')
parser.add_argument('conda_file', help='The file for the created Python environment')

args = parser.parse_args()

# Load YAML file
with open(args.conda_file, "r") as handle:
    yaml_script = loader(handle.read())

# Ensure correct Python version in dependencies
python_replacement_string = f"python {args.python}*"
try:
    for dep_index, dep_value in enumerate(yaml_script['dependencies']):
        if re.match(r'python([ ><=*]+[0-9.*]*)?$', dep_value):
            yaml_script['dependencies'].pop(dep_index)
            break
except (KeyError, TypeError):
    yaml_script['dependencies'] = []
finally:
    yaml_script['dependencies'].insert(0, python_replacement_string)

# Find package manager (mamba preferred, conda fallback)
mamba_path = shutil.which("mamba")
conda_path = shutil.which("conda")

if mamba_path:
    package_manager = mamba_path
    print(f"Using Mamba: {mamba_path}")
elif conda_path:
    package_manager = conda_path
    print(f"Using Conda: {conda_path}")
else:
    raise RuntimeError("Neither Conda nor Mamba were found. Please install one of them.")

# Print environment details
print(f"Creating environment '{args.name}' with Python {args.python}")
print(f"Using package manager: {package_manager}")

# Create the environment using the preferred package manager
with temp_cd():
    temp_file_name = "temp_script.yaml"
    with open(temp_file_name, 'w') as f:
        f.write(yaml.dump(yaml_script))
    
    try:
        sp.run([package_manager, "env", "create", "-n", args.name, "-f", temp_file_name], check=True)
    except sp.CalledProcessError as e:
        print(f"Error creating environment: {e}")
        exit(1)

