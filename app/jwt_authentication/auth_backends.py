from jwt_authentication.models import JWTToken
from rest_framework import authentication


class JWTAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"
    model = JWTToken
