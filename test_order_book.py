import pytest

import order_book as ob


def test_order_book():
    obook = ob.OrderBook()

    obook.bid(1000, 5)
    obook.ask(300, 4)

    assert obook.Bids.count == 1
    assert obook.Asks.count == 0

    assert obook.Bids.sizes[-1] == 700
