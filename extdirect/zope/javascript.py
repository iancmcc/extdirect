import zope.interface
from zope.viewlet.manager import WeightOrderedViewletManager
from interfaces import IExtDirectJavaScriptManager

class ExtDirectJavaScriptManager(WeightOrderedViewletManager):
    zope.interface.implements(IExtDirectJavaScriptManager)

