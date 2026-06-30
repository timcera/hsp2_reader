"""Collection of functions for the manipulation of time series."""

# Local folder imports
from .hsp2_reader import hdf5
from .toolbox_utils.src.toolbox_utils.tsutils import about as _about


def about():
    """Display version number and system information."""
    _about(__name__)


__all__ = ["about", "hdf5"]
