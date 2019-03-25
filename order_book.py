class OrderBook:
    def __init__(self):
        self.Bids = OrderNode()
        self.Asks = OrderNode()

    def bid(self, size, limit):
        self._order(T1=self.Bids,
                    T2=self.Asks,
                    key=lambda x, y: x <= y,
                    direction='left',
                    size=size,
                    limit=limit)

    def ask(self, size, limit):
        self._order(T1=self.Asks,
                    T2=self.Bids,
                    key=lambda x, y: x >= y,
                    direction='right',
                    size=size,
                    limit=limit)

    def _order(self, T1, T2, key, direction, size, limit):
        try:
            node = search_tree(T2, limit, key, direction)
            search_size = node.size
            search_limit = node.limit
            delete_tree_node(node)
        except ValueError:
            add_tree_node(T1, size, limit)
        else:
            new_size = abs(size - search_size)
            if size > search_size:
                self._order(T1, T2, key, direction, new_size, limit)
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

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.size is None:
            return "Empty Tree"

        ret = "(%d,%d)" % (self.size, self.limit)
        if self.left is not None:
            ret = '[%s] <-- %s' % (repr(self.left), ret)

        if self.right is not None:
            ret = '%s --> [%s]' % (ret, repr(self.right))

        return ret


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


def search_tree(T, limit, key, direction):
    node = T
    ret = None
    while node is not None and node.limit is not None:
        if key(node.limit, limit):
            ret = node
            if direction == 'left':
                node = node.left
            elif direction == 'right':
                node = node.right
        elif limit <= node.limit:
            node = node.left
        else:
            node = node.right

    if ret is not None:
        return ret
    else:
        raise ValueError('Node not found.')


def delete_tree_node(node):
    if node.parent is None and node.left is None and node.right is None:
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
    else:
        node.size = new_node.size
        node.limit = new_node.limit
        node.left = new_node.left
        node.right = new_node.right


if __name__ == '__main__':
    ob = OrderBook()
    ob.ask(400, 4)
    ob.ask(500, 5)
    ob.ask(300, 3)

    ob.bid(200, 5)
    ob.bid(50, 3)
    ob.ask(250, 3)
    print(ob.Asks)
    print(ob.Bids)
