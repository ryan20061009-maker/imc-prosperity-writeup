# IMC Prosperity 4 Strategy Writeup

This repository contains my post-competition writeup for **IMC Prosperity 4**, where my team achieved **Global Rank 31**.

The goal of this repository is to document our strategy design process, trading intuition, implementation details, visual analysis, manual challenge reasoning, and lessons learned from the competition.

> This is a post-competition portfolio repository. The writeup focuses on explaining the ideas and observations behind the strategies rather than presenting a production-ready trading system.

## Overview

- Competition: IMC Prosperity 4
- Result: Global Rank 31
- Focus: algorithmic trading, market making, statistical arbitrage, visual analysis, risk control
- Language: Python

## Repository Structure

```text
imc-prosperity-4-postmortem/
├── README.md
├── final_submission.py
├── strategy_writeup.md
├── analysis/
│   ├── round1_2.md
│   ├── round3_4.md
│   ├── round5.md
│   └── manual_challenges.md
├── figures/
├── notes/
│   ├── failed_ideas.md
│   └── lessons_learned.md
└── src/
    ├── trader.py
    ├── strategies.py
    └── utils.py
```

## Strategy Summary

A complete strategy writeup is available in:

```text
strategy_writeup.md
```

Round-by-round notes are available in:

```text
analysis/
```

## Main Algorithmic Ideas

- identifying strong directional drift
- market making around observed spread behavior
- exploiting temporary order book imbalance
- testing option pricing ideas through implied volatility
- using lead-lag correlation between products
- using medium-term mean reversion on noisy products
- filtering noisy order book levels to estimate a cleaner fair value
- rapidly screening many products in the final round

## Manual Challenge Notes

Manual challenge notes are summarized in:

```text
analysis/manual_challenges.md
```

## Disclaimer

This repository is for learning and portfolio purposes. It is not financial advice and does not represent a real-money trading system.
