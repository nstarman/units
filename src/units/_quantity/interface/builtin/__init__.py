"""Builtin interfaces."""

__all__: list[str] = []


from importlib.util import find_spec

from . import numpy_interface
from .numpy_interface import *

__all__ += numpy_interface.__all__

# Dask
if find_spec("dask"):
    from . import dask_interface
    from .dask_interface import *

    __all__ += dask_interface.__all__
