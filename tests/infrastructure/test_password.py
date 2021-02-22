from auth.infrastructure.password import Password


def test_password_generate_password():
    password = 'a-secret'

    hashed_password = Password.hash_password(password)

    assert hashed_password
    assert hashed_password != password


def test_password_validate_password():
    password = 'a-secret'
    hashed_password = Password.hash_password(password)

    is_valid = Password.validate_password(password, hashed_password)

    assert is_valid
