import json

class User:

    def __init__(self, name, number, carrier):
        self.name = name
        self.phone_num = number
        self.carrier = carrier


    def __str__(self):
        return f'User(\n\t{self.name}\n\t{self.phone_num}\n\t{self.carrier}\n)'
    

    def user_msg(self, msg):
        self.msg = msg
    

    @classmethod
    def __json_to_dict(cls, user_data):
        return cls(
            name=user_data['name'],
            number=user_data['phone_num'],
            carrier=user_data['carrier']
        )
    

    @classmethod
    def load_users(cls):
        with open('users.json', 'r') as json_file:
            return [cls.__json_to_dict(user) for user in json.load(json_file)]
        

    @staticmethod
    def get_user_by_number(users, number):
        for user in users:
            if user.phone_num == number:
                return user
        return None        