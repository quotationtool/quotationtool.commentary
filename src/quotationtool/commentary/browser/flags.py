import zope.component
from zope.viewlet.viewlet import ViewletBase
from zope.schema import getValidationErrors
import zc.relation


class IsCommentedFlag(ViewletBase):
    
    def render(self):
        cat = zope.component.getUtility(
            zc.relation.interfaces.ICatalog,
            context = self.context)
        comments = list(cat.findRelations(
            cat.tokenizeQuery({'icomment-about': self.context})
            ))
        if len(comments) >= 1:
            return u'<span class="is-commented">C:%d</span>' % len(comments)
        return u""
