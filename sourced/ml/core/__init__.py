"""MLonCode Core Library."""
try:
    import modelforge.configuration

    modelforge.configuration.refresh()
except ImportError:
    pass

__version__ = "0.0.1"
