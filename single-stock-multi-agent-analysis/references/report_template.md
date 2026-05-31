# Report Template

Use this structure for a full single-stock report.

```markdown
# <Ticker> <Company> Multi-Agent Review

As of: <timestamp and timezone>
Market: <market>
Horizon: <1-8 weeks unless user specifies otherwise>

## 1. Committee Conclusion

- Rating: <Strong Buy | Buy | Watch | Avoid | Sell Risk>
- Weighted score: <-2.000 to +2.000>
- Confidence: <0.00 to 1.00>
- Core thesis:
- Main risk:
- Data limitations:

## 2. Capability and Source Disclosure

| Capability or Source | Required | Available | Missing | Fallback | Install or Action |
| --- | --- | --- | --- | --- | --- |

## 3. Scorecard

| Agent | Score | Confidence | Evidence | Stance | Key Reason | Kill Switch |
| --- | ---: | ---: | --- | --- | --- | --- |

## 4. Agent Memos

### Data Steward
### News & Catalyst
### Industry & Macro
### Business & Moat
### Financial Quality
### Valuation
### Technical & Trading
### Flow & Positioning
### Risk Officer
### Portfolio/Trade Planner

## 5. Debate and Reconciliation

- Conflicts:
- What changed after challenge:
- Points of unresolved disagreement:
- Facts needed before upgrading/downgrading:

## 6. Trade Plan

| Field | Plan |
| --- | --- |
| Entry zone | |
| Add trigger | |
| Reduce trigger | |
| Stop loss | |
| Take profit | |
| Invalidation | |
| Position sizing | |
| Monitoring plan | |

## 7. Scenario Table

| Scenario | Probability | Price/Return Path | Evidence | Trigger | Action |
| --- | ---: | --- | --- | --- | --- |
| Bull | | | | | |
| Base | | | | | |
| Bear | | | | | |

## 8. Risk Register

| Risk | Probability | Impact | Monitoring Signal | Action If Triggered |
| --- | ---: | ---: | --- | --- |

## 9. Follow-Up Checklist

- ...

## 10. Sources

- ...
```

Rating guide:

- `Strong Buy`: weighted score >= `1.10` and risk kill switches are not active.
- `Buy`: weighted score >= `0.45`.
- `Watch`: weighted score > `-0.25`, or the setup is promising but evidence/confidence is not enough.
- `Avoid`: weighted score > `-0.90` with unfavorable timing or risk/reward.
- `Sell Risk`: weighted score <= `-0.90`, or a critical risk/kill switch is active.
