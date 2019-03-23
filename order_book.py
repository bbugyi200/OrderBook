class OrderBook:
    def __init__(self):
        self.Bids = OrderTracker('Bids')
        self.Asks = OrderTracker('Asks')

    def __str__(self):
        return '{}\n\n{}'.format(str(self.Bids), str(self.Asks))

    def __repr__(self):
        return '(Bids:{}, Asks:{})'.format(repr(self.Bids), repr(self.Asks))

    def bid(self, size, limit):
        self.Bids.new(size, limit)
        self.Bids -= self.Asks

    def ask(self, size, limit):
        self.Asks.new(size, limit)
        self.Asks -= self.Bids


class OrderTracker:
    def __init__(self, name):
        self.name = name
        self.sizes = []
        self.limits = []
        self.count = 0

    def __sub__(self, Other):
        size, limit = self.sizes[-1], self.limits[-1]

        return self

    def __str__(self):
        table = '\n'.join('{}\tat ${}'.format(size, limit)
                          for size, limit in zip(self.sizes, self.limits))
        return "========== {} ==========\n{}".format(self.name, table)

    def __repr__(self):
        return str(list(zip(self.sizes, self.limits)))

    def new(self, size, limit):
        self.sizes.append(size)
        self.limits.append(limit)

        self.count += 1

    def pop(self):
        self.sizes.pop()
        self.limits.pop()

        self.count -= 1
