from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=True)
    fullname = pw.TextField(null=False)
    email = pw.TextField(unique=True)
    password = pw.TextField(null=False)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def validate(self):
        duplicate_username = User.get_or_none(User.name == self.name)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username and duplicate_username.id != self.id:
            self.errors.append('Username not unique.')

        if duplicate_email and duplicate_email.id != self.id:
            self.errors.append('Email not unique.')



