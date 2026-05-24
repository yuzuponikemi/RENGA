from abc import ABC, abstractmethod
from ..models import CopilotLog


class LogReader(ABC):
    @abstractmethod
    def read(self) -> list[CopilotLog]: ...
