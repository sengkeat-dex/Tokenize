# Comprehensive PowerShell script to initialize and push the repository to GitHub

Write-Host "=== Tokenize Repository Git Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "tokenization_digital_wallet.csv")) {
    Write-Host "Error: Please run this script from the project directory (where tokenization_digital_wallet.csv is located)" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "1. Initializing git repository..." -ForegroundColor Green
git init

Write-Host "2. Configuring git user..." -ForegroundColor Green
git config --global user.email "sengkeat-dex@outlook.com"
git config --global user.name "sengkeat-dex"

Write-Host "3. Adding all files explicitly..." -ForegroundColor Green
# Add files explicitly to ensure they are tracked
git add tokenization_digital_wallet.csv
git add README.md
git add .gitignore
git add package.json
git add server.py
git add server.js
git add start.bat
git add start.sh
git add git_setup_instructions.txt
git add push_to_github.bat
git add push_to_github.ps1
git add complete_git_setup.ps1
git add init_git.bat
git add init_git.ps1

# Add directories
if (Test-Path "tokenize_backend") {
    git add tokenize_backend/
}
if (Test-Path "tokenize_frontend") {
    git add tokenize_frontend/
}
if (Test-Path "tokenize_wasm") {
    git add tokenize_wasm/
}

Write-Host "4. Checking git status..." -ForegroundColor Green
$gitStatus = git status --porcelain
if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-Host "Warning: No files to commit. This might indicate an issue with file permissions or gitignore." -ForegroundColor Yellow
    Write-Host "Checking for untracked files:" -ForegroundColor Yellow
    git status
} else {
    Write-Host "Files to be committed:" -ForegroundColor Yellow
    git status --porcelain
}

Write-Host "5. Making initial commit..." -ForegroundColor Green
try {
    git commit -m "Initial commit with tokenization platform"
    Write-Host "Commit successful!" -ForegroundColor Green
} catch {
    Write-Host "Warning: Commit failed. This might be because no files were added." -ForegroundColor Yellow
    Write-Host "Checking what files git can see:" -ForegroundColor Yellow
    git ls-files
}

Write-Host "6. Renaming branch to main..." -ForegroundColor Green
git branch -M main

Write-Host "7. Checking if remote origin exists..." -ForegroundColor Green
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "Remote origin already exists. Removing it..." -ForegroundColor Yellow
    git remote remove origin
}

Write-Host "8. Adding remote origin..." -ForegroundColor Green
git remote add origin https://github.com/sengkeat-dex/Tokenize.git

Write-Host "9. Pushing to GitHub..." -ForegroundColor Green
try {
    git push -u origin main
    Write-Host "Success! Repository has been pushed to GitHub." -ForegroundColor Green
} catch {
    Write-Host "Error pushing to GitHub. You might need to use force push if the repository already exists:" -ForegroundColor Yellow
    Write-Host "git push -u origin main --force" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
pause