add_library(blck_fx_common STATIC)

target_sources(blck_fx_common
    PRIVATE
        src/version.cpp
)

target_include_directories(blck_fx_common
    PUBLIC
        include
)

target_link_libraries(blck_fx_common PUBLIC nlohmann_json::nlohmann_json)

message(STATUS "Common library configured")