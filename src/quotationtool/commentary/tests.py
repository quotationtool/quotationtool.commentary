import unittest
import doctest
import zope.interface
import zope.component
from zope.component.testing import PlacelessSetup, setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig

import quotationtool.commentary


def setUpZCML(self):
    """ We test ZCML here:
        >>> from zope.configuration.xmlconfig import XMLConfig
        >>> import quotationtool.commentary
        >>> XMLConfig('configure.zcml', quotationtool.commentary)()

    We also use this to bring up the config:
    """
    XMLConfig('configure.zcml', quotationtool.commentary)()


def setUpOnlySome(test):
    # we need a vocabulary of languages
    from quotationtool.commentary.source import plainTextCommentFactory, CommentSourceTypeVocabulary
    from quotationtool.commentary.interfaces import ICommentSourceFactory 
    zope.component.provideUtility(
        plainTextCommentFactory,
        ICommentSourceFactory,
        name = 'plaintext')
    from zope.schema import vocabulary
    from zope.schema.interfaces import IVocabularyFactory, IVocabulary
    vocabulary.setVocabularyRegistry(vocabulary.VocabularyRegistry())
    vr = vocabulary.getVocabularyRegistry()
    vr.register(
        'quotationtool.commentary.CommentSourceTypes', 
        CommentSourceTypeVocabulary)


class SourceTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(SourceTests, self).setUp()
        setUpZCML(self)

    def test_Types(self):
        import zope.schema
        field = zope.schema.Choice(
            title = u"source type",
            vocabulary = 'quotationtool.commentary.CommentSourceTypes')
        self.assertTrue(field.validate(u'plaintext') is None)
        self.assertTrue(field.validate(u'rest') is None)
        self.assertTrue(field.validate(u'html') is None)
        self.assertRaises(zope.schema.interfaces.ConstraintNotSatisfied, 
                          field.validate, (u'fails'))
        # if there is an other type registered in the renderer
        # package that is not known here, it should fail
        from quotationtool.renderer.plaintext import plainTextFactory
        from quotationtool.renderer.interfaces import ISourceFactory
        zope.component.provideUtility(
            plainTextFactory,
            provides = ISourceFactory,
            name = 'other_text_syntax')
        self.assertRaises(zope.schema.interfaces.ConstraintNotSatisfied, 
                          field.validate, (u'other_text_syntax'))
        # but it should be OK for quotationtool.renderer.SourceTypes
        rfield = zope.schema.Choice(
            title = u"source type",
            vocabulary = 'quotationtool.renderer.SourceTypes')
        self.assertTrue(rfield.validate('other_text_syntax') is None)

    def test_PlainText(self):
        """ Test if quotationtool.renderer still works."""
        quotation = zope.component.createObject('plaintext', u"Hello World!")
        from quotationtool.renderer.plaintext import PlainText
        self.assertTrue(isinstance(quotation, PlainText))


class SiteCreationTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(SiteCreationTests, self).setUp()
        setUpZCML(self)
        import quotationtool.site
        XMLConfig('configure.zcml', quotationtool.site)

    def test_ExampleContainer(self):
        """ Test if container is created on a new site event."""
        from quotationtool.site.site import QuotationtoolSite
        from zope.container.btree import BTreeContainer
        root = BTreeContainer()
        root['quotationtool'] = site = QuotationtoolSite()
        self.assertTrue('comments' in site.keys())
        from quotationtool.commentary.commentcontainer import CommentContainer
        self.assertTrue(isinstance(site['comments'], CommentContainer))
        from quotationtool.commentary.interfaces import ICommentContainer
        ut = zope.component.getUtility(
            ICommentContainer, 
            context = site)
        self.assertTrue(ut is site['comments'])

    def test_RelationIndex(self):
        """ Test if a relation index is created on a new site event."""
        from quotationtool.site.site import QuotationtoolSite
        from zope.container.btree import BTreeContainer
        root = BTreeContainer()
        root['quotationtool'] = site = QuotationtoolSite()
        from zc.relation.interfaces import ICatalog
        cat = zope.component.getUtility(
            ICatalog, context = site)
        # TODO
        #self.assertTrue('ifigure-reference' in list(cat.iterSearchIndexes()))


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            doctest.DocFileSuite('README.txt',
                                 setUp = setUpOnlySome,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            unittest.makeSuite(SourceTests),
            unittest.makeSuite(SiteCreationTests),
            ))
