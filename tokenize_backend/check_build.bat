@echo off
echo Checking if tokenize_backend compiles
echo ===================================

echo Running cargo check...
cargo check

if %errorlevel% neq 0 (
    echo Compilation check failed.
    echo This may be due to missing build tools.
    echo Try running setup_build_tools.bat to install the required tools.
    exit /b 1
)

echo Compilation check passed!
echo You can now build and run the server with build_and_run.bat