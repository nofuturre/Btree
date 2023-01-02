class BTreeNode:
  def __init__(self, leaf=False):
    self.leaf = leaf
    self.records = []
    self.pointers = []