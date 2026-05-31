#!/usr/bin/env python3
"""Aggregate a validated single-stock agent scorecard into a final rating."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_scorecard import load_json, validate_scorecard


DEFAULT_WEIGHTS = {
    "news_catalyst": 0.15,
    "industry_macro": 0.10,
    "business_moat": 0.05,
    "financial_quality": 0.15,
    "valuation": 0.15,
    "technical_trading": 0.20,
    "flow_positioning": 0.10,
    "risk_officer": 0.10,
}

EVIDENCE_MULTIPLIER = {
    "A": 1.00,
    "B": 0.85,
    "C": 0.65,
    "D": 0.40,
}

TRADE_PLAN_REQUIRED_FIELDS = [
    "entry_zone",
    "add_trigger",
    "reduce_trigger",
    "stop_loss",
    "take_profit",
    "invalidation",
    "position_sizing",
    "monitoring_plan",
]


def rating_for_score(score: float) -> str:
    if score >= 1.10:
        return "Strong Buy"
    if score >= 0.45:
        return "Buy"
    if score > -0.25:
        return "Watch"
    if score > -0.90:
        return "Avoid"
    return "Sell Risk"


def aggregate(payload: dict[str, Any]) -> dict[str, Any]:
    rows = {row["agent"]: row for row in payload["agent_scorecards"]}

    weighted_score = 0.0
    confidence_numerator = 0.0
    confidence_denominator = 0.0
    contributions: dict[str, float] = {}

    for agent, weight in DEFAULT_WEIGHTS.items():
        row = rows[agent]
        evidence = EVIDENCE_MULTIPLIER[row["evidence_grade"]]
        contribution = row["score"] * weight * row["confidence"] * evidence
        contributions[agent] = round(contribution, 4)
        weighted_score += contribution
        confidence_numerator += row["confidence"] * evidence * weight
        confidence_denominator += weight

    risk = rows["risk_officer"]
    risk_evidence = EVIDENCE_MULTIPLIER[risk["evidence_grade"]]
    risk_deduction = max(0.0, -risk["score"] * DEFAULT_WEIGHTS["risk_officer"] * risk["confidence"] * risk_evidence)
    confidence = confidence_numerator / confidence_denominator if confidence_denominator else 0.0

    return {
        "ticker": payload["ticker"],
        "market": payload["market"],
        "horizon": payload["horizon"],
        "as_of": payload["as_of"],
        "rating": rating_for_score(weighted_score),
        "weighted_score": round(weighted_score, 3),
        "confidence": round(confidence, 3),
        "risk_deduction": round(risk_deduction, 3),
        "contributions": contributions,
        "trade_plan_required_fields": TRADE_PLAN_REQUIRED_FIELDS,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scorecard", type=Path, help="Path to a scorecard JSON file.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
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

    result = aggregate(payload)
    indent = 2 if args.pretty else None
    print(json.dumps(result, indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
