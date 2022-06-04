from enum import Enum


class NODE_LEVEL(Enum):
    ROOT = 0
    NO_RANK = 0
    SUPERKINGDOM = 1



class TREE:
    def __init__(self):
        self.root: NODE = NODE()


class NODE:
    def __init__(self, parent):
        self.parent: NODE = parent
        self.name: str = name
        self.child: list = []
