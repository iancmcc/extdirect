import os

from django import template

from extdirect.router import DirectProviderDefinition
from extdirect.django import registry

register = template.Library()

def do_direct_providers(parser, token):
    tokens = token.split_contents()
    return ScriptNode()

class ScriptNode(template.Node):
    def render(self, context):
        js = []
        for klass, name, ns in registry.classes():
            js.append(DirectProviderDefinition(
                klass, '/extdirect/%s/' % name, ns).render())
        return '\n'.join(js)

register.tag('direct_providers', do_direct_providers)
