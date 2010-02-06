============
Introduction
============

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
    ... #doctest: +NORMALIZE_WHITESPACE
    <script type="text/javascript">
    Ext.Direct.addProvider({"url": "/utils",
        "namespace": "Remote",
        "type": "remoting",
        "id": "TestUtils",
        "actions": {"TestUtils": [{"name": "capitalize", "len": 1}, 
                                  {"name": "today", "len": 1}]}});
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


===========
Zope Router
===========

Using extdirect in Zope is extremely simple, due to a custom ZCML
directive that registers both a BrowserView for the server-side API and a
viewlet to deliver the provider definition to the client.

1. Define your class
   
   e.g., in myapi.py:

   from extdirect.zope import DirectRouter

   class MyApi(DirectRouter):

       def a_method(self):
           return 'A Value'


2. Register the class as a direct router

   <configure xmlns="http://namespaces.zope.org/browser">

     <include package="extdirect.zope" file="meta.zcml"/>

       <directRouter
          name="myapi"
          namespace="MyApp.remote"
          class=".myapi.MyApi"
          />

   </configure>


3. Provide the extdirect viewletManager in your template. 
   (Note: Ext is a prerequisite.)

    <tal:block tal:content="structure provider:extdirect"/>


4. Call methods at will!

    <script>

      function a_method_callback(result){
          ... do something with result ...
      }

      MyApp.remote.a_method({}, a_method_callback);

    </script>

=============
Django Router
=============

So, you have a Django app, and you want to add Ext.Direct. Here's how:

    1. Add 'extdirect.django' to INSTALLED_APPS in settings.py
    
    2. In a new file called direct.py, define your router class and register it:
    
            from extdirect.django import DirectRouter, register_router

            class MyRouter(DirectRouter):
                def uppercase(self, word):
                    return word.upper()
                def lowercase(self, word):
                    return word.lower()

            register_router(MyRouter, 'Remote')
        
       The arguments to register_router are the router class, the client-side
       namespace, and an optional url under /extdirect at which the router
       should be available (defaults to the name of the class).


    3. In the root URLconf, map the extdirect urls by adding:

        (r'^extdirect/', include('extdirect.django.urls'))

    4. Also in the root URLconf, add these two lines:

        import extdirect.django as extdirect
        extdirect.autodiscover()

    5. In your template, load the provider definitions:
        
            {% load direct_providers %}
            {% direct_providers %}

    6. That's it. You should now have access on that template to the remote
       methods:
            
            Remote.MyRouter.uppercase({word:'a word'}, callback);

        
