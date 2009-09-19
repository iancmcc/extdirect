import zope.interface
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet.viewlet import JavaScriptViewlet
from interfaces import IExtDirectJavaScriptManager

class ExtDirectJavaScriptManager(WeightOrderedViewletManager):
    zope.interface.implements(IExtDirectJavaScriptManager)

ExtBaseViewlet = JavaScriptViewlet('ext-base.js')
ExtSourceViewlet = JavaScriptViewlet('ext-all.js')
