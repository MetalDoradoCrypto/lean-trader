# lean-trader

Automated systematic trading with QuantConnect Lean - AI-generated strategies, backtesting, and iteration.

## Setup

1. Install Docker
2. Install Lean CLI: `pip install lean`
3. Run `lean init` with your QuantConnect credentials
4. Authenticate with GitHub: `gh auth login`

## Workflow

1. Write strategy → commit
2. Run backtest → `lean backtest`
3. Analyze results
4. Iterate and improve
5. Commit results

## Project Structure

- `strateg/` - Trading strategies
- `backtests/` - Backtest results
