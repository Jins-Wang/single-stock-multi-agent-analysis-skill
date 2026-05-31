# Scorecard Schema

The final report must include a machine-checkable scorecard for the 10-agent committee. Save it as JSON when the user asks for a full report or when the analysis is substantial.

Recommended path:

```text
reports/<ticker>/<ticker>_<company>_scorecard_<YYYY-MM-DD>.json
```

## Required Top-Level Fields

```json
{
  "ticker": "AAPL",
  "company": "Apple Inc.",
  "market": "US",
  "horizon": "1-8 weeks",
  "as_of": "2026-05-31T09:00:00+08:00",
  "agent_scorecards": []
}
```

## Required Agents

The `agent_scorecards` array must contain exactly these agent identifiers:

- `data_steward`
- `news_catalyst`
- `industry_macro`
- `business_moat`
- `financial_quality`
- `valuation`
- `technical_trading`
- `flow_positioning`
- `risk_officer`
- `portfolio_trade_planner`

## Required Agent Fields

Each row must contain:

```json
{
  "agent": "valuation",
  "score": -0.5,
  "confidence": 0.65,
  "evidence_grade": "B",
  "horizon": "1-8 weeks",
  "positives": ["..."],
  "negatives": ["..."],
  "kill_switch": "..."
}
```

Rules:

- `score`: numeric, from `-2` to `+2`.
- `confidence`: numeric, from `0` to `1`.
- `evidence_grade`: `A`, `B`, `C`, or `D`.
- `positives` and `negatives`: lists of strings.
- `kill_switch`: non-empty string explaining the condition that invalidates the agent's view.

## Default 1-8 Week Weights

| Agent | Weight |
| --- | ---: |
| News & Catalyst | 15% |
| Industry & Macro | 10% |
| Business & Moat | 5% |
| Financial Quality | 15% |
| Valuation | 15% |
| Technical & Trading | 20% |
| Flow & Positioning | 10% |
| Risk Officer | 10% |

Data Steward and Portfolio/Trade Planner are gating agents. They do not add alpha score directly, but they can cap confidence, block a rating, or require a smaller position.

## Helper Commands

Validate a scorecard:

```bash
python3 ~/.codex/skills/single-stock-multi-agent-analysis/scripts/validate_scorecard.py reports/AAPL/AAPL_scorecard_2026-05-31.json
```

Aggregate final rating:

```bash
python3 ~/.codex/skills/single-stock-multi-agent-analysis/scripts/aggregate_scorecard.py reports/AAPL/AAPL_scorecard_2026-05-31.json --pretty
```
