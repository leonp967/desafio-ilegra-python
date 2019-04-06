class Salesman:
    def __init__(self, cpf, name, salary):
        self.name = name
        self.cpf = int(cpf)
        self.salary = float(salary)
        self.sales_list = []

    @classmethod
    def from_list(cls, list):
        return cls(list[0], list[1], list[2])

    def add_sale(self, sale):
        self.sales_list.append(sale)