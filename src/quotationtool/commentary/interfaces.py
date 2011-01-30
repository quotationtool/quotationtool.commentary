import zope.interface
import zope.schema
from zope.container.interfaces import IContained, IContainer
from zope.container.constraints import containers, contains

from i18n import _
from quotationtool.relation.schema import Relation


class ICommentSourceFactory(zope.interface.Interface):
    """A factory for a source format for a commentary texts (attribute
    'comment' of ICommentaryBase objects)."""
    

class ICommentaryBase(zope.interface.Interface):
    """A simple comment."""

    comment = zope.schema.Text(
        title = _('isimplecomment-comment-title',
                  u"Comment"),
        description = _('isimplecomment-comment-desc',
                        u"The comment text."),
        required = True,
        )

    source_type = zope.schema.Choice(
        title = _('isimplecomment-sourcetype-title', u"Text Format"),
        description = _('isimplecomment-sourcetype-desc',
                        u"Choose text format"),
        required = True,
        default = 'quotationtool.comment.plaintext',
        vocabulary = 'quotationtool.commentary.CommentSourceTypes',
        )

    length = zope.schema.Int(
        title = u"Lenght",
        description = u"Length in bytes of the quotation attribute. This is stored for performance reasons. It must be set automatically when quotation is set or modified.",
        required = True,
        )


class ICommentaryContainer(zope.interface.Interface):
    """The schema part of a container for comments."""


class ICommentable(zope.interface.Interface):
    """A marker interface for commentable objects."""
    

class IComment(IContained, ICommentaryBase):
    """Unified comment."""

    containers('.ICommentContainer')

    about = Relation(
        title = _('icomment-about-title',
                  u"About"),
        description = _('icomment-about-desc',
                        u"The item the comment is about."),
        precondition = [ICommentable],
        required = True,
        )


class ICommentContainer(IContainer):
    """A container for unified comments."""

    contains(IComment)

    _count = zope.schema.Int(
        title = _('icommentcontainer-count-title',
                  u"Count"),
        description = _('icommentcontainer-count-desc',
                        u"Number of comments yet added. This is used to choose the name of a comment. It is never decremented on comment deletion."),
        required = True,
        default = 0,
        )


### BBB: more specialized comments are deprecated. We only use
### unified comments.

class ICommentAboutFigure(ICommentaryBase):
    """A comment about a figure."""

    containers('.ICommentAboutFigureContainer')

    figure = Relation(
        title = _('icommentaboutfigure-figure-title',
                  u"Figure"),
        description = _('icommentaboutfigure-figure-desc',
                        u"The item, the comment is about."),
        precondition = [zope.interface.Interface],
        required = True,
        )


class ICommentAboutFigureContainer(IContainer):
    """The container part of a container for comments."""

    contains(ICommentAboutFigure)


class ICommentAboutReference(ICommentaryBase):
    """A comment about a figure."""

    containers('.ICommentAboutFigureContainer')

    figure = Relation(
        title = _('icommentaboutfigure-figure-title',
                  u"Figure"),
        description = _('icommentaboutfigure-figure-desc',
                        u"The item, the comment is about."),
        precondition = [zope.interface.Interface],
        required = True,
        )


class ICommentAboutReferenceContainer(IContainer):
    """The container part of a container for comments."""

    contains(ICommentAboutReference)
