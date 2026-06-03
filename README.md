# IMC Prosperity 4 Postmortem

Our team achieved **Global Rank 31** in **IMC Prosperity 4**.

This repository is a compact writeup of our algorithmic and manual trading strategies.

---

## Structure

```text
.
├── README.md
├── final_submission.py
└── figures/
```

---

## Tools

### Local backtesting

We used local backtests to compare parameter choices and discard clearly bad ideas.  
The most useful checks were PnL stability, position usage, and whether a strategy depended on a few lucky trades.

### Plotting scripts

For each new product, we first plotted prices, moving averages, correlations, and lagged correlations.  
Most of our final ideas came from visual inspection before coding the actual strategy.

### Prosperity visualizer

The visualizer was useful for reading order book structure and checking bot trades.

![Prosperity visualizer example](figures/visualizer_robot_ironing.png)

![Bid / ask / mid visualization](figures/visualizer_bid_ask_mid.png)

---

# Algorithm Challenge

## Round 1 / Round 2: ASH and ROOT

Products:

- `INTARIAN_PEPPER_ROOT`
- `ASH_COATED_OSMIUM`

### INTARIAN_PEPPER_ROOT

`INTARIAN_PEPPER_ROOT` showed a very strong upward drift.

**Final strategy:** buy to the position limit at the beginning and hold.

The only nontrivial part was execution. Buying the full position too aggressively could sweep multiple ask levels, so we still had to account for slippage.

![INTARIAN_PEPPER_ROOT trend](figures/round1_root_trend.png)

### ASH_COATED_OSMIUM

`ASH_COATED_OSMIUM` had a large spread, so it was suitable for market making.

**Baseline strategy:** quote inside the spread.

```text
bid = best_bid + 1
ask = best_ask - 1
```

![ASH_COATED_OSMIUM spread](figures/round1_ash_spread.png)

The key extra observation was that one side of the order book sometimes disappeared.  
When this happened, we placed more aggressive quotes to exploit the temporary lack of liquidity.

![ASH order book disappearing](figures/round1_ash_orderbook_disappear.png)

---

## Round 3 / Round 4: HYDROGEL, VELVET, and Options

Products:

- `VELVETFRUIT_EXTRACT`
- `HYDROGEL_PACK`
- VELVET options

### Initial option attempt

Options were introduced in this round. Our first idea was to compute implied volatility with Black-Scholes and look for a volatility smile.

This did not work well. The fitted IV curve was not stable enough to produce a reliable trading rule.

![Initial IV smile attempt](figures/options_iv_smile_attempt.png)

In Round 3, we had no strong option strategy, so we mostly used passive quoting. The result was weak.

### VELVETFRUIT_EXTRACT

After inspecting the data, we found that a longer-horizon mean-reversion strategy worked better than our early short-EMA version.

The Round 3 mean-reversion attempt failed mostly because the EMA parameters were poorly chosen. After tuning the horizon, the strategy improved significantly.

![VELVETFRUIT_EXTRACT macro view](figures/round34_velvet_macro_inventory.png)

We also noticed that the market seemed to contain a double-layer market maker plus noisier retail-like orders.  
For fair value estimation, filtering out the noisy outer orders worked better than directly using the raw best bid / best ask.

### Options

In Round 4, we stopped treating the options as pure volatility products. Most options moved almost like leveraged versions of the underlying `VELVETFRUIT_EXTRACT`.

**Final idea:** first trade VELVET correctly, then use selected options as leveraged exposure to the same signal.

### HYDROGEL_PACK

We did not find a very strong standalone signal for `HYDROGEL_PACK`.

**Final strategy:** market making plus EMA mean reversion.

---

## Round 5: Large Product Universe

Round 5 had many products, so the main problem was prioritization.

![Round 5 product overview](figures/round5_product_overview.png)

### Fast filtering

We first tested simple market making on all products.  
If a product was already profitable with market making, we kept it simple and moved on.

### Correlation and lag search

For the remaining products, we searched for correlated pairs and lead-lag relationships.

**Strategy:** buy the relatively cheap product and sell the relatively expensive related product.

For some pairs, a lagged correlation was stronger than the same-time correlation, so we used the leading product to predict the lagging one.

![Lag correlation analysis](figures/round5_lag_correlation.png)

### Abnormal straight-line products

Some products occasionally entered a special state where the price became almost a straight line and jumped by around 100 each time.

We added special-case code to detect and trade this regime separately instead of applying the normal market-making logic.

![Abnormal straight-line price behavior](figures/round5_abnormal_price_jump.png)

---

# Manual Challenge

## Round 1: Walrasian Auction

### Rules

The first manual challenge was a sealed opening auction for two products:

- `DRYLAND_FLAX`
- `EMBER_MUSHROOM`

For each product, we submitted one limit order with a price and quantity.  
After all orders were submitted, the exchange chose a single clearing price that maximized traded volume. If multiple prices produced the same maximum volume, the higher price was chosen.

