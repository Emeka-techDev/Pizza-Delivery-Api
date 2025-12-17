from fastapi import FastAPI
from auth_routes import auth_router
from database import create_db_and_tables
from order_routes import order_router
from models.models import User, Order #import models so they are included in db on start on

app = FastAPI()


#create db on start
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    print("Request received")
    return {"message": "API is running"}

app.include_router(auth_router)
app.include_router(order_router)

