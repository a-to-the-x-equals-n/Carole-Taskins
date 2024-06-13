class User:

    def __init__(self, name, number, carrier):
        self.name = name
        self.phone_num = number
        self.carrier = carrier
        self.sms = ''


    def __str__(self):
        return f'User(\n\t{self.name}\n\t{self.phone_num}\n\t{self.carrier}\n)'
    

    @classmethod
    def from_dict(cls, user_data):
        return cls(
            name = user_data['name'],
            number = user_data['phone_num'],
            carrier = user_data['carrier']
        )       