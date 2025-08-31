# Check TensorRT dependency in CMakeLists.txt
_Exported on 31/08/2025 at 15:54:05 GMT+5:30 from Cursor (1.5.7)_

---

**User**

Can you go through @CMakeLists.txt and tell me whether it depends on the `TensorRT` package?

---

**Cursor**

Yes, the `CMakeLists.txt` file does depend on TensorRT. Here's the evidence:

1. **TensorRT Libraries Linked**: The file links against TensorRT libraries in the `target_link_libraries` section:
   - `nvinfer` (line 91) - TensorRT's inference engine
   - `nvonnxparser` (line 92) - TensorRT's ONNX parser

2. **Custom TensorRT Wrapper**: It includes a subdirectory for `tensorrtbuffer` (line 9), which appears to be a custom wrapper or utility for TensorRT, and links against it (line 100).

The dependency is implicit rather than explicit - there are no `find_package(TensorRT)` calls, but the linking against TensorRT's core libraries (`nvinfer` and `nvonnxparser`) makes TensorRT a required dependency for building this project. The project uses TensorRT for neural network inference, likely for computer vision tasks given the presence of OpenCV and other CV-related components.

---

**User**

I have not installed `TensorRT` at the default location. 
Instead, I have installed it at `/home/skumar/ext_ssd/TensorRT-8.6.1.6`.
Is there a way to update @CMakeLists.txt to make it look for the `TensorRT` at this location instead?

---

**Cursor**

```cmake
cmake_minimum_required(VERSION 3.5)
project(air_slam)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE "release")
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
add_definitions(-w)

# Add custom TensorRT installation path
set(CMAKE_PREFIX_PATH "${CMAKE_PREFIX_PATH};/home/skumar/ext_ssd/TensorRT-8.6.1.6")
set(TENSORRT_ROOT "/home/skumar/ext_ssd/TensorRT-8.6.1.6")

add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/tensorrtbuffer)
add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/DBoW2)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  geometry_msgs
  image_transport
  nav_msgs
  roscpp
  rospy
  std_msgs
  sensor_msgs
  tf
)

find_package(OpenCV 4.2 REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(CUDA REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package(Boost REQUIRED)
find_package(G2O REQUIRED)
find_package(Gflags REQUIRED)
find_package(Glog REQUIRED)

catkin_package(
 INCLUDE_DIRS include
 LIBRARIES ${PROJECT_NAME}_lib
 CATKIN_DEPENDS geometry_msgs image_transport nav_msgs roscpp rospy std_msgs
)

include_directories(
  ${PROJECT_SOURCE_DIR}
  ${PROJECT_SOURCE_DIR}/include
  ${OpenCV_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
  ${CUDA_INCLUDE_DIRS}
  ${YAML_CPP_INCLUDE_DIR}
  ${Boost_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
  ${G2O_INCLUDE_DIR}
  ${GFLAGS_INCLUDE_DIRS} 
  ${GLOG_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME}_lib SHARED
  src/g2o_optimization/vertex_line3d.cc
  src/g2o_optimization/vertex_vi_pose.cc
  src/g2o_optimization/vertex_imu.cc
  src/g2o_optimization/edge_project_point.cc
  src/g2o_optimization/edge_project_line.cc
  src/g2o_optimization/edge_imu.cc
  src/g2o_optimization/edge_relative_pose.cc
  src/g2o_optimization/g2o_optimization.cc
  src/bow/FSuperpoint.cc
  src/bow/database.cc
  src/super_point.cpp
  src/feature_detector.cc
  src/super_glue.cpp
  src/light_glue.cpp
  src/plnet.cpp
  src/utils.cc
  src/camera.cc
  src/imu.cc
  src/dataset.cc
  src/frame.cc
  src/point_matcher.cc
  src/mappoint.cc
  src/mapline.cc
  src/line_processor.cc
  src/ros_publisher.cc
  src/map.cc
  src/map_builder.cc
  src/map_refiner.cc
  src/map_user.cc
  src/timer.cc
  src/debug.cc
)

target_link_libraries(${PROJECT_NAME}_lib
  nvinfer
  nvonnxparser
  ${OpenCV_LIBRARIES}
  ${CUDA_LIBRARIES}
  ${Boost_LIBRARIES}
  ${G2O_LIBRARIES}
  ${GFLAGS_LIBRARIES} 
  ${GLOG_LIBRARIES}
  yaml-cpp
  tensorrtbuffer
  DBoW2
  -lboost_serialization
)

add_executable(visual_odometry demo/visual_odometry.cpp)
target_link_libraries(visual_odometry ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(map_refinement demo/map_refinement.cpp)
target_link_libraries(map_refinement ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(relocalization demo/relocalization.cpp)
target_link_libraries(relocalization ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(test_feature demo/test_feature.cpp)
target_link_libraries(test_feature ${PROJECT_NAME}_lib ${catkin_LIBRARIES})
```

