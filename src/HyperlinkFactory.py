from platform import system, uname
from os.path import normpath, exists
from enum import Enum, auto
from typing import Union
from platform import system

from TraceElements import TextEditor
from Constants import k_editor_cfg_map, k_wsl_bin_misc_path

from robot.running import Keyword as LibraryKeyword, UserKeyword

class OSType(Enum):
    linux = auto()
    wsl = auto()
    windows = auto()
    unsupported = auto()

class HyperlinkFactory:
    def __init__(self, editor: TextEditor = None):
        """Constructor of the Hyperlink Factory
        """
        self.editor = editor
        self._detect_os()

    def create_hyperlink(self, implementation: Union[LibraryKeyword, UserKeyword], text: str) -> str:
        """Add hyperlink to keyword name pointing to source file and line number
        """
        if self.editor is None:
            return text
        path = normpath(implementation.source)
        lineno = implementation.lineno
        uri_scheme = k_editor_cfg_map[self.editor][0]['uri_scheme']
        url = f"{uri_scheme}://file//wsl.localhost/Ubuntu-22.04/{path}:{lineno}?reuseWindow=true"
        return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"
    
    def _detect_os(self) -> None:
        """Determine operating system
        """
        os = system()
        if os == "Windows":
            self.os = OSType.windows
        elif os == "Linux":
            # Check if running inside WSL
            if "microsoft" in uname().release.lower() or exists(k_wsl_bin_misc_path):
                self.os = OSType.wsl
            else:
                self.os = OSType.linux
        else:
            self.os = OSType.unsupported