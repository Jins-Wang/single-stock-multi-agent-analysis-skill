---
name: single-stock-multi-agent-analysis
description: Use when the user asks to analyze a single stock, one equity ticker, A-share stock, HK/US stock, ETF-like equity, buy/sell timing for one ticker, or requests a multi-dimensional stock assessment with sentiment, K-line, fundamentals, valuation, risk, scenarios, and a sourced report.
---

# Single Stock Multi-Agent Analysis

## Overview

Use this skill to run a reproducible, multi-dimensional analysis for one stock. Separate facts from inference, use fresh sources, and produce a sourced risk-aware report instead of an unconditional trading call.

## Execution Workflow

### 1. Classify the Request

Identify:

- Ticker, exchange, company name, and whether it is A-share, HK, US, or other.
- User horizon: intraday, next trading day, 1-4 weeks, medium term, long term.
- Output need: quick recommendation, full report, chart, exported file, or recurring monitor.
- Whether the user asks for buy/sell. If yes, answer with scenarios, position-risk framing, and invalidation points; do not give an unconditional instruction.

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

Before collecting data, explicitly disclose the runtime capabilities and installation status. Do not claim that a plugin, skill, package, or tool is installed unless you verified it in the current turn. Use a compact table with `required`, `available`, `missing`, `fallback`, and `install action` columns.

Minimum capability rows to disclose:

- `single-stock-multi-agent-analysis` skill: required; this active skill provides the workflow.
- Python environment plus `akshare`, `pandas`, `numpy`, `matplotlib`: required for local A-share/Qlib OHLCV, calculations, and charts; run the bundled checker and install missing packages with the selected Python executable.
- Current web/source access: required for fresh prices, announcements, filings, and news; if browsing is unavailable, mark the report source-limited.
- Dedicated finance/quote tool: recommended for quote verification; use it when exposed, otherwise verify with public market-data sources.
- Multi-agent/subagent tools: required for true parallel multi-agent execution when this skill is explicitly invoked for the multi-agent workflow; use tool discovery for subagent/spawn capabilities if available. If unavailable or policy blocks spawning, simulate independent agent memos sequentially and label them clearly as simulated tracks.
- Browser or Chrome plugin: optional for authenticated/profile-dependent pages, visual inspection, or manual page workflows; use only when exposed and needed.
- Automation/reminder tool: optional for recurring monitors; use it only when the user asks to watch, monitor, remind, or follow up.
- Skill installer: optional setup support for installing this skill or companion skills from a GitHub repo; after installing a skill, tell the user to restart Codex.

No other Codex skill is mandatory by default. If the user asks for an output that maps to another installed skill, explicitly name and invoke it before work begins, for example `spreadsheets:Spreadsheets` for workbook/Google Sheets output, `presentations:Presentations` for PPTX/decks, `documents:documents` for DOCX, or `market-analysis-orchestrator` for broad multi-asset context. If an optional companion skill or plugin is missing, say it is optional and help install it only when the user wants that output or explicitly asks for installation.

Check tool availability:

- Browse the web for current prices, latest announcements, news, analyst reports, and any data likely to have changed.
- If a dedicated financial-service/finance tool is exposed, use it for quote verification.
- If subagent tools are available and the user explicitly requested multi-agent work or explicitly invoked this skill for the multi-agent workflow, use subagents. If policy or tools prevent subagents, simulate independent agent memos sequentially and label them as such.

### 3. Collect Fresh Source Data

Use at least one primary source and one verification source when feasible.

For A-shares:

- Prefer official filings from CNINFO/SSE/SZSE for annual reports, quarterly reports, equity issuance, dividends, risk warnings, and governance events.
- Use local AkShare/Qlib for daily OHLCV if available.
- If an Eastmoney endpoint fails, try `ak.stock_zh_a_daily(symbol="sh600353", ...)`, `stock_zh_a_hist_tx`, Sina/Tencent/Yahoo/Investing, or official exchange pages.
- Record fallback/cache behavior.

