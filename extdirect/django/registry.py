_CLASS_REGISTRY = []

def classes():
    return _CLASS_REGISTRY

def register_router(klass, ns, name=None):
    if not name:
        name = klass.__name__
        tpl = (klass, name, ns)
        if tpl not in _CLASS_REGISTRY:
            _CLASS_REGISTRY.append(tpl)