After the auction, inventory was settled at fixed merchant prices:

```text
DRYLAND_FLAX     settlement price = 30
EMBER_MUSHROOM   settlement price = 20, with 0.10 fee per unit traded
```

### Solver

The brute force is straightforward. For every possible submitted price and quantity, simulate the auction, compute the clearing price, compute our filled quantity, and then compute settlement PnL.

The scoring function used in the solver was:

```text
PnL = filled_quantity * (settlement_price - clearing_price - fee)
```

where `fee = 0` for `DRYLAND_FLAX` and `fee = 0.10` for `EMBER_MUSHROOM`.

### Brute-force skeleton

```python
def clearing_price_after_order(book_buys, book_sells, my_side, my_price, my_qty):
    buys = book_buys.copy()
    sells = book_sells.copy()

    if my_side == "BUY":
        buys.append((my_price, my_qty, "ME"))
    else:
        sells.append((my_price, my_qty, "ME"))

    candidate_prices = sorted(set(p for p, _, _ in buys + sells))
    best_price = None
    best_volume = -1

    for p in candidate_prices:
        demand = sum(q for price, q, _ in buys if price >= p)
        supply = sum(q for price, q, _ in sells if price <= p)
        volume = min(demand, supply)

        # tie-break: higher clearing price
        if volume > best_volume or (volume == best_volume and (best_price is None or p > best_price)):
            best_volume = volume
            best_price = p

    return best_price, best_volume


def eval_order(book_buys, book_sells, side, price, qty, settlement, fee=0.0):
    clearing, total_volume = clearing_price_after_order(book_buys, book_sells, side, price, qty)

    # Writeup-level simplification:
    # the final solver also handles price-time priority for partial fills at the clearing price.
    if side == "BUY":
        filled = qty if price >= clearing else 0
        pnl = filled * (settlement - clearing - fee)
    else:
        filled = qty if price <= clearing else 0
        pnl = filled * (clearing - settlement - fee)

    return pnl, clearing, filled


def brute_force(book_buys, book_sells, side, prices, quantities, settlement, fee=0.0):
    best = None

    for price in prices:
        for qty in quantities:
            pnl, clearing, filled = eval_order(
                book_buys, book_sells, side, price, qty, settlement, fee
            )
            candidate = (pnl, price, qty, clearing, filled)
            if best is None or candidate[0] > best[0]:
                best = candidate

    return best
```

We used this to brute-force the two auctions and then cross-checked the answer by manually inspecting the order book.

---

## Round 2: Invest & Expand

### Rules

Round 2 was an allocation problem with a fixed budget of `50,000` XIRECs.  
We had to allocate percentages to three components:

```text
Research + Scale + Speed <= 100
```

The payoff model was:

```text
net_pnl = research_value * scale_value * speed_multiplier - budget_used
```

with

```text
research_value(x) = 200000 * ln(1 + x) / ln(101)
scale_value(x)    = 7 * x / 100
budget_used       = 50000 * (research + scale + speed) / 100
```

`Speed` was the game-theoretic part. It did not directly enter as a smooth function; instead, it determined a rank-based multiplier. Higher speed gave a better multiplier, but if many teams chose the same speed, the tie rule changed the effective payoff.

### Optimizing Research and Scale for fixed Speed

For a fixed speed allocation `v`, the remaining budget is

```text
B = 100 - v
```

We use the full remaining budget between Research and Scale because both increase gross PnL and the budget penalty is already linear.

So:

```text
scale = B - research
```

For a fixed speed multiplier `m`, the optimization becomes:

```text
maximize:
    200000 * ln(1 + r) / ln(101) * 7 * (B - r) / 100 * m
    - 50000 * (r + (B-r) + v) / 100
```

Since `r + (B-r) + v = 100`, the budget cost is constant after fixing speed and using the whole budget.

So we only need to maximize:

```text
f(r) = ln(1 + r) * (B - r)
```

The first-order condition is:

```text
(B - r) / (1 + r) = ln(1 + r)
```

This gives a unique optimum for Research, and then Scale is determined by:

```text
scale = B - research
```

### Example: if Speed = 1

If we choose:

```text
speed = 1
```

then:

```text
B = 99
```

Solving

```text
(99 - r) / (1 + r) = ln(1 + r)
```

gives approximately:

```text
research ≈ 22.95
scale    ≈ 76.05
speed    = 1
```

This is why, once speed was chosen, the other two parameters were essentially determined by a one-dimensional optimization.

### Code used for the one-dimensional search

```python
import math

def research_value(x):
    return 200000 * math.log(1 + x) / math.log(101)

def scale_value(x):
    return 7 * x / 100

def net_pnl(research, scale, speed, speed_multiplier):
    budget_used = 50000 * (research + scale + speed) / 100
    gross = research_value(research) * scale_value(scale) * speed_multiplier
    return gross - budget_used

def optimize_research_scale(speed, speed_multiplier=0.5, step=0.01):
    B = 100 - speed
    best = None

    n = int(B / step)
    for i in range(n + 1):
        research = i * step
        scale = B - research
        pnl = net_pnl(research, scale, speed, speed_multiplier)
        candidate = (pnl, research, scale, speed)
        if best is None or candidate[0] > best[0]:
            best = candidate

    return best

print(optimize_research_scale(speed=1, speed_multiplier=0.5))
```

