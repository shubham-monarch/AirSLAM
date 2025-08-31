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



