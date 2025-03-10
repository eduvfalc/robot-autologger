from Constants import k_tab
from robot.libraries.BuiltIn import BuiltIn as robot_builtin

from robot.running import Keyword as KeywordData

def args_to_str(data: KeywordData) -> str:
    """Convert keyword arguments to string to be used in trace
    """
    return k_tab.join(str(arg) for arg in get_args_list(data))

def get_args_list(data: KeywordData) -> list:
    args = []
    for arg in data.args:
        args.append(robot_builtin().replace_variables(arg))
    return args