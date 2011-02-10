import unittest
import zope.component
import zope.interface
from zope.component.testing import setUp, tearDown, PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig
from zope.site.folder import rootFolder
import zope.publisher
from zope.security.testing import Principal
from zope.publisher.browser import TestRequest as ZopeTestRequest, BrowserView
from zope.publisher.interfaces.browser import IBrowserRequest
import z3c.form
from zope.container.interfaces import IContained
from persistent import Persistent
from zope.intid.interfaces import IIntIds

import quotationtool.commentary
from quotationtool.commentary.interfaces import ICommentable
from quotationtool.skin.interfaces import IQuotationtoolBrowserLayer


def setUpZCML(test):
    XMLConfig('configure.zcml', quotationtool.commentary)()
    XMLConfig('configure.zcml', quotationtool.commentary.browser)()


class DummyCommentable(Persistent):
    zope.interface.implements(ICommentable, IContained)
    __name__ = __parent__ = None


class DummyView(BrowserView):
    def __call__(self): return self.context.__name__


class IntIds(object):
    zope.interface.implements(IIntIds)

    d = {}

    def getId(self, obj):
        for key, val in self.d.values():
            if val == obj: return int(key)

    def getObject(self, id):
        return self.d[str(id)]


def generateContent():
    root = rootFolder()
    root['d1'] = d1 = DummyCommentable()
    assert(d1.__name__ == 'd1')
    assert(d1.__parent__ == root)
    root['c1'] = c1 = quotationtool.commentary.comment.Comment()
    c1.about = d1
    c1.source_type = 'plaintext'
    c1.comment = u"Hello World! Listen to dummy no 1."
    intids = IntIds()
    intids.d['1'] = d1
    intids.d['2'] = c1
    zope.component.provideUtility(intids, IIntIds)
    return root


class TestRequest(ZopeTestRequest):
    # we have to implement the layer interface which the templates and
    # layout are registered for. See the skin.txt file in the
    # zope.publisher.browser module.
    zope.interface.implements(
        z3c.form.interfaces.IFormLayer,
        IQuotationtoolBrowserLayer,
        IBrowserRequest
        )

    principal = Principal('testing')



class ViewTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        setUp(self)
        setUpZCML(self)

    def tearDown(self):
        tearDown(self)

    def OFFtest_BrowserViews(self):
        root = generateContent()
        request = TestRequest()

        from quotationtool.commentary.browser import view
        v = view.ListView(root['c1'], request)
        print v()
        self.assertTrue(isinstance(v(), unicode))
        


def test_suite():
    return unittest.TestSuite((
            unittest.makeSuite(ViewTests),
            ))
