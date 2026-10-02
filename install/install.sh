#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git"
EXPECTED_REMOTE="github.com/simondalmasso/cerrar-cuenta-bancaria-ar"
BASE="${AGENT_SKILLS_HOME:-$HOME/.agents/skills}"
TARGET="${1:-$BASE/cerrar-cuenta-bancaria-ar}"

normalize_github_remote() {
  local u="$1"
  local path=""
  case "$u" in
    git@github.com:*) path="${u#git@github.com:}" ;;
    ssh://git@github.com/*) path="${u#ssh://git@github.com/}" ;;
    https://github.com/*) path="${u#https://github.com/}" ;;
    http://github.com/*) path="${u#http://github.com/}" ;;
    git://github.com/*) path="${u#git://github.com/}" ;;
    *) printf '%s' "$u" | tr '[:upper:]' '[:lower:]'; return ;;
  esac
  path="${path%/}"
  path="${path%.git}"
  printf 'github.com/%s' "$path" | tr '[:upper:]' '[:lower:]'
}

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git is required." >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"

if [ -d "$TARGET/.git" ]; then
  origin="$(git -C "$TARGET" remote get-url origin 2>/dev/null || true)"
  normalized="$(normalize_github_remote "$origin")"
  if [ "$normalized" != "$EXPECTED_REMOTE" ]; then
    echo "ERROR: target is a git repository, but origin is not this project." >&2
    echo "Target: $TARGET" >&2
    echo "Origin: ${origin:-<missing>}" >&2
    echo "Expected: $REPO_URL" >&2
    echo "Nothing was changed." >&2
    exit 1
  fi
  echo "Updating verified installation: $TARGET"
  git -C "$TARGET" pull --ff-only origin main
elif [ -e "$TARGET" ]; then
  echo "ERROR: target exists and is not this git checkout: $TARGET" >&2
  echo "Choose another path; the installer will not overwrite it." >&2
  exit 1
else
  git clone --depth 1 "$REPO_URL" "$TARGET"
fi

if command -v python3 >/dev/null 2>&1; then
  python3 "$TARGET/scripts/validate_repo.py"
else
  echo "NOTE: python3 not found; installation completed but local validation was skipped."
fi

echo "Installed at: $TARGET"
echo "The skill does not configure or access any bank account."