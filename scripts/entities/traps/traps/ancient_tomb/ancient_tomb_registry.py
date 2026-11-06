TRAP_REGISTRY = {}
TRAP_TABLE = {}


def register_trap(key_or_keys, weight=None):
    def decorator(cls):
        keys_list = key_or_keys if isinstance(key_or_keys, (list, tuple)) else [key_or_keys]
        for key in keys_list:
            TRAP_REGISTRY[key] = cls
            if weight is not None:
                TRAP_TABLE[key] = weight
        return cls
    return decorator