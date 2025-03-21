# smolagents/config.py

# Global configuration for the smolagents library
class SmolConfig:
    _use_prefect = False  # Default to False

    @classmethod
    def set_use_prefect(cls, value: bool):
        """Set the global use_prefect flag."""
        cls._use_prefect = bool(value)

    @classmethod
    def get_use_prefect(cls) -> bool:
        """Get the current value of use_prefect."""
        return cls._use_prefect

# Optional: Context manager for temporary changes
from contextlib import contextmanager

@contextmanager
def prefect_enabled(enabled: bool = True):
    """Temporarily enable or disable Prefect globally."""
    original = SmolConfig.get_use_prefect()
    SmolConfig.set_use_prefect(enabled)
    try:
        yield
    finally:
        SmolConfig.set_use_prefect(original)