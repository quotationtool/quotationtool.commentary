import zope.interface
import zope.component
from zope.container.btree import BTreeContainer
from zope.schema.fieldproperty import FieldProperty
from zope.exceptions.interfaces import UserError
from zope.dublincore.interfaces import IWriteZopeDublinCore

import interfaces
from i18n import _
from quotationtool.site.interfaces import INewQuotationtoolSiteEvent


class CommentContainer(BTreeContainer):
    """An implementation of a container for comments."""

    zope.interface.implements(interfaces.ICommentContainer,
                              interfaces.ICommentaryContainer)

    __name__ = __parent__ = None

    _count = FieldProperty(interfaces.ICommentContainer['_count'])

    def __setitem__(self, key, value):
        if key != unicode(_count + 1):
            raise UserError(_(u"You want to use $KEY as key for the comment, but it should be %COUNT!", mapping={'KEY': key, 'COUNT': self.count}))
        super(CommentContainer, self).__setitem(key, value)
        self._count += 1
            

@zope.component.adapter(INewQuotationtoolSiteEvent)
def createCommentContainer(event):
    site = event.object
    site['comments'] = comments = CommentContainer()
    sm = site.getSiteManager()
    sm.registerUtility(
        comments,
        interfaces.ICommentContainer)
    
    IWriteZopeDublinCore(comments).title = u"Comments"

