class UserWithInvalidEmail(Exception):
    pass


class ActivationNotFound(Exception):
    pass


class ActivationExpired(Exception):
    pass


class InvalidResetPasswordToken(Exception):
    pass


class ResetPasswordTokenExpired(Exception):
    pass
