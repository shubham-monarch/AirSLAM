#!/bin/bash

source /opt/ros/noetic/setup.bash
source ../../devel/setup.bash

roslaunch /workspace/src/AirSLAM/launch/map_refinement/monarch.launch

echo ""
echo "✅ Map refinement launch completed!"
