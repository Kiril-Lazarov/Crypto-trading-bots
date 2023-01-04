class Asset:
    def __init__(self, init_qty, name):
        self.name = name
        self.init_qty = init_qty
        self.total_quantity = self.init_qty

    def __repr__(self):
        return f"Name: {self.name} Init: {self.init_qty}, total_quantity: {self.total_quantity}"
