add_library(blackfox_apo SHARED
    src/main.cpp
)
target_include_directories(blackfox_apo PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)


target_include_directories(blackfox_apo PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    "C:/Program Files (x86)/Windows Kits/10/Include/10.0.26100.0/um"
    "C:/Program Files (x86)/Windows Kits/10/Include/10.0.26100.0/shared"
    "C:/Program Files (x86)/Windows Kits/10/Include/10.0.26100.0/winrt"
)

target_link_libraries(blackfox_apo PRIVATE
    "C:/Program Files (x86)/Windows Kits/10/Lib/10.0.26100.0/um/x64/AudioEngineBaseAPO.lib"
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