import zope.interface
import zope.component
from zope.component.factory import Factory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory

from quotationtool.renderer import plaintext, rest, html
from interfaces import  ICommentSourceFactory


htmlCommentFactory = Factory(
    html.HTMLSource,
    html.htmlSourceFactory.title,
    html.htmlSourceFactory.description
    )


plainTextCommentFactory = Factory(
    plaintext.PlainText,
    plaintext.plainTextFactory.title,
    plaintext.plainTextFactory.description
    )


restCommentFactory = Factory(
    rest.ReST,
    rest.restFactory.title,
    rest.restFactory.description,
    )


def CommentSourceTypeVocabulary(context):
    """Creates a vocabulary of all factories for commentary sources."""

    terms = []
    for name, factory in zope.component.getUtilitiesFor(ICommentSourceFactory):
        terms.append(SimpleTerm(name, title = factory.title))
    return SimpleVocabulary(terms)

zope.interface.alsoProvides(CommentSourceTypeVocabulary, IVocabularyFactory)
