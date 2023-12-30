__all__ = ["result_unit"]

from collections.abc import Callable

from astropy.units import dimensionless_unscaled

from units._dimension.core import Dimension
from units._unit.core import Unit

dimensionless = Unit(dimensionless_unscaled)


def result_unit(op: str, *units: Unit) -> Unit:
    """Get the result unit of an operation.

    Parameters
    ----------
    op : str
        The operation to perform.
    *units : `~astropy.units.Unit`
        The units to operate on.

    Returns
    -------
    `~astropy.units.Unit`
        The result unit.
    """
    return _RESULT_UNIT_OP[op](units)


def _trig(units: tuple[Unit, ...]) -> Unit:
    if len(units) != 1:
        msg = "trig operation requires exactly one unit."
        raise ValueError(msg)
    if units[0].dimensions != Dimension("angle"):
        msg = "trig operation requires a dimensionless unit."
        raise ValueError(msg)
    return dimensionless


def _sigmoid(units: tuple[Unit, ...]) -> Unit:
    if len(units) != 1:
        msg = "sigmoid operation requires exactly one unit."
        raise ValueError(msg)
    if units[0].dimensions != Dimension("dimensionless"):
        msg = "sigmoid operation requires a dimensionless unit."
        raise ValueError(msg)
    return dimensionless


_RESULT_UNIT_OP: dict[str, Callable[[tuple[Unit, ...]], Unit]] = {
    "add": lambda units: units[0] + units[1],
    "subtract": lambda units: units[0] - units[1],
    "multiply": lambda units: units[0] * units[1],
    "divide": lambda units: units[0] / units[1],
    "cos": _trig,
    "sin": _trig,
    "numpy.cos": _trig,
    "pytorch.sigmoid": _sigmoid,
}
