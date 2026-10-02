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

function Invoke-GitCapture([string[]]$GitArgs) {
  $oldPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try {
    $output = & git @GitArgs 2>$null
    $code = $LASTEXITCODE
  } finally {
    $ErrorActionPreference = $oldPreference
  }
  [pscustomobject]@{
    Code = $code
    Output = (($output | ForEach-Object { "$_" }) -join "`n").Trim()
  }
}

function Normalize-GitHubRemote([string]$Url) {
  if (-not $Url) { return "" }
  $u = $Url.Trim().TrimEnd('/')
  $path = $null
  if ($u -match '^git@github\.com:(.+)$') {
    $path = $Matches[1]
  } elseif ($u -match '^ssh://git@github\.com/(.+)$') {
    $path = $Matches[1]
  } elseif ($u -match '^https://github\.com/(.+)
    return $u.ToLowerInvariant()
  }
  $path = $path.TrimEnd('/')
  if ($path.EndsWith(".git", [System.StringComparison]::OrdinalIgnoreCase)) {
    $path = $path.Substring(0, $path.Length - 4)
  }
  return ("github.com/" + $path).ToLowerInvariant()
}

function Fail-Unverified([string]$Reason) {
  throw "$Reason Target=$Target. Refusing to update or execute repository code."
}

if ([string]::IsNullOrWhiteSpace($Target)) {
  throw "target path cannot be empty."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "git is required."
}

$Parent = Split-Path -Parent $Target
New-Item -ItemType Directory -Path $Parent -Force | Out-Null

if (Test-Path (Join-Path $Target ".git")) {
  $originResult = Invoke-GitCapture @("-C", $Target, "remote", "get-url", "origin")
  if ($originResult.Code -ne 0) {
    Fail-Unverified "Origin cannot be read."
  }
  $Origin = $originResult.Output
  $Normalized = Normalize-GitHubRemote $Origin
  if ($Normalized -ne $ExpectedRemote) {
    Fail-Unverified "Origin is not this project. Origin=$Origin Expected=$RepoUrl."
  }

  $branchResult = Invoke-GitCapture @("-C", $Target, "symbolic-ref", "--quiet", "--short", "HEAD")
  if ($branchResult.Code -ne 0 -or $branchResult.Output -ne "main") {
    $found = if ($branchResult.Output) { $branchResult.Output } else { "<detached>" }
    Fail-Unverified "Existing installation must be on branch main; found $found."
  }

  $statusResult = Invoke-GitCapture @("-C", $Target, "status", "--porcelain", "--untracked-files=normal")
  if ($statusResult.Code -ne 0 -or $statusResult.Output) {
    Fail-Unverified "Existing installation contains local or untracked changes."
  }

  Write-Host "Verifying and updating installation: $Target"
  $fetchResult = Invoke-GitCapture @("-C", $Target, "fetch", "--quiet", "origin", "main")
  if ($fetchResult.Code -ne 0) {
    Fail-Unverified "git fetch origin main failed."
  }

  $ancestorResult = Invoke-GitCapture @("-C", $Target, "merge-base", "--is-ancestor", "HEAD", "refs/remotes/origin/main")
  if ($ancestorResult.Code -ne 0) {
    Fail-Unverified "Local HEAD is ahead of or diverged from origin/main."
  }

  $mergeResult = Invoke-GitCapture @("-C", $Target, "merge", "--ff-only", "refs/remotes/origin/main")
  if ($mergeResult.Code -ne 0) {
    Fail-Unverified "Fast-forward to origin/main failed."
  }

  $headResult = Invoke-GitCapture @("-C", $Target, "rev-parse", "HEAD")
  $remoteResult = Invoke-GitCapture @("-C", $Target, "rev-parse", "refs/remotes/origin/main")
  if ($headResult.Code -ne 0 -or $remoteResult.Code -ne 0 -or $headResult.Output -ne $remoteResult.Output) {
    Fail-Unverified "Update did not land exactly on origin/main."
  }

  $statusAfter = Invoke-GitCapture @("-C", $Target, "status", "--porcelain", "--untracked-files=normal")
  if ($statusAfter.Code -ne 0 -or $statusAfter.Output) {
    Fail-Unverified "Working tree changed unexpectedly during verification."
  }
} elseif (Test-Path $Target) {
  throw "Target exists and is not this git checkout: $Target. Choose another path; nothing was overwritten."
} else {
  $cloneResult = Invoke-GitCapture @("clone", "--depth", "1", $RepoUrl, $Target)
  if ($cloneResult.Code -ne 0) { throw "git clone failed." }
}

