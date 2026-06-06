# Single Stock Multi-Agent Analysis Skill

`single-stock-multi-agent-analysis` is a Codex skill for producing sourced, risk-aware single-stock research reports. It is designed for one already-screened ticker or company at a time, including A-shares, Hong Kong stocks, US stocks, and ETF-like equities.

The skill does not make unconditional trading calls. When a user asks whether to buy or sell, it frames the answer with a 10-agent research committee, structured scorecard, scenario analysis, risk controls, invalidation points, data freshness, and source limitations.

## What It Does

- Classifies the stock request by ticker, market, time horizon, and output need.
- Checks local Python dependencies before analysis.
- Collects fresh market data, filings, announcements, news, and comparable context.
- Runs ten independent analysis agents:
  - Data Steward
  - News and Catalyst
  - Industry and Macro
  - Business and Moat
  - Financial Quality
  - Valuation
  - Technical and Trading
  - Flow and Positioning
  - Risk Officer
  - Portfolio/Trade Planner
- Forces the agents to challenge each other before producing the final committee view.
- Scores each dimension from `-2` to `+2`, with confidence, evidence grade, and kill switches.
- Generates a Markdown report, machine-checkable scorecard JSON, and, when OHLCV data is available, a simple price trend chart.

## Repository Structure

```text
single-stock-multi-agent-analysis/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── agent_roles.md
│   ├── report_template.md
│   ├── scorecard_schema.md
│   └── source_quality.md
└── scripts/
    ├── aggregate_scorecard.py
    ├── check_dependencies.py
    └── validate_scorecard.py
```

The installable Codex skill is the `single-stock-multi-agent-analysis/` directory.

## Installation

### Option 1: Install With Codex Skill Installer

Ask Codex:

```text
Use $skill-installer to install the skill from:
https://github.com/Jins-Wang/single-stock-multi-agent-analysis-skill/tree/main/single-stock-multi-agent-analysis
```

Restart Codex after installation so the new skill is picked up.

### Option 2: Manual Install

Clone this repository, then copy the skill folder into your Codex skills directory:

```bash
git clone git@github.com:Jins-Wang/single-stock-multi-agent-analysis-skill.git
mkdir -p ~/.codex/skills
cp -R single-stock-multi-agent-analysis-skill/single-stock-multi-agent-analysis ~/.codex/skills/
```

Restart Codex after copying.

## Runtime Dependencies

For local A-share and Qlib workflows, the skill expects:

- `akshare`
- `pandas`
- `numpy`
- `matplotlib`

Check dependencies with:

```bash
python3 ~/.codex/skills/single-stock-multi-agent-analysis/scripts/check_dependencies.py
```

If working inside `/Users/jins/Documents/Qlib`, prefer the Qlib environment:

```bash
/Users/jins/Documents/Qlib/envs/qlib/bin/python ~/.codex/skills/single-stock-multi-agent-analysis/scripts/check_dependencies.py
```

Install missing packages into the selected Python environment:

```bash
<python> -m pip install akshare pandas numpy matplotlib
```

The scorecard helper scripts use only the Python standard library.

## Optional Codex Capabilities

The skill explicitly checks and discloses runtime capability status before analysis:

- Web/source access for fresh prices, filings, announcements, and news
- Finance or quote tools, when exposed, for quote verification
- Subagent tools for true multi-agent parallel analysis
- Browser or Chrome plugins for authenticated or visual web workflows
- Automation tools for recurring monitors or follow-up checks
- Output skills such as Spreadsheets, Presentations, or Documents when the requested deliverable needs them

If true subagent execution is unavailable, the skill falls back to labeled sequential memos for each analysis track.

## Scorecard Workflow

Full analyses should save a scorecard JSON under:

```text
reports/<ticker>/<ticker>_<company>_scorecard_<YYYY-MM-DD>.json
```

Validate the schema:

```bash
python3 ~/.codex/skills/single-stock-multi-agent-analysis/scripts/validate_scorecard.py <scorecard.json>
```

Aggregate the final rating:

```bash
python3 ~/.codex/skills/single-stock-multi-agent-analysis/scripts/aggregate_scorecard.py <scorecard.json> --pretty
```

Default ratings are `Strong Buy`, `Buy`, `Watch`, `Avoid`, and `Sell Risk`. The default horizon is `1-8 weeks` unless the user specifies a different horizon.

## Example Prompts

```text
Use $single-stock-multi-agent-analysis to analyze 600353.SH with a 1-8 week horizon and save a full Markdown report plus scorecard JSON.
```

```text
Use $single-stock-multi-agent-analysis to review AAPL. Focus on fundamentals, valuation, recent news, and whether the current technical setup supports adding exposure.
```

```text
Use $single-stock-multi-agent-analysis to assess whether I should consider buying this stock next Monday. Give scenarios, invalidation points, and what would change the view.
```

## Report Output

For full analyses, reports are saved under:

```text
reports/<ticker>/<ticker>_<company>_review_<YYYY-MM-DD>.md
```

A complete report includes:

- Core conclusion, confidence, timestamp, and timezone
- Method table and multi-agent interaction summary
- Data source and freshness table
- 10-agent structured scorecard
- Key metrics table
- Individual agent memos
- Debate and reconciliation summary
- Trade plan with entry zone, add/reduce triggers, stop loss, take profit, invalidation, and position sizing
- Risk register with probability, impact, monitoring signal, and action if triggered
- Bull, base, and bear scenarios
- Follow-up monitoring list
- Source links

## Important Notes

- Always verify fresh data before making time-sensitive conclusions.
- Forums and social sentiment should be treated as low-confidence unless corroborated.
- Official filings and exchange/company disclosures should be prioritized over media summaries.
- The skill is for research support and does not provide personalized financial advice.
