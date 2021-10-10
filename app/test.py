from werkzeug.security import generate_password_hash, check_password_hash

class User:
    user_id = None
    username = None

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username


user = User(1,'ethan')
print(user.user_id)
print(user.username)

"""
sha256$bHNxh8u2unr9rEFo$d2fb8d2099ce0e5426eccb8add254313a58459f90525740361e395e3340fd266
sha256$99dLtsFafFaqHcLT$70781a30ea1dd8923cc6bc80e5070920db672369a4d81a11e3637bb3528cb23

$Hn7rAFfQr7IqzKe8$514033825663298eca213315a5b5cc138f5c4e04daa0b2e995ca8cb3a6a7b2a5
$BEi7IuexXa6bzd3J$e5feb1cce9e8283216a5b1efa7d7f7fed72d2350322190fa9c200b095d2b2567
"""
print(generate_password_hash('password'))