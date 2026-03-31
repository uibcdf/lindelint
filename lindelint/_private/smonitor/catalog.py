# LinDelInt Diagnostics Catalog

CODES = {
    "LDL-E001": {
        "title": "Invalid Dimension",
        "user_message": "LinDelInt only works in 2D or 3D space. Current dimension: {dimension}.",
        "user_hint": "Ensure the points provided have 2 or 3 coordinates.",
    },
    "LDL-W010": {
        "title": "Degenerate Triangulation",
        "user_message": "The triangulation of points might be degenerate (simplices: {n_simplices}).",
        "user_hint": "Check for overlapping points or nearly collinear/coplanar point sets.",
    }
}

SIGNALS = {
    "lindelint.mesh.stats": {
        "description": "Geometric properties of the constructed Delaunay mesh.",
        "level": "DEBUG"
    },
    "lindelint.interpolator.do_your_thing": {
        "description": "Emitted during interpolation execution.",
        "level": "INFO"
    },
    "lindelint.interpolator.breakdown": {
        "description": "Breakdown of points inside vs outside the hull.",
        "level": "DEBUG"
    }
}
