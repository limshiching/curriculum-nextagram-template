from models.base_model import BaseModel
from models.user import User
import peewee as pw
import os

class Donation(BaseModel):
    user = pw.ForeignKeyField(User, backref='donations', unique=False)
    amount = pw.DecimalField(decimal_places=2)
