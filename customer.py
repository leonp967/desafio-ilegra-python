class Customer:
    def __init__(self, cnpj, name, bussiness_area):
        self.cnpj = int(cnpj)
        self.name = name
        self.bussiness_area = bussiness_area

    @classmethod
    def from_list(cls, list):
        return cls(list[0], list[1], list[2])
        