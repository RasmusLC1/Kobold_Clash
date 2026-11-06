# Global registry dictionary
DECORATION_REGISTRY = {}

def Register_Decoration(key):
    def decorator(cls): # cls = Classmethods
        DECORATION_REGISTRY[key] = cls
        return cls
    
    return decorator

