from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property
import os

class User(BaseModel):
    name = pw.CharField(unique=True)
    fullname = pw.TextField(null=False)
    email = pw.TextField(unique=True)
    password = pw.TextField(null=False)
    profile_image = pw.TextField(null=True)
    bio = pw.TextField(null=True)
    private = pw.BooleanField(default=False)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def validate(self):
        duplicate_username = User.get_or_none(User.name == self.name)
        duplicate_email = User.get_or_none(User.email == self.email)

        if not User.get_or_none(User.id == self.id):

            if duplicate_username and duplicate_username.id != self.id:
                self.errors.append('Username not unique.')

            if duplicate_email and duplicate_email.id != self.id:
                self.errors.append('Email not unique.')

            else:
                self.password = generate_password_hash(self.password)


    @hybrid_property
    def profile_image_url(self):
        if self.profile_image:
            return os.environ.get('S3_LOCATION') + self.profile_image
        else:
            return os.environ.get('S3_LOCATION') + 'lFE32.jpg'


