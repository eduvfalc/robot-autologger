from shutil import get_terminal_size
from datetime import datetime
from typing import Union
from enum import Enum, auto

from Constants import k_newline_skip_list, k_skip_list, k_tab
from TraceElements import Trace, Color, Label
from TraceFactories import StartKeywordTraceFactory, EndKeywordTraceFactory

from robot.libraries.BuiltIn import BuiltIn
from robot.running import (TestSuite as TestSuiteData, 
                           TestCase as TestCaseData, 
                           Keyword as KeywordData, LibraryKeyword, UserKeyword)
from robot.result import (TestSuite as TestSuiteResult, 
                          TestCase as TestCaseResult, 
                          Keyword as KeywordResult)

class KeywordEvent(Enum):
    """Types of Listener events
    """
    start = auto()
    end = auto()

class AutoLogger:
    """Logging facility 
    """
    def __init__(self, print_args: bool = False,
                 print_elapsed_time: bool = False):
        """Constructor for the AutoLogger class.
        """
        self._init_log_factories()
        self._print_legend()
        self.builtin = BuiltIn()
        self.print_args = print_args
        self.print_elapsed_time = print_elapsed_time

    def start_suite(self, data: TestSuiteData, 
                    result: TestSuiteResult) -> None:
        """Print the test suite name and documentation.
        """
        docs = data.doc.replace("\n", " ")
        self._print_divider("=")
        print(f'Test suite: {data.name}\n'
              f'Documentation: {docs}')

    def start_test(self, data: TestCaseData, 
                   result: TestCaseResult):
        """ Print the test case name and documentation.
        The keyword level tracking is reset at test start
        """
        self._init_kw_trackers()
        self._print_divider("=")
        docs = data.doc.replace("\n", " ")
        print(f'Test case: {data.name}\n'
              f'Documentation: {docs}')
        self._print_divider("-")
    
    def end_suite(self, data: TestSuiteData, 
                  result: TestSuiteResult):
        """Print the suite results.
        These are:
        - execution time (in seconds)
        - total number of tests executed
        - number of tests passed
        - number of tests failed
        - number of tests skipped
        - suite result (PASS or FAIL)
        """
        color = Color.green if 'PASS' in result.status else Color.red
        self._print_divider("=")
        self._print_suite_stats(result)
        print(f'Suite result: {Trace(color=color.value, text=result.status).to_str()}')
        self._print_divider("=")

    def end_test(self, data: TestCaseData, 
                 result: TestCaseResult):
        """Print test case elapsed time and the test result.
        """
        color = Color.green if 'PASS' in result.status else Color.red
        time_elapsed = self._compute_time_elapsed_in_seconds(result.starttime, result.endtime)
        trace = Trace(color=color.value, text=result.status).to_str()
        self._print_divider("=")
        print(f'Test case finished in {time_elapsed} seconds\n'
              f'Test result: {trace}')

    def start_keyword(self, data: KeywordData, 
                           implementation: Union[LibraryKeyword, UserKeyword], 
                           result: KeywordResult):
        """Print start keyword trace

        <indentation> <label or adjust> <trace> <arguments>

        The <label or adjust> is printed if the keyword called is not in the test case body (root level)
        The <arguments> are only printed if the keyword is not in the skip list AND has arguments.
        """
        self._update_kw_tracking(KeywordEvent.start)
        # ignore keywords that were not executed
        if 'NOT RUN' not in result.status:
            # adjust line indent based on keyword level
            indent = (self.curr_kw_lvl - 1) * '\t'
            # add hourglass tag for first nested call, adjust indent otherwise
            label_or_adjust = f'{Trace(label=Label.call.value).to_str()} ' if self.curr_kw_lvl > self.prev_kw_lvl else '  '
            # get trace from start keyword trace factory
            trace = self.start_keyword_factory.create_trace(data=data).to_str()
            # some keywords write to the terminal so we have to adapt
            terminator = '\n' if data.name not in k_newline_skip_list else ' '
            # process arguments and create its trace
            args = self._args_to_str(data) if self.print_args and data.name not in k_skip_list else ''
            args_trace = Trace(color=Color.magenta.value, text=args).to_str()
            # print the whole thing combined
            print((indent + label_or_adjust if (self.curr_kw_lvl - 1) else '') + 
                  trace + ((k_tab + args_trace) if args else ''), end=terminator)

    def end_keyword(self, data: KeywordData, 
                         implementation: UserKeyword, 
                         result: KeywordResult):
        """Print end keyword trace

        <indentation> <result> <trace>
        """
        self._update_kw_tracking(KeywordEvent.end)
        if 'NOT RUN' not in result.status and data.name not in k_skip_list:
            # adjust line indent based on keyword level
            indent = self.curr_kw_lvl * '\t'
            # adjust indent if keyword is not at root level
            adjust = '  ' if self.curr_kw_lvl else ''
            # get trace from end keyword trace factory
            trace = self.end_keyword_factory.create_trace(data=data, result=result).to_str()
            # if the keyword failed, there should be a message
            msg = ': ' + result.message if result.message else ''
            msg = Trace(color=Color.red.value, text=msg).to_str()
            # compute total time elapsed if enabled
            dt_secs = str(result.elapsed_time.total_seconds()) if self.print_elapsed_time else ''
            elapsed_time = Trace(color=Color.blue.value, text=('finished in ' + dt_secs + ' seconds')).to_str()
            # print the whole thing combined
            print((indent + adjust if self.curr_kw_lvl else '') + 
                  trace + ((k_tab + elapsed_time) if dt_secs else ''))

    def report_file(self, path: str) -> None:
        """Print path to report file
        """
        print(Trace(label=Label.report.value, 
                    text=f'Report file path: ' + str(path)).to_str())

    def log_file(self, path: str) -> None:
        """Print path to log file
        """
        print(Trace(label=Label.report.value, 
                    text=f'Log file path: ' + str(path)).to_str())

    def output_file(self, path: str) -> None:
        """Print path to output file
        """
        print(Trace(label=Label.report.value, 
                    text=f'Output file path: ' + str(path)).to_str())

    def _print_legend(self) -> None:
        print(f'{Trace(text="Robot Framework Pretty Logger").to_str()}\n'
              f'{Trace(text="Legend:").to_str()} '
              f'{Trace(label=Label.success.value, text="Pass").to_str()} '
              f'{Trace(label=Label.fail.value, text="Fail").to_str()} '
              f'{Trace(label=Label.busy.value, text="Running").to_str()} '
              f'{Trace(label=Label.call.value, text="Nested call").to_str()}')
        
    def _print_suite_stats(self, result) -> None:
        elapsed_time = self._compute_time_elapsed_in_seconds(result.starttime, result.endtime)
        print(f'Test suite finished in {elapsed_time} seconds\n'
              f'{result.statistics.total} executed,'
              f'{Trace(color=Color.green.value, text=result.statistics.passed).to_str()} passed,'
              f'{Trace(color=Color.red.value, text=result.statistics.failed).to_str()} failed,'
              f' {result.statistics.skipped} skipped')
    
    def _print_divider(self, character: str) -> None:
        print(character * get_terminal_size().columns)

    def _init_kw_trackers(self) -> None:
        """Initialize keyword trackers
        """
        self.curr_kw_lvl = self.prev_kw_lvl = 0

    def _compute_time_elapsed_in_seconds(self, start_time: str = 0, 
                                         end_time: str = 0) -> float:
        """Compute the time elapsed between two timestamps.
        """
        time_format = "%Y%m%d %H:%M:%S.%f"
        elapsed_time = datetime.strptime(end_time, time_format) - datetime.strptime(start_time, time_format)
        return elapsed_time.total_seconds()

    def _init_log_factories(self) -> None:
        """Initialize the log factories used in the Listener events
        """
        self.start_keyword_factory = StartKeywordTraceFactory()
        self.end_keyword_factory = EndKeywordTraceFactory()

    def _args_to_str(self, data) -> str:
        return k_tab.join(str(arg) for arg in self._get_args_list(data))

    def _get_args_list(self, data) -> list:
        args = []
        for arg in data.args:
            args.append(self.builtin.replace_variables(arg))
        return args
    
    def _update_kw_tracking(self, event: KeywordEvent) -> None:
        """Update keyword tracking based on event type
        """
        if event == KeywordEvent.start:
            self.curr_kw_lvl += 1
        elif event == KeywordEvent.end:
            self.prev_kw_lvl = self.curr_kw_lvl
            self.curr_kw_lvl -= 1