import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://postgres:@localhost:5432/auth')