### Speed decision

The actual hard part was choosing `Speed`.

If everyone chose `0`, the tie rule could make `0` a Nash-like equilibrium.  
However, we expected many teams to think that choosing `1` would slightly beat the crowd choosing `0`. If too many teams did this, then choosing `0` could lose its advantage.

Our final choice was therefore:

```text
speed = 1
research ≈ 23
scale ≈ 76
```

The exact Research / Scale values were rounded for submission.

---

## Round 3: Choosing a Bid

### Rules

We modeled this round as choosing a bid `p` while the payout also depended on the market-wide average `T`.

The simplified structure was:

- choose a bid `p`;
- profit increases when the bid captures more counterparties;
- bidding too high reduces per-unit margin;
- being below the average `T` creates a nonlinear penalty.

The payoff had the same qualitative shape as:

```text
profit(p, T) = base_profit(p) * penalty(p, T)
```

where the penalty was asymmetric: being too low relative to the average was worse than being slightly high.

### Our model

Ignoring the population effect, the best bid was around `33`.

The real problem was estimating the distribution of the average `T`.  
We tried to approximate player behavior with a normal distribution and computed expected profit under that assumption.

![Manual Round 3 EV curve](figures/manual_round3_ev_curve.png)

We used a model close to:

```text
T ~ Normal(41.5, 3^2)
```

Under this belief, the expected-value peak moved upward, so we chose around `39`.

The realized optimum seemed closer to `34` or `35`, meaning the player pool was less aggressive than our model expected.

---

## Round 4: Options Portfolio Optimization

### Rules

Round 4 was a portfolio construction problem. We could trade the underlying asset, vanilla calls and puts, and exotic options.

The score was based on average PnL across simulated paths of the underlying.  
The key instruments included:

- underlying asset,
- vanilla calls,
- vanilla puts,
- chooser option,
- binary put,
- knock-out put.

The underlying followed a high-volatility geometric Brownian motion model, so the problem was not just expected value. Tail risk mattered because the final score used a finite number of simulated paths.

### Payoff model

For vanilla options:

```text
call payoff = max(S_T - K, 0)
put payoff  = max(K - S_T, 0)
```

For the chooser option:

```text
if S_tau > 50:
    payoff = max(S_T - 50, 0)
else:
    payoff = max(50 - S_T, 0)
```

For the binary put:

```text
payoff = 10 if S_T < 40 else 0
```

For the knock-out put:

```text
payoff = max(45 - S_T, 0) only if the path never goes below 35
```

### Our approach

Our first approach was to maximize expected value directly.  
This produced a very risky portfolio and performed badly.

The better approach would have been:

1. simulate many paths,
2. compute each product's payoff on each path,
3. search over position vectors,
4. rank portfolios by both mean PnL and tail-risk metrics.

A risk-aware scoring function could look like:

```text
score = mean_pnl + 0.05 * p05 + 0.01 * p01 - 0.10 * std - 0.05 * cvar_5
```

Our actual submission was too EV-focused, which led to a large loss.

---

## Round 5: News-Based Portfolio

### Rules

The final manual round was a one-day portfolio allocation problem.  
We could buy or sell nine goods based on news, with a total gross allocation limit of `100%`.

The main constraint was the convex fee:

```text
fee_i = (abs(q_i) / 100)^2 * 1,000,000
```

where `q_i` is the percentage allocation to product `i`.

The total allocation constraint was:

```text
sum(abs(q_i)) <= 100
```

### Our approach

We converted each news story into a directional score, then allocated more weight to higher-conviction ideas.

Our submitted portfolio was:

![Manual Round 5 result](figures/manual_round5_result.png)

The important fee observation is that concentration is expensive.  
A single `100%` position pays:

```text
1,000,000
```

in fees, while splitting exposure across independent views can reduce the total fee.

For example, an equal split across `n` active products has total fee:

```text
n * (100 / n / 100)^2 * 1,000,000
= 1,000,000 / n
```

So if the signals are comparable, diversification is strongly favored by the fee structure.

---

# Summary

Main profitable ideas:

- ROOT: buy and hold the strong upward drift.
- ASH: market make inside the wide spread and exploit missing order-book sides.
- VELVET: longer-horizon mean reversion.
- Options: use selected options as leveraged exposure to VELVET.
- Round 5: combine quick market-making filters, correlation search, lag search, and special regime handling.

Main mistakes:

- Trying to force unstable IV-smile analysis in Round 3.
- Poor EMA parameter choice in early VELVET experiments.
- Trusting correlation too quickly in Round 5.
- Ignoring risk in Manual Round 4.
