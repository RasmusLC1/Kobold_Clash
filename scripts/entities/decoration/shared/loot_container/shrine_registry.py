SHRINE_REGISTRY = {}

def Register_Light_Source(key):
    def decorator(cls):
        SHRINE_REGISTRY[key] = cls
        return cls
    return decorator