class OrderBook:
    def __init__(self):
        self.Bids = OrderNode()
        self.Asks = OrderNode()

    def bid(self, size, limit):
        self.order(T1=self.Bids,
                   T2=self.Asks,
                   key=lambda x, y: x <= y,
                   size=size,
                   limit=limit)

    def ask(self, size, limit):
        self.order(T1=self.Asks,
                   T2=self.Bids,
                   key=lambda x, y: x >= y,
                   size=size,
                   limit=limit)

    def order(self, T1, T2, key, size, limit):
        search_size, search_limit = search_tree(T2, limit, key=key)

        if search_size == 0:
            add_tree_node(T1, size, limit)
            return

        new_size = abs(size - search_size)
        if search_size < size:
            self.order(T1, T2, key, new_size, limit)
        elif size < search_size:
            add_tree_node(T2, new_size, search_limit)


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
