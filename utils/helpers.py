__all__ = ['deep_merge', 'safe_get']

def deep_merge(a: dict, b: dict) -> dict:
    """
    Recursively merge dict b into dict a, preserving existing non-empty values.
    Returns a new merged dict.
    """
    result = dict(a)
    for key, value in b.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        elif key in result:
            # preserve non-empty strings or dicts from 'a' if 'b' is empty
            a_val, b_val = result[key], value
            if (isinstance(a_val, (str, dict, list)) and not a_val == '') and (
                value == '' or value == {} or value == [] or value is None
            ):
                continue  # skip overwrite
            result[key] = value
        else:
            result[key] = value
    return result

def safe_get(d, *keys, default=None):
    """
    Safely get a nested key from a dict.

    Example:
        safe_get(data, "user", "name", default="N/A")
    """
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return default
    return d