# Global registry dictionary
EFFECT_REGISTRY = {}

def register_effect(key):
    def decorator(cls): # cls = Classmethods
        EFFECT_REGISTRY[key] = cls
        return cls
    
    return decorator