$Python = Get-Command python -ErrorAction SilentlyContinue
if ($Python) {
  & $Python.Source (Join-Path $Target "scripts\validate_repo.py")
  if ($LASTEXITCODE -ne 0) { throw "repository validation failed." }
} else {
  Write-Host "NOTE: Python not found; installation completed but local validation was skipped."
}

Write-Host "Installed at: $Target"
Write-Host "The skill does not configure or access any bank account."
) {
    $path = $Matches[1]
  } else {
    return $u.ToLowerInvariant()
  }
  $path = $path.TrimEnd('/')
  if ($path.EndsWith(".git", [System.StringComparison]::OrdinalIgnoreCase)) {
    $path = $path.Substring(0, $path.Length - 4)
  }
  return ("github.com/" + $path).ToLowerInvariant()
}

function Fail-Unverified([string]$Reason) {
  throw "$Reason Target=$Target. Refusing to update or execute repository code."
}

if ([string]::IsNullOrWhiteSpace($Target)) {
  throw "target path cannot be empty."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "git is required."
}

$Parent = Split-Path -Parent $Target
New-Item -ItemType Directory -Path $Parent -Force | Out-Null

if (Test-Path (Join-Path $Target ".git")) {
  $originResult = Invoke-GitCapture @("-C", $Target, "remote", "get-url", "origin")
  if ($originResult.Code -ne 0) {
    Fail-Unverified "Origin cannot be read."
  }
  $Origin = $originResult.Output
  $Normalized = Normalize-GitHubRemote $Origin
  if ($Normalized -ne $ExpectedRemote) {
    Fail-Unverified "Origin is not this project. Origin=$Origin Expected=$RepoUrl."
  }

  $branchResult = Invoke-GitCapture @("-C", $Target, "symbolic-ref", "--quiet", "--short", "HEAD")
  if ($branchResult.Code -ne 0 -or $branchResult.Output -ne "main") {
    $found = if ($branchResult.Output) { $branchResult.Output } else { "<detached>" }
    Fail-Unverified "Existing installation must be on branch main; found $found."
  }

  $statusResult = Invoke-GitCapture @("-C", $Target, "status", "--porcelain", "--untracked-files=normal")
  if ($statusResult.Code -ne 0 -or $statusResult.Output) {
    Fail-Unverified "Existing installation contains local or untracked changes."
  }

  Write-Host "Verifying and updating installation: $Target"
  $fetchResult = Invoke-GitCapture @("-C", $Target, "fetch", "--quiet", "origin", "main")
  if ($fetchResult.Code -ne 0) {
    Fail-Unverified "git fetch origin main failed."
  }

  $ancestorResult = Invoke-GitCapture @("-C", $Target, "merge-base", "--is-ancestor", "HEAD", "refs/remotes/origin/main")
  if ($ancestorResult.Code -ne 0) {
    Fail-Unverified "Local HEAD is ahead of or diverged from origin/main."
  }

  $mergeResult = Invoke-GitCapture @("-C", $Target, "merge", "--ff-only", "refs/remotes/origin/main")
  if ($mergeResult.Code -ne 0) {
    Fail-Unverified "Fast-forward to origin/main failed."
  }

  $headResult = Invoke-GitCapture @("-C", $Target, "rev-parse", "HEAD")
  $remoteResult = Invoke-GitCapture @("-C", $Target, "rev-parse", "refs/remotes/origin/main")
  if ($headResult.Code -ne 0 -or $remoteResult.Code -ne 0 -or $headResult.Output -ne $remoteResult.Output) {
    Fail-Unverified "Update did not land exactly on origin/main."
  }

  $statusAfter = Invoke-GitCapture @("-C", $Target, "status", "--porcelain", "--untracked-files=normal")
  if ($statusAfter.Code -ne 0 -or $statusAfter.Output) {
    Fail-Unverified "Working tree changed unexpectedly during verification."
  }
} elseif (Test-Path $Target) {
  throw "Target exists and is not this git checkout: $Target. Choose another path; nothing was overwritten."
} else {
  $cloneResult = Invoke-GitCapture @("clone", "--depth", "1", $RepoUrl, $Target)
  if ($cloneResult.Code -ne 0) { throw "git clone failed." }
}

