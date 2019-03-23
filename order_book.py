class OrderBook:
    def __init__(self):
        self.Bids = OrderNode()
        self.Asks = OrderNode()

    def bid(self, size, limit):
        key = lambda x, y: x <= y
        ask_size, ask_limit = self.search(self.Asks, limit, key=key)

        if ask_size < 0:
            self.add_node(self.Bids, size, limit)
        elif ask_size < size:
            self.bid(size - ask_size, limit)
        elif size < ask_size:
            self.add_node(self.Asks, ask_size - size, ask_limit)

    def ask(self, size, limit):
        key = lambda x, y: x >= y
        bid_size, bid_limit = self.search(self.Bids, limit, key=key)

        if bid_size < 0:
            self.add_node(self.Asks, size, limit)
        elif bid_size < size:
            self.bid(size - bid_size, limit)
        elif size < bid_size:
            self.add_node(self.Bids, bid_size - size, bid_limit)

    def add_node(self, head, size, limit):
        if head.size is None and head.limit is None:
            head.size = size
            head.limit = limit
            return

        new_node = OrderNode(size, limit)

        curr = prev = head
        while curr is not None:
            prev = curr
            if curr.limit >= limit:
                curr = curr.left
            else:
                curr = curr.right

        if prev.limit >= limit:
            prev.left = new_node
        else:
            prev.right = new_node

    def search(self, head, target_limit, key):
        pass


class OrderNode:
    def __init__(self, size=None, limit=None):
        self.left = self.right = self.parent = None
        self.size = size
        self.limit = limit
