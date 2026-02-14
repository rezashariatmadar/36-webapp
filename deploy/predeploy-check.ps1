$ErrorActionPreference = "Stop"

function Invoke-Checked {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Command
  )
  Invoke-Expression $Command
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed with exit code ${LASTEXITCODE}: $Command"
  }
}

Write-Host "[1/5] Backend tests"
$previousDebug = $env:DJANGO_DEBUG
$env:DJANGO_DEBUG = "True"
Invoke-Checked "uv run pytest"
if ($null -eq $previousDebug) {
  Remove-Item Env:DJANGO_DEBUG -ErrorAction SilentlyContinue
} else {
  $env:DJANGO_DEBUG = $previousDebug
}

if (-not $env:DJANGO_SECRET_KEY) {
  throw "DJANGO_SECRET_KEY is not set."
}
if ($env:DJANGO_SECRET_KEY.StartsWith("django-insecure-")) {
  throw "DJANGO_SECRET_KEY uses insecure default prefix."
}
if (-not $env:DJANGO_ALLOWED_HOSTS) {
  throw "DJANGO_ALLOWED_HOSTS is not set."
}
if (-not $env:DJANGO_CSRF_TRUSTED_ORIGINS) {
  throw "DJANGO_CSRF_TRUSTED_ORIGINS is not set."
}

Write-Host "[2/5] Django deploy security checks"
$env:DJANGO_DEBUG = "False"
Invoke-Checked "uv run python manage.py check --deploy --fail-level WARNING"

Write-Host "[3/5] Migration plan"
Invoke-Checked "uv run python manage.py migrate --plan"

Write-Host "[4/5] Frontend tests"
Push-Location frontend
Invoke-Checked "npm run test"

Write-Host "[5/5] Frontend build"
Invoke-Checked "npm run build"
Pop-Location

Write-Host "Pre-deploy checks passed."