```cmake
cmake_minimum_required(VERSION 3.5)
project(air_slam)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE "release")
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
add_definitions(-w)

# Add custom TensorRT installation path
set(CMAKE_PREFIX_PATH "${CMAKE_PREFIX_PATH};/home/skumar/ext_ssd/TensorRT-8.6.1.6")
set(TENSORRT_ROOT "/home/skumar/ext_ssd/TensorRT-8.6.1.6")

add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/tensorrtbuffer)
add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/DBoW2)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  geometry_msgs
  image_transport
  nav_msgs
  roscpp
  rospy
  std_msgs
  sensor_msgs
  tf
)

find_package(OpenCV 4.2 REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(CUDA REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package(Boost REQUIRED)
find_package(G2O REQUIRED)
find_package(Gflags REQUIRED)
find_package(Glog REQUIRED)

catkin_package(
 INCLUDE_DIRS include
 LIBRARIES ${PROJECT_NAME}_lib
 CATKIN_DEPENDS geometry_msgs image_transport nav_msgs roscpp rospy std_msgs
)

include_directories(
  ${PROJECT_SOURCE_DIR}
  ${PROJECT_SOURCE_DIR}/include
  ${OpenCV_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
  ${CUDA_INCLUDE_DIRS}
  ${YAML_CPP_INCLUDE_DIR}
  ${Boost_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
  ${G2O_INCLUDE_DIR}
  ${GFLAGS_INCLUDE_DIRS}
  ${GLOG_INCLUDE_DIRS}
  ${TENSORRT_ROOT}/include
)

add_library(${PROJECT_NAME}_lib SHARED
  src/g2o_optimization/vertex_line3d.cc
  src/g2o_optimization/vertex_vi_pose.cc
  src/g2o_optimization/vertex_imu.cc
  src/g2o_optimization/edge_project_point.cc
  src/g2o_optimization/edge_project_line.cc
  src/g2o_optimization/edge_imu.cc
  src/g2o_optimization/edge_relative_pose.cc
  src/g2o_optimization/g2o_optimization.cc
  src/bow/FSuperpoint.cc
  src/bow/database.cc
  src/super_point.cpp
  src/feature_detector.cc
  src/super_glue.cpp
  src/light_glue.cpp
  src/plnet.cpp
  src/utils.cc
  src/camera.cc
  src/imu.cc
  src/dataset.cc
  src/frame.cc
  src/point_matcher.cc
  src/mappoint.cc
  src/mapline.cc
  src/line_processor.cc
  src/ros_publisher.cc
  src/map.cc
  src/map_builder.cc
  src/map_refiner.cc
  src/map_user.cc
  src/timer.cc
  src/debug.cc
)

target_link_libraries(${PROJECT_NAME}_lib
  nvinfer
  nvonnxparser
  ${OpenCV_LIBRARIES}
  ${CUDA_LIBRARIES}
  ${Boost_LIBRARIES}
  ${G2O_LIBRARIES}
  ${GFLAGS_LIBRARIES} 
  ${GLOG_LIBRARIES}
  yaml-cpp
  tensorrtbuffer
  DBoW2
  -lboost_serialization
)

add_executable(visual_odometry demo/visual_odometry.cpp)
target_link_libraries(visual_odometry ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(map_refinement demo/map_refinement.cpp)
target_link_libraries(map_refinement ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(relocalization demo/relocalization.cpp)
target_link_libraries(relocalization ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(test_feature demo/test_feature.cpp)
target_link_libraries(test_feature ${PROJECT_NAME}_lib ${catkin_LIBRARIES})
```

