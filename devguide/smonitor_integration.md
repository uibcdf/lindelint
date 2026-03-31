# SMonitor Integration

LinDelInt follows the **SMonitor** standard for diagnostics and telemetry.

## Diagnostic Codes

| Code | Level | Title | Description / Hint |
| :--- | :--- | :--- | :--- |
| `LDL-E001` | ERROR | Invalid Dimension | Only 2D or 3D spaces are supported. |
| `LDL-W010` | WARNING | Degenerate Mesh | The Delaunay triangulation resulted in zero simplices. Check for overlapping points. |

## Telemetry Signals

- **`lindelint.mesh.stats` (DEBUG):** Reports the number of simplices and base points in the Delaunay mesh.
- **`lindelint.interpolator.breakdown` (DEBUG):** Provides a detailed count of points processed in each phase:
    - `inside`: Points within the convex hull.
    - `triangles`: Points projected onto boundary faces.
    - `edges`: Points projected onto boundary edges.
    - `corners`: Points mapped to the nearest vertex.
- **`lindelint.interpolator.do_your_thing` (INFO):** Reports engine used, number of points, and execution time.
