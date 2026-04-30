add_library(blackfox_apo SHARED
    src/main.cpp
)

# Better way - let CMake + Visual Studio find the SDK automatically
target_include_directories(blackfox_apo PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(blackfox_apo PRIVATE
    AudioEngineBaseAPO.lib
    ksuser.lib
    avrt.lib
    ole32.lib
)

set_target_properties(blackfox_apo PROPERTIES 
    OUTPUT_NAME "blackfoxCustomAPO"
    SUFFIX ".dll"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

target_compile_definitions(blackfox_apo PRIVATE
    WIN32_LEAN_AND_MEAN
    NOMINMAX
)