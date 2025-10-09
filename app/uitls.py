from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import jwt

from app.config import security_settings


def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(seconds=15),
) -> str:
    return jwt.encode(
        payload={
            **data,
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM],
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Expired token",
        )
    except jwt.PyJWTError:
        return None
