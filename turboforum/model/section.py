from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass
from session import DBSession
from auth import Group, User
from thread import Thread
from tg import predicates, request

__all__ = ['Section']

class Section(MappedClass):
    """
    Section definition.
    """
    class __mongometa__:
        session = DBSession
        name = 'sections'
        indexes = [('_view',),('_write',),('_moderate',),('_admin',),]

    _id = FieldProperty(s.ObjectId)
    display_name = FieldProperty(s.String)

    _view = ForeignIdProperty(Group, uselist=True)
    view = RelationProperty(Group, via='_view')

    _write = ForeignIdProperty(Group, uselist=True)
    write = RelationProperty(Group, via='_write')

    _moderate = ForeignIdProperty(User, uselist=True)
    moderate = RelationProperty(User, via='_moderate')

    _admin = ForeignIdProperty(User, uselist=True)
    admin = RelationProperty(User, via='_admin')

    _threads = ForeignIdProperty(Thread, uselist=True)
    threads = RelationProperty(Thread)

    @property
    def can_be_viewed(self):
        return predicates.in_any_group(self.view).check_authorization(request.environ)

    @property
    def can_be_written(self):
        return predicates.in_any_group(self.write).check_authorization(request.environ)

    @property
    def can_be_moderated(self):
        return predicates.in_any_group(self.moderate).check_authorization(request.environ)

    @property
    def can_be_administered(self):
        return predicates.in_any_group(self.admin).check_authorization(request.environ)