# API Conventions

To ensure consistency within the **MolSysSuite**, LinDelInt follows strict conventions for its computational interface.

## Core Interface: `Interpolator`

The primary class is `Interpolator`. It is initialized with base data and provides a unified method for interpolation.

### Method Naming

| Method | Intent | Status |
| :--- | :--- | :--- |
| `do_your_thing(points)` | Main execution method. | **Legacy** (Current) |
| `interpolate(points)` | Alias for `do_your_thing`. | **Recommended** (Future) |

### Input Standards

- **Points:** Must be a 2D NumPy array of shape `(N, D)`, where `D` is 2 or 3.
- **Properties:** Must be a 2D NumPy array of shape `(N, P)`, where `P` is the number of properties to interpolate.
- **Data Types:** `float64` is preferred for coordinates to avoid precision issues in Delaunay triangulation.

## Parameter Handling

- All public methods must be decorated with `@arg_digest()` to ensure point arrays are correctly formed.
- Execution engines (`auto`, `parallel`, `vectorized`) are specified at instantiation.
