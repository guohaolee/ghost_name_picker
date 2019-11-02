from fireo.fields import TextField, NumberField, IDField, DateTime
from fireo.models import Model

class User(Model):
    id = IDField()
    name = TextField()
    email = TextField()
    profile_pic = TextField()
    last_login = DateTime()

    class Meta:
        collection_name = 'users'
