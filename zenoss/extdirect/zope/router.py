from zope.publisher.browser import BrowserView
from zenoss.extdirect.router import DirectRouter

class ZopeDirectRouter(DirectRouter):
    def __call__(self):
        body = self.request.bodyStream.getCacheStream().getvalue()
        self.request.response.setHeader('Content-Type', 'application/json')
        return super(ZopeDirectRouter, self).__call__(body)
