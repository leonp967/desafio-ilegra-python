class SaleItem:
    def __init__(self, id, quantity, price):
        self.id = int(id)
        self.quantity = int(quantity)
        self.price = float(price)

    @classmethod
    def from_list(cls, list):
        return cls(list[0], list[1], list[2])