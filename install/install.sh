#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git"
BASE="${AGENT_SKILLS_HOME:-$HOME/.agents/skills}"
TARGET="${1:-$BASE/cerrar-cuenta-bancaria-ar}"

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git is required." >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"

if [ -d "$TARGET/.git" ]; then
  echo "Updating existing installation: $TARGET"
  git -C "$TARGET" pull --ff-only
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
