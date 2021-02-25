import datetime

import jwt

from auth.settings import JWT_SECRET_TOKEN, TOKEN_EXPIRATION_TIME


class Token:

    def validate_token(self, token):
        return jwt.decode(token, JWT_SECRET_TOKEN, algorithms=['HS256'])

    def generate_token(self, user_id, session_id, expire_in=TOKEN_EXPIRATION_TIME):
        claims_data = self.__build_claims_data(user_id)
        claims_data['session_id'] = session_id

        if expire_in:
            now = datetime.datetime.now()
            exp = now + datetime.timedelta(seconds=expire_in)
            claims_data['exp'] = datetime.datetime.timestamp(exp)

        token = self.__build_token(claims_data)

        return token

    def generate_refresh_token(self, user_id):
        claims_data = self.__build_claims_data(user_id)

        token = self.__build_token(claims_data)

        return token

    def __build_claims_data(self, user_id):
        now = datetime.datetime.now()
        claims_data = {
            'iat': datetime.datetime.timestamp(now),
            'iss': 'auth_svc',
            'user_id': user_id,
        }

        return claims_data

    def __build_token(self, data):
        return jwt.encode(
            data,
            JWT_SECRET_TOKEN,
            algorithm='HS256'
        )