```cmake
cmake_minimum_required(VERSION 3.5)
project(air_slam)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE "release")
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
add_definitions(-w)

# Add custom TensorRT installation path
set(CMAKE_PREFIX_PATH "${CMAKE_PREFIX_PATH};/home/skumar/ext_ssd/TensorRT-8.6.1.6")
set(TENSORRT_ROOT "/home/skumar/ext_ssd/TensorRT-8.6.1.6")

add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/tensorrtbuffer)
add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/DBoW2)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  geometry_msgs
  image_transport
  nav_msgs
  roscpp
  rospy
  std_msgs
  sensor_msgs
  tf
)

find_package(OpenCV 4.2 REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(CUDA REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package(Boost REQUIRED)
find_package(G2O REQUIRED)
find_package(Gflags REQUIRED)
find_package(Glog REQUIRED)

catkin_package(
 INCLUDE_DIRS include
 LIBRARIES ${PROJECT_NAME}_lib
 CATKIN_DEPENDS geometry_msgs image_transport nav_msgs roscpp rospy std_msgs
)

include_directories(
  ${PROJECT_SOURCE_DIR}
  ${PROJECT_SOURCE_DIR}/include
  ${OpenCV_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
  ${CUDA_INCLUDE_DIRS}
  ${YAML_CPP_INCLUDE_DIR}
  ${Boost_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
  ${G2O_INCLUDE_DIR}
  ${GFLAGS_INCLUDE_DIRS}
  ${GLOG_INCLUDE_DIRS}
  ${TENSORRT_ROOT}/include
)

# Add TensorRT library directory
link_directories(${TENSORRT_ROOT}/lib)

add_library(${PROJECT_NAME}_lib SHARED
  src/g2o_optimization/vertex_line3d.cc
  src/g2o_optimization/vertex_vi_pose.cc
  src/g2o_optimization/vertex_imu.cc
  src/g2o_optimization/edge_project_point.cc
  src/g2o_optimization/edge_project_line.cc
  src/g2o_optimization/edge_imu.cc
  src/g2o_optimization/edge_relative_pose.cc
  src/g2o_optimization/g2o_optimization.cc
  src/bow/FSuperpoint.cc
  src/bow/database.cc
  src/super_point.cpp
  src/feature_detector.cc
  src/super_glue.cpp
  src/light_glue.cpp
  src/plnet.cpp
  src/utils.cc
  src/camera.cc
  src/imu.cc
  src/dataset.cc
  src/frame.cc
  src/point_matcher.cc
  src/mappoint.cc
  src/mapline.cc
  src/line_processor.cc
  src/ros_publisher.cc
  src/map.cc
  src/map_builder.cc
  src/map_refiner.cc
  src/map_user.cc
  src/timer.cc
  src/debug.cc
)

target_link_libraries(${PROJECT_NAME}_lib
  nvinfer
  nvonnxparser
  ${OpenCV_LIBRARIES}
  ${CUDA_LIBRARIES}
  ${Boost_LIBRARIES}
  ${G2O_LIBRARIES}
  ${GFLAGS_LIBRARIES} 
  ${GLOG_LIBRARIES}
  yaml-cpp
  tensorrtbuffer
  DBoW2
  -lboost_serialization
)

add_executable(visual_odometry demo/visual_odometry.cpp)
target_link_libraries(visual_odometry ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(map_refinement demo/map_refinement.cpp)
target_link_libraries(map_refinement ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(relocalization demo/relocalization.cpp)
target_link_libraries(relocalization ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(test_feature demo/test_feature.cpp)
target_link_libraries(test_feature ${PROJECT_NAME}_lib ${catkin_LIBRARIES})
```

