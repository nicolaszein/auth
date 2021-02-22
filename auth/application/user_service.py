from auth.infrastructure.user_adapter import UserAdapter


class UserService:

    def __init__(self):
        self.__user_adapter = UserAdapter()

    def signup(self, full_name, email, password):
        return self.__user_adapter.create(full_name=full_name, email=email, password=password)
