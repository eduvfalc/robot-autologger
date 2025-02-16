from enum import Enum
from collections import namedtuple

class Color(Enum):
    """ANSI escape sequences for colors
    """
    red     = "\033[91m"
    green   = "\033[92m"
    magenta = "\033[35m"
    blue    = "\033[34m"

class TextFormat(Enum):
    """ANSI escape sequences for text formatting
    """
    clear  = "\033[0m"
    bold   = "\033[1m"
    italic = "\033[3m"

class Label(Enum):
    """Various character options for trace labeling
    """
    success = '✅'
    fail    = '❌'
    busy    = '⌛'
    log     = '🤖'
    sleep   = '💤'
    call    = '↪'
    report  = '📃'

class Trace(namedtuple('Trace', ['label', 'color', 'text_format', 'text'])):
    """A trace object.

    A trace is of the format:

    <label> <color> <text_format> <text> </text_format> </color>
    """
    def __new__(cls, label='', color='', text_format='', text=''):
        return super().__new__(cls, label, color, text_format, text)
    
    def to_str(self) -> str:
        """Return a trace as a string.
        """
        trace = ' '.join(str(item) for item in self if item != '')
        return trace + TextFormat.clear.value