from models.base_model import BaseModel
import peewee as pw
import datetime
from werkzeug.security import generate_password_hash
import os
from playhouse.hybrid import hybrid_property


class User(BaseModel):
    name = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    username = pw.CharField(unique=True)
    password = pw.CharField(null=False)
    profile_image = pw.CharField(null=True)
    private = pw.BooleanField(default=False)

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
        if not self.id:  # this will help us to generate hash password for the FIRST TIME, other then go manually
            self.password = generate_password_hash(self.password)
            print('password hash generated')

    @hybrid_property
    def profile_image_url(self):
        if self.profile_image:
            return os.environ.get('S3_LOCATION') + self.profile_image
        else:
            return os.environ.get('S3_LOCATION') + 'markzukerberg.jpeg'
