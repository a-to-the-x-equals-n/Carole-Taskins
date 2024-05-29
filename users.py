
class User:

    def __init__(self, first, last, number, carrier):
        self.f_name = first
        self.l_name = last
        self.num = number
        self.carrier = carrier

    def __str__(self):
        return f'{self.f_name}'
        