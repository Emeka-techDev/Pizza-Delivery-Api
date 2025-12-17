from fastapi import HTTPException
from sqlmodel import select
from database import SessionDep
from models.models import User
from schemas.AuthSchema import Token
from schemas.UserSchema import LoginModel, SignUpModel
from utils.auth_utils import authenticate_user, create_access_token, create_refresh_token, get_password_hash
from sqlalchemy.exc import IntegrityError

async def login_repo(request:LoginModel, session:SessionDep):
    user = authenticate_user(session, request.email, request.password)
        
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    token = await create_access_token({"sub": user.email})
    refresh_token = await create_refresh_token({"sub": user.email})

    return Token(access_token=token, refresh_token=refresh_token, token_type="Bearer")

async def create_user_repo(request:SignUpModel, session: SessionDep):    
   
    db_email =  session.exec(
        select(User).filter(User.email==request.email)
    ).first()
    db_username=  session.exec(
        select(User).filter(User.username==request.username)
    ).first()

    if db_email is not None:
        raise HTTPException(status_code=422,  detail= "Email already exist")
    
    
    if db_username is not None:
        raise HTTPException(status_code=422,  detail= "Username already exist")
    

    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=get_password_hash(request.password),
        is_staff=request.is_staff,
        is_active=request.is_active
    )

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    
    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=500,  
            detail= "Unable to create user account")
    
    return new_user