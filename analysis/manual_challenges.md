# Manual Challenge Notes

The manual challenges were different from the algorithmic rounds. Instead of implementing a trading bot, we had to model the game, reason about other teams' behavior, and choose a decision under uncertainty.

## Manual Round 1

### Round Introduction

Manual Round 1 was relatively deterministic compared with later rounds. The main task could be solved by directly modeling the rules and searching through possible choices.

### Our Approach

We wrote a simple brute-force program to enumerate possibilities and choose the best result.

### Reflection

For this round, the key was not complicated strategy, but accurately translating the rules into code.

## Manual Round 2

### Round Introduction

Manual Round 2 involved a strategic game with multiple parameters. Given the speed parameter, the other two parameters had essentially unique best choices, so the main game-theoretic decision was how much speed to choose.

### Our Approach

Because of the tie-breaking rule, if everyone chose `0`, that would form a Nash equilibrium. However, we expected that some players might choose `1`, thinking that it would beat players choosing `0`.

If too many players thought this way, choosing `0` might no longer be profitable. Therefore, we chose `1`.

### Reflection

This round was less about pure optimization and more about predicting how other teams would reason.

## Manual Round 3

### Round Introduction

Manual Round 3 could be abstracted as choosing a number between `0` and `50`. The goal was to choose a number close to the median, with an asymmetric penalty: choosing too high was punished less than choosing too low.

### Our Approach

Ignoring later behavioral effects, the theoretical best answer seemed to be around `33`.

However, we did not know how other teams would behave, so I designed a similar survey-style problem and sampled responses. The survey result was not very useful, and we eventually chose around `39`.

In hindsight, the actual best answer seemed to be around `34` or `35`, which was lower than our final choice.

![Manual Round 3 EV curve](../figures/manual_round3_ev_curve.png)

### Reflection

Our choice was probably too greedy. The main difficulty was estimating the distribution of other players' choices.

## Manual Round 4

### Round Introduction

Manual Round 4 was an allocation / investment-style problem where the objective involved expected value, but risk also mattered.

### Our Approach

Our strategy mostly ignored risk and focused on maximizing expected value.

### Result

This led to a large loss.

### Reflection

This was an important lesson: maximizing expected value without controlling downside risk can perform very badly in competition settings.

## Manual Round 5

### Round Introduction

Manual Round 5 involved choosing buy/sell decisions and capital allocation across multiple tradable goods.

### Our Result

Our final allocation is shown below.

![Manual Round 5 result](../figures/manual_round5_result.png)

### Reflection

This round required balancing expected PnL, fees, and allocation size. Compared with earlier rounds, the decision was closer to a portfolio allocation problem.
