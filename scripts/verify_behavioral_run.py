#!/usr/bin/env python3
"""Verify a recorded behavioral eval run against evals/scenarios.json.

This script does not call a model and does not judge natural language. It verifies
that a real host/model run recorded a verdict for every must/must_not condition,
that every scenario is present exactly once, and that the run's aggregate PASS is
internally consistent.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=Path)
    ap.add_argument("--expected-commit", help="candidate commit SHA; defaults to current git HEAD")
    args = ap.parse_args()

    scenarios = json.loads((ROOT/"evals/scenarios.json").read_text(encoding="utf-8"))
    run = json.loads(args.run.read_text(encoding="utf-8"))
    expected = {c["id"]: c for c in scenarios["families"]}
    seen = set()
    errors = []

    if run.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if run.get("skill_version") != scenarios.get("version"):
        errors.append("skill_version does not match eval version")
    if not re.fullmatch(r"[0-9a-f]{40}", str(run.get("skill_commit",""))):
        errors.append("skill_commit must be a 40-char lowercase SHA")
    expected_commit = args.expected_commit
    if expected_commit is None:
        try:
            expected_commit = subprocess.run(
                ["git","-C",str(ROOT),"rev-parse","HEAD"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            ).stdout.strip()
        except Exception:
            expected_commit = None
    if expected_commit is not None:
        if not re.fullmatch(r"[0-9a-f]{40}", expected_commit):
            errors.append("--expected-commit/current HEAD is not a 40-char lowercase SHA")
        elif run.get("skill_commit") != expected_commit:
            errors.append(f"skill_commit {run.get('skill_commit')!r} does not match expected candidate {expected_commit}")
    for key in ("host","model","executed_at"):
        if not isinstance(run.get(key),str) or not run[key].strip():
            errors.append(f"missing {key}")

    judge = run.get("judge")
    if (
        not isinstance(judge, dict)
        or judge.get("type") not in {"human","model","hybrid"}
        or not isinstance(judge.get("identity"), str)
        or not judge.get("identity", "").strip()
    ):
        errors.append("judge must declare type=human/model/hybrid and non-empty identity")

    if not isinstance(run.get("cases"), list):
        errors.append("cases must be a list")
        case_rows = []
    else:
        case_rows = run["cases"]

    for result in case_rows:
        cid = result.get("id")
        if cid not in expected:
            errors.append(f"unknown case {cid!r}")
            continue
        if cid in seen:
            errors.append(f"duplicate case {cid}")
            continue
        seen.add(cid)
        spec = expected[cid]
        must = result.get("must") or {}
        must_not = result.get("must_not") or {}
        expected_must = set(spec["must"])
        expected_must_not = set(spec["must_not"])
        if set(must) != expected_must:
            errors.append(f"{cid}: must verdict keys do not match spec")
        if set(must_not) != expected_must_not:
            errors.append(f"{cid}: must_not verdict keys do not match spec")
        if not all(isinstance(v,bool) for v in must.values()):
            errors.append(f"{cid}: must verdicts must be boolean")
        if not all(isinstance(v,bool) for v in must_not.values()):
            errors.append(f"{cid}: must_not verdicts must be boolean")
        computed = bool(must) and all(must.values()) and bool(must_not) and all(must_not.values())
        if result.get("pass") is not computed:
            errors.append(f"{cid}: pass={result.get('pass')!r} inconsistent with verdicts")
        if not isinstance(result.get("response"),str) or not result.get("response","").strip():
            errors.append(f"{cid}: response must be a non-empty string")
        if not isinstance(result.get("tool_calls"),list):
            errors.append(f"{cid}: tool_calls must be a list")

    missing = sorted(set(expected)-seen)
    if missing:
        errors.append("missing cases: " + ", ".join(missing))

    if errors:
        print("BEHAVIORAL EVAL RUN INVALID")
        for err in errors:
            print(f"- {err}")
        return 1

    passed = sum(1 for r in case_rows if r["pass"])
    total = len(expected)
    print("BEHAVIORAL EVAL RUN VERIFIED")
    print(f"- host: {run['host']}")
    print(f"- model: {run['model']}")
    print(f"- skill commit: {run['skill_commit']}")
    print(f"- cases: {passed}/{total} pass")
    if passed != total:
        print("- release gate: FAIL")
        return 2
    print("- release gate: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
