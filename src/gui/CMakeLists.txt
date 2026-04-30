add_executable(blck_fx-eq_gui WIN32)

target_sources(blck_fx-eq_gui
    PRIVATE
        src/main.cpp
)

target_include_directories(blck_fx-eq_gui
    PRIVATE
        include
        ${CMAKE_SOURCE_DIR}/src/common/include
)

target_link_libraries(blck_fx-eq_gui PRIVATE blck_fx_common)

message(STATUS "GUI application configured")