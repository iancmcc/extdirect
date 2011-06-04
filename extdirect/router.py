import inspect
from xml.dom.minidom import getDOMImplementation

class DirectException(Exception):
    pass


try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise DirectException("No JSON library available. Please install"
                              " simplejson or upgrade to Python 2.6.")


class DirectRouter(object):
    """
    Basic Ext.Direct router class.

    Ext.Direct allows one to create an API that communicates with a single URL,
    which then routes requests to the appropriate method. The client-side API
    object matches the server-side API object.

    This base class parses an Ext.Direct request, which contains the name of
    the method and any data that should be passed, and routes the data to the
    approriate method. It then receives the output of that call and puts it
    into the data structure expected by Ext.Direct.

    Call an instance of this class with the JSON from an Ext.Direct request.
    """
    def __call__(self, body):
        """
        """
        # Decode the request data
        body = json.loads(body)
        self._body = body

        if isinstance(body, list):
            directRequests = body
        elif isinstance(body, dict):
            directRequests = [body]
        else:
            raise DirectException("Body is not a support type: %s" % body)

        responses = []

        for req in directRequests:
            responses.append(self._doRequest(req))

        if len(responses) == 1:
            responses = responses[0]

        return json.dumps(responses)

    def _doRequest(self, request):

        # Double-check that this request is meant for this class
        action = request.get('action')
        clsname = self.__class__.__name__
        if action != clsname:
            raise DirectException(("Action specified in request ('%s') is"
                                  " not named %s.") % (action, clsname))

        # Pull out the method name and make sure it exists on this class
        method = request.get('method')
        if not method:
            raise DirectException("No method specified. Is this a valid"
                                  " Ext.Direct request?")
        try:
            _targetfn = getattr(self, method)
        except AttributeError:
            raise DirectException("'%s' is not the name of a method on %s" % (
                method, clsname
            ))

        # Pull out any arguments. Sent as an array containing a hash map, so
        # get the first member.
        data = request.get('data')
        if not data:
            data = {}
        else:
            data = data[0]

        # Cast all keys as strings, in case of encoding or other wrinkles
        data = dict((str(k), v) for k,v in data.iteritems())
        self._data = data

        # Finally, call the target method, passing in the data
        result = _targetfn(**data)

        return {
            'type':'rpc',
            'tid': request['tid'],
            'action': action,
            'method': method,
            'result': result
        }


class DirectProviderDefinition(object):
    """
    Turns a L{DirectRouter} subclass into JavaScript object representing the
    config of the client-side API.

    Inspects the given subclass and retrieves the names of all public methods,
    then defines those as actions on the Ext.Direct provider, and creates the
    JS that adds the provider.

    See http://extjs.com/products/extjs/direct.php for a full explanation of
    protocols and features of Ext.Direct.
    """
    def __init__(self, routercls, url, ns=None, timeout=None, format="text/html"):
        """
        @param routercls: A L{DirectRouter} subclass
        @type routercls: class
        @param url: The url at which C{routercls} is available
        @type url: str
        @param ns: The client-side namespace in which the provider should live.
                   The provider will be available at [ns].[routercls.__name__].
                   For example, if ns is 'Zenoss.remote' and routercls is named
                   'EventConsole', client-side code would call
                   C{Zenoss.remote.EventConsole.my_method(params, callback)}.
        """
        self.routercls = routercls
        self.url = url
        self.ns = ns
        self.timeout = timeout
        self.format = format

    def _config(self):
        actions = []
        for name, value in inspect.getmembers(self.routercls):
            if name.startswith("_"):
                continue
            if inspect.ismethod(value):

                ## Update this when extdirect doesn't freak out when you specify
                ## actual lens (we're passing them all in as a single dict, so
                ## from the perspective of Ext.Direct they are all len 1)
                #args = inspect.getargspec(value)[0]
                #args.remove('self')
                #arglen = len(args)
                arglen = 1

                actions.append({'name':name, 'len':arglen})
        config = {
            'id': self.routercls.__name__,
            'type': 'remoting',
            'url': self.url,
            'actions': {
                self.routercls.__name__: actions
            }
        }
        if self.timeout:
            config['timeout'] = self.timeout
        if self.ns:
            config['namespace'] = self.ns
        return config

    def _xml(self):
        """
        Return the API definition as XML
        """
        config = self._config()['actions']
        impl = getDOMImplementation()
        doc = impl.createDocument(None, 'DirectAPI', None)
        try:
            for router_name, methods in config.iteritems():
                router_node = doc.createElement(router_name)
                methods_node = doc.createElement('methods')
                router_node.appendChild(methods_node)
                for method in methods:
                    meth_node = doc.createElement('method')
                    meth_node.setAttribute('name', method['name'])
                    meth_node.setAttribute('len', method['len'])
                    methods_node.appendChild(meth_node)
                doc.documentElement.appendChild(router_node)
            return doc.toxml()
        finally:
            doc.unlink()

    def _json(self):
        """
        Return the API definition as JSON
        """
        config = self._config()['actions']
        return json.dumps(config)

    def _js(self):
        return """
Ext.onReady(function(){
    Ext.Direct.addProvider(%s);
});
        """ % json.dumps(self._config())

    def _script(self):
        """
        Return a fully-formed script tag containing the definition.
        """
        return """
<script type="text/javascript">
%s
</script>
        """ % self._js()

    def render(self):
        """
        Generate and return an Ext.Direct provider definition, wrapped in a
        <script> tag and ready for inclusion in an HTML document.
        """
        renderers = {
            'text/html': self._script,
            'text/javascript': self._js,
            'application/xml': self._xml,
            'application/json': self._json
        }
        if self.format not in renderers:
            raise DirectException("%s is an unknown format for the API.") % self.format
        return renderers[self.format]()

