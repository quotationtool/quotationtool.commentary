import zope.component
import zc.relation

from quotationtool.site.interfaces import INewQuotationtoolSiteEvent
import quotationtool.relation
import interfaces


@zope.component.adapter(INewQuotationtoolSiteEvent)
def createCommentRelationIndex(event):
    """Create a new relation index when a new site is created."""
    cat = zope.component.getUtility(
        zc.relation.interfaces.ICatalog,
        context = event.object)
    cat.addValueIndex(
        interfaces.IComment['about'],
        dump = quotationtool.relation.dump,
        load = quotationtool.relation.load,
        name = 'icomment-about')
