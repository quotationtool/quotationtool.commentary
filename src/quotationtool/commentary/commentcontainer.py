import zope.interface
import zope.component
from zope.container.btree import BTreeContainer
from zope.schema.fieldproperty import FieldProperty
from zope.exceptions.interfaces import UserError
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.container.contained import NameChooser
from zope.container.interfaces import INameChooser

import interfaces
from quotationtool.site.interfaces import INewQuotationtoolSiteEvent


class CommentContainer(BTreeContainer):
    """An implementation of a container for comments."""

    zope.interface.implements(interfaces.ICommentContainer,
                              interfaces.ICommentaryContainer)

    __name__ = __parent__ = None

    _count = FieldProperty(interfaces.ICommentContainer['_count'])

    def __setitem__(self, key, value):
        super(CommentContainer, self).__setitem__(key, value)
        self._count += 1
            

class CommentNameChooser(NameChooser):
    """ A name chooser for comment objects in the container."""
    
    zope.interface.implements(INameChooser)
    zope.component.adapts(interfaces.ICommentContainer)

    def chooseName(self, name, obj):
        self.checkName(unicode(self.context._count + 1), obj)
        return unicode(self.context._count + 1)


@zope.component.adapter(INewQuotationtoolSiteEvent)
def createCommentContainer(event):
    site = event.object
    site['comments'] = comments = CommentContainer()
    sm = site.getSiteManager()
    sm.registerUtility(
        comments,
        interfaces.ICommentContainer)
    
    IWriteZopeDublinCore(comments).title = u"Comments"

