from .interpolator_vectorized import InterpolatorVectorized
from argdigest import arg_digest
from depdigest import dep_digest
import numpy as np
import smonitor

class Interpolator():
    """
    High-level interface for Linear Delaunay Interpolation.
    Automatically selects the most efficient engine available.
    """

    @arg_digest()
    def __init__(self, points, properties, engine='auto'):
        
        self.points = points
        self.properties = properties
        self.engine_type = engine
        self._engine = None

        # --- SMonitor Diagnostic: Dimension Check ---
        dim = points.shape[1]
        if dim not in [2, 3]:
            smonitor.emit_from_catalog(
                "LDL-E001",
                extra={"dimension": dim},
                source="lindelint.Interpolator",
            )
            raise ValueError(f"LinDelInt only works in 2D or 3D space. Current dimension: {dim}")

        if engine == 'auto' or engine == 'parallel':
            try:
                from .interpolator_parallel import InterpolatorParallel
                self._engine = InterpolatorParallel(points, properties)
                self.engine_type = 'parallel'
            except ImportError:
                if engine == 'parallel':
                    raise ImportError("Numba is required for the 'parallel' engine.")
                engine = 'gpu'

        if (engine == 'auto' or engine == 'gpu') and self._engine is None:
            try:
                from .interpolator_gpu import InterpolatorGPU, HAS_CUPY
                if HAS_CUPY:
                    self._engine = InterpolatorGPU(points, properties)
                    self.engine_type = 'gpu'
                elif engine == 'gpu':
                    raise ImportError("CuPy is required for the 'gpu' engine.")
            except ImportError:
                if engine == 'gpu': raise
                engine = 'vectorized'

        if self._engine is None:
            self._engine = InterpolatorVectorized(points, properties)
            if engine == 'sequential':
                self.engine_type = 'sequential (vectorized fallback)'
            else:
                self.engine_type = 'vectorized'

    def do_your_thing(self, points):
        """
        Performs interpolation.
        """
        import time
        t_start = time.time()
        
        result = self._engine.do_your_thing(points)
        
        t_end = time.time()
        smonitor.emit(
            "INFO",
            "lindelint.interpolator.do_your_thing",
            source="lindelint.Interpolator",
            extra={
                "n_points": points.shape[0],
                "engine": self.engine_type,
                "time": t_end - t_start,
            },
        )
        
        return result
