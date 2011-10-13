import zope.interface
import zope.component
from z3c.table import table, column
from z3c.table.interfaces import ITable, IColumn
from zope.contentprovider.interfaces import IContentProvider
from z3c.pagelet.browser import BrowserPagelet
from zope.dublincore.interfaces import IZopeDublinCore
from zope.authentication.interfaces import IAuthentication
from zope.proxy import removeAllProxies
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.intid.interfaces import IIntIds
from zope.i18n import translate

from quotationtool.renderer.interfaces import IHTMLRenderer

from quotationtool.commentary.interfaces import _


class ICommentsTable(ITable):
    """A table representing a collection of comments."""


class CommentaryTable(table.Table, BrowserPagelet):
    """ The comments in the commentary container."""

    zope.interface.implements(ICommentsTable)

    render = BrowserPagelet.render

    cssClasses = {
        'table': u'container-listing',
        'thead': u"head",
        }
    cssClassEven = u"even"
    cssClassOdd = u"odd"


class ISortingColumn(IColumn):
    """ A column that provides sorting table rows."""


class TextColumn(column.Column):
    """ The text column of a comments table."""

    #zope.interface.implements(ISortingColumn)

    header = _('commentary-columnheader-text',
               u"Text")
    weight = 100
    
    limit = 200

    def renderCell(self, item):
        source = zope.component.createObject(
            item.source_type, 
            item.comment)
        renderer = zope.component.getMultiAdapter(
            (removeAllProxies(source), self.request),
            IHTMLRenderer, name = u'')
        intids = zope.component.getUtility(
            IIntIds, context=self.context)
        cid = intids.getId(item)
        cell = renderer.render(limit = self.limit)
        more_anchor = _('more-link', "[Read more]")
        cell += "<div><a href='%s'>%s</a></div>" % (
            absoluteURL(item.about, self.request)+'/@@comment.html?id='+unicode(cid)+'#tabs',
            translate(more_anchor, context=self.request, default=more_anchor))
        return cell


class CreatorColumn(column.Column):
    """ The creator column of a comments table."""

    zope.interface.implements(ISortingColumn)

    header = _('commentary-columnheader-creator',
               u"By")
    weight = 100
    
    def renderCell(self, item):
        creator = u"Unkown"
        dc = IZopeDublinCore(item, None)
        if dc is None:
            return creator
        pau = zope.component.queryUtility(
            IAuthentication,
            context = self.context
            )
        if pau is not None:
            try:
                creator = pau.getPrincipal(dc.creators[0]).title
            except Exception:
                pass
        return creator


class DCSortingColumn(object):
    """Mixin class for sorting unformatted dublincore values."""

    def getSortKey(self, item):
        dc = IZopeDublinCore(item, None)
        return self.getValue(dc)


class CreatedColumn(DCSortingColumn, column.CreatedColumn):
    """Column representing the dublincore created value. """

    zope.interface.implements(ISortingColumn)


class ModifiedColumn(DCSortingColumn, column.ModifiedColumn):
    """Column representing the dublincore modified value. """

    zope.interface.implements(ISortingColumn)

