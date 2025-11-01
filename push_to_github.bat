@echo off
echo Initializing git repository...
git init

echo Configuring git user...
git config --global user.email "sengkeat-dex@outlook.com"
git config --global user.name "sengkeat-dex"

echo Adding all files...
git add .

echo Checking git status...
git status

echo Making initial commit...
git commit -m "Initial commit with tokenization platform"

echo Renaming branch to main...
git branch -M main

echo Checking if remote origin exists...
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo Remote origin already exists. Removing it...
    git remote remove origin
)

echo Adding remote origin...
git remote add origin https://github.com/sengkeat-dex/Tokenize.git

echo Pushing to GitHub...
git push -u origin main

echo Done! Repository has been pushed to GitHub.
pause