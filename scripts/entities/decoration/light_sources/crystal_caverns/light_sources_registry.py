LIGHT_SOURCE_REGISTRY = {}
LIGHT_SOURCE_PROBABILITY = {}

def Register_Light_Source(key, probability):
    def decorator(cls):
        LIGHT_SOURCE_REGISTRY[key] = cls
        LIGHT_SOURCE_PROBABILITY[key] = probability
        return cls
    return decorator