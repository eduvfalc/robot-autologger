from TraceElements import Trace

from abc import ABC, abstractmethod
from typing import Union

from robot.running import Keyword as KeywordData, LibraryKeyword, UserKeyword
from robot.result import Keyword as KeywordResult

class ICustomTrace(ABC):
    """An interface for the customization of traces logged during listener events
    """
    @abstractmethod
    def create_trace(self, data: KeywordData, 
                     implementation: Union[LibraryKeyword, UserKeyword],
                     result: KeywordResult) -> Trace:
        """Create a trace
        """
        pass