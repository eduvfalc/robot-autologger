# robot-autologger
The Robot Autologger is a terminal logger for Robot Framework that uses the linstener interface to automate . It can be used to automatically log listener events and provide real time test execution reporting. By default, Robot Framework's native logging doesn't provide much information about test performance _while_ the text is executed. The Robot Autologger is here to enable real time reporting to Robot Framework users.

An example of the Robot Autologger output is:

![Alt text](docs/example.png)

The Autologger allows users to enable/disable keyword arguments and elapsed time information. These features are disabled by default.

# Usage

To add the Robot Autologger to your Robot Framework test suite execution, add the following arguments to the `robot` command:

```
robot --console quiet \
      --listener /path/to/Listener.py:True:True \
      /path/to/test_suite.robot
```