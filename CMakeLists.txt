cmake_minimum_required(VERSION 3.28)
project(blck_fx-eq LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

option(BUILD_APO "Build APO" ON)
option(BUILD_GUI "Build GUI" ON)

# External dependencies
add_subdirectory(external)

# Common code
add_subdirectory(src/common)

# APO DLL
if(BUILD_APO)
    add_subdirectory(src/apo)
endif()

# GUI App
if(BUILD_GUI)
    add_subdirectory(src/gui)
endif()

message(STATUS "✅ blck_fx-eq root configured successfully!")
message(STATUS "Version: 0.1.0-alpha")