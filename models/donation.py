import os
import peewee as pw
from models.base_model import BaseModel
from models.user import User
from models.image import Image


class Donation(BaseModel):
    user = pw.ForeignKeyField(User, backref='donations', unique=False)
    image = pw.ForeignKeyField(Image, backref='donations')
    amount = pw.DecimalField(decimal_places=2)
