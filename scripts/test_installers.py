#!/usr/bin/env python3
"""Adversarial installer regression tests using real Git semantics.

Network transport is replaced only for 'git fetch origin main' so CI remains
offline/deterministic. Status, ancestry, branch and merge behavior use the
runner's real Git binary.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git"
REAL_GIT = shutil.which("git")
BASH = shutil.which("bash")
PWSH = shutil.which("pwsh")

if not REAL_GIT or not BASH:
    raise SystemExit("git and bash are required")

def run(cmd, *, env=None, cwd=None, check=True):
    return subprocess.run(
        [str(x) for x in cmd],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
    )

def git(*args, cwd=None, check=True):
    return run([REAL_GIT, *args], cwd=cwd, check=check)

def expect_fail(cmd, *, env, marker: Path | None = None):
    result = run(cmd, env=env, check=False)
    if result.returncode == 0:
        raise AssertionError(f"expected failure, got success:\n{result.stdout}")
    if marker is not None and marker.exists():
        raise AssertionError(f"untrusted validator executed: {marker}")
    return result

def expect_ok(cmd, *, env):
    result = run(cmd, env=env, check=False)
    if result.returncode != 0:
        raise AssertionError(f"expected success, rc={result.returncode}:\n{result.stdout}")
    return result

def set_identity(path: Path):
    git("-C", path, "config", "user.email", "ci@example.invalid")
    git("-C", path, "config", "user.name", "CI")

def make_wrapper(fakebin: Path, origin: Path):
    wrapper = fakebin / "git"
    wrapper.write_text(
        """#!/usr/bin/env bash
set -euo pipefail
real_git="$REAL_GIT"
workdir=""
args=("$@")
if [ "${1:-}" = "-C" ]; then
  workdir="$2"
  shift 2
fi
if [ "${1:-}" = "fetch" ] && [ "${2:-}" = "--quiet" ] && [ "${3:-}" = "origin" ] && [ "${4:-}" = "main" ]; then
  exec "$real_git" -C "$workdir" fetch --quiet "$LOCAL_ORIGIN" main:refs/remotes/origin/main
fi
if [ -n "$workdir" ]; then
  exec "$real_git" -C "$workdir" "$@"
