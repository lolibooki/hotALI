import json


class Tree:
    def __init__(self, root, branches):
        self.root = root
        self.branches = branches

    def __repr__(self):
        # a = ' '.join(self.root) + ' '.join(self.branches)
        return json.dumps(self.branches) + self.root  # a
