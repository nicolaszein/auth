import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://postgres:@localhost:5432/auth')
TOKEN_EXPIRATION_TIME = os.getenv('TOKEN_EXPIRATION_TIME', 7200)
JWT_SECRET_TOKEN = os.getenv('JWT_SECRET_TOKEN', '')