Perfect! I've updated your `CMakeLists.txt` file to look for TensorRT at your custom installation location. Here are the changes I made:

## Changes Made:

1. **Added TensorRT path variables** (lines 9-11):
   - Set `CMAKE_PREFIX_PATH` to include your TensorRT installation directory
   - Set `TENSORRT_ROOT` variable pointing to `/home/skumar/ext_ssd/TensorRT-8.6.1.6`

2. **Added TensorRT include directory** (line 58):
   - Added `${TENSORRT_ROOT}/include` to the `include_directories` list

3. **Added TensorRT library directory** (lines 61-62):
   - Added `link_directories(${TENSORRT_ROOT}/lib)` to ensure the linker can find the TensorRT libraries

## How it works:

- `CMAKE_PREFIX_PATH` tells CMake to search for packages in your custom TensorRT directory
- `TENSORRT_ROOT` provides a convenient variable for referencing the installation path
- The include directory addition ensures header files are found during compilation
- The link directory ensures the linker can find `nvinfer` and `nvonnxparser` libraries

Now when you build your project, CMake should automatically find TensorRT at `/home/skumar/ext_ssd/TensorRT-8.6.1.6` instead of the default system location.

You can test this by running `catkin_make` from your workspace root. If you encounter any issues, the build error messages will help identify if any paths need adjustment.

---

**User**

can you now run `catkin clean -y` and then `catkin_make` to test if  the build is successful? 

---

**Cursor**

```cmake
cmake_minimum_required(VERSION 3.6)
project(tensorrtbuffer)

set(CMAKE_CXX_STANDARD 17)

if(POLICY CMP0146)
    cmake_policy(SET CMP0146 OLD)
endif()

find_package(CUDA REQUIRED)
include_directories("${CUDA_INCLUDE_DIRS}")

# Add TensorRT include directory from custom installation
include_directories("/home/skumar/ext_ssd/TensorRT-8.6.1.6/include")

include_directories(
    ${PROJECT_SOURCE_DIR}/include
)

set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

add_library(tensorrtbuffer SHARED src/logger.cpp src/sample_options.cpp src/sample_utils.cpp)




```

```cmake
cmake_minimum_required(VERSION 3.6)
project(tensorrtbuffer)

set(CMAKE_CXX_STANDARD 17)

if(POLICY CMP0146)
    cmake_policy(SET CMP0146 OLD)
endif()

find_package(CUDA REQUIRED)
include_directories("${CUDA_INCLUDE_DIRS}")

# Add TensorRT include directory from custom installation
include_directories("/home/skumar/ext_ssd/TensorRT-8.6.1.6/include")

# Add TensorRT library directory
link_directories("/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib")

include_directories(
    ${PROJECT_SOURCE_DIR}/include
)

set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

add_library(tensorrtbuffer SHARED src/logger.cpp src/sample_options.cpp src/sample_utils.cpp)




```

```cmake
cmake_minimum_required(VERSION 3.6)
project(tensorrtbuffer)

set(CMAKE_CXX_STANDARD 17)

if(POLICY CMP0146)
    cmake_policy(SET CMP0146 OLD)
endif()

find_package(CUDA REQUIRED)
include_directories("${CUDA_INCLUDE_DIRS}")

# Add TensorRT include directory from custom installation
include_directories("/home/skumar/ext_ssd/TensorRT-8.6.1.6/include")

# Add TensorRT library directory
link_directories("/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib")

include_directories(
    ${PROJECT_SOURCE_DIR}/include
)

set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

add_library(tensorrtbuffer SHARED src/logger.cpp src/sample_options.cpp src/sample_utils.cpp)

# Link TensorRT libraries
target_link_libraries(tensorrtbuffer
    nvinfer
    nvonnxparser
)




```

