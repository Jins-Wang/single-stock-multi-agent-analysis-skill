---
name: single-stock-multi-agent-analysis
description: Use when the user asks to deeply analyze one already-screened stock, one equity ticker, A-share, HK or US stock, ETF-like equity, buy/sell timing for one ticker, or requests a sourced multi-agent stock assessment with scorecard, confidence, trade plan, and risk controls.
---

# Single Stock Multi-Agent Analysis

## Overview

Use this skill for a deep, sourced, risk-aware review of one already-screened stock. The default horizon is `1-8 weeks` unless the user specifies another horizon. The output must separate facts from inference, show source freshness, use a 10-agent research committee, and produce a structured scorecard instead of a loose narrative.

This skill is not a stock screener. If the user asks to find stocks from a universe, use or suggest a screening workflow such as `idea-generation` or `market-analysis-orchestrator` before returning to this single-stock review.

## Execution Workflow

### 1. Classify the Request

Identify:

- Ticker, exchange, company name, currency, and market type: A-share, HK, US, or other.
- Whether the stock has already been screened. If not, ask the user for the target ticker or switch to a screening skill if they asked for stock selection.
- User horizon. Default to `1-8 weeks` for swing/trading review.
- Output need: quick recommendation, full Markdown report, scorecard JSON, chart, spreadsheet, deck, document, or recurring monitor.
- Whether the user asks for buy/sell timing. If yes, answer with scenarios, position-risk framing, levels, and invalidation points; do not give an unconditional instruction.

Always state the data timestamp and timezone. For relative dates such as "next Monday", convert to an exact date.

### 2. Check Tools and Dependencies First

Run the bundled dependency checker before data work:

```bash
python3 ~/.codex/skills/single-stock-multi-agent-analysis/scripts/check_dependencies.py
```

If working in `/Users/jins/Documents/Qlib`, prefer its environment:

```bash
/Users/jins/Documents/Qlib/envs/qlib/bin/python ~/.codex/skills/single-stock-multi-agent-analysis/scripts/check_dependencies.py
```

Required Python packages for local A-share/Qlib work: `akshare`, `pandas`, `numpy`, `matplotlib`.

If any required package is missing, install into the selected Python environment:

```bash
<python> -m pip install akshare pandas numpy matplotlib
```

Then rerun the dependency checker. If installation fails, continue with web/finance sources and clearly mark the analysis as source-limited.

Before collecting data, explicitly disclose runtime capabilities and installation status. Do not claim that a plugin, skill, package, or tool is installed unless verified in the current turn. Use a compact table with `required`, `available`, `missing`, `fallback`, and `install action` columns.

Minimum capability rows to disclose:

- `single-stock-multi-agent-analysis` skill: required; this active skill provides the workflow.
- Python environment plus `akshare`, `pandas`, `numpy`, `matplotlib`: required for local A-share/Qlib OHLCV, calculations, and charts.
- Helper scripts: `validate_scorecard.py` and `aggregate_scorecard.py`; required for machine-checkable scorecards in full analyses.
- Reference files: `agent_roles.md`, `scorecard_schema.md`, `source_quality.md`, and `report_template.md`; required for full committee output.
- Current web/source access: required for fresh prices, announcements, filings, and news.
- Dedicated finance/quote tool: recommended for quote verification; use it when exposed, otherwise verify with public market-data sources.
- Multi-agent/subagent tools: recommended for true parallel independent agent execution. If unavailable, simulate independent agent memos sequentially and label them as simulated tracks.
- Browser or Chrome plugin: optional for authenticated/profile-dependent pages, visual inspection, or manual page workflows.
- Automation/reminder tool: optional for recurring monitors; use it only when the user asks to watch, monitor, remind, or follow up.
- Skill installer: optional setup support for installing this skill or companion skills from a GitHub repo. After installing a skill, tell the user to restart Codex.
- Output companion skills: optional. Invoke `spreadsheets:Spreadsheets` for workbook output, `presentations:Presentations` for PPTX/decks, or `documents:documents` for DOCX only when the user asks for that deliverable.

