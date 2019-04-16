"""MLonCode research playground."""
import pkg_resources
pkg_resources.declare_namespace(__name__)
try:
    import modelforge.configuration

    modelforge.configuration.refresh()
except ImportError:
    pass

__version__ = "0.8.3"
