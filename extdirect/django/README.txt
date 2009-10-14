extdirect.django

A Django app providing an extdirect router

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

       If you don't have Ext on the page already, you can write a stripped-down
       version directly to the page by adding +direct.js to the template tag:

            {% direct_providers +direct.js %}

    6. That's it. You should now have access on that template to the remote
       methods:
            
            Remote.MyRouter.uppercase({word:'a word'}, callback);

        
