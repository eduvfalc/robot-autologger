# keywords whose logs should not add a new line
k_newline_skip_list = [
    "Log To Console"
]

# keywords whose logging should be skipped
k_skip_list = [
    "Log",
    "Log To Console",
    "Log Many",
    "Comment"
]

# tab (4 spaces for indentations)
k_tab = 4 * ' '

# editor configurations
k_editor_cfg_map = {'code': 
                        [
                            {
                                'uri_scheme' : 'vscode'
                            }
                        ]
                    }
                            
# path used to check if linux is running inside WSL
k_wsl_bin_misc_path = "/proc/sys/fs/binfmt_misc/WSL"