@echo off
echo Setting up Rust build environment for tokenize_backend
echo ======================================================

echo Installing required build tools...
echo This will install the Visual Studio Build Tools which are needed to compile Rust dependencies.

echo Checking if Rust is installed...
rustc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Rust is not installed. Please install Rust from https://www.rust-lang.org/
    echo Then run this script again.
    pause
    exit /b 1
)

echo Rust is installed. Checking for build tools...

echo Installing Visual Studio Build Tools...
echo Please follow the installer prompts to install the C++ build tools.
echo You may need to restart your computer after installation.

REM This will open the Visual Studio download page
start "" "https://visualstudio.microsoft.com/visual-cpp-build-tools/"

echo.
echo After installing the build tools, you can compile the Rust backend with:
echo   cd tokenize_backend
echo   cargo build --release
echo.
echo Then run it with:
echo   cargo run --release
echo.

pause