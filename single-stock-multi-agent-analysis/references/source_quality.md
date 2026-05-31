# Source Quality

Always separate verified facts from inference. Prefer recent primary sources for time-sensitive conclusions.

## Evidence Grades

| Grade | Meaning | Examples |
| --- | --- | --- |
| A | Primary, current, and directly relevant. | Official filings, exchange announcements, company IR releases, audited reports, current quote from a reliable market-data source. |
| B | Reputable secondary source or clean derived calculation from primary/market data. | Major financial media, broker summaries with disclosed assumptions, calculated indicators from verified OHLCV. |
| C | Useful but indirect, stale, incomplete, or partially corroborated. | News aggregators, unsourced consensus pages, older industry data, forum sentiment corroborated by price/volume only. |
| D | Weak, anecdotal, unverifiable, or stale. | Rumors, isolated social posts, unverified screenshots, stale data without timestamp. |

## Confidence Caps

Apply these caps unless stronger evidence is found:

- If no current price or recent filing/announcement source is available: final confidence <= `0.60`.
- If the thesis depends on rumors or forum sentiment: related agent confidence <= `0.45`.
- If financials are older than the latest required reporting period: Financial Quality confidence <= `0.55`.
- If OHLCV history is shorter than 60 trading days for a 1-8 week setup: Technical & Trading confidence <= `0.60`.
- If valuation uses only one comparable or one multiple: Valuation confidence <= `0.60`.

## Source Table Minimum

Every full report should include:

| Source | Type | As Of | What It Supports | Evidence Grade | Limitation |
| --- | --- | --- | --- | --- | --- |
| Company filing | Primary | YYYY-MM-DD | Revenue, earnings, risk disclosures | A | ... |
| Market data source | Market data | YYYY-MM-DD HH:MM TZ | Price, volume, indicators | A/B | ... |
| News source | Secondary | YYYY-MM-DD | Catalyst context | B/C | ... |
