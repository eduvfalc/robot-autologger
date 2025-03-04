from robot.running import (TestSuite as TestSuiteData, 
                           TestCase as TestCaseData, 
                           Keyword as KeywordData, LibraryKeyword, UserKeyword)
from robot.result import (TestSuite as TestSuiteResult, 
                          TestCase as TestCaseResult, 
                          Keyword as KeywordResult)

from AutoLogger import AutoLogger

class Listener:
    """Robot Framework Listener v3 interface implementation.
    """
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, print_args: bool = False,
                 print_elapsed_time: bool = False,
                 index_keywords: bool = False,
                 editor: str = None):
        self.logger = AutoLogger(print_args,
                                 print_elapsed_time, 
                                 index_keywords,
                                 editor)

    def start_suite(self, data: TestSuiteData, 
                    result: TestSuiteResult):
        self.logger.start_suite(data, result)

    def start_test(self, data: TestCaseData, 
                   result: TestCaseResult):
        self.logger.start_test(data, result)
    
    def end_suite(self, data: TestSuiteData, 
                  result: TestSuiteResult):
        self.logger.end_suite(data, result)

    def end_test(self, data: TestCaseData, 
                 result: TestCaseResult):
        self.logger.end_test(data, result)

    def start_user_keyword(self, data: KeywordData, 
                           implementation: UserKeyword, 
                           result: KeywordResult):
        self.logger.start_keyword(data, implementation, result)

    def end_user_keyword(self, data: KeywordData, 
                         implementation: UserKeyword, 
                         result: KeywordResult):
        self.logger.end_keyword(data, implementation, result)

    def start_library_keyword(self, data: KeywordData, 
                              implementation: LibraryKeyword, 
                              result: KeywordResult):
        self.logger.start_keyword(data, implementation, result)


    def end_library_keyword(self, data: KeywordData, 
                            implementation: LibraryKeyword, 
                            result: KeywordResult):
        self.logger.end_keyword(data, implementation, result)

    def report_file(self, path: str):
        self.logger.report_file(path)
        
    def log_file(self, path: str):
        self.logger.log_file(path)

    def output_file(self, path: str):
        self.logger.output_file(path)