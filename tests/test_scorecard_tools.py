#!/usr/bin/env python3
"""Regression tests for the skill scorecard helper scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "single-stock-multi-agent-analysis"
VALIDATE = SKILL_DIR / "scripts" / "validate_scorecard.py"
AGGREGATE = SKILL_DIR / "scripts" / "aggregate_scorecard.py"

sys.path.insert(0, str(SKILL_DIR / "scripts"))

import aggregate_scorecard


def sample_scorecard() -> dict:
    agents = [
        ("data_steward", 0.0, 0.95, "A"),
        ("news_catalyst", 1.0, 0.70, "B"),
        ("industry_macro", 0.5, 0.60, "B"),
        ("business_moat", 1.0, 0.75, "B"),
        ("financial_quality", 1.5, 0.80, "A"),
        ("valuation", -0.5, 0.65, "B"),
        ("technical_trading", 1.5, 0.72, "B"),
        ("flow_positioning", 0.5, 0.55, "C"),
        ("risk_officer", -1.0, 0.85, "A"),
        ("portfolio_trade_planner", 1.0, 0.70, "B"),
    ]
    return {
        "ticker": "AAPL",
        "company": "Apple Inc.",
        "market": "US",
        "horizon": "1-8 weeks",
        "as_of": "2026-05-31T09:00:00+08:00",
        "agent_scorecards": [
            {
                "agent": name,
                "score": score,
                "confidence": confidence,
                "evidence_grade": grade,
                "horizon": "1-8 weeks",
                "positives": ["test positive"],
                "negatives": ["test negative"],
                "kill_switch": "test invalidation",
            }
            for name, score, confidence, grade in agents
        ],
    }


class ScorecardToolTests(unittest.TestCase):
    def test_default_weights_sum_to_one(self) -> None:
        self.assertAlmostEqual(sum(aggregate_scorecard.DEFAULT_WEIGHTS.values()), 1.0)

    def write_json(self, payload: dict) -> Path:
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with handle:
            json.dump(payload, handle)
        return Path(handle.name)

    def test_validate_scorecard_accepts_complete_schema(self) -> None:
        path = self.write_json(sample_scorecard())
        result = subprocess.run(
            [sys.executable, str(VALIDATE), str(path)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("scorecard: OK", result.stdout)

    def test_validate_scorecard_rejects_missing_required_agent(self) -> None:
        payload = sample_scorecard()
        payload["agent_scorecards"] = [
            row
            for row in payload["agent_scorecards"]
            if row["agent"] != "risk_officer"
        ]
        path = self.write_json(payload)
        result = subprocess.run(
            [sys.executable, str(VALIDATE), str(path)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required agents: risk_officer", result.stderr)

    def test_aggregate_scorecard_outputs_rating_and_trade_fields(self) -> None:
        path = self.write_json(sample_scorecard())
        result = subprocess.run(
            [sys.executable, str(AGGREGATE), str(path)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertIn(payload["rating"], {"Strong Buy", "Buy", "Watch", "Avoid", "Sell Risk"})
        self.assertIn("weighted_score", payload)
        self.assertIn("confidence", payload)
        self.assertIn("risk_deduction", payload)
        self.assertIn("trade_plan_required_fields", payload)
        self.assertIn("entry_zone", payload["trade_plan_required_fields"])


if __name__ == "__main__":
    unittest.main()
