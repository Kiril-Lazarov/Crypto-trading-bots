class Asset:
    def __init__(self, init_qty, name):
        self.name = name
        self.init_qty = init_qty
        self.quantity = self.init_qty
