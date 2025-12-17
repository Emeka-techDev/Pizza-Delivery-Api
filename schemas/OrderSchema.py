from typing import Optional
from pydantic import BaseModel

from schemas.UserSchema import UserModel



class OrderModel(BaseModel):
    quantity: int
    order_status:Optional[str]="PENDING"
    pizza_size:Optional[str]="SMALL"

class OrderResponse(BaseModel):
    quantity: int
    order_status: str
    pizza_size: str
    user_id: int
    user: UserModel


class UserOrderResponse(BaseModel):
    quantity: int
    order_status: str
    pizza_size: str


class UserUpdateOrder(BaseModel):
    quantity: int
    pizza_size: str

class AdminUpdateOrder(BaseModel):
    order_status: str
  

    

