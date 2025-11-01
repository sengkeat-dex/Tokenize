@echo off
echo Building and running tokenize_backend
echo ====================================

echo Checking if Rust is installed...
rustc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Rust is not installed. Please install Rust from https://www.rust-lang.org/
    echo Then run this script again.
    pause
    exit /b 1
)

echo Rust is installed.

echo Building release version...
cargo build --release

if %errorlevel% neq 0 (
    echo Build failed. This may be due to missing build tools.
    echo.
    echo To fix this issue:
    echo 1. Run setup_build_tools.bat to install the required build tools
    echo 2. Or use the Python server (server.py) which requires no compilation
    echo.
    pause
    exit /b 1
)

echo Build successful!
echo Starting server...
echo Server will be available at http://127.0.0.1:3030
echo Press Ctrl+C to stop the server.
echo.

cargo run --release