param(
  [string]$Target = $(if ($env:AGENT_SKILLS_HOME) {
    Join-Path $env:AGENT_SKILLS_HOME "cerrar-cuenta-bancaria-ar"
  } else {
    Join-Path $HOME ".agents\skills\cerrar-cuenta-bancaria-ar"
  })
)

$ErrorActionPreference = "Stop"
$RepoUrl = "https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "git is required."
}

$Parent = Split-Path -Parent $Target
New-Item -ItemType Directory -Path $Parent -Force | Out-Null

if (Test-Path (Join-Path $Target ".git")) {
  Write-Host "Updating existing installation: $Target"
  git -C $Target pull --ff-only
} elseif (Test-Path $Target) {
  throw "Target exists and is not this git checkout: $Target. Choose another path; nothing was overwritten."
} else {
  git clone --depth 1 $RepoUrl $Target
}

$Python = Get-Command python -ErrorAction SilentlyContinue
if ($Python) {
  & $Python.Source (Join-Path $Target "scripts\validate_repo.py")
} else {
  Write-Host "NOTE: Python not found; installation completed but local validation was skipped."
}

Write-Host "Installed at: $Target"
Write-Host "The skill does not configure or access any bank account."
