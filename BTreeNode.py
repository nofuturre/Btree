class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.records = []
        self.pointers = []
        self.parent = None

    def full(self, d):
        if len(self.records) < 2 * d:
            return False
        else:
            return True

    def underflow(self, d):
        if len(self.records) == d and self.parent is not None:
            return True
        elif len(self.records) == 1 and self.parent is None:
            return True
        else:
            return False
