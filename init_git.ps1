# Initialize git repository
Write-Host "Initializing git repository..."
git init

# Create README.md if it doesn't exist
if (-not (Test-Path "README.md")) {
    Write-Host "Creating README.md..."
    "# Tokenize" > README.md
} else {
    Write-Host "README.md already exists"
}

# Add all files to git
Write-Host "Adding files to git..."
git add .

# Make first commit
Write-Host "Making first commit..."
git commit -m "first commit"

# Rename branch to main
Write-Host "Renaming branch to main..."
git branch -M main

Write-Host "Git repository initialized successfully!"