from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int | None = Field(default=None, primary_key=True, index=True)
    username: str
    email: str = Field(unique=True)
    hashed_password: str 
    is_staff: bool = False   
    is_active: bool = False
    orders: list["Order"] = Relationship(back_populates="user")
  

class OrderStatus(str, Enum):
    PENDING = "pending"
    IN_TRANSIT = "in-transit"
    DELIVERED = "delivered"

class PIZZA_SIZES(str, Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra-large'


class Order(SQLModel, table=True):
    __tablename__ = 'orders'
    id: int | None = Field(default=None, primary_key=True)
    quantity: int = Field(nullable=False)
    order_status: OrderStatus = Field(default=OrderStatus.PENDING)
    pizza_size: PIZZA_SIZES = Field(default=PIZZA_SIZES.SMALL)
    user_id: int | None = Field(default=None, foreign_key="users.id")    
    user: User | None = Relationship(back_populates="orders")