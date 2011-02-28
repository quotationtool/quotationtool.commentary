import zope.interface
import zope.component
from zope.proxy import removeAllProxies
import zc.relation
from zope.intid.interfaces import IIntIds
from zope.exceptions.interfaces import UserError
from z3c.formui import form
from z3c.form import field
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.container.interfaces import INameChooser
from zope.traversing.browser import absoluteURL
import zc.resourcelibrary

from quotationtool.renderer.interfaces import IHTMLRenderer
from quotationtool.skin.interfaces import ITabbedContentLayout

from quotationtool.commentary import interfaces
from quotationtool.commentary.comment import Comment
from quotationtool.commentary.interfaces import _


class AddComment(form.AddForm):

    zope.interface.implements(ITabbedContentLayout)

    fields = field.Fields(interfaces.IComment).select('comment')

    label = _('comment-add-label', u"Add a comment")

    def __init__(self, context, request):
        super(AddComment, self).__init__(context, request)
        zc.resourcelibrary.need('quotationtool.tinymce.Comment')

    def create(self, data):
        obj = Comment()
        form.applyChanges(self, obj, data)
        obj.source_type = 'html'
        obj.about = removeAllProxies(self.context)

        # Grant the current user the Edit permission by assigning him
        # the quotationtool.Creator role, but only locally in the
        # context of the newly created object.
        manager = IPrincipalRoleManager(obj)
        manager.assignRoleToPrincipal(
            'quotationtool.Creator',
            self.request.principal.id)
    
        return obj

    def add(self, obj):
        container = zope.component.getUtility(
            interfaces.ICommentContainer,
            context = self.context,
            )
        self._name = INameChooser(container).chooseName(None, obj)
        container[self._name] = self._obj = obj

    def nextURL(self):
        return absoluteURL(self.context, self.request) + u"/@@comments.html"


class EditComment(form.EditForm):

    zope.interface.implements(ITabbedContentLayout)

    label = _('comment-edit-label', u"Change comment")

    fields = field.Fields(interfaces.IComment).select('comment', 'source_type')

