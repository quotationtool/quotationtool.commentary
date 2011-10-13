import zope.interface
import zope.component
from zope.viewlet.manager import ViewletManager
from z3c.menu.ready2go import ISiteMenu
from z3c.menu.ready2go.manager import MenuManager
from z3c.menu.ready2go.item import SiteMenuItem

from quotationtool.skin.interfaces import ISubNavManager
from quotationtool.skin.browser.nav import MainNavItem


class ICommentaryMainNavItem(zope.interface.Interface): 
    """ A marker interface for the commentary's item in the main navigation."""
    pass


class CommentaryMainNavItem(MainNavItem):
    """The commentary navigation item in the main navigation."""

    zope.interface.implements(ICommentaryMainNavItem)


class ICommentarySubNav(ISubNavManager):
    """A manager for the commentary subnavigation."""

CommentarySubNav = ViewletManager('commentarysubnav',
                                    ISiteMenu,
                                    bases = (MenuManager,))

ICommentarySubNav.implementedBy(CommentarySubNav)
