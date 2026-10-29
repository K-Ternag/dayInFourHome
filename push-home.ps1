$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

function Invoke-Git {
    & git @args
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed (exit $LASTEXITCODE). No force push was performed."
    }
}

$repository = 'https://github.com/K-Ternag/dayInFourHome.git'

# Check connectivity before changing the local repository.
Invoke-Git ls-remote $repository
if (-not (Test-Path -LiteralPath '.git')) {
    Invoke-Git init -b main
}
$branch = & git branch --show-current
if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') {
    throw 'Expected the main branch. Stopping without changing branches.'
}
$remotes = & git remote
if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git remotes.' }
if ($remotes -contains 'origin') {
    $origin = & git remote get-url origin
    if ($LASTEXITCODE -ne 0 -or $origin -ne $repository) {
        throw 'Origin points to another repository. Stopping without replacing it.'
    }
} else {
    Invoke-Git remote add origin $repository
}

& git config --get user.name | Out-Null
if ($LASTEXITCODE -ne 0) { Invoke-Git config --local user.name 'K-Ternag' }
& git config --get user.email | Out-Null
if ($LASTEXITCODE -ne 0) {
    Invoke-Git config --local user.email '10904273+K-Ternag@users.noreply.github.com'
}

$files = @(
    '.gitignore', '.nojekyll', 'app-ads.txt', 'README.md', 'app.js', 'assets-data.js', 'assets',
    'browser_check.py', 'build_site.py', 'delete-account.html', 'guide.html',
    'index.html', 'privacy.html', 'site-config.js', 'styles.css', 'support.html',
    'terms.html', 'verification.json', 'verify_site.py', 'push-home.ps1',
    'index.en.html', 'guide.en.html', 'support.en.html', 'privacy.en.html',
    'delete-account.en.html', 'terms.en.html', 'build_english.py', 'test_localization.cjs'
)
Invoke-Git add -- @files
& git diff --cached --quiet
if ($LASTEXITCODE -eq 1) {
    Invoke-Git commit -m 'Add Day in Four homepage with refined responsive layout'
} elseif ($LASTEXITCODE -ne 0) {
    throw 'Cannot inspect staged changes.'
}
Invoke-Git push -u origin main
Write-Host 'Pushed successfully: https://github.com/K-Ternag/dayInFourHome'
