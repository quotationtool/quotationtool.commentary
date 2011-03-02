import zope.component
from zope.viewlet.viewlet import ViewletBase
from zope.schema import getValidationErrors
import zc.relation
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class IsCommentedFlag(ViewletBase):

    template = ViewPageTemplateFile('iscommented.pt')
    
    def count(self):
        cat = zope.component.getUtility(
            zc.relation.interfaces.ICatalog,
            context = self.context)
        comments = list(cat.findRelations(
            cat.tokenizeQuery({'icomment-about': self.context})
            ))
        return len(comments)

    def render(self):
        return self.template()
