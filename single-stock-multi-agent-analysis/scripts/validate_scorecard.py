#!/usr/bin/env python3
"""Validate a single-stock multi-agent scorecard JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_AGENTS = [
    "data_steward",
    "news_catalyst",
    "industry_macro",
    "business_moat",
    "financial_quality",
    "valuation",
    "technical_trading",
    "flow_positioning",
    "risk_officer",
    "portfolio_trade_planner",
]

REQUIRED_TOP_LEVEL_FIELDS = ["ticker", "market", "horizon", "as_of", "agent_scorecards"]
REQUIRED_AGENT_FIELDS = [
    "agent",
    "score",
    "confidence",
    "evidence_grade",
    "horizon",
    "positives",
    "negatives",
    "kill_switch",
]
EVIDENCE_GRADES = {"A", "B", "C", "D"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("scorecard must be a JSON object")
    return payload


def validate_scorecard(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in payload:
            errors.append(f"missing top-level field: {field}")

    rows = payload.get("agent_scorecards")
    if not isinstance(rows, list):
        errors.append("agent_scorecards must be a list")
        return errors

    seen: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"agent_scorecards[{index}] must be an object")
            continue

        for field in REQUIRED_AGENT_FIELDS:
            if field not in row:
                errors.append(f"agent_scorecards[{index}] missing field: {field}")

        agent = row.get("agent")
        if isinstance(agent, str):
            seen.add(agent)
            if agent not in REQUIRED_AGENTS:
                errors.append(f"unknown agent: {agent}")
        else:
            errors.append(f"agent_scorecards[{index}].agent must be a string")

        score = row.get("score")
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            errors.append(f"agent_scorecards[{index}].score must be numeric")
        elif score < -2 or score > 2:
            errors.append(f"agent_scorecards[{index}].score must be between -2 and 2")

        confidence = row.get("confidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            errors.append(f"agent_scorecards[{index}].confidence must be numeric")
        elif confidence < 0 or confidence > 1:
            errors.append(f"agent_scorecards[{index}].confidence must be between 0 and 1")

        grade = row.get("evidence_grade")
        if grade not in EVIDENCE_GRADES:
            errors.append(f"agent_scorecards[{index}].evidence_grade must be A, B, C, or D")

        for field in ("positives", "negatives"):
            value = row.get(field)
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                errors.append(f"agent_scorecards[{index}].{field} must be a list of strings")

        kill_switch = row.get("kill_switch")
        if not isinstance(kill_switch, str) or not kill_switch.strip():
            errors.append(f"agent_scorecards[{index}].kill_switch must be a non-empty string")

    missing = [agent for agent in REQUIRED_AGENTS if agent not in seen]
    if missing:
        errors.append(f"missing required agents: {', '.join(missing)}")

    duplicates = sorted(agent for agent in seen if sum(1 for row in rows if isinstance(row, dict) and row.get("agent") == agent) > 1)
    if duplicates:
        errors.append(f"duplicate agents: {', '.join(duplicates)}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scorecard", type=Path, help="Path to a scorecard JSON file.")
    args = parser.parse_args(argv)

    try:
        payload = load_json(args.scorecard)
        errors = validate_scorecard(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"scorecard: ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"scorecard: ERROR: {error}", file=sys.stderr)
        return 1

    print(f"scorecard: OK ({len(payload['agent_scorecards'])} agents)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
