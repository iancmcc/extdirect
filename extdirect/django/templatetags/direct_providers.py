import os

from django import template

from extdirect.router import DirectProviderDefinition
from extdirect.django import registry

register = template.Library()

def do_direct_providers(parser, token):
    tokens = token.split_contents()
    directSource = len(tokens)>1 and tokens[1]=='+direct.js'
    return ScriptNode(directSource)

class ScriptNode(template.Node):
    def __init__(self, directSource):
        self.directSource = directSource
    def render(self, context):
        js = []
        if self.directSource:
            import extdirect
            src = os.path.join(os.path.dirname(extdirect.__file__),
                               'javascript', 'direct.js')
            f = open(src)
            js.append('<script>%s</script>' % f.read())
            f.close()
        for klass, name, ns in registry.classes():
            js.append(DirectProviderDefinition(
                klass, '/extdirect/%s/' % name, ns).render())
        return '\n'.join(js)

register.tag('direct_providers', do_direct_providers)
