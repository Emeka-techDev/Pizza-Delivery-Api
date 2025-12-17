
from .constants import REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from database import SessionDep
from schemas.AuthSchema import TokenData, Token
from models.models import User




password_hash = PasswordHash.recommended()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


security = HTTPBearer()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(session: SessionDep, email: str):        
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user:
        return None
        # raise HTTPException(status_code=404, details={"user not found"})
    
    return user
   


def authenticate_user(session: SessionDep, email:str, password: str):
    user = get_user(session, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "type" : "access"          
    })

    print(f"encode jwt {to_encode}")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"type {payload.get("type")}")
        print(f"sub {payload.get("sub")}")

        if payload.get("type") != "access":  
            raise credentials_exception
        
        email = payload.get("sub")
        print(f"email is {email}")
       

        if email is None :            
            raise credentials_exception
        
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def create_refresh_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp" : expire,
        "type": "refresh",
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def validate_refresh_token(session: SessionDep, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    email = payload.get("sub")

    if email is None:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    user = get_user(session, email)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    new_access_token = await create_access_token({"sub": email})

    return  Token(
        access_token=new_access_token,
        refresh_token=token,
        token_type="bearer",
    )