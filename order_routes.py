from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from repository.OrderRepo import admin_delete_order_repo, admin_update_order_repo, create_order_repo, index_repo, show_order_repo, show_user_order_repo, update_order_repo
from utils.auth_utils import get_current_user
from sqlmodel import select
from models.models import User
from database import SessionDep
from models.models import Order
from schemas.OrderSchema import AdminUpdateOrder, OrderModel, OrderResponse, UserOrderResponse, UserUpdateOrder

order_router = APIRouter(
    prefix="/order",
    tags=["Order"]
)


@order_router.post('/create-order', response_model=OrderResponse)
async def create_order(request:OrderModel, session: SessionDep, current_user : Annotated[User, Depends(get_current_user)]):
    """
        # Placing an Order
        This requires the following fields
        - quantity : integer
        - pizza_size: str

    """
    
    
    return await create_order_repo(request, session, current_user)


@order_router.get("/", response_model=list[OrderResponse])
async def index(session: SessionDep, current_user : Annotated[User, Depends(get_current_user)]):
    """
        # Listing  all Orders
        Admin/Staff only.

    """    
    return await index_repo(session, current_user)

@order_router.get("/{order_id}", response_model=OrderResponse)
async def show(order_id:str, session: SessionDep, current_user : Annotated[User, Depends(get_current_user)]):
    """
        # Getting an order by Id
        Admin/Staff only.

    """
    return await show_order_repo(order_id, session, current_user)

@order_router.get("/user/orders", response_model=list[UserOrderResponse])
async def userOrders(session: SessionDep, current_user : Annotated[User, Depends(get_current_user)]):
    """
        # List order made by currently authenticated user

    """
    
    return current_user.orders
    # statement = select(Order).where(Order.user_id == current_user.id)
    # return session.exec(statement).all()


@order_router.get("/user/order/{order_id}", response_model=UserOrderResponse)
async def showUserOrder(order_id:int, session: SessionDep, current_user : Annotated[User, Depends(get_current_user)]):
    """
        ## GET a specific order by the currently logged in User

    """
    
    return await show_user_order_repo(order_id, session, current_user)


@order_router.patch("/user/orders/{order_id}", response_model=UserOrderResponse)
async def updateOrder(order_id:int, request: UserUpdateOrder,  session: SessionDep, current_user : Annotated[User, Depends(get_current_user)]):
    """
        ## Updating a specific order by the currently logged in User
        It requires the following fields
        - quantity :int
        - pizza_size : SMALL|MEDIUM|LARGE  field value must be one of this values

        Request would throw an error if order has been processed already

    """
    return await update_order_repo(order_id, request, session, current_user)


@order_router.patch("/admin/orders/{order_id}", response_model=UserOrderResponse)
async def adminUpdateOrder(order_id:int, request: AdminUpdateOrder,  session: SessionDep, current_user : Annotated[User, Depends(get_current_user)]):
    """
        ## Updating a specific order by the Admin
        Admin Only
        It requires the following fields
        - order_status : PENDING|IN-TRANSIT|DELIVERED  field value must be one of this values

        Request would throw an error if order has been processed already

    """
    return await admin_update_order_repo(order_id, request, session, current_user)



@order_router.delete("/admin/orders/{order_id}", status_code=204)
async def adminDeleteOrder(order_id:int, session: SessionDep, current_user : Annotated[User, Depends(get_current_user)]):
    """
        ## Deleting a specific order by the Admin
        Admin Only
        It requires the following fields
        - order_id (url parameter)


    """     
    await admin_delete_order_repo(order_id, session, current_user)



