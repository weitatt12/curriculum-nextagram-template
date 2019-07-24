import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property
import os


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    image_path = pw.TextField(null=True)

    @hybrid_property
    def image_path_url(self):
        return os.environ.get('S3_LOCATION') + self.image_path


# image.image_url
