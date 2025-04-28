def filter_none_values(d: dict) -> dict:
    """
    Returns a new dictionary excluding keys with None values.

    Args:
        d (dict): The original dictionary.

    Returns:
        dict: A new dictionary with all None-value keys removed.
    """
    return {k: v for k, v in d.items() if v is not None}