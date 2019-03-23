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
        n2_size, n2_limit = self.search(N2, limit, key=key)

        new_size = abs(size - n2_size)
        if n2_size == 0:
            self.add_node(N1, size, limit)
        elif n2_size < size:
            self.order(N1, N2, key, new_size, limit)
        elif size < n2_size:
            self.add_node(N2, new_size, n2_limit)

    def add_node(self, head, size, limit):
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

    def search(self, head, target_limit, key):
        pass


class OrderNode:
    def __init__(self, size=None, limit=None):
        self.left = self.right = self.parent = None
        self.size = size
        self.limit = limit
