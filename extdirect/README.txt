extdirect

To use this package, you must either have simplejson installed, or be using
Python 2.6 (which includes simplejson as the json package).

ExtJS 3.0 provides Ext.Direct, an extremely simple way to remote server-side
methods to the client side. extdirect provides a Python implementation
of a server-side Ext.Direct router, which can accept and parse Ext.Direct
request data, route it to the correct method, and create, encode and return the
proper data structure wrapping the results. extdirect also provides a
class that can generate the client-side JavaScript defining an Ext.Direct
provider from a router class.

For a full description of Ext.Direct's features, see:

    http://www.extjs.com/products/extjs/direct.php

You may download Ext and use it in your application normally; if you would
prefer, a stripped-down version including only resources necessary for
Ext.Direct is included with this package in the javascript directory, along
with instructions for building it from any version of Ext>=3.0.

Let's see how the server side works. First, we'll define a router:

    >>> from extdirect.router import DirectRouter
    >>> class TestUtils(DirectRouter):
    ...
    ...     def capitalize(self, word):
    ...         return word.upper()
    ...
    ...     def today(self):
    ...         return "Today is Wednesday."

We've defined two methods we want remoted to the client.

Although we don't have a real client in this test runner, here's how one would
generate the code that needs to be given to the client defining the provider.
Ignoring actual implementation, which would depend on the framework being used,
let's say we'll have this class available at URL '/utils', and we want our
client-side namespace containing these methods simply to be called 'Remote.'

    >>> from extdirect.router import DirectProviderDefinition
    >>> print DirectProviderDefinition(TestUtils, '/utils', 'Remote').render()
    <script type="text/javascript">
    Ext.onReady(function(){
        Ext.Direct.addProvider({
            type: 'remoting',
            url: '/utils',
            actions: {
                "TestUtils":[
                  {name:"capitalize", len:1},{name:"today", len:1}
                ]
            },
            namespace: 'Remote'
        });
    });
    </script>

Now, assuming that, one way or another, we've provided this code to the client
and our class is available at that URL, we are now able to access these methods
from the browser:
    
    Remote.TestUtils.capitalize({word:'foo'}, console.log)

That example would make a call to the 'capitalize' method on our TestUtils
class and feed the result to our callback, which in this case merely prints the
result to the JS console.

Let's see how that would work from the perspective of the server. That call
would make a POST request with a JSON-encoded body, so let's create that
manually:

    >>> from extdirect.router import json
    >>> data = {"action":"TestUtils","method":"capitalize","data":[{"word":"foo"}],"type":"rpc","tid":1}
    >>> body = json.dumps(data)

Our class name is passed in as "action", the method name as "method", and
whatever data we sent as a single-member array containing a hash of our
parameters. For our purposes, "type" will always be "rpc". Ext.Direct requests
also provide a transaction id ("tid") which may be used as you see fit to
handle the possibility of stale data.

Now, let's make an instance of our server-side class:

    >>> utils = TestUtils()

This instance is callable and accepts the request body, and returns a
JSON-encoded object exhibiting the structure expected by Ext.Direct on the
client:

    >>> utils(body)
    '{"tid": 1, "action": "TestUtils", "type": "rpc", "method": "capitalize", "result": "FOO"}'

Notice the "result", which is what we'd expect. The client would decode this
object and pass the "result" value to the callback. Just for fun, let's check
out our other defined method:

    >>> data = {"action":"TestUtils","method":"today","data":[],"type":"rpc","tid":1}
    >>> body = json.dumps(data)
    >>> resultob = json.loads(utils(body))
    >>> print resultob['result']
    Today is Wednesday.

