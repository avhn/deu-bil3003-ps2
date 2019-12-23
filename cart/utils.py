# -*- coding: utf-8 -*-


is_convertable = lambda x: False not in [s.isnumeric() for s in x.split('.')]


def normalize(val: str):
    """
    Normalize a string value.
    """
    val = val.replace("'", "")
    return (val.isdecimal() and int(val) or float(val)) if is_convertable(val) else val
