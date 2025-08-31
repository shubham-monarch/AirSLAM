- Ensure prerequisites are installed (ROS Noetic, CUDA 12.x, TensorRT 8.6.1.6, OpenCV 4.2, Eigen3, G2O, Ceres, Boost, Python).
- Clean the workspace (recommended before rebuilds):
  ```bash
  source /opt/ros/noetic/setup.bash
  cd /media/skumar/External/catkin_ws
  catkin clean -y
  ```
- If prior builds created root-owned artifacts, remove them:
  ```bash
  sudo rm -rf /media/skumar/External/catkin_ws/build /media/skumar/External/catkin_ws/devel
  # or: sudo chown -R $(whoami):$(whoami) /media/skumar/External/catkin_ws/{build,devel}
  ```
- Build with TensorRT headers/libs from `/home/skumar/ext_ssd/TensorRT-8.6.1.6`:
  ```bash
  CMAKE_INCLUDE_PATH=/home/skumar/ext_ssd/TensorRT-8.6.1.6/include \
  CMAKE_LIBRARY_PATH=/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib \
  CPATH=/home/skumar/ext_ssd/TensorRT-8.6.1.6/include \
  LIBRARY_PATH=/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib \
  catkin_make
  ```
- Source the workspace after a successful build:
  ```bash
  source /media/skumar/External/catkin_ws/devel/setup.bash
  ```
- (Optional) Verify `LD_LIBRARY_PATH` contains TensorRT libs for runtime:
  ```bash
  echo "$LD_LIBRARY_PATH" | tr ':' '\n' | grep TensorRT-8.6.1.6/lib || true
  ```
- Run VO demo launch (RViz enabled by default):
  ```bash
  roslaunch air_slam monarch.launch
  ```
