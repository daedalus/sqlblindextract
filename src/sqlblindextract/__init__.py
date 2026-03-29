__version__ = "0.1.0"
__all__ = [
    "measure",
    "getlength",
    "getbits",
    "getdata",
]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import getbits, getdata, getlength, measure


def __getattr__(name: str) -> object:
    if name in __all__:
        from . import core

        return getattr(core, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
