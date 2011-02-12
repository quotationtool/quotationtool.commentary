import zope.interface
import zope.component
from z3c.pagelet.browser import BrowserPagelet
from zope.proxy import removeAllProxies
import zc.relation
from zope.intid.interfaces import IIntIds
from zope.exceptions.interfaces import UserError

from quotationtool.renderer.interfaces import IHTMLRenderer
from quotationtool.skin.interfaces import ITabbedContentLayout

from quotationtool.commentary import interfaces
from quotationtool.commentary.interfaces import _


class CommentContainerFrontpage(BrowserPagelet):
    """A frontpage for the commentary container."""


class CommentsPagelet(BrowserPagelet):
    """A list of the comments about a commentable object.  This view
    takes a commentable object as context."""

    zope.interface.implements(ITabbedContentLayout)

    add_comment_option = True

    limit = 200

    def comments(self):
        """Returns a list of comments that are related to the
        commentable object in the context."""
        cat = zope.component.getUtility(
            zc.relation.interfaces.ICatalog,
            context = self.context)
        return sorted(cat.findRelations(
            cat.tokenizeQuery({'icomment-about': self.context})
            ))


class SingleCommentPagelet(BrowserPagelet):

    zope.interface.implements(ITabbedContentLayout)

    add_comment_option = True

    limit = None

    def __init__(self, context, request):
        super(SingleCommentPagelet, self).__init__(context, request)
        id = request.form.get('id', None)
        try:
            id = int(id)
            intids = zope.component.getUtility(
                IIntIds, context=self.context)
            self.comment = intids.queryObject(id, default = None)
            if not interfaces.IComment.providedBy(self.comment):
                raise Exception
        except:
            raise UserError(_(u"Invalid object ID"))
    
    def renderComment(self):
        source = zope.component.createObject(
            self.comment.source_type, 
            self.comment.comment)
        renderer = zope.component.getMultiAdapter(
            (removeAllProxies(source), self.request),
            IHTMLRenderer, name = u'')
        return renderer.render(limit = self.limit)
