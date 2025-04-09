# robot-autologge
A logging facility for Robot Framework Listeners.

![Alt text](docs/example.png)

# Arguments

* `print_args`: bool, print keyword arguments
* `print_elapsed_time`: bool, print keyword elapsed time
* `index_keywords`: bool, print keyword uri
* `code_editor`: str, code editor to use in environments that support uri navigation

# Usage

To add the Robot Autologger to your Robot Framework test suite execution, add the following arguments to the `robot` command:

```
robot --console quiet --listener /path/to/Listener.py:<print args>:<print_elapsed_time>:<index_keywords>:<code_editor>
```

`--console quiet` since the `--listener` takes care of logging events from the test suite. 