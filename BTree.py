from math import floor

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

        if record.key == 5:
            pass

        self.insert_leaf(self.root, record)

    def delete(self, key):
        if self.search_key(key) is None:
            print("\nKey not in the tree")
            return

        self.delete_key(key)

    def insert_leaf(self, page, record):
        if len(page.pointers) == 0:
            if page.full(self.d):
                self.split(page, 0, record)
            else:
                page.records.append(record)
                page.records.sort(key=lambda x: x.key)
            return

        i = find_pointer(page, record)
        if page.pointers[i].leaf:
            if len(page.pointers[i].records) >= (2 * self.d):
                if self.find_non_full_sibling(page, i) is not None:
                    self.compensate(page, i, True, record)
                    return
                else:
                    self.split(page.pointers[i], i, record)
                    return
        self.insert_leaf(page.pointers[i], record)

    def insert_non_leaf(self, page, record, i):
        self.update(self.root)

        if not page.full(self.d):
            page.records.insert(i, record)
            return

        else:
            if self.find_non_full_sibling(page, i) is not None:
                self.compensate(page, i, True, record)
                return
            else:
                self.split(page, i, record)
                return

    def split(self, page, i, record=None):
        if page == self.root:
            tmp = page
            tmp.records.append(record)
            tmp.records.sort(key=lambda x: x.key)
            tmp1 = BTreeNode(page.leaf)
            tmp2 = BTreeNode(page.leaf)

            tmp1.records = tmp.records[self.d + 1:]
            tmp2.records = tmp.records[0: self.d]
            tmp1.pointers = tmp.pointers[self.d + 1:]
            tmp2.pointers = tmp.pointers[0: self.d]
            tmp1.parent = page
            tmp2.parent = page

            page.leaf = False
            page.pointers = [tmp2, tmp1]
            page.records = [tmp.records[floor(len(tmp.records) / 2)]]
        else:
            tmp = page
            z = BTreeNode(tmp.leaf)
            if record is not None:
                tmp.records.append(record)
                tmp.records.sort(key=lambda x: x.key)

            page.parent.pointers.insert(i + 1, z)
            self.insert_non_leaf(page.parent, tmp.records[self.d], i)

            z.records = tmp.records[self.d + 1:]
            tmp.records = tmp.records[0: self.d]
            if not tmp.leaf:
                z.pointers = tmp.pointers[self.d + 1: 2 * self.d]
                tmp.pointers = tmp.pointers[0: self.d]

    def compensate(self, page, i, up, new=None):
        if up:
            sibling = self.find_non_full_sibling(page, i)
        else:
            sibling = self.find_non_underflow_sibling(page, i)
        record = lambda x: page.records[i] if i < x else page.records[sibling]

        r = page.pointers[i].records + [record(sibling)] + page.pointers[sibling].records + [new]
        r.sort(key=lambda x: x.key)

        middle = floor(len(r) / 2)

        if i < sibling:
            page.records[i] = r[middle]
            page.pointers[sibling].records = r[middle + 1:]
            page.pointers[i].records = r[0: middle]
        else:
            page.records[sibling] = r[middle]
            page.pointers[sibling].records = r[:middle]
            page.pointers[i].records = r[middle + 1:]
        if not page.pointers[i].leaf:
            p = page.pointers[i].pointers + page.pointers[sibling].pointers
            if i < sibling:
                page.pointers[sibling].pointers = p[floor(len(p) / 2):]
                page.pointers[i].records = r[:floor(len(p) / 2)]
            else:
                page.pointers[sibling].records = r[:floor(len(p) / 2)]
                page.pointers[i].records = r[floor(len(p) / 2):]

    def merge(self, page, i, k):
        if len(page.pointers[i + 1].records) == self.d:
            sibling = i + 1
        elif len(page.pointers[i - 1].records) == self.d:
            sibling = i - 1
        else:
            return False

        record = lambda x: page.records[i] if i < x else page.records[sibling]

        r = page.pointers[i].records + [record(sibling)] + page.pointers[sibling].records

        page.pointers[i].records = r
        if not page.pointers[i].leaf:
            p = page.pointers[i].pointers + page.pointers[sibling].pointers
            page.pointers[i].pointers = p

        if page.parent is None and len(page.records) == 1:
            page.pointers = []
            page.records = [rec for rec in r if rec.key != k]
            page.leaf = True
            return False
        else:
            page.pointers.remove(sibling)
            page.delete_key(record(sibling).key)
            return True

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

    def update(self, x):
        if len(x.pointers) > 0:
            for i in x.pointers:
                i.parent = x
                self.update(i)

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

    def delete_key(self, k, x=None):
        self.update(self.root)

        if x is not None:
            i = 0
            while i < len(x.records) and k > x.records[i].key:
                i += 1
            if i < len(x.records) and k == x.records[i].key and x.leaf:
                if len(x.records) <= self.d:
                    if self.find_non_underflow_sibling(x.parent, i) is not None:
                        self.compensate(x.parent, i, False)
                    else:
                        if not self.merge(x.parent, i, k):
                            return
                x.records = [record for record in x.records if record.key != k]
                return True
            elif i < len(x.records) and k == x.records[i].key:
                tmp = self.find_key(x.pointers[i], "max")
                if tmp is None:
                    tmp = self.find_key(x.pointers[i+1], "min")
                    if tmp is None:
                        return False
                if self.delete_key(tmp.key):
                    x.records.pop(i)
                    x.records.insert(i, tmp)
                    return True
                else:
                    return False

            elif x.leaf:
                return False
            else:
                return self.delete_key(k, x.pointers[i])

        else:
            return self.delete_key(k, self.root)

    def print_record(self, key):
        record = self.search_key(key)
        print(f"\nKey: {record.key}\nMass: {record.mass}\nHeat: {record.heat}\nDelta temperatures: "
              f"{record.delta_temp}\nEnergy: {record.energy}")

    def find_non_full_sibling(self, page, i):
        try:
            l1 = page.pointers[i + 1].full(self.d)
        except IndexError:
            l1 = True

        try:
            l2 = page.pointers[i - 1].full(self.d)
        except IndexError:
            l2 = True

        if not l1:
            return i + 1
        elif not l2:
            return i - 1
        else:
            return

    def find_non_underflow_sibling(self, page, i):
        try:
            l1 = page.pointers[i + 1].underflow(self.d)
        except IndexError:
            l1 = False

        try:
            l2 = page.pointers[i - 1].underflow(self.d)
        except IndexError:
            l2 = False

        if not l1:
            return i + 1
        elif not l2 and i > 0:
            return i - 1
        else:
            return

    def find_key(self, page, value):
        if value == "min":
            tmp = 0
        elif value == "max":
            tmp = len(page.records) - 1
        else:
            return
        if page.leaf:
            if len(page.records) - 1 >= self.d:
                return page.records[tmp]
            else:
                return
        else:
            return self.find_key(page.pointers[tmp], value)

    def full_children(self, page):
        for pointer in page.pointers:
            if not pointer.full(self.d):
                return False
        return True


