import zope.interface
from z3c.menu.ready2go.item import ContextMenuItem


class ICommentableTab(zope.interface.Interface): pass
class CommentableTab(ContextMenuItem):
    zope.interface.implements(ICommentableTab)
