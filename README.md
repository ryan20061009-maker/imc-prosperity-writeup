# IMC Prosperity Strategy Writeup

This repository documents our team's research process, tools, and algorithmic trading strategies for IMC Prosperity.

The goal of this writeup is not only to present the final trader, but also to record how we analyzed each product, tested hypotheses, built tools, and improved our strategy round by round.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Tools](#tools)
  - [Backtester](#backtester)
  - [Visualizer](#visualizer)
  - [Analysis Scripts](#analysis-scripts)
- [Algorithmic Challenge](#algorithmic-challenge)
  - [Tutorial: TOMATOES and EMERALDS](#tutorial-tomatoes-and-emeralds)
  - [Round 1: ASH and ROOT](#round-1-ash-and-root)
  - [Round 2: Improved ASH and ROOT](#round-2-improved-ash-and-root)
  - [Round 3: VELV and HYDRO](#round-3-velv-and-hydro)
  - [Round 4: Improved VELV and HYDRO](#round-4-improved-velv-and-hydro)
  - [Round 5: Mixed Universe](#round-5-mixed-universe)
- [Manual Challenge](#manual-challenge)
- [Final Architecture](#final-architecture)
- [Lessons Learned](#lessons-learned)
- [FAQ](#faq)

## Overview

IMC Prosperity is an algorithmic trading competition where teams submit a trading bot to trade fictional products in a simulated exchange.

Our approach was mainly data-driven:

1. Understand the product behavior.
2. Build tools to visualize order books and trades.
3. Form simple hypotheses.
4. Backtest the strategy.
5. Keep only robust ideas.
6. Merge product-specific strategies into one final trader.

## Product-Round Mapping

| Stage | Products | Main Focus |
|---|---|---|
| Tutorial | `TOMATOES`, `EMERALDS` | Basic market making and fair value trading |
| Round 1 | `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT` | Market making, mean reversion, order book analysis |
| Round 2 | `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT` | Improved ASH/ROOT strategy, bot behavior, thin-book attack |
| Round 3 | `VELVETFRUIT_EXTRACT`, `HYDROGEL_PACK` | VELV-HYDRO relationship, residual trading |
| Round 4 | `VELVETFRUIT_EXTRACT`, `HYDROGEL_PACK` | Improved VELV/HYDRO strategy, option-like products |
| Round 5 | Around 50 products | Product screening, cross-product signals, final merge |

## Repository Structure

```text
.
├── README.md
├── src/                  # Final and historical strategy code
├── tools/                # Backtester, visualizer, and analysis scripts
├── writeups/             # Round-by-round writeups
├── notebooks/            # Research notebooks
├── data/                 # Market data by round
├── results/              # Backtest outputs and plots
├── docs/                 # Extra notes and lessons
└── README_assets/        # Images used by the README
```

# Tools

Good tooling was one of the most important parts of the competition. Instead of only looking at final PnL, we tried to understand why each strategy made or lost money.

## Backtester

We used a local backtester to quickly test strategy changes before submitting.

The backtester helped us inspect:

- total PnL,
- per-product PnL,
- position over time,
- order limit violations,
- strategy behavior on different days.

Typical workflow:

```text
write strategy
→ run local backtest
→ inspect PnL and logs
→ adjust parameters
→ test out-of-sample
```

See [`tools/backtester`](tools/backtester).

## Visualizer

We used visualization tools to inspect market behavior.

Important plots included:

- mid price over time,
- best bid and best ask,
- spread,
- order book depth,
- trades by timestamp,
- position,
- PnL,
- custom signals.

This was especially useful for detecting:

- stable fair values,
- mean reversion,
- large liquidity walls,
- thin order books,
- bot trading patterns,
- lead-lag relationships.

See [`tools/visualizer`](tools/visualizer).

## Analysis Scripts

We wrote scripts to compute:

- mid price,
- wall mid,
- spread distribution,
- order book imbalance,
- EMA,
- rolling mean,
- future return,
- cross-product correlation,
- lagged correlation,
- residual signals.

See [`tools/analysis_scripts`](tools/analysis_scripts).

# Algorithmic Challenge

## Tutorial: TOMATOES and EMERALDS

### Products

- `TOMATOES`
- `EMERALDS`

### Main Idea

The tutorial round helped us build the basic trading framework.

For `EMERALDS`, the fair value was stable, so we used simple fair-value market making.

```python
FAIR_VALUE = 10000

if best_ask < FAIR_VALUE:
    buy

if best_bid > FAIR_VALUE:
    sell
```

For `TOMATOES`, we tested more dynamic fair value estimates such as recent average and EMA.

### Takeaway

The tutorial taught us the basic structure of a trader:

```text
read order book
→ estimate fair value
→ generate orders
→ respect position limit
→ save traderData
```

More details: [`writeups/tutorial.md`](writeups/tutorial.md)

---

## Round 1: ASH and ROOT

### Products

- `ASH_COATED_OSMIUM`
- `INTARIAN_PEPPER_ROOT`

### Initial Observations

In Round 1, we focused on understanding the two new products.

We analyzed:

- price stability,
- spread,
- order book depth,
- imbalance,
- trade patterns,
- possible bot behavior.

### ASH_COATED_OSMIUM

ASH was more suitable for market making and fair-value-based trading.

Strategies tested:

- passive market making,
- mean reversion,
- inventory-aware quoting,
- wall-mid estimation.

### INTARIAN_PEPPER_ROOT

ROOT was less stable and had more directional risk.

Strategies tested:

- price reversion,
- spread filter,
- imbalance signal,
- simple taker strategy.

### Final Strategy

TODO: Fill in final Round 1 ASH/ROOT logic.

### What Did Not Work

TODO: Record failed experiments.

More details: [`writeups/round1.md`](writeups/round1.md)

---

## Round 2: Improved ASH and ROOT

### Products

- `ASH_COATED_OSMIUM`
- `INTARIAN_PEPPER_ROOT`

### Main Improvement

Round 2 reused the same products, but we improved our strategy using more detailed order book analysis.

### Wall Mid

We used the idea of wall mid:

```python
wall_mid = (bid_wall_price + ask_wall_price) / 2
```

This helped when the best bid and ask were noisy.

### Thin-book Attack

We also tested whether a very thin bid or ask side could be exploited.

General idea:

```text
if ask side is thin and future buy pressure is likely:
    buy through the ask
    sell back later

if bid side is thin and future sell pressure is likely:
    sell through the bid
    buy back later
```

### Final Strategy

TODO: Fill in final Round 2 strategy.

More details: [`writeups/round2.md`](writeups/round2.md)

---

## Round 3: VELV and HYDRO

### Products

- `VELVETFRUIT_EXTRACT`
- `HYDROGEL_PACK`

### Main Idea

Round 3 introduced a new relationship between VELV and HYDRO.

We tested whether HYDRO could predict VELV or whether their residual had mean-reverting behavior.

General model:

```python
fair_velv = a * hydro_mid + b
residual = velv_mid - fair_velv
```

Trading rule:

```python
if residual < -threshold:
    buy VELV

if residual > threshold:
    sell VELV
```

### HYDROGEL_PACK

HYDRO also had its own mean-reversion / market-making opportunities.

### Final Strategy

TODO: Fill in Round 3 final VELV/HYDRO strategy.

More details: [`writeups/round3.md`](writeups/round3.md)

---

## Round 4: Improved VELV and HYDRO

### Products

- `VELVETFRUIT_EXTRACT`
- `HYDROGEL_PACK`
- `VEV_*`

### Main Improvement

Round 4 improved the VELV-HYDRO model and added option-like products.

We studied:

- VELV-HYDRO residual,
- option fair value,
- implied volatility,
- strike selection,
- EMA-based anomaly detection.

### Residual Trading

```python
fair_velv = a * hydro_mid + b
residual = velv_mid - fair_velv

if residual < -threshold:
    buy VELV
    buy selected VEV products

if residual > threshold:
    sell VELV
    sell selected VEV products
```

### Final Strategy

TODO: Fill in final Round 4 logic.

More details: [`writeups/round4.md`](writeups/round4.md)

---

## Round 5: Mixed Universe

### Products

Round 5 contained around 50 products.

### Main Challenge

The challenge was no longer one specific product, but quickly identifying which products had usable patterns.

### Product Screening Workflow

```text
for each product:
    plot price and spread
    test market making
    test mean reversion
    test momentum
    test lead-lag relationship
    keep only robust strategies
```

### Strategy Families

We tested:

- market making,
- mean reversion,
- momentum,
- lead-lag trading,
- cross-product residual trading.

### Final Strategy

TODO: Fill in final product list and strategy modules.

More details: [`writeups/round5.md`](writeups/round5.md)

---

# Manual Challenge

TODO: Add notes for each manual round.

See [`writeups/manual_challenge.md`](writeups/manual_challenge.md)

# Final Architecture

Our final trader used product-specific strategy modules.

```python
class Trader:
    def run(self, state):
        result = {}

        # load traderData
        # update indicators
        # run product-specific strategies
        # check position limits
        # save traderData

        return result, conversions, traderData
```

The main design principle was:

```text
simple signal
+ product-specific assumptions
+ strict position control
+ robust backtesting
```

# Lessons Learned

## 1. Good tools matter

Visualization and backtesting were often more important than complicated models.

## 2. Simple strategies are strong

Most profitable strategies came from simple observations.

## 3. Spread is expensive

A signal can look profitable before transaction cost but fail after crossing the spread.

## 4. Position limits must be handled carefully

Many errors came from exceeding position limits or not accounting for existing inventory.

## 5. Product-specific logic beats universal logic

Different products had very different behavior, so one universal strategy was not enough.

## 6. Out-of-sample testing is important

A strategy that worked on one day was not always robust.

# FAQ

## What is wall mid?

Wall mid is a fair value estimate based on large bid and ask liquidity levels.

```python
wall_mid = (bid_wall_price + ask_wall_price) / 2
```

## Why not use only raw mid price?

Raw mid price can be noisy when the best bid or ask is only a small order. Wall mid can be more stable when the book contains large liquidity walls.

## How did we choose thresholds?

Mostly by combining:

- visual inspection,
- parameter sweeps,
- backtesting,
- out-of-sample validation.

## What else did we try?

TODO:

- failed ASH/ROOT variants,
- failed VELV/HYDRO thresholds,
- failed Round 5 product relationships,
- overfitted strategies that were removed.
