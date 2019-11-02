from fireo.fields import TextField, NumberField, IDField, BooleanField
from fireo.models import Model

class GhostRecord(Model):

    id = IDField()
    name = TextField()
    description = TextField()
    picked = BooleanField(default=False)
    user_first_name = TextField(default=None)
    user_last_name = TextField(default=None)
    user_email = TextField(default=None)
    user_ghost_name = TextField(default=None)
    class_name = 'ghost_name'

    class Meta:
        collection_name = 'ghost_name'

    @classmethod
    def get_unallocated_ghost(cls):
        return cls.collection.filter('picked', '==', False).fetch()

    @classmethod
    def get_allocated_ghost(cls):
        return cls.collection.filter('picked', '==', True).fetch()

    @classmethod
    def get_single_ghost(cls, ghost):
        return cls.collection.get(f"{cls.class_name}/{ghost}")

    @classmethod
    def get_email_record(cls, email):
        return cls.collection.filter('user_email', '==', email).fetch()

    @classmethod
    def reset(cls, email):
        """ reset the record """
        record = cls.collection.filter('user_email', '==', email).fetch()
        for r in record:
            r.picked = False
            r.user_first_name = None
            r.user_last_name = None
            r.user_email = None
            r.user_ghost_name = None
            r.save()