Comments:
=========

This module provides classes that offer a commentary feature. It
allows the user to write comments on each object that is marked with a
special interface: ICommentable.

First, let's examine the schema of comments:

    >>> from quotationtool.commentary.interfaces import IComment
    >>> IComment.names()
    ['about', '__parent__']

    >>> from zope.schema import getFieldNames
    >>> getFieldNames(IComment)
    ['comment', 'source_type', 'about', '__name__', 'length', '__parent__']

Now, let's see how comment objects work. First create one.

    >>> from quotationtool.commentary.comment import Comment
    >>> comment = Comment()

When setting the comment attribute, the length attribute is calculated
automatically. This is for performance aspects (avoid calculating
length on each read...)

    >>> comment.comment = michel_says = u"""Thus Commentary averts the
    ...     chance element of discourse by giving it its due: it gives us
    ...     the opportunity to say something other than the text itself,
    ...     but on condition that it is the text itself which is uttered
    ...     and, in some ways, finalised."""

    >>> comment.length == len(michel_says)
    True

The source_type argument accepts values from a vocabulary:

    >>> comment.source_type = 'plaintext'


'about' attribute--commentable objects:
---------------------------------------

The about argument takes an object, but it is restricted to objects
that provide ICommentable. ICommentable is a marker interface. You can
use the classImplements method from zope.interface to even mark
classes that you did not write retroactively.

    >>> bad = object()
    >>> comment.about = bad
    Traceback (most recent call last):
    ...
    RelationPreconditionError

    >>> class Commentable(object):
    ...     pass

    >>> from quotationtool.commentary.interfaces import ICommentable
    >>> from zope.interface import classImplements
    >>> classImplements(Commentable, ICommentable)
    >>> commented = Commentable()
    >>> comment.about = commented


Container:
----------

Containment is restricted, too. Comment objects live in a comment
container.

    >>> from quotationtool.commentary.commentcontainer import CommentContainer
    >>> comments = CommentContainer()
    >>> from zope.container.constraints import checkObject
    >>> checkObject(comments, 'bad', bad)
    Traceback (most recent call last):
    ...
    InvalidItemType: (<quotationtool.commentary.commentcontainer.CommentContainer object at ...>, <object object at ...>, (<InterfaceClass quotationtool.commentary.interfaces.IComment>,))
    >>> checkObject(bad, 'comment', comment)
    Traceback (most recent call last):
    ...
    InvalidContainerType: (<object object at ...>, [<InterfaceClass quotationtool.commentary.interfaces.ICommentContainer>])

    >>> checkObject(comments, 'comment', comment)

