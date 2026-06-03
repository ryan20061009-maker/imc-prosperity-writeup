"""
Utility functions for analysis, logging, and strategy debugging.
"""


def mid_price(order_depth):
    """Compute mid price from best bid and best ask if available."""
    if not hasattr(order_depth, "buy_orders") or not hasattr(order_depth, "sell_orders"):
        return None
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None

    best_bid = max(order_depth.buy_orders.keys())
    best_ask = min(order_depth.sell_orders.keys())
    return (best_bid + best_ask) / 2
