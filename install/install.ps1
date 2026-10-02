param(
  [string]$Target = $(if ($env:AGENT_SKILLS_HOME) {
    Join-Path $env:AGENT_SKILLS_HOME "cerrar-cuenta-bancaria-ar"
  } else {
    Join-Path $HOME ".agents\skills\cerrar-cuenta-bancaria-ar"
  })
)

$ErrorActionPreference = "Stop"
$RepoUrl = "https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git"
$ExpectedRemote = "github.com/simondalmasso/cerrar-cuenta-bancaria-ar"

function Normalize-GitHubRemote([string]$Url) {
  if (-not $Url) { return "" }
  $u = $Url.Trim()
  $path = $null
  if ($u -match '^git@github\.com:(.+)$') {
    $path = $Matches[1]
  } elseif ($u -match '^ssh://git@github\.com/(.+)$') {
    $path = $Matches[1]
  } elseif ($u -match '^https?://github\.com/(.+)$') {
    $path = $Matches[1]
  } elseif ($u -match '^git://github\.com/(.+)$') {
    $path = $Matches[1]
  } else {
    return $u.TrimEnd('/').ToLowerInvariant()
  }
  $path = $path.TrimEnd('/')
  if ($path.EndsWith(".git", [System.StringComparison]::OrdinalIgnoreCase)) {
    $path = $path.Substring(0, $path.Length - 4)
  }
  return ("github.com/" + $path).ToLowerInvariant()
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "git is required."
}

$Parent = Split-Path -Parent $Target
New-Item -ItemType Directory -Path $Parent -Force | Out-Null

if (Test-Path (Join-Path $Target ".git")) {
  $Origin = (& git -C $Target remote get-url origin 2>$null)
  $Normalized = Normalize-GitHubRemote $Origin
  if ($Normalized -ne $ExpectedRemote) {
    throw "Target is a git repository but origin is not this project. Target=$Target Origin=$Origin Expected=$RepoUrl. Nothing was changed."
  }
  Write-Host "Updating verified installation: $Target"
  & git -C $Target pull --ff-only
  if ($LASTEXITCODE -ne 0) { throw "git pull failed." }
} elseif (Test-Path $Target) {
  throw "Target exists and is not this git checkout: $Target. Choose another path; nothing was overwritten."
} else {
  & git clone --depth 1 $RepoUrl $Target
  if ($LASTEXITCODE -ne 0) { throw "git clone failed." }
}

$Python = Get-Command python -ErrorAction SilentlyContinue
if ($Python) {
  & $Python.Source (Join-Path $Target "scripts\validate_repo.py")
} else {
  Write-Host "NOTE: Python not found; installation completed but local validation was skipped."
}

Write-Host "Installed at: $Target"
Write-Host "The skill does not configure or access any bank account."
