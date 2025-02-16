from typing import Union

from ICustomTrace import ICustomTrace
from TraceElements import Trace, Label, Color

from robot.libraries.BuiltIn import BuiltIn
from robot.running import Keyword as KeywordData, LibraryKeyword, UserKeyword
from robot.result import Keyword as KeywordResult

class StartKeywordTraceFactory(ICustomTrace):
    def __init__(self):
        self.lib_builtin = BuiltIn()

    def create_trace(self, data: KeywordData = None, 
                     implementation: Union[LibraryKeyword, UserKeyword] = None, 
                     result: KeywordResult = None) -> Trace:
        """Creates a trace for the start keyword event

        The `result` argument is not used.
        """
        return Trace(label=self._get_label(data),
                     text=self._get_text(data))

    def _get_label(self, data) -> str:
        """Start keyword trace label rules
        """
        match data.name:
            case _ if "Log" in data.name:
                return Label.log.value
            case _ if "Sleep" in data.name:
                return Label.sleep.value
            case _:
                return Label.busy.value
            
    def _get_text(self, data):
        """Start keyword trace text rules
        """
        match data.name:
            case _ if data.name == "Log":
                return self.lib_builtin.replace_variables(data.args[0])
            case _ if data.name == "Log Many":
                return self.args_to_str(data)
            case _ if data.name == "Log To Console":
                return ''
            case _:
                return self.lib_builtin.replace_variables(data.name)
            
class EndKeywordTraceFactory(ICustomTrace):
    """An implementation of ICustomTrace for end keyword events
    """
    def __init__(self):
        self.lib_builtin = BuiltIn()

    def create_trace(self, data: KeywordData = None, 
                     implementation: Union[LibraryKeyword, UserKeyword] = None, 
                     result: KeywordResult = None) -> Trace:
        """Creates a trace for the end keyword event
        """
        return Trace(label=self._get_label(result),
                     text=data.name)

    def _get_label(self, result) -> str:
        """End keyword trace label rules
        """
        match result:
            case _ if 'PASS' in result.status:
                return Label.success.value
            case _ if 'FAIL' in result.status:
                return Label.fail.value
            case _ if 'NOT RUN' in result.status:
                return ''