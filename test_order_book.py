import pytest

import order_book as ob


def test_order_book1(obook):
    obook.bid(1000, 5)
    obook.ask(300, 4)

    assert obook.Bids.size == 700
    assert obook.Asks.size is None


def test_order_book2(obook):
    obook.ask(700, 4)
    print('Asks: %s' % (obook.Asks,))
    obook.ask(500, 5)
    print('Asks: %s' % (obook.Asks,))
    obook.bid(1000, 5)
    print('Asks: %s' % (obook.Asks,))

    print('Bids: %s' % (obook.Bids,))

    assert obook.Bids.size is None
    assert obook.Asks.limit == 5
    assert obook.Asks.size == 200


def test_delete_tree_node(obook):
    obook.ask(700, 4)
    obook.ask(500, 5)
    obook.ask(400, 3)

    ob.delete_tree_node(obook.Asks)

    assert obook.Asks.limit == 3


@pytest.fixture
def obook():
    return ob.OrderBook()
