import os
from pathlib import Path

# Base path
base_path = r"G:\Мой диск\hellcaster\химия\blck_fx-eq"

def create_project_structure():
    base = Path(base_path)
    base.mkdir(parents=True, exist_ok=True)

    def mkdir(path):
        Path(path).mkdir(parents=True, exist_ok=True)

    def touch(file):
        Path(file).touch(exist_ok=True)

    # ==================== Top-level directories ====================
    mkdir(base / ".vscode")
    mkdir(base / "build")
    mkdir(base / "external")
    mkdir(base / "src")
    mkdir(base / "cmake")
    mkdir(base / "docs")
    mkdir(base / "presets")
    mkdir(base / "logs")

    # ==================== external ====================
    mkdir(base / "external" / "imgui")
    mkdir(base / "external" / "glfw")
    mkdir(base / "external" / "json")

    # ==================== src ====================
    # apo
    mkdir(base / "src" / "apo" / "include")
    mkdir(base / "src" / "apo" / "src")
    touch(base / "src" / "apo" / "CMakeLists.txt")

    # gui
    mkdir(base / "src" / "gui" / "include")
    mkdir(base / "src" / "gui" / "src")
    mkdir(base / "src" / "gui" / "assets" / "fonts")
    mkdir(base / "src" / "gui" / "assets" / "icons")
    mkdir(base / "src" / "gui" / "assets" / "themes")
    touch(base / "src" / "gui" / "CMakeLists.txt")

    # common
    mkdir(base / "src" / "common" / "include" / "dsp")
    mkdir(base / "src" / "common" / "include" / "config")
    mkdir(base / "src" / "common" / "include" / "utils")
    mkdir(base / "src" / "common" / "src")
    touch(base / "src" / "common" / "include" / "version.h")

    # src root CMake
    touch(base / "src" / "CMakeLists.txt")

    # ==================== Other files ====================
    touch(base / "README.md")
    touch(base / "LICENSE")
    touch(base / ".gitignore")
    touch(base / "docs" / "architecture.md")   # as mentioned in comment

    print(f"✅ Project structure successfully created at:\n{base.resolve()}")

if __name__ == "__main__":
    create_project_structure()