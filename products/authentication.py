import jwt

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTUser:
    def __init__(self, payload):
        self.payload = payload
        self.is_authenticated = True
        self.is_anonymous = False

    @property
    def username(self):
        return self.payload.get("UserName")

    @property
    def id(self):
        return self.payload.get("IdUser")


class ProductJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        header = request.headers.get("Authorization")

        if not header:
            return None

        parts = header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed(
                "Token phải có dạng Bearer <token>."
            )

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token đã hết hạn.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Token không hợp lệ.")

        return JWTUser(payload), token
