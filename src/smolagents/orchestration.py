# smolagents/orchestration.py

import logging
from typing import Any, Callable, Optional

# Conditional Prefect import
try:
    from prefect import flow, task
    from prefect.tasks import NO_CACHE
    PREFECT_AVAILABLE = True
except ImportError:
    PREFECT_AVAILABLE = False
    flow = lambda x: x  # No-op decorator
    task = lambda x, **kwargs: x
    NO_CACHE = None

from smolagents.config import SmolConfig

# Conditional Orchestration Decorator
class PrefectOrchestrator:
    def __init__(self, name: str | Callable[[Any], str], type: str = 'task', cache_policy: Optional[Any] = None, retry: Optional[int] = 0):
        self.name = name
        self.type = type.lower()
        self.cache_policy = cache_policy
        if self.type not in ['task', 'flow']:
            raise ValueError(f"Invalid type '{self.type}'. Must be 'task' or 'flow'.")

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        use_prefect = SmolConfig.get_use_prefect()
        name = self.name(obj) if callable(self.name) else self.name
        # print(f"\n\n\n\nuse_prefect:{use_prefect}, type:{self.type}, name:{name}\n\n\n\n")
        if use_prefect and PREFECT_AVAILABLE:
            if self.type == 'task':
                return task(self.func, name=name, cache_policy=self.cache_policy).__get__(obj, objtype)
            elif self.type == 'flow':
                decorated = flow(self.func, name=name)
                return lambda *args, **kwargs: decorated(obj, *args, **kwargs)
        return self.func.__get__(obj, objtype)

    def __call__(self, func):
        self.func = func
        return self
    
    

