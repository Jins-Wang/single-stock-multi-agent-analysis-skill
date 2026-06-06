# Agent Roles

Use these roles for an already-screened single stock. Agents should work independently first, then challenge each other before the final committee view.

| Agent | Primary Question | Core Output |
| --- | --- | --- |
| Data Steward | Is the data fresh, sourced, internally consistent, and complete enough? | Source table, missing data, stale data flags, evidence grade caps. |
| News & Catalyst | What could change investor expectations over the next 1-8 weeks? | Bullish/bearish catalysts, event timing, credibility, duration. |
| Industry & Macro | Is the sector, macro, policy, rate, currency, or commodity backdrop helping? | Sector trend, macro sensitivity, peer context, policy exposure. |
| Business & Moat | Is the business quality durable enough to support the thesis? | Revenue model, moat, customer/supplier power, competitive position. |
| Financial Quality | Are growth, margins, cash flow, balance sheet, and accounting quality improving? | Quality of earnings, cash conversion, leverage, working capital, surprises. |
| Valuation | Is the risk/reward attractive versus history, peers, and scenarios? | Multiples, DCF or sum-of-parts notes when feasible, upside/downside ranges. |
| Technical & Trading | Is the 1-8 week price/volume setup favorable? | Trend state, support/resistance, momentum, volatility, entry/exit levels. |
| Flow & Positioning | Is the stock crowded, neglected, accumulated, or under distribution? | Turnover, fund/ETF flow clues, short interest if available, ownership changes. |
| Risk Officer | What can break the thesis and how severe is it? | Risk register, probability/impact, kill switches, position cap guidance. |
| Portfolio/Trade Planner | How should the conclusion become an executable plan? | Entry zone, add/reduce triggers, stop loss, take profit, sizing, monitoring. |

## Agent Memo Contract

Each agent returns this compact structure:

```json
{
  "agent": "technical_trading",
  "stance": "bullish|neutral|bearish|mixed",
  "score": 1.0,
  "confidence": 0.72,
  "evidence_grade": "B",
  "horizon": "1-8 weeks",
  "key_findings": ["..."],
  "positives": ["..."],
  "negatives": ["..."],
  "what_would_change_view": ["..."],
  "kill_switch": "...",
  "sources": [{"title": "...", "url": "...", "as_of": "..."}]
}
```

Score scale:

- `+2`: strong positive.
- `+1`: positive.
- `0`: neutral or insufficient edge.
- `-1`: negative.
- `-2`: strong negative.

Confidence is `0.00` to `1.00`. Evidence grade is `A`, `B`, `C`, or `D` as defined in `source_quality.md`.
