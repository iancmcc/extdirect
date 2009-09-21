from django.conf.urls.defaults import *
import registry

class UrlPatterns(object):
    def __iter__(self):
        urls = []
        for klass, name, ns in registry.classes():
            print klass, name, ns
            regex = r'%s/$' % name
            urls.append((regex, klass()))
        return (x for x in patterns('', *urls))

urlpatterns = UrlPatterns()
