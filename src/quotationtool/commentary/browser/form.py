import zope.interface
import zope.component
from zope.proxy import removeAllProxies
import zc.relation
from zope.intid.interfaces import IIntIds
from zope.exceptions.interfaces import UserError
from z3c.formui import form
from z3c.form import field
from z3c.form.interfaces import DISPLAY_MODE
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


class SimpleEditForm(form.EditForm):

    label = _('comment-edit-label', u"Change comment")

    fields = field.Fields(interfaces.IComment).select('comment')#, 'source_type')

    def __init__(self, context, request):
        super(SimpleEditForm, self).__init__(context, request)
        zc.resourcelibrary.need('quotationtool.tinymce.Comment')

    def updateWidgetsOFF(self):
        super(SimpleEditForm, self).updateWidgets()
        self.widgets['source_type'].mode = DISPLAY_MODE

    def nextURL(self):
        return absoluteURL(self.context.about, self.request)


class EditFormOFF(form.EditForm):
    """ Edit the comment in the context of the commented item.

    TODO: How to get permission right???"""

    zope.interface.implements(ITabbedContentLayout)

    label = _('comment-edit-label', u"Change comment")

    fields = field.Fields(interfaces.IComment).select('comment')#, 'source_type')

    def __init__(self, context, request):
        super(SimpleEditForm, self).__init__(context, request)
        zc.resourcelibrary.need('quotationtool.tinymce.Comment')

    def getContent(self):
        comment_id = self.request.form.get('id', None)
        try:
            comment_id = int(comment_id)
            intids = zope.component.getUtility(
                IIntIds, context=self.context)
            self.comment = intids.queryObject(id, default = None)
            if not interfaces.IComment.providedBy(self.comment):
                raise Exception
        except:
            raise UserError(_(u"Invalid object ID"))
        return self.comment

    def updateWidgetsOFF(self):
        super(SimpleEditForm, self).updateWidgets()
        self.widgets['source_type'].mode = DISPLAY_MODE

    def nextURL(self):
        return absoluteURL(self.context.about, self.request)