$Python = Get-Command python -ErrorAction SilentlyContinue
if ($Python) {
  & $Python.Source (Join-Path $Target "scripts\validate_repo.py")
  if ($LASTEXITCODE -ne 0) { throw "repository validation failed." }
} else {
  Write-Host "NOTE: Python not found; installation completed but local validation was skipped."
}

Write-Host "Installed at: $Target"
Write-Host "The skill does not configure or access any bank account."
) {
    $path = $Matches[1]
  } else {
    return $u.ToLowerInvariant()
  }
  $path = $path.TrimEnd('/')
  if ($path.EndsWith(".git", [System.StringComparison]::OrdinalIgnoreCase)) {
    $path = $path.Substring(0, $path.Length - 4)
  }
  return ("github.com/" + $path).ToLowerInvariant()
}

function Fail-Unverified([string]$Reason) {
  throw "$Reason Target=$Target. Refusing to update or execute repository code."
}

if ([string]::IsNullOrWhiteSpace($Target)) {
  throw "target path cannot be empty."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "git is required."
}

$Parent = Split-Path -Parent $Target
New-Item -ItemType Directory -Path $Parent -Force | Out-Null

if (Test-Path (Join-Path $Target ".git")) {
  $originResult = Invoke-GitCapture @("-C", $Target, "remote", "get-url", "origin")
  if ($originResult.Code -ne 0) {
    Fail-Unverified "Origin cannot be read."
  }
  $Origin = $originResult.Output
  $Normalized = Normalize-GitHubRemote $Origin
  if ($Normalized -ne $ExpectedRemote) {
    Fail-Unverified "Origin is not this project. Origin=$Origin Expected=$RepoUrl."
  }

  $branchResult = Invoke-GitCapture @("-C", $Target, "symbolic-ref", "--quiet", "--short", "HEAD")
  if ($branchResult.Code -ne 0 -or $branchResult.Output -ne "main") {
    $found = if ($branchResult.Output) { $branchResult.Output } else { "<detached>" }
    Fail-Unverified "Existing installation must be on branch main; found $found."
  }

  $statusResult = Invoke-GitCapture @("-C", $Target, "status", "--porcelain", "--untracked-files=normal")
  if ($statusResult.Code -ne 0 -or $statusResult.Output) {
    Fail-Unverified "Existing installation contains local or untracked changes."
  }

  Write-Host "Verifying and updating installation: $Target"
  $fetchResult = Invoke-GitCapture @("-C", $Target, "fetch", "--quiet", "origin", "main")
  if ($fetchResult.Code -ne 0) {
    Fail-Unverified "git fetch origin main failed."
  }

  $ancestorResult = Invoke-GitCapture @("-C", $Target, "merge-base", "--is-ancestor", "HEAD", "refs/remotes/origin/main")
  if ($ancestorResult.Code -ne 0) {
    Fail-Unverified "Local HEAD is ahead of or diverged from origin/main."
  }

  $mergeResult = Invoke-GitCapture @("-C", $Target, "merge", "--ff-only", "refs/remotes/origin/main")
  if ($mergeResult.Code -ne 0) {
    Fail-Unverified "Fast-forward to origin/main failed."
  }

  $headResult = Invoke-GitCapture @("-C", $Target, "rev-parse", "HEAD")
  $remoteResult = Invoke-GitCapture @("-C", $Target, "rev-parse", "refs/remotes/origin/main")
  if ($headResult.Code -ne 0 -or $remoteResult.Code -ne 0 -or $headResult.Output -ne $remoteResult.Output) {
    Fail-Unverified "Update did not land exactly on origin/main."
  }

  $statusAfter = Invoke-GitCapture @("-C", $Target, "status", "--porcelain", "--untracked-files=normal")
  if ($statusAfter.Code -ne 0 -or $statusAfter.Output) {
    Fail-Unverified "Working tree changed unexpectedly during verification."
  }
} elseif (Test-Path $Target) {
  throw "Target exists and is not this git checkout: $Target. Choose another path; nothing was overwritten."
} else {
  $cloneResult = Invoke-GitCapture @("clone", "--depth", "1", $RepoUrl, $Target)
  if ($cloneResult.Code -ne 0) { throw "git clone failed." }
}

$Python = Get-Command python -ErrorAction SilentlyContinue
if ($Python) {
  & $Python.Source (Join-Path $Target "scripts\validate_repo.py")
  if ($LASTEXITCODE -ne 0) { throw "repository validation failed." }
} else {
  Write-Host "NOTE: Python not found; installation completed but local validation was skipped."
}

