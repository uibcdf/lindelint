# LinDelInt DepDigest Configuration

LIBRARIES = {
    'numpy': {'type': 'hard', 'pypi': 'numpy'},
    'scipy': {'type': 'hard', 'pypi': 'scipy'},
    'cupy': {'type': 'soft', 'pypi': 'cupy'},
}

MAPPING = {
    'Delaunay': 'scipy.spatial',
    'KDTree': 'scipy.spatial',
    'cupy_array': 'cupy',
}
