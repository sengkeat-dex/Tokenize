# PowerShell script to initialize and push the repository to GitHub

Write-Host "Initializing git repository..." -ForegroundColor Green
git init

Write-Host "Configuring git user..." -ForegroundColor Green
git config --global user.email "sengkeat-dex@outlook.com"
git config --global user.name "sengkeat-dex"

Write-Host "Adding all files..." -ForegroundColor Green
git add .

Write-Host "Checking git status..." -ForegroundColor Green
git status

Write-Host "Making initial commit..." -ForegroundColor Green
git commit -m "Initial commit with tokenization platform"

Write-Host "Renaming branch to main..." -ForegroundColor Green
git branch -M main

Write-Host "Checking if remote origin exists..." -ForegroundColor Green
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "Remote origin already exists. Removing it..." -ForegroundColor Yellow
    git remote remove origin
}

Write-Host "Adding remote origin..." -ForegroundColor Green
git remote add origin https://github.com/sengkeat-dex/Tokenize.git

Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host "Done! Repository has been pushed to GitHub." -ForegroundColor Green