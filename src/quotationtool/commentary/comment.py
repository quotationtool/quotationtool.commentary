import zope.interface
from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty
from zope.container.contained import Contained

import interfaces


class Comment(Persistent, Contained):
    """Implementation of comment."""

    zope.interface.implements(interfaces.IComment)

    __name__ = __parent__ = None

    about = FieldProperty(interfaces.IComment['about'])
    _comment = FieldProperty(interfaces.IComment['comment'])
    length = FieldProperty(interfaces.IComment['length'])
    source_type = FieldProperty(interfaces.IComment['source_type'])

    def getComment(self):
        return self._comment
    def setComment(self, val):
        self._comment = val
        self.length = len(val)
    comment = property(getComment, setComment)
