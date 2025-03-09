from urllib.parse import urlencode
from os.path import normpath
from platform import system
from enum import Enum, auto
from typing import Union

from TraceElements import TextEditor
from Constants import k_editor_cfg_map

from robot.running import Keyword as LibraryKeyword, UserKeyword

class HyperlinkFactory:
    def __init__(self, editor: str):
        """Initialize HyperlinkFactory with an editor
        """
        self.editor = editor

    def create_hyperlink(self, implementation: Union[LibraryKeyword, UserKeyword], text: str) -> str:
        """Generate a hyperlink to a keyword's source file and line number
        """
        if not self.editor:
            return implementation.name  # Return plain text if no editor is set

        path = normpath(implementation.source)
        lineno = implementation.lineno
        editor_config = k_editor_cfg_map.get(self.editor, [{}])[0]  # Get editor config or empty dict
        uri_scheme = editor_config.get("uri_scheme", "")
        uri_args_list = editor_config.get("args", [])
        # Flatten args list of dicts into a single dictionary
        uri_args_dict = {key: value for arg in uri_args_list for key, value in arg.items()}
        # Convert dictionary to query string (e.g., "reuseWindow=true")
        query_string = urlencode(uri_args_dict) if uri_args_dict else ""
        # Construct the hyperlink
        hyperlink = (
            (f"{uri_scheme}://" if uri_scheme else "") +
            f"file:/{path}:{lineno}" +
            (f"?{query_string}" if query_string else "")
        )

        return f"\033]8;;{hyperlink}\033\\{text}\033]8;;\033\\"
