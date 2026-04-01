# CLAUDE.md - QuantConnect Lean Trading System

## Purpose
This file defines the conventions for building systematic trading strategies with QuantConnect Lean.

## Project Structure
```
lean-trader/
├── strateg/           # Trading strategies
├── research/          # Data fetching and analysis
├── backtests/         # Backtest results
├── reports/           # Evaluation reports
├── skills/            # Trading skills
│   ├── backtest-expert/
│   ├── edge-strategy-reviewer/
│   ├── trade-hypothesis-ideator/
│   └── technical-analyst/
└── logs/              # Execution logs
```

## Development Philosophy

### Core Principle
**"Find strategies that break the least, not profit the most"**

- 20% generating ideas
- 80% trying to break them
- Add friction everywhere
- Seek plateaus, not peaks

### Strategy Development Workflow

1. **HYPOTHESIS** - State the edge in ONE sentence
2. **CODIFY** - Define rules with zero discretion
   - Entry conditions (exact, timing, price type)
   - Exit conditions (stop loss %, take profit %, time-based)
   - Position sizing (% of portfolio, volatility-adjusted)
   - Filters (volume minimum, volatility conditions)
   - Universe (what instruments are eligible)
3. **BACKTEST IN-SAMPLE** - 5+ years, multiple regimes
4. **STRESS TEST** - Parameter sensitivity, friction, time
5. **OUT-OF-SAMPLE VALIDATION** - Walk-forward analysis
6. **EVALUATE** - Deploy / Refine / Abandon

## Backtest Standards

When writing strategies:
- Always include clear `Initialize()` with symbol, resolution, cash
- Provide one-paragraph explanation before code
- Implement proper risk management:
  - Position sizing
  - Stop loss
  - Maximum drawdown limits
- Use realistic costs (commissions + slippage)

## Code Style
- Follow PEP8
- Add docstrings to all functions
- Use meaningful variable names
- Comment complex logic

## Metrics to Track
| Metric | Good | Bad |
|--------|------|-----|
| Profit Factor | >1.5 | <1.2 |
| Win Rate | >55% | <50% |
| Max Drawdown | <15% | >30% |
| Sharpe Ratio | >1.5 | <1.0 |
| Total Trades | 200+ | <30 |

## Key Reminders
- Small edges require large samples to prove
- If results look "too good to be true", audit for bias
- Strategy must work in multiple market regimes
- Never optimize on out-of-sample data
