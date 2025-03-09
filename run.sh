#!/usr/bin/env bash
robot --console quiet \
      --listener src/Listener.py:True:True:True:code \
      --outputdir ..//out/test-run/ \
      ../RobotDemo/data_driven.robot
