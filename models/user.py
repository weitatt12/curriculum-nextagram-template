from models.base_model import BaseModel
import peewee as pw
import datetime
from werkzeug.security import generate_password_hash


class User(BaseModel):
    name = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    username = pw.CharField(unique=True)
    password = pw.CharField(null=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def validate(self):
        duplicate_users = User.get_or_none(User.name == self.name)
        duplicate_emails = User.get_or_none(User.email == self.email)

        if duplicate_users and duplicate_users.id != self.id:
            self.errors.append("User not valid")
        if duplicate_emails and duplicate_emails.id != self.id:
            self.errors.append("Email not valid")
        else:
            self.password = generate_password_hash(self.password)