fi
exec "$real_git" "$@"
""",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)

def clone_target(origin: Path, target: Path):
    git("clone", "-q", origin, target)
    git("-C", target, "remote", "set-url", "origin", CANONICAL)
    set_identity(target)

def installer_commands(target: Path):
    yield "bash", [BASH, str(ROOT / "install/install.sh"), str(target)]
    if PWSH:
        yield "powershell", [PWSH, "-NoProfile", "-File", str(ROOT / "install/install.ps1"), "-Target", str(target)]

with tempfile.TemporaryDirectory(prefix="skill-installer-tests-") as td:
    td = Path(td)
    seed = td / "seed"
    shutil.copytree(ROOT, seed, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".pytest_cache"))
    git("init", "-q", "-b", "main", seed)
    set_identity(seed)
    git("-C", seed, "add", ".")
    git("-C", seed, "commit", "-q", "-m", "fixture: audited repository state")

    origin = td / "origin.git"
    git("clone", "-q", "--bare", seed, origin)
    git("--git-dir", origin, "symbolic-ref", "HEAD", "refs/heads/main")

    fakebin = td / "fakebin"
    fakebin.mkdir()
    make_wrapper(fakebin, origin)

    env = os.environ.copy()
    env["REAL_GIT"] = REAL_GIT
    env["LOCAL_ORIGIN"] = str(origin)
    env["PATH"] = str(fakebin) + os.pathsep + env["PATH"]

    for label, cmd_builder in list(installer_commands(td / "placeholder")):
        # Foreign origin must fail before any update logic.
        foreign = td / f"{label}-foreign"
        git("init", foreign)
        git("-C", foreign, "remote", "add", "origin", "https://github.com/example/not-this-skill.git")
        (foreign / "scripts").mkdir()
        (foreign / "scripts/validate_repo.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
        cmd = [cmd_builder[0], *cmd_builder[1:-1], str(foreign)] if label == "bash" else [*cmd_builder[:-1], str(foreign)]
        expect_fail(cmd, env=env)

        # Dirty tracked content must fail and never execute it.
        dirty = td / f"{label}-dirty"
        clone_target(origin, dirty)
        marker = td / f"{label}-dirty-executed"
        (dirty / "scripts/validate_repo.py").write_text(
            f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n",
            encoding="utf-8",
        )
        cmd = [BASH, str(ROOT / "install/install.sh"), str(dirty)] if label == "bash" else [PWSH, "-NoProfile", "-File", str(ROOT / "install/install.ps1"), "-Target", str(dirty)]
        expect_fail(cmd, env=env, marker=marker)

        # Clean local child commit (ahead of origin/main) must also fail.
        ahead = td / f"{label}-ahead"
        clone_target(origin, ahead)
        marker = td / f"{label}-ahead-executed"
        (ahead / "scripts/validate_repo.py").write_text(
            f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n",
            encoding="utf-8",
        )
        git("-C", ahead, "add", "scripts/validate_repo.py")
        git("-C", ahead, "commit", "-q", "-m", "trojan local commit")
        cmd = [BASH, str(ROOT / "install/install.sh"), str(ahead)] if label == "bash" else [PWSH, "-NoProfile", "-File", str(ROOT / "install/install.ps1"), "-Target", str(ahead)]
        expect_fail(cmd, env=env, marker=marker)

        # Detached / non-main checkouts are intentionally refused.
        detached = td / f"{label}-detached"
        clone_target(origin, detached)
        git("-C", detached, "checkout", "-q", "--detach")
        cmd = [BASH, str(ROOT / "install/install.sh"), str(detached)] if label == "bash" else [PWSH, "-NoProfile", "-File", str(ROOT / "install/install.ps1"), "-Target", str(detached)]
        expect_fail(cmd, env=env)

    # Prepare two legitimate stale installs before advancing origin.
    stale_targets = {}
    for label, _ in installer_commands(td / "placeholder2"):
        target = td / f"{label}-stale"
        clone_target(origin, target)
        stale_targets[label] = target

    updater = td / "updater"
    git("clone", "-q", origin, updater)
    set_identity(updater)
    (updater / ".ci-update-marker.md").write_text("safe fast-forward\n", encoding="utf-8")
    git("-C", updater, "add", ".ci-update-marker.md")
    git("-C", updater, "commit", "-q", "-m", "ci: safe update fixture")
    git("-C", updater, "push", "-q", "origin", "main")

    for label, target in stale_targets.items():
        cmd = [BASH, str(ROOT / "install/install.sh"), str(target)] if label == "bash" else [PWSH, "-NoProfile", "-File", str(ROOT / "install/install.ps1"), "-Target", str(target)]
        expect_ok(cmd, env=env)
        if not (target / ".ci-update-marker.md").is_file():
            raise AssertionError(f"{label}: legitimate stale install did not fast-forward")
        local = git("-C", target, "rev-parse", "HEAD").stdout.strip()
        remote = git("--git-dir", origin, "rev-parse", "refs/heads/main").stdout.strip()
        if local != remote:
            raise AssertionError(f"{label}: HEAD {local} != origin/main {remote}")

    # URL normalization matrix: secure canonical transports accepted; insecure or credentialed forms rejected.
    accepted_origins = [
        CANONICAL,
        "HTTPS://GITHUB.COM/SIMONDALMASSO/CERRAR-CUENTA-BANCARIA-AR.GIT",
        "git@github.com:simondalmasso/cerrar-cuenta-bancaria-ar.git",
        "ssh://git@github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git",
    ]
    rejected_origins = [
        "http://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git",
        "git://github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git",
        "https://user:token@github.com/simondalmasso/cerrar-cuenta-bancaria-ar.git",
        "https://github.com/example/not-this-skill.git",
    ]
    for label, _ in installer_commands(td / "placeholder-matrix"):
        for idx, remote in enumerate(accepted_origins):
            target = td / f"{label}-accepted-{idx}"
            git("clone", "-q", origin, target)
            git("-C", target, "remote", "set-url", "origin", remote)
            cmd = [BASH, str(ROOT / "install/install.sh"), str(target)] if label == "bash" else [PWSH, "-NoProfile", "-File", str(ROOT / "install/install.ps1"), "-Target", str(target)]
            expect_ok(cmd, env=env)
        for idx, remote in enumerate(rejected_origins):
            target = td / f"{label}-rejected-{idx}"
            git("clone", "-q", origin, target)
            git("-C", target, "remote", "set-url", "origin", remote)
            cmd = [BASH, str(ROOT / "install/install.sh"), str(target)] if label == "bash" else [PWSH, "-NoProfile", "-File", str(ROOT / "install/install.ps1"), "-Target", str(target)]
            expect_fail(cmd, env=env)

    # Repo-local insteadOf rewrite must remain fail-closed: get-url reveals it.
    attacker = td / "attacker.git"
    git("init", "--bare", attacker)
    for label, _ in installer_commands(td / "placeholder3"):
        target = td / f"{label}-instead-of"
        git("clone", "-q", origin, target)
        git("-C", target, "remote", "set-url", "origin", CANONICAL)
        git("-C", target, "config", f"url.{attacker.as_uri()}.insteadOf", CANONICAL)
        cmd = [BASH, str(ROOT / "install/install.sh"), str(target)] if label == "bash" else [PWSH, "-NoProfile", "-File", str(ROOT / "install/install.ps1"), "-Target", str(target)]
        expect_fail(cmd, env=env)

print("INSTALLER ADVERSARIAL TESTS PASS")
print("- foreign origin rejected")
print("- dirty worktree rejected before validator execution")
print("- local-ahead trojan commit rejected before validator execution")
print("- detached/non-main checkout rejected")
print("- legitimate stale main fast-forwards to origin/main")
print("- secure URL normalization matrix enforced consistently")
print("- repo-local insteadOf rewrite remains fail-closed")
if not PWSH:
    print("- PowerShell runtime not available locally; PowerShell cases skipped")
