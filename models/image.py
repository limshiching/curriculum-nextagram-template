from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
import os

class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images', unique=False)
    image_path = pw.TextField(null=True)

    @hybrid_property
    def image_path_url(self):
        if self.image_path:
            return os.environ.get('S3_LOCATION') + self.image_path
