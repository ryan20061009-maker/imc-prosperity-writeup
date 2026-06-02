"""Final trader placeholder.

Replace this file with the final submitted strategy or use it as a clean entry point
for merging product-specific modules.
"""

from typing import Dict, List

try:
    from datamodel import Order, TradingState
except ImportError:
    Order = object
    TradingState = object


class Trader:
    def run(self, state: TradingState):
        result: Dict[str, List[Order]] = {}
        conversions = 0
        traderData = ""

        # TODO: load traderData
        # TODO: update indicators
        # TODO: run product-specific strategies
        # TODO: check position limits
        # TODO: save traderData

        return result, conversions, traderData
