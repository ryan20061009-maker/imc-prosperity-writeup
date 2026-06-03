# IMC Prosperity 4 Strategy Writeup

## 1. Competition Result

Our team achieved **Global Rank 31** in IMC Prosperity 4.

This writeup summarizes our strategy design process, implementation choices, visual analysis, manual challenge reasoning, and lessons learned.

## 2. Overall Approach

Our workflow was to first inspect each product visually, then build simple strategies around the most obvious market structure.

For each product, we usually asked:

- Is there a stable fair value?
- Is there a strong drift?
- Is the spread wide enough for market making?
- Is there a relation with another product?
- Does the order book contain obvious abnormal behavior?
- How can we control inventory under the position limit?

A repeated lesson was that simple but robust strategies were often more useful than complicated ideas that were difficult to validate.

## 3. Algorithm Challenge

### Round 1 / Round 2: ASH and ROOT

Round 1 and Round 2 introduced two main products: `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.

At a high level, `INTARIAN_PEPPER_ROOT` behaved like a product with strong directional movement, while `ASH_COATED_OSMIUM` was more suitable for order-book-based trading and market making.

For details, see:

```text
analysis/round1_2.md
```

### Round 3 / Round 4: HYDROGEL_PACK, VELVETFRUIT_EXTRACT, and VEV Options

Round 3 and Round 4 introduced a more complex setting with `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and options related to `VELVETFRUIT_EXTRACT`.

Our initial attempt was to analyze options through Black-Scholes implied volatility, but the IV smile did not directly give us a profitable strategy. We then shifted toward empirical relationships, especially the relation between `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`, and later improved the strategy through medium-term mean reversion.

For details, see:

```text
analysis/round3_4.md
```

### Round 5: Many Products

Round 5 introduced a large universe of products, making it impossible to manually study every product deeply in the limited time.

Our approach was to quickly screen products locally, keep strategies that were profitable under simple market making, and focus research time on the remaining products. We also looked for cross-product correlation and abnormal price behavior.

For details, see:

```text
analysis/round5.md
```

## 4. Manual Challenge

The manual challenges required a different style of reasoning from the algorithmic rounds. Instead of writing a trading bot, we had to model the game, infer other participants' behavior, and sometimes balance expected value against risk.

For details, see:

```text
analysis/manual_challenges.md
```

## 5. Key Lessons

1. Visual inspection was extremely useful for quickly understanding market structure.
2. A good trading idea still needs execution and inventory control.
3. Option pricing intuition was useful, but a clean theoretical model did not immediately translate into PnL.
4. Empirical lead-lag relationships could be useful, but they were easy to overfit.
5. In the final round, speed of analysis mattered as much as depth.
6. Manual challenges were partly mathematical modeling and partly player-behavior prediction.

## 6. Future Improvements

If I were to redo the competition, I would improve:

- the local backtesting framework,
- product-specific visualization scripts,
- automatic parameter search,
- more robust inventory-aware order sizing,
- better distinction between stable signals and overfitted correlations,
- more systematic manual challenge simulations.
