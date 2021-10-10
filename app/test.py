class User:
    user_id = None
    username = None

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username


user = User(1,'ethan')
print(user.user_id)
print(user.username)
