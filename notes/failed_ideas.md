# Failed Ideas

## Pure IV Smile Trading

### Idea

Use Black-Scholes to compute implied volatility for the VEV options, then trade based on the fitted IV smile.

### Result

The idea did not directly produce stable PnL.

### Why It Failed

The IV curve alone was not enough. We also needed a better understanding of the underlying movement, option liquidity, and practical execution.

## Round 3 VELVET Mean Reversion

### Idea

Use EMA-based mean reversion on `VELVETFRUIT_EXTRACT`.

### Result

The early version failed.

### Why It Failed

The EMA parameter was poorly tuned. After adjusting the horizon in Round 4, the same broad idea worked much better.

## Naive Correlation Trading

### Idea

If two products had high correlation, trade them as a pair.

### Result

This produced some candidate ideas, but was risky.

### Why It Was Risky

High correlation did not always imply a stable lead-lag or arbitrage relationship. Some relationships could be temporary or overfit to the sample.
