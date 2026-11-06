# Global registry dictionary
EFFECTS_REGISTRY = {}

def register_effect(key):
    def decorator(cls): # cls = Classmethods
        EFFECTS_REGISTRY[key] = cls
        return cls
    
    return decorator