Perfect! 🎉 The build was successful! 

## Build Results:
✅ **Exit code: 0** - Build completed successfully  
✅ All targets compiled without errors:
- `tensorrtbuffer` library
- `air_slam_lib` shared library  
- All executables: `test_feature`, `map_refinement`, `relocalization`, `visual_odometry`

## Summary of Changes Made:
I updated **two CMakeLists.txt files** to properly configure TensorRT from your custom installation:

### 1. Main CMakeLists.txt (`/media/skumar/External/catkin_ws/src/AirSLAM/CMakeLists.txt`):
- Added `CMAKE_PREFIX_PATH` to include your TensorRT directory
- Set `TENSORRT_ROOT` variable 
- Added TensorRT include directory
- Added TensorRT library directory

### 2. TensorRT Buffer CMakeLists.txt (`/media/skumar/External/catkin_ws/src/AirSLAM/3rdparty/tensorrtbuffer/CMakeLists.txt`):
- Added TensorRT include directory
- Added TensorRT library directory  
- Linked TensorRT libraries (`nvinfer`, `nvonnxparser`)

The key issue was that the `tensorrtbuffer` subdirectory needed its own TensorRT configuration since it builds as a separate CMake project. Now your project successfully finds and links TensorRT from `/home/skumar/ext_ssd/TensorRT-8.6.1.6` instead of the default system location.

Your AirSLAM project should now build and run correctly with your custom TensorRT installation! 🚀

---

**User**

can you now run launch @monarch.launch to test ths. Set `visualization` to `false`.

---

**Cursor**

```cmake
cmake_minimum_required(VERSION 3.5)
project(air_slam)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE "release")
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
add_definitions(-w)

# Add custom TensorRT installation path
set(CMAKE_PREFIX_PATH "${CMAKE_PREFIX_PATH};/home/skumar/ext_ssd/TensorRT-8.6.1.6")
set(TENSORRT_ROOT "/home/skumar/ext_ssd/TensorRT-8.6.1.6")

add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/tensorrtbuffer)
add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/DBoW2)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  geometry_msgs
  image_transport
  nav_msgs
  roscpp
  rospy
  std_msgs
  sensor_msgs
  tf
)

find_package(OpenCV 4.2 REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(CUDA REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package(Boost REQUIRED)
find_package(G2O REQUIRED)
find_package(Gflags REQUIRED)
find_package(Glog REQUIRED)

catkin_package(
 INCLUDE_DIRS include
 LIBRARIES ${PROJECT_NAME}_lib
 CATKIN_DEPENDS geometry_msgs image_transport nav_msgs roscpp rospy std_msgs
)

include_directories(
  ${PROJECT_SOURCE_DIR}
  ${PROJECT_SOURCE_DIR}/include
  ${OpenCV_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
  ${CUDA_INCLUDE_DIRS}
  ${YAML_CPP_INCLUDE_DIR}
  ${Boost_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
  ${G2O_INCLUDE_DIR}
  ${GFLAGS_INCLUDE_DIRS}
  ${GLOG_INCLUDE_DIRS}
  ${TENSORRT_ROOT}/include
)

# Add TensorRT library directory
link_directories(${TENSORRT_ROOT}/lib)

add_library(${PROJECT_NAME}_lib SHARED
  src/g2o_optimization/vertex_line3d.cc
  src/g2o_optimization/vertex_vi_pose.cc
  src/g2o_optimization/vertex_imu.cc
  src/g2o_optimization/edge_project_point.cc
  src/g2o_optimization/edge_project_line.cc
  src/g2o_optimization/edge_imu.cc
  src/g2o_optimization/edge_relative_pose.cc
  src/g2o_optimization/g2o_optimization.cc
  src/bow/FSuperpoint.cc
  src/bow/database.cc
  src/super_point.cpp
  src/feature_detector.cc
  src/super_glue.cpp
  src/light_glue.cpp
  src/plnet.cpp
  src/utils.cc
  src/camera.cc
  src/imu.cc
  src/dataset.cc
  src/frame.cc
  src/point_matcher.cc
  src/mappoint.cc
  src/mapline.cc
  src/line_processor.cc
  src/ros_publisher.cc
  src/map.cc
  src/map_builder.cc
  src/map_refiner.cc
  src/map_user.cc
  src/timer.cc
  src/debug.cc
)

target_link_libraries(${PROJECT_NAME}_lib
  nvinfer
  nvinfer_plugin
  nvonnxparser
  ${OpenCV_LIBRARIES}
  ${CUDA_LIBRARIES}
  ${Boost_LIBRARIES}
  ${G2O_LIBRARIES}
  ${GFLAGS_LIBRARIES}
  ${GLOG_LIBRARIES}
  yaml-cpp
  tensorrtbuffer
  DBoW2
  -lboost_serialization
)

add_executable(visual_odometry demo/visual_odometry.cpp)
target_link_libraries(visual_odometry ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(map_refinement demo/map_refinement.cpp)
target_link_libraries(map_refinement ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(relocalization demo/relocalization.cpp)
target_link_libraries(relocalization ${PROJECT_NAME}_lib ${catkin_LIBRARIES})

add_executable(test_feature demo/test_feature.cpp)
target_link_libraries(test_feature ${PROJECT_NAME}_lib ${catkin_LIBRARIES})
```

