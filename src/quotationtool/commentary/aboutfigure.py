# BBB: remove this in 0.2.0
import zope.interface
from zope.container.btree import BTreeContainer
from persistent import Persistent
from zope.schema.fieldproperty import FieldProperty
from zope.container.contained import Contained
import zope.component
import BTrees

import interfaces


class CommentAboutFigureContainer(BTreeContainer):
    """Implementation of a container for comments about figures."""

    zope.interface.implements(interfaces.ICommentaryContainer,
                              interfaces.ICommentAboutFigureContainer)

    __name__ = __parent__ = None



class CommentAboutFigure(Persistent, Contained):
    """Implementation of CommentAboutFigure object.
    """
    
    zope.interface.implements(interfaces.ICommentAboutFigure)

    __name__ = __parent__ = None

    figure = FieldProperty(interfaces.ICommentAboutFigure['figure'])
    _comment = FieldProperty(interfaces.ICommentAboutFigure['comment'])
    length = FieldProperty(interfaces.ICommentAboutFigure['length'])
    source_type = FieldProperty(interfaces.ICommentAboutFigure['source_type'])

    def getComment(self):
        return self._comment
    def setComment(self, val):
        self._comment = val
        self.length = len(val)
    comment = property(getComment, setComment)
