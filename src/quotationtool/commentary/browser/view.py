import zope.interface
import zope.component
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.proxy import removeAllProxies
import zc.relation
from zope.intid.interfaces import IIntIds

from quotationtool.renderer.interfaces import IHTMLRenderer


class MetaView(BrowserView):
    """ Show meta data on comment."""

    template = ViewPageTemplateFile('meta.pt')

    def __call__(self):
        return self.template()


class RenderComment(object):
    """A mixin class that provides a method for rendering the
    comment text."""

    limit = None #do not truncate 
    
    def renderComment(self):
        source = zope.component.createObject(
            self.context.source_type, 
            self.context.comment)
        renderer = zope.component.getMultiAdapter(
            (removeAllProxies(source), self.request),
            IHTMLRenderer, name = u'')
        return renderer.render(limit = self.limit)


class DetailsView(BrowserView, RenderComment):
    """The @@details view which can be called from within a zpt."""

    template = ViewPageTemplateFile('details.pt')

    bibliographyURL = None

    def __call__(self):
        return self.template()

    @property
    def comment(self):
        return self.context


class ListView(BrowserView, RenderComment):
    """The @@list view which can be called from within a zpt."""

    template = ViewPageTemplateFile('list.pt')

    limit = 200

    def __call__(self):
        return self.template()

    def id(self):
        ids = zope.component.getUtility(
            IIntIds, context = self.context)
        return ids.getId(self.context)