```cmake
cmake_minimum_required(VERSION 3.6)
project(tensorrtbuffer)

set(CMAKE_CXX_STANDARD 17)

if(POLICY CMP0146)
    cmake_policy(SET CMP0146 OLD)
endif()

find_package(CUDA REQUIRED)
include_directories("${CUDA_INCLUDE_DIRS}")

# Add TensorRT include directory from custom installation
include_directories("/home/skumar/ext_ssd/TensorRT-8.6.1.6/include")

# Add TensorRT library directory
link_directories("/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib")

include_directories(
    ${PROJECT_SOURCE_DIR}/include
)

set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

add_library(tensorrtbuffer SHARED src/logger.cpp src/sample_options.cpp src/sample_utils.cpp)

# Link TensorRT libraries
target_link_libraries(tensorrtbuffer
    nvinfer
    nvinfer_plugin
    nvonnxparser
)




```

---

**User**

run `catkin clean -y` and then `catkin_make`

But why do we need to pass the `export LD_LIBRARY_PATH` command, when have already specified this location in @CMakeLists.txt and built the project.

---

**Cursor**

Short answer: because linking and runtime search are different.

- At build time, your edits let the linker find and link against TensorRT (nvinfer, nvinfer_plugin, nvonnxparser). That’s what `include_directories`, `link_directories`, and `target_link_libraries` handle.
- At run time, the dynamic loader still needs to know where to find those `.so` files. `link_directories` does not affect the runtime search path. Unless you embed an rpath/runpath or configure the system loader, the loader won’t look in `/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib` by default—hence the need for `LD_LIBRARY_PATH`.

Ways to avoid exporting `LD_LIBRARY_PATH` manually:
- Add rpath in CMake so your binaries know where to look at runtime:
  - Set build/install rpath to `${TENSORRT_ROOT}/lib` (and optionally `$ORIGIN`-relative paths).
- Register the path system-wide:
  - Add `/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib` to a file in `/etc/ld.so.conf.d/` and run `sudo ldconfig`.
- Set it in the ROS launch:
  - Add `<env name="LD_LIBRARY_PATH" value="/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib:$(env LD_LIBRARY_PATH)"/>` in the `visual_odometry` node.
- Wrap the node with a small launcher script that exports `LD_LIBRARY_PATH` before exec.

If you want, I can implement the rpath approach in `CMakeLists.txt`, or add the env var to `monarch.launch`.

