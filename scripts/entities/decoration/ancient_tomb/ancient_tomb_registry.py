# Global registry dictionary
DECORATION_REGISTRY = {}

def register_ability(key):
    def decorator(cls): # cls = Classmethods
        DECORATION_REGISTRY[key] = cls
        return cls
    
    return decorator