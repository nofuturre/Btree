from BTreeNode import BTreeNode


def find_pointer(page, record):
    i = len(page.records) - 1
    while i >= 0 and record.key < page.records[i].key:
        i -= 1
    return i + 1


class BTree:
    def __init__(self, d):
        self.root = BTreeNode(True)
        self.d = d

    def insert(self, record):
        if self.search_key(record.key) is not None:
            print("\nKey already in the tree")
            return

        root = self.root
        if len(root.records) == (2 * self.d):
            tmp = BTreeNode()
            self.root = tmp
            tmp.pointers.insert(0, root)
            self.split(tmp, 0)
            self.insert_non_full(tmp, record)
        else:
            self.insert_non_full(root, record)

    def insert_non_full(self, page, record):
        if page.leaf:
            page.records.append(record)
            page.records.sort(key=lambda x: x.key)
        else:
            i = find_pointer(page, record)
            if len(page.pointers[i].records) == (2 * self.d):
                self.split(page, i)
                if record.key > page.records[i].key:
                    i += 1
            self.insert_non_full(page.pointers[i], record)

    def split(self, x, i):
        y = x.pointers[i]
        z = BTreeNode(y.leaf)
        x.pointers.insert(i + 1, z)
        x.records.insert(i, y.records[self.d])
        z.records = y.records[self.d + 1: 2 * self.d]
        y.records = y.records[0: self.d]
        if not y.leaf:
            z.pointers = y.pointers[self.d + 1: 2 * self.d]
            y.pointers = y.pointers[0: self.d]

    def compensate(self):
        pass

    def print_tree(self, x, l=0, p=True):
        if p:
            print(f"\nDepth {l} ")
        print("*", end=" ")
        for i in x.records:
            print(f"{i.key} *", end=" ")
        print("\t", end="")
        l += 1
        if len(x.pointers) > 0:
            for i in x.pointers:
                if i == x.pointers[0]:
                    self.print_tree(i, l, True)
                else:
                    self.print_tree(i, l, False)
        print()

    def search_key(self, k, x=None):
        if x is not None:
            i = 0
            while i < len(x.records) and k > x.records[i].key:
                i += 1
            if i < len(x.records) and k == x.records[i].key:
                return x.records[i]
            elif x.leaf:
                return None
            else:
                return self.search_key(k, x.pointers[i])

        else:
            return self.search_key(k, self.root)

    def print_record(self, key):
        record = self.search_key(key)
        print(f"\nKey: {record.key}\nMass: {record.mass}\nHeat: {record.heat}\nDelta temperatures: "
              f"{record.delta_temp}\nEnergy: {record.energy}")