No other Codex skill is mandatory by default.

### 3. Collect Fresh Source Data

Use at least one primary source and one verification source when feasible. Apply the source quality rules in `references/source_quality.md`.

For A-shares:

- Prefer official filings from CNINFO/SSE/SZSE for annual reports, quarterly reports, equity issuance, dividends, risk warnings, inquiry letters, governance events, and major shareholder changes.
- Use local AkShare/Qlib for daily OHLCV if available.
- If an Eastmoney endpoint fails, try `ak.stock_zh_a_daily(symbol="sh600353", ...)`, `stock_zh_a_hist_tx`, Sina/Tencent/Yahoo/Investing, or official exchange pages.
- Record fallback/cache behavior.

For HK/US/global equities:

- Use finance/quote tools where exposed, official filings, exchange/company investor relations, and reputable market-data pages.
- Prefer SEC/EDGAR for US filings, HKEX/company IR for HK filings, and official exchange/company sources where available.

Collect these minimum facts:

- Latest close/current quote, market cap, volume/turnover, currency, and date.
- 6-12 months daily OHLCV; longer if available.
- Latest annual report and latest quarter or interim period.
- Recent announcements, news, regulatory events, major shareholder changes, dividends, financing, M&A, litigation, inquiry letters, lockups, pledges, risk warnings.
- Industry/topic catalysts and logical comparable companies.

### 4. Dispatch the 10-Agent Research Committee

Use the roles in `references/agent_roles.md`. When using subagents, keep prompts self-contained and ask each agent to return facts, inference, score, confidence, evidence grade, sources, and cross-check questions.

Required agents:

1. **Data Steward**
   - Checks data freshness, source quality, missing data, conflicting numbers, stale prices, and confidence caps.
   - Can block a strong rating if source quality is too weak.

2. **News & Catalyst**
   - Reviews announcements, media narrative, corporate actions, earnings dates, product/regulatory catalysts, forum sentiment as low-confidence context, and event duration.

3. **Industry & Macro**
   - Assesses sector cycle, policy, rates, FX, commodity inputs, regulation, peer performance, and macro sensitivity.

4. **Business & Moat**
   - Reviews revenue model, competitive position, customer/supplier power, product durability, management execution, and business quality.

5. **Financial Quality**
   - Analyzes revenue, gross margin, operating margin, net profit, adjusted/recurring profit, ROE/ROIC, free cash flow, leverage, cash conversion, receivables, inventory, dilution, and accounting quality.

6. **Valuation**
   - Compares market cap, PE TTM/static, PB, PS, EV/EBITDA, dividend yield, history, peers, and scenario upside/downside. Use DCF or sum-of-parts only when inputs are supportable.

7. **Technical & Trading**
   - Calculates MA5/10/20/60/120/250, 5/20/60/120/250-day returns, RSI14, MACD, 20/60/120/250-day annualized volatility, recent high/low, support/resistance, gap behavior, volume, and turnover.
   - Classifies the setup as trend confirmation, breakout, failed breakout, range-bound, high-volatility distribution, or capitulation/reversal.

8. **Flow & Positioning**
   - Reviews turnover, liquidity, ETF/index inclusion, northbound/southbound flow when relevant, fund ownership if available, short interest where available, insider/shareholder activity, lockups, and crowding.

9. **Risk Officer**
   - Builds the risk register with probability, impact, monitoring signal, and action if triggered.
   - Identifies kill switches that override a positive score.

10. **Portfolio/Trade Planner**
    - Converts the committee result into an executable plan: entry zone, add trigger, reduce trigger, stop loss, take profit, invalidation, position sizing, and monitoring plan.
    - If portfolio context is missing, use generic risk-budget language rather than personalized advice.

### 5. Force Agent Interaction

After first-pass memos, run a challenge round:

- Give each agent the other agents' key conclusions.
- Ask each agent to identify conflicts, over-optimism, over-pessimism, stale facts, missing data, and what would change its view.
- Preserve disagreements in the final report instead of smoothing them away.

