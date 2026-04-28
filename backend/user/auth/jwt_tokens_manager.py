from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
from user.schemas import AccessTokenResponse, AccessTokenPayload
from database.config import settings

def create_access_token(user_id: int, login: str) -> AccessTokenResponse:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode = {
        'sub': str(user_id),
        'login': login,
        'exp': expire
    }

    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return AccessTokenResponse(access_token=token, login=login, user_id=user_id)


def decode_access_token(token: str) -> AccessTokenPayload | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get('sub')
        login = payload.get('login')

        if user_id is None or login is None:
            return None
        
        return AccessTokenPayload(user_id=int(user_id), login=login)
    
    except JWTError as e:
        print("JWTError:", e)
        return None
