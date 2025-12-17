from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select

from database import SessionDep
from models.models import User
from repository.UserRepo import create_user_repo, login_repo
from schemas.AuthSchema import Token
from schemas.UserSchema import LoginModel, SignUpModel, UserModel
from utils.auth_utils import authenticate_user, create_access_token, create_refresh_token, get_current_user, get_password_hash, validate_refresh_token
from sqlalchemy.exc import IntegrityError

security = HTTPBearer()

auth_router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.post('/user/create', response_model=UserModel)
async def createUser(request:SignUpModel, session: SessionDep):
    """
        ## Creating a User
        It requires the following fields
        ```
            username: str
            email: str 
            password: str 
            is_staff: bool = False   
            is_active: bool = False
        ```
    """ 
    return await create_user_repo(request, session)   

@auth_router.post('/login', response_model=Token)
async def login(request:LoginModel, session:SessionDep):
    """
        ## Login a User
        It requires the following fields
        ```
            - email: str 
            - password: str 
        ```
        and returns a token pare `access` and `refresh_token`
    """ 
    return await login_repo(request, session)
   
 


@auth_router.post("/refresh", response_model=Token)
async def refresh_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], session: SessionDep ):
    """
        ## Create a fresh token
        It creates access token. It requires a refresh token to be made in the header
    
    """ 
    return await validate_refresh_token(session, credentials)
    

