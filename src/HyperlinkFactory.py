from urllib.parse import urlencode
from os.path import normpath
from typing import Union

from Constants import k_editor_cfg_map

from robot.running import Keyword as LibraryKeyword, UserKeyword

class HyperlinkFactory:
    def __init__(self, editor: str):
        """Initialize HyperlinkFactory with an editor
        """
        self.editor = editor
        editor_config = k_editor_cfg_map.get(self.editor, [{}])[0]
        self.uri_scheme = editor_config.get("uri_scheme", "")
        uri_args_list = editor_config.get("args", [])
        uri_args_dict = {key: value for arg in uri_args_list for key, value in arg.items()}
        self.uri_args_query_str = urlencode(uri_args_dict) if uri_args_dict else ""

    def create_hyperlink(self, implementation: Union[LibraryKeyword, UserKeyword], 
                         text: str) -> str:
        """Generate a hyperlink to a keyword's source file and line number
        """
        if not self.editor:
            # Return plain text if no editor is set
            return implementation.name  

        # Construct the uri
        uri = (
            (f"{self.uri_scheme}://" if self.uri_scheme else "") +
            f"file:/{normpath(implementation.source)}:{implementation.lineno}" +
            (f"?{self.uri_args_query_str}" if self.uri_args_query_str else "")
        )

        # Create and return hyperlink
        return f"\033]8;;{uri}\033\\{text}\033]8;;\033\\"