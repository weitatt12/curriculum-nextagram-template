import os
import peewee as pw
from models.base_model import BaseModel
from models.user import User


class FanIdol(BaseModel):
    fan = pw.ForeignKeyField(User, backref="idols")
    idol = pw.ForeignKeyField(User, backref="fans")
    approved = pw.BooleanField(default=False)

    class Meta:
        indexes = ((('fan', 'idol'), True),)
