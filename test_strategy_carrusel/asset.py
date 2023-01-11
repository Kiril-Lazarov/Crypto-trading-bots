class Asset:
    def __init__(self, init_qty, name, on_charge = False):
        self.init_qty = init_qty
        self.name = name
        self.on_charge = on_charge

        self.real_quantity = self.init_qty

    def __repr__(self):
        return f"Name: {self.name} On charge: {self.on_charge} Init: {self.init_qty}," \
               f" real_quantity: {self.real_quantity}"


