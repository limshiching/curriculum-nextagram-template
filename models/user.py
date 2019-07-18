from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=True)
    fullname = pw.TextField(null=False)
    email = pw.TextField(unique=True)
    password = pw.TextField(null=False)
