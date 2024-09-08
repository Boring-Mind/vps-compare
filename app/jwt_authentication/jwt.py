from datetime import datetime, timedelta

import jwt
import pytz
from commons.typing import JSON_DICT
from django.conf import settings


class JWT:
    @staticmethod
    def encode(payload: JSON_DICT) -> str:
        datetime_now = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))

        default_claims = {
            "iat": datetime_now,
            "nbf": datetime_now,
            "exp": datetime_now + timedelta(seconds=settings.JWT_TTL_SECONDS),
        }
        # Those are optional claims, that may be hard to set up for MVP.
        if settings.JWT_ISSUER:
            default_claims["iss"] = settings.JWT_ISSUER
        if settings.JWT_AUDIENCE:
            default_claims["aud"] = settings.JWT_AUDIENCE

        return jwt.encode(
            payload | default_claims,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def decode(token: str) -> JSON_DICT:
        required_claims = [
            "iat",
            "nbf",
            "exp",
        ]
        # Those are optional claims, that may be hard to set up for MVP.
        if settings.JWT_VALIDATE_AUD:
            required_claims.append("aud")
        if settings.JWT_VALIDATE_ISS:
            required_claims.append("iss")

        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=settings.JWT_ALGORITHM,
            options={
                "require": required_claims,
                "verify_aud": settings.JWT_VALIDATE_AUD,
                "verify_iss": settings.JWT_VALIDATE_ISS,
            },
            # Audience and issuer verification is optional. Can be disabled in settings
            audience=settings.JWT_AUDIENCE if settings.JWT_VALIDATE_AUD else None,
            issuer=settings.JWT_ISSUER if settings.JWT_VALIDATE_ISS else None,
        )
