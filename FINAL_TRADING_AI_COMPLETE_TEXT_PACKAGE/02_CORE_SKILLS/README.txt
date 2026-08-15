# Professional Quant Research Skill Pack

A modular skill library for AI agents performing systematic trading research.

## Design goals

- Evidence-first research
- Reproducibility
- Point-in-time data discipline
- Realistic backtesting
- Multiple-testing awareness
- Anti-overfitting
- Anti-over-filtering
- Independent risk controls
- Execution-state verification
- Self-auditing
- Continuous improvement without post-hoc rule mining

## Recommended loading order

Core:
`01` → `02` → `03` → `04` → `05` → `06` → `07` → `08`

When coding:
`14`

When ML is proposed:
`09`

When execution is proposed:
`10` + `11`

For every research program:
`12` + `13` + `15`

## Important architecture rule

These are skills, not a giant checklist. An agent should load the smallest relevant set, combine them when necessary, and avoid redundant work.

## Research standard

The pack explicitly accounts for the fact that extensive strategy searching can inflate historical performance through selection bias and backtest overfitting. The research ledger is therefore a first-class component. See the cited literature in the relevant skill files.

No skill guarantees profitable trading.
