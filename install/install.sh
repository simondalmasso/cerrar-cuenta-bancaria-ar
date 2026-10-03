#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git"
EXPECTED_REMOTE="github.com/simondalmasso/cerrar-cuenta-bancaria-ar"
BASE="${AGENT_SKILLS_HOME:-$HOME/.agents/skills}"

if [ "$#" -gt 0 ] && [ -z "$1" ]; then
  echo "ERROR: target path cannot be empty." >&2
  exit 1
fi
TARGET="${1:-$BASE/cerrar-cuenta-bancaria-ar}"

normalize_github_remote() {
  local u="$1"
  local lower=""
  local path=""
  u="${u%/}"
  lower="$(printf '%s' "$u" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    git@github.com:*) path="${lower#git@github.com:}" ;;
    ssh://git@github.com/*) path="${lower#ssh://git@github.com/}" ;;
    https://github.com/*) path="${lower#https://github.com/}" ;;
    *) printf '%s' "$lower"; return ;;
  esac
  path="${path%/}"
  path="${path%.git}"
  printf 'github.com/%s' "$path"
}

die_unverified() {
  echo "ERROR: existing target is not a clean, canonical main checkout of this project." >&2
  echo "Target: $TARGET" >&2
  echo "Refusing to update or execute repository code." >&2
  exit 1
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
    echo "Origin: ${origin:-<missing>}" >&2
    echo "Expected: $REPO_URL" >&2
    die_unverified
  fi

  branch="$(git -C "$TARGET" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
  if [ "$branch" != "main" ]; then
    echo "ERROR: existing installation must be on branch main; found: ${branch:-<detached>}." >&2
    die_unverified
  fi

  if [ -n "$(git -C "$TARGET" status --porcelain --untracked-files=normal)" ]; then
    echo "ERROR: existing installation contains local or untracked changes." >&2
    die_unverified
  fi

  echo "Verifying and updating installation: $TARGET"
  git -C "$TARGET" fetch --quiet origin main

  if ! git -C "$TARGET" merge-base --is-ancestor HEAD refs/remotes/origin/main; then
    echo "ERROR: local HEAD is ahead of or diverged from origin/main." >&2
    die_unverified
  fi

  git -C "$TARGET" merge --ff-only refs/remotes/origin/main >/dev/null

  head_sha="$(git -C "$TARGET" rev-parse HEAD)"
  remote_sha="$(git -C "$TARGET" rev-parse refs/remotes/origin/main)"
  if [ "$head_sha" != "$remote_sha" ]; then
    echo "ERROR: update did not land exactly on origin/main." >&2
    die_unverified
  fi
  if [ -n "$(git -C "$TARGET" status --porcelain --untracked-files=normal)" ]; then
    echo "ERROR: working tree changed unexpectedly during verification." >&2
    die_unverified
  fi
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
