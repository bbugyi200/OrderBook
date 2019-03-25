"""Unit tests for the order_book.py module."""

import pytest

import order_book


def test_order_book1(ob):
    ob.bid(1000, 5)
    ob.ask(300, 4)

    assert ob.Bids.size == 700
    assert ob.Bids.limit == 5
    assert ob.Asks.isEmpty()


def test_order_book2(ob):
    ob.ask(700, 4)
    ob.ask(500, 5)
    ob.bid(1000, 5)

    assert ob.Bids.isEmpty()
    assert ob.Asks.limit == 5
    assert ob.Asks.size == 200


def test_order_book3(ob):
    ob.bid(1000, 5)
    ob.ask(700, 6)

    assert ob.Bids.size == 1000
    assert ob.Bids.limit == 5
    assert ob.Asks.size == 700
    assert ob.Asks.limit == 6

    ob.ask(1600, 4.5)

    assert ob.Bids.isEmpty()
    assert ob.Asks.left.size == 600
    assert ob.Asks.left.limit == 4.5


def test_delete_tree_node(ob):
    ob.ask(700, 4)
    ob.ask(500, 5)
    ob.ask(400, 3)

    order_book.delete_tree_node(ob.Asks)

    assert ob.Asks.size == 400
    assert ob.Asks.limit == 3


@pytest.fixture
def ob():
    return order_book.OrderBook()
