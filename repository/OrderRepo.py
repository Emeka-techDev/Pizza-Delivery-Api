from typing import Annotated

from fastapi import HTTPException

from database import SessionDep
from models.models import Order, User
from schemas.OrderSchema import AdminUpdateOrder, OrderModel, UserUpdateOrder
from sqlmodel import select



def check_is_staff(current_user: User):
    if not current_user.is_staff:
        raise HTTPException(status_code=403, detail="Only super admin can access this route")
    
    return True

async def create_order_repo(request:OrderModel, session: SessionDep, current_user : User):  
    new_order = Order(quantity=request.quantity, pizza_size=request.pizza_size, user_id=current_user.id)
    
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    return new_order

async def index_repo(session: SessionDep, current_user : User):
    check_is_staff(current_user)
    
    return session.exec(select(Order)).all()


async def show_order_repo(order_id:str, session: SessionDep, current_user : User):
    check_is_staff(current_user)
    
    order = session.get(Order, order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist for this user")
    
    return order


async def show_user_order_repo(order_id:int, session: SessionDep, current_user : User):
    
    statement = select(Order).where(Order.user_id == current_user.id).where(Order.id == order_id)
    order =  session.exec(statement).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist for this user")
    
    return order

async def update_order_repo(order_id:int, request: UserUpdateOrder,  session: SessionDep, current_user : User):
   
    statement = select(Order).where(Order.user_id == current_user.id).where(Order.id == order_id)
    order =  session.exec(statement).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist for this user")
    
    if order.order_status != "pending":
        raise HTTPException(status_code=400, detail="Order has already been processed")

    
    order.quantity = request.quantity
    order.pizza_size = request.pizza_size

    session.add(order)
    session.commit()
    session.refresh(order)

    return order


async def admin_update_order_repo(order_id:int, request: AdminUpdateOrder,  session: SessionDep, current_user : User):
   
    order =  session.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist for this user")

    
    order.order_status = request.order_status

    session.add(order)
    session.commit()
    session.refresh(order)

    return order

async def admin_delete_order_repo(order_id:int, session: SessionDep, current_user : User):  
    if not current_user.is_staff:
        raise HTTPException(status_code=403, detail="Only staff can access this route")
    
    order =  session.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist for this user")

    session.delete(order)
    session.commit()

