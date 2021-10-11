class User:
    username = None
    password = None
    test = 'unchanged'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get(self, username, password):
        self.username = username
        self.password = password
        self.test = 'changed'
        return self


user2 = User.get(User, 'username', 'password2')
user1 = User('ethan', 'password')

print('User1: ' + user1.username + ' ' + user1.test)
print('User2: ' + user2.username + ' ' + user2.test)