# setup_project.py
import os
from pathlib import Path

def write_file(path: str, content: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✓ Created: {path}")

# ========================= PROJECT STRUCTURE =========================
root = Path(".")

# Create all directories
dirs = [
    ".vscode",
    "build",
    "external/imgui",
    "external/glfw",
    "external/json",
    "src/apo/include",
    "src/apo/src",
    "src/gui/include",
    "src/gui/src",
    "src/gui/assets/fonts",
    "src/gui/assets/icons",
    "src/gui/assets/themes",
    "src/common/include/dsp",
    "src/common/include/config",
    "src/common/include/utils",
    "src/common/src",
    "cmake",
    "docs",
    "presets",
    "logs"
]

for d in dirs:
    (root / d).mkdir(parents=True, exist_ok=True)

print("📁 All directories created.\n")

# ========================= ROOT CMakeLists.txt =========================
write_file("CMakeLists.txt", r"""
cmake_minimum_required(VERSION 3.28)
project(blck_fx-eq LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

add_subdirectory(src/common)
add_subdirectory(src/apo)
add_subdirectory(src/gui)

install(TARGETS blackfoxCustomAPO blck_fx-eq_gui
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION bin)
""")

# ========================= COMMON LIBRARY =========================
write_file("src/common/CMakeLists.txt", r"""
add_library(blck_fx_common STATIC)

target_sources(blck_fx_common PRIVATE
    src/version.cpp
)

target_include_directories(blck_fx_common PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/external/json
)

target_link_libraries(blck_fx_common PUBLIC)
""")

write_file("src/common/include/version.h", r"""
#pragma once
#define BLCK_FX_EQ_VERSION "1.0.0"
#define BLCK_FX_EQ_APO_NAME "blackfoxCustomAPO"
""")

write_file("src/common/src/version.cpp", r"""
#include "version.h"
""")

# ========================= APO (DLL) =========================
write_file("src/apo/CMakeLists.txt", r"""
add_library(blackfoxCustomAPO SHARED)

target_sources(blackfoxCustomAPO PRIVATE
    src/BlackFoxAPO.cpp
)

target_include_directories(blackfoxCustomAPO PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src/common/include
)

target_link_libraries(blackfoxCustomAPO PRIVATE blck_fx_common)
""")

write_file("src/apo/include/BlackFoxAPO.h", r"""
#pragma once
#include <audioenginebaseapo.h>
#include <initguid.h>

class BlackFoxAPO : public CBaseAudioProcessingObject
{
public:
    DECLARE_APO_REGISTRY(BlackFoxAPO);

    BlackFoxAPO();
    ~BlackFoxAPO();

    STDMETHODIMP Initialize(UINT32 u32NumInputConnections,
                            APO_CONNECTION_PROPERTY* pInputConnections,
                            UINT32 u32NumOutputConnections,
                            APO_CONNECTION_PROPERTY* pOutputConnections) override;

    STDMETHODIMP APOProcess(UINT32 u32NumInputConnections,
                            APO_CONNECTION_PROPERTY** ppInputConnections,
                            UINT32 u32NumOutputConnections,
                            APO_CONNECTION_PROPERTY** ppOutputConnections) override;

    STDMETHODIMP Reset() override;

private:
    bool m_initialized = false;
};
""")

write_file("src/apo/src/BlackFoxAPO.cpp", r"""
#include "BlackFoxAPO.h"
#include <iostream>
#include <cstring>

BlackFoxAPO::BlackFoxAPO() : CBaseAudioProcessingObject() {}

BlackFoxAPO::~BlackFoxAPO() {}

STDMETHODIMP BlackFoxAPO::Initialize(UINT32 u32NumInputConnections,
                                     APO_CONNECTION_PROPERTY* pInputConnections,
                                     UINT32 u32NumOutputConnections,
                                     APO_CONNECTION_PROPERTY* pOutputConnections)
{
    m_initialized = true;
    std::cout << "[BlackFoxAPO] Initialized\n";
    return S_OK;
}

STDMETHODIMP BlackFoxAPO::APOProcess(UINT32 u32NumInputConnections,
                                     APO_CONNECTION_PROPERTY** ppInputConnections,
                                     UINT32 u32NumOutputConnections,
                                     APO_CONNECTION_PROPERTY** ppOutputConnections)
{
    // Identity pass-through for now
    if (ppInputConnections[0]->pBuffer && ppOutputConnections[0]->pBuffer) {
        memcpy(ppOutputConnections[0]->pBuffer,
               ppInputConnections[0]->pBuffer,
               ppInputConnections[0]->u32BufferSize);
    }
    return S_OK;
}

STDMETHODIMP BlackFoxAPO::Reset()
{
    return S_OK;
}
""")

# ========================= GUI (Basic skeleton) =========================
write_file("src/gui/CMakeLists.txt", r"""
add_executable(blck_fx-eq_gui WIN32)

target_sources(blck_fx-eq_gui PRIVATE
    src/main.cpp
)

target_include_directories(blck_fx-eq_gui PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src/common/include
)

# Dear ImGui will be added later
target_link_libraries(blck_fx-eq_gui PRIVATE blck_fx_common)
""")

write_file("src/gui/src/main.cpp", r"""
#include <iostream>
#include "version.h"

int main()
{
    std::cout << "blck_fx-eq GUI v" << BLCK_FX_EQ_VERSION << "\n";
    std::cout << "GUI will be implemented with Dear ImGui in Phase 5.\n";
    system("pause");
    return 0;
}
""")

# ========================= README =========================
write_file("README.md", r"""
# blck_fx-eq

Custom 5-band system-wide Equalizer APO + GUI (C++23)

**Status**: Phase 1 completed (skeleton)

Next: Phase 2 → Real APO + Phase 3 → Registration
""")

print("\n🎉 Project setup completed successfully!")
print("\nNow run these commands:")
print("   cmake -B build -G \"Visual Studio 17 2022\" -A x64")
print("   cmake --build build --config Release")