import pytest

import order_book


def test_order_book1(ob):
    ob.bid(1000, 5)
    ob.ask(300, 4)

    assert ob.Bids.size == 700
    assert ob.Asks.size is None


def test_order_book2(ob):
    ob.ask(700, 4)
    ob.ask(500, 5)
    ob.bid(1000, 5)

    assert ob.Bids.size is None
    assert ob.Asks.limit == 5
    assert ob.Asks.size == 200


def test_delete_tree_node(ob):
    ob.ask(700, 4)
    ob.ask(500, 5)
    ob.ask(400, 3)

    order_book.delete_tree_node(ob.Asks)

    assert ob.Asks.limit == 3


@pytest.fixture
def ob():
    return order_book.OrderBook()
