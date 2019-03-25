"""
My attempt at designing a data structure which efficiently tracks
limit orders (i.e. bids and asks).
"""


class OrderBook:
    """Abstract representation of a limit order book."""
    def __init__(self):
        self.Bids = OrderNode()
        self.Asks = OrderNode()

    def __repr__(self):
        return 'Bids: %s\nAsks: %s' % (self.Bids, self.Asks)

    def bid(self, size, limit):
        """Submit a Bid Order.

        Args:
            size (int): Size of the order.
            limit (float): Price limit of the order.
        """
        self._order(T1=self.Bids,
                    T2=self.Asks,
                    order_type='bid',
                    size=size,
                    limit=limit)
        return self

    def ask(self, size, limit):
        """Submit an ask order.

        Args:
            size (int): Size of the order.
            limit (float): Price limit of the order.
        """
        self._order(T1=self.Asks,
                    T2=self.Bids,
                    order_type='ask',
                    size=size,
                    limit=limit)
        return self

    def _order(self, T1, T2, order_type, size, limit):
        """Submit a generic limit order (either an 'ask' or a 'bid').

        Args:
            T1 (OrderNode): Order tree that will be added to.
            T2 (OrderNode): Order tree that will be searched for entries
                which can fill the currently requested order.
            order_type (str): Either 'ask' or 'bid'.
            size (int): Size of the order.
            limit (float): Price limit of the order.
        """
        assert order_type in ['ask', 'bid'], 'Invalid order type: %s' % (order_type,)

        try:
            op = '<=' if order_type == 'bid' else '>='
            node = search_tree(T2, limit, op)

            search_size = node.size
            search_limit = node.limit

            delete_tree_node(node)
        except ValueError:
            add_tree_node(T1, size, limit)
        else:
            new_size = abs(size - search_size)
            if size > search_size:
                self._order(T1, T2, order_type, new_size, limit)
            elif size < search_size:
                add_tree_node(T2, new_size, search_limit)
            elif size == search_size:
                # No action required. Both orders (ask and bid)
                # have already been removed from their respective
                # order trees.
                pass


class OrderNode:
    """Used to construct a tree data structure that stores limit orders.

    Args:
        size (int): Size of the order.
        limit (float): Price limit of the order.
    """
    def __init__(self, size=None, limit=None):
        self.left = self.right = self.parent = None
        self.size = size
        self.limit = limit

    def __repr__(self):
        if self.size is None:
            return "Empty Tree"

        ret = "[(%d, %0.1f)]" % (self.size, self.limit)
        if self.left is not None:
            ret = '[%s <-- %s]' % (repr(self.left), ret.strip('[]'))

        if self.right is not None:
            ret = '[%s --> %s]' % (ret.strip('[]'), repr(self.right))

        return ret

    def isRoot(self):
        """
        Predicate that checks if this order node is the root of the
        order tree.
        """
        return all([self.parent is None,
                    self.left is None,
                    self.right is None])

    def isEmpty(self):
        """Predicate that checks if this order tree is empty.

        This method should only be called when (and should only
        return True when) this node is the root of the order tree.
        """
        is_empty = self.size is None and self.limit is None
        assert self.isRoot() or not is_empty, "OrderNode is empty but NOT root."

        return is_empty


def add_tree_node(T, size, limit):
    """Add node to an order tree.

    Args:
        T (OrderNode): The root of the order tree to add to.
        size (int): Size of the order.
        limit (float): Price limit of the order.
    """
    if T.isEmpty():
        T.size = size
        T.limit = limit
        return

    new_node = OrderNode(size, limit)

    curr = prev = T
    while curr is not None:
        prev = curr
        if limit <= curr.limit:
            curr = curr.left
        else:
            curr = curr.right

    new_node.parent = prev
    if limit <= prev.limit:
        prev.left = new_node
    else:
        prev.right = new_node


def delete_tree_node(node):
    """Delete a node from an order tree.

    Args:
        node (OrderNode): The node to be deleted.
    """
    if all([node.parent is None, node.left is None, node.right is None]):
        node.limit = None
        node.size = None
        return

    if node.left is None and node.right is None:
        new_node = None
    elif node.left is None:
        new_node = node.right
    elif node.right is None:
        new_node = node.left
    else:
        temp = node
        while temp.left is not None:
            temp = temp.left

        node.limit = temp.limit
        node.size = temp.size
        delete_tree_node(temp)
        return

    if node.parent is not None:
        if node.parent.left == node:
            node.parent.left = new_node
        elif node.parent.right == node:
            node.parent.right = new_node
    elif new_node is not None:
        node.size = new_node.size
        node.limit = new_node.limit
        node.left = new_node.left
        node.right = new_node.right
    else:
        raise RuntimeError(
            'Check the correctness of this algorithm. The variable '
            'new_node is equal to None, which should not be '
            'possible.'
        )


def search_tree(T, limit, op):
    """Binary search over an order tree.

    Args:
        T (OrderNode): The root of the order tree to search.
        limit (float): Price limit of the order.
        op (str): The comparison operator to use in the search.
            Must be either '<=' or '>='.

    Returns:
        OrderNode object that matches the search criteria. If no
        matching node can be found, a ValueError exception is raised.
    """
    assert op in ['<=', '>='], "Invalid op argument: %s" % (op,)

    curr = prev = T
    while curr is not None and curr.limit is not None:
        prev = curr
        if op == '<=':
            curr = curr.left
        elif op == '>=':
            curr = curr.right

    if op == '<=':
        search_key = lambda x, y: x <= y
    elif op == '>=':
        search_key = lambda x, y: x >= y

    if prev.limit is not None and search_key(prev.limit, limit):
        return prev
    else:
        raise ValueError(
            'No OrderNode could be found that matches the specified '
            'search criteria.'
        )


if __name__ == '__main__':
    ob = OrderBook()

    ob.ask(400, 4)
    ob.ask(500, 5)
    ob.ask(300, 3)

    ob.bid(200, 5)
    ob.bid(50, 3)

    ob.ask(250, 3)
    ob.ask(600, 3.5)

    print(ob.Asks)
    print(ob.Bids)