Write-Host "Installed at: $Target"
Write-Host "The skill does not configure or access any bank account."
) {
    $path = $Matches[1]
  } else {
    return $u.ToLowerInvariant()
  }
  $path = $path.TrimEnd('/')
  if ($path.EndsWith(".git", [System.StringComparison]::OrdinalIgnoreCase)) {
    $path = $path.Substring(0, $path.Length - 4)
  }
  return ("github.com/" + $path).ToLowerInvariant()
}

function Fail-Unverified([string]$Reason) {
  throw "$Reason Target=$Target. Refusing to update or execute repository code."
}

if ([string]::IsNullOrWhiteSpace($Target)) {
  throw "target path cannot be empty."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "git is required."
}

$Parent = Split-Path -Parent $Target
New-Item -ItemType Directory -Path $Parent -Force | Out-Null

if (Test-Path (Join-Path $Target ".git")) {
  $originResult = Invoke-GitCapture @("-C", $Target, "remote", "get-url", "origin")
  if ($originResult.Code -ne 0) {
    Fail-Unverified "Origin cannot be read."
  }
  $Origin = $originResult.Output
  $Normalized = Normalize-GitHubRemote $Origin
  if ($Normalized -ne $ExpectedRemote) {
    Fail-Unverified "Origin is not this project. Origin=$Origin Expected=$RepoUrl."
  }

  $branchResult = Invoke-GitCapture @("-C", $Target, "symbolic-ref", "--quiet", "--short", "HEAD")
  if ($branchResult.Code -ne 0 -or $branchResult.Output -ne "main") {
    $found = if ($branchResult.Output) { $branchResult.Output } else { "<detached>" }
    Fail-Unverified "Existing installation must be on branch main; found $found."
  }

  $statusResult = Invoke-GitCapture @("-C", $Target, "status", "--porcelain", "--untracked-files=normal")
  if ($statusResult.Code -ne 0 -or $statusResult.Output) {
    Fail-Unverified "Existing installation contains local or untracked changes."
  }

  Write-Host "Verifying and updating installation: $Target"
  $fetchResult = Invoke-GitCapture @("-C", $Target, "fetch", "--quiet", "origin", "main")
  if ($fetchResult.Code -ne 0) {
    Fail-Unverified "git fetch origin main failed."
  }

  $ancestorResult = Invoke-GitCapture @("-C", $Target, "merge-base", "--is-ancestor", "HEAD", "refs/remotes/origin/main")
  if ($ancestorResult.Code -ne 0) {
    Fail-Unverified "Local HEAD is ahead of or diverged from origin/main."
  }

  $mergeResult = Invoke-GitCapture @("-C", $Target, "merge", "--ff-only", "refs/remotes/origin/main")
  if ($mergeResult.Code -ne 0) {
    Fail-Unverified "Fast-forward to origin/main failed."
  }

  $headResult = Invoke-GitCapture @("-C", $Target, "rev-parse", "HEAD")
  $remoteResult = Invoke-GitCapture @("-C", $Target, "rev-parse", "refs/remotes/origin/main")
  if ($headResult.Code -ne 0 -or $remoteResult.Code -ne 0 -or $headResult.Output -ne $remoteResult.Output) {
    Fail-Unverified "Update did not land exactly on origin/main."
  }

  $statusAfter = Invoke-GitCapture @("-C", $Target, "status", "--porcelain", "--untracked-files=normal")
  if ($statusAfter.Code -ne 0 -or $statusAfter.Output) {
    Fail-Unverified "Working tree changed unexpectedly during verification."
  }
} elseif (Test-Path $Target) {
  throw "Target exists and is not this git checkout: $Target. Choose another path; nothing was overwritten."
} else {
  $cloneResult = Invoke-GitCapture @("clone", "--depth", "1", $RepoUrl, $Target)
  if ($cloneResult.Code -ne 0) { throw "git clone failed." }
}

$Python = Get-Command python -ErrorAction SilentlyContinue
if ($Python) {
  & $Python.Source (Join-Path $Target "scripts\validate_repo.py")
  if ($LASTEXITCODE -ne 0) { throw "repository validation failed." }
} else {
  Write-Host "NOTE: Python not found; installation completed but local validation was skipped."
}

Write-Host "Installed at: $Target"
Write-Host "The skill does not configure or access any bank account."
