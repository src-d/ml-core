import sys
from unittest import SkipTest

from modelforge import slogging


utmain = sys.modules["__main__"]
if utmain.__package__ == "unittest" and utmain.__spec__ is None:
    from collections import namedtuple
    ModuleSpec = namedtuple("ModuleSpec", ["name"])
    utmain.__spec__ = ModuleSpec("unittest.__main__")
    del ModuleSpec
del utmain


def has_tensorflow():
    try:
        import tensorflow  # noqa
        return True
    except ImportError:
        return False


def setup():
    slogging.setup("INFO", False)