At minimum, reconcile:

- Whether news/catalysts are backed by disclosed revenue, orders, margins, or policy facts.
- Whether technical strength is trend quality or crowded theme trading.
- Whether valuation is supported by current financials or by future optionality.
- Whether fundamentals show recurring improvement or one-off gains.
- Whether flow confirms accumulation or warns of distribution/crowding.
- Whether any Risk Officer kill switch downgrades the trade plan.

### 6. Build the Scorecard

Every full analysis must include the scorecard schema in `references/scorecard_schema.md`.

Each agent must provide:

- `score`: from `-2` to `+2`.
- `confidence`: from `0.00` to `1.00`.
- `evidence_grade`: `A`, `B`, `C`, or `D`.
- `horizon`: usually `1-8 weeks`.
- `positives`, `negatives`, and `kill_switch`.

Default 1-8 week weights:

| Dimension | Weight |
| --- | ---: |
| Technical & Trading | 20% |
| News & Catalyst | 15% |
| Financial Quality | 15% |
| Valuation | 15% |
| Flow & Positioning | 10% |
| Industry & Macro | 10% |
| Business & Moat | 5% |
| Risk Officer | 10% deduction or contribution |

Data Steward and Portfolio/Trade Planner are gating agents. They do not add alpha score directly, but they can cap confidence, block a strong rating, or reduce position size.

When saving a full report, also save:

```text
reports/<ticker>/<ticker>_<company>_scorecard_<YYYY-MM-DD>.json
```

Validate it:

```bash
python3 ~/.codex/skills/single-stock-multi-agent-analysis/scripts/validate_scorecard.py <scorecard.json>
```

Aggregate it:

```bash
python3 ~/.codex/skills/single-stock-multi-agent-analysis/scripts/aggregate_scorecard.py <scorecard.json> --pretty
```

Rating guide:

- `Strong Buy`: weighted score >= `1.10` and no active kill switch.
- `Buy`: weighted score >= `0.45`.
- `Watch`: weighted score > `-0.25`, or evidence is promising but not strong enough.
- `Avoid`: weighted score > `-0.90` with unfavorable risk/reward or timing.
- `Sell Risk`: weighted score <= `-0.90`, or a critical kill switch is active.

### 7. Produce the Report

Use `references/report_template.md` for full reports.

Save a Markdown report when the user asks for a full analysis or when the work is substantial:

```text
reports/<ticker>/<ticker>_<company>_review_<YYYY-MM-DD>.md
```

Include:

1. Committee conclusion, rating, weighted score, confidence, data timestamp, and limitations.
2. Capability and source disclosure table.
3. Source quality/freshness table.
4. Key market and financial metrics table.
5. 10-agent scorecard.
6. Individual agent memos.
7. Debate and reconciliation summary.
8. Scenario table: bull, base, bear.
9. Trade plan: entry zone, add/reduce triggers, stop loss, take profit, invalidation, position sizing, and monitoring.
10. Risk register with probability, impact, monitoring signal, and action if triggered.
11. Follow-up checklist.
12. Source links.

For visual output, generate a simple daily trend chart when local OHLCV exists. Use `matplotlib`; save under the same report folder and embed with an absolute path.

### 8. Answer Buy/Sell Timing Questions

When the user asks "can I buy next Monday?" or similar:

- Browse/check latest post-report news first.
- Give a clear operational stance such as "do not chase at open", "wait for pullback confirmation", "only small trial position after breakout confirmation", or "stand aside until invalidation clears" when supported.
- Tie the stance to concrete levels, catalysts, valuation, flow, and risk.
- State exact invalidation points and what data would change the view.
- Include risk-budget guidance such as trial size, maximum loss per idea, and conditions for adding or reducing.
- Avoid pretending certainty; avoid personalized suitability unless the user supplied portfolio/risk context.

### 9. Cleanup

If subagents were spawned, close them after their outputs have been integrated. Mention failed data sources, fallbacks, missing packages, stale data, or unverified claims in the final answer.