For HK/US/global equities:

- Use finance/quote tools where exposed, official filings, exchange/company investor relations, and reputable market-data pages.

Collect these minimum facts:

- Latest close/current quote, market cap, volume/turnover, date.
- 6-12 months daily OHLCV; longer if available.
- Latest annual report and latest quarter.
- Recent announcements, news, regulatory events, major shareholder changes, dividends, financing, M&A, litigation, inquiry letters, risk warnings.
- Industry/topic catalysts and comparable companies.

### 4. Dispatch Independent Dimensions

Use four independent analysis tracks. When using subagents, keep prompts self-contained and ask each agent to return facts, inference, sources, and cross-check questions.

1. **Sentiment / News / Announcements**
   - Latest announcements, media narratives, forums/股吧 as low-confidence sentiment, regulatory inquiry, litigation, M&A, financing, dividends, insider/shareholder activity.
   - Output bullish, bearish, neutral events with strength, duration, credibility.

2. **Fundamentals / Financial Quality**
   - Business segments, revenue, gross margin, net profit, adjusted/扣非 profit, ROE, cash flow, debt ratio, R&D, accounts receivable, inventory, segment mix.
   - Highlight recurring vs non-recurring profit and working-capital pressure.

3. **K-line / Technicals / Trading Structure**
   - Calculate MA5/10/20/60/120/250, returns over 5/20/60/120/250 days, RSI14, MACD, 20/60/120/250-day annualized volatility, recent high/low, support/resistance, volume and turnover.
   - Identify whether price action is trend confirmation, high-volatility distribution, breakout, failed breakout, or range-bound.

4. **Valuation / Comparables / Risk**
   - Compute market cap, PE TTM/static, PB, PS, dividend yield, and compare with logical peer groups.
   - Assess theme premium, liquidity, financing, pledge/lockup/restriction, dilution, governance, delisting/regulatory risk.

### 5. Force Agent Interaction

After first-pass memos, make the dimensions interact:

- Give each track the other tracks' key conclusions.
- Ask each track to identify conflicts, over-optimism, over-pessimism, missing facts, and what would change its view.
- Preserve disagreements in the final report instead of smoothing them away.

At minimum, reconcile:

- Whether sentiment is backed by disclosed revenue/orders.
- Whether technical strength is trend quality or crowded theme trading.
- Whether valuation is supported by current financials or by future optionality.
- Whether fundamentals show recurring improvement or one-off gains.

### 6. Produce the Report

Save a Markdown report when the user asks for a full analysis or when the work is substantial. In a workspace, use:

```text
reports/<ticker>/<ticker>_<company>_review_<YYYY-MM-DD>.md
```

Include:

1. Core conclusion, confidence, data timestamp.
2. Multi-agent method table and interaction summary.
3. Data source and freshness table.
4. Key metrics table.
5. Sentiment/news analysis.
6. Fundamentals analysis.
7. K-line/technical analysis, with chart if generated.
8. Valuation and peer comparison.
9. Bull/base/bear scenarios with invalidation points.
10. Risk checklist.
11. Follow-up monitoring list.
12. Source links.

For visual output, generate a simple daily trend chart when local OHLCV exists. Use `matplotlib`; save under the same report folder and embed with an absolute path.

### 7. Answer Buy/Sell Timing Questions

When the user asks "can I buy next Monday?" or similar:

- Browse/check latest post-report news first.
- Give a clear operational stance such as "do not chase at open", "wait for pullback confirmation", or "only small trial position after breakout confirmation" when supported.
- Tie the stance to concrete levels, catalysts, valuation, and risk.
- State exact invalidation points and what data would change the view.
- Avoid pretending certainty; avoid personalized suitability unless the user supplied portfolio/risk context.

### 8. Cleanup

If subagents were spawned, close them after their outputs have been integrated. Mention any failed data source, fallback, missing package, or unverified claim in the final answer.
