class OrderBook:
    def __init__(self):
        self.Bids = OrderNode()
        self.Asks = OrderNode()

    def bid(self, size, limit):
        self.order(N1=self.Bids,
                   N2=self.Asks,
                   key=lambda x, y: x <= y,
                   size=size,
                   limit=limit)

    def ask(self, size, limit):
        self.order(N1=self.Asks,
                   N2=self.Bids,
                   key=lambda x, y: x >= y,
                   size=size,
                   limit=limit)

    def order(self, N1, N2, key, size, limit):
        search_size, search_limit = search_tree(N2, limit, key=key)

        if search_size == 0:
            add_tree_node(N1, size, limit)
            return

        new_size = abs(size - search_size)
        if search_size < size:
            self.order(N1, N2, key, new_size, limit)
        elif size < search_size:
            add_tree_node(N2, new_size, search_limit)


class OrderNode:
    def __init__(self, size=None, limit=None):
        self.left = self.right = self.parent = None
        self.size = size
        self.limit = limit


#####################################################################
#  Tree Algorithms                                                  #
#####################################################################
def add_tree_node(head, size, limit):
    if head.size is None and head.limit is None:
        head.size = size
        head.limit = limit
        return

    new_node = OrderNode(size, limit)

    curr = prev = head
    while curr is not None:
        prev = curr
        if limit <= curr.limit:
            curr = curr.left
        else:
            curr = curr.right

    if limit <= prev.limit:
        prev.left = new_node
    else:
        prev.right = new_node

    new_node.parent = prev


def search_tree(head, target_limit, key):
    pass
