# Lean Trader

Automated systematic trading strategy development system. **Runs 24/7 without human intervention.**

## Architecture

```
                    ┌─────────────────┐
                    │   ORCHESTRATOR   │
                    │   (orchestrator.py) │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ RESEARCH      │   │ GENERATE      │   │ BACKTEST      │
│ (data fetch)  │   │ (strategy gen)│   │ (simulated)  │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ binance_data  │   │ Lean Python   │   │ evaluate_     │
│ yfinance_data │   │ strategies    │   │ backtest.py   │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                    ┌───────────────┐
                    │ COMMIT+PUSH   │
                    │ GitHub        │
                    └───────────────┘
```

## Workflow (24/7 Loop)

1. **Research** - Fetch market data from Binance, Yahoo Finance
2. **Generate** - Create new trading strategies with random parameters
3. **Backtest** - Simulate results (real backtests require QuantConnect credentials)
4. **Evaluate** - Score using backtest-expert methodology
5. **Push** - Commit all changes to GitHub

## Project Structure

```
lean-trader/
├── orchestrator.py      # Main 24/7 loop
├── strateg/            # Generated strategies
│   ├── RSI_Momentum_20260401_120000.py
│   └── ...
├── backtests/          # Backtest results
│   └── *_backtest.json
├── reports/           # Evaluation reports
│   └── *_eval.json
├── research/          # Data fetching scripts
│   ├── binance_data.py
│   └── yfinance_data.py
├── data/              # Market data CSVs
├── logs/              # Orchestrator logs
│   └── orchestrator.log
└── skills/            # Trading skills
    ├── backtest-expert/
    ├── technical-analyst/
    └── ...
```

## Running

### Start Orchestrator (24/7)

```bash
cd ~/lean-trader
python3 orchestrator.py
```

### Manual Commands

```bash
# Fetch market data
python3 research/binance_data.py BTCUSDT 365
python3 research/yfinance_data.py SPY 2020-01-01

# Run backtest evaluation
python3 ~/.hermes/skills/trading/systematic-trading/scripts/evaluate_backtest.py \
    --total-trades 150 --win-rate 62 --avg-win-pct 1.8 \
    --avg-loss-pct 1.2 --max-drawdown-pct 15 --years-tested 8 \
    --num-parameters 3 --slippage-tested --output-dir reports/

# Git operations
git status
git log --oneline -10
```

## Strategies Generated

The orchestrator generates strategies based on these templates:

| Type | Entry Condition | Stop | Take |
|------|----------------|------|------|
| RSI_Momentum | RSI<30 + price>SMA200 | 3% | 6% |
| MACD_Cross | MACD>Signal | 2% | 4% |
| BB_Bounce | Price at lower BB + RSI<35 | 2.5% | 5% |
| Volume_Surge | Volume>2xSMA + price up | 2% | 4% |
| EMA_Cross | EMA9>EMA21 | 2% | 4% |

## Evaluation Criteria

Strategies are evaluated on 5 dimensions:

1. **Sample Size** - 200+ trades = high confidence
2. **Expectancy** - Profit Factor >1.5 = good
3. **Risk Management** - Drawdown <15% = acceptable
4. **Robustness** - Works across 10+ years = stable
5. **Execution Realism** - Win rate <80% = realistic

## Verdict System

- **DEPLOY** (score 0.86+) - Ready for paper/live trading
- **REFINE** (score 0.60) - Core logic sound, needs tuning
- **ABANDON** (score 0.30) - Fails critical tests

## Next Steps

To enable **real backtests** with QuantConnect Lean:

1. Create account at https://quantconnect.com/account
2. Get API credentials
3. Run `lean init` in project directory
4. Enter credentials when prompted

## GitHub

https://github.com/MetalDoradoCrypto/lean-trader

## Skills Used

- `backtest-expert` - Rigorous backtesting methodology
- `trade-hypothesis-ideator` - Generate hypotheses
- `technical-analyst` - Chart pattern analysis
- `edge-strategy-reviewer` - Strategy quality gate
- `systematic-trading` - Main workflow skill
