from sqlmodel import SQLModel
from database import engine
from models.models import User, Order  # import models

target_metadata = SQLModel.metadata