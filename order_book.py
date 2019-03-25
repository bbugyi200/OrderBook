class OrderBook:
    def __init__(self):
        self.Bids = OrderNode()
        self.Asks = OrderNode()

    def bid(self, size, limit):
        self._order(T1=self.Bids,
                    T2=self.Asks,
                    key=lambda x, y: x <= y,
                    size=size,
                    limit=limit)

    def ask(self, size, limit):
        self._order(T1=self.Asks,
                    T2=self.Bids,
                    key=lambda x, y: x >= y,
                    size=size,
                    limit=limit)

    def _order(self, T1, T2, key, size, limit):
        try:
            node = search_tree(T2, limit, key=key)
            search_size = node.size
            search_limit = node.limit
        except ValueError:
            add_tree_node(T1, size, limit)
        else:
            new_size = abs(size - search_size)
            if size > search_size:
                self._order(T1, T2, key, new_size, limit)
            elif size < search_size:
                add_tree_node(T2, new_size, search_limit)


#####################################################################
#  Tree Algorithms                                                  #
#####################################################################
class OrderNode:
    def __init__(self, size=None, limit=None):
        self.left = self.right = self.parent = None
        self.size = size
        self.limit = limit


def add_tree_node(T, size, limit):
    if T.size is None and T.limit is None:
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


def search_tree(T, limit, key):
    node = T
    while node is not None:
        if key(node.limit, limit):
            delete_tree_node(T, node)
            return node
        elif limit <= node.limit:
            node = node.left
        else:
            node = node.right

    raise ValueError('Node not found.')


def delete_tree_node(T, node):
    pass
