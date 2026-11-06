# Global registry dictionary
ABILITY_REGISTRY = {}

def register_ability(key):
    def decorator(cls): # cls = Classmethods
        ABILITY_REGISTRY[key] = cls
        return cls
    
    return decorator



