from typing import Any
import logging
from rich.console import Console
from rich.logging import RichHandler
from .singleton import SingletonMeta


class AppLogger(metaclass=SingletonMeta):
    _logger = None

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def get_logger(self) -> logging.Logger | None:
        return self._logger


class RichConsoleHandler(RichHandler):
    def __init__(self, width: int = 200, style: Any = None, **kwargs: Any) -> None:
        super().__init__(
            console=Console(color_system="256", width=width, style=style), **kwargs
        )
