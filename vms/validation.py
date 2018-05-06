def is_empty(val=None):
    if not val:
        return  True
    if isinstance(val, str) and len(val) == 0:
        return True
    return False
