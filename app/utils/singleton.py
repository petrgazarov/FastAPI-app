from typing import Dict, Type, Any, Tuple
from threading import Lock


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances: Dict[Type[Any], Any] = {}

    _lock: Lock = Lock()

    def __call__(cls: Any, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
