# -*- coding: utf-8 -*-


def normalize(val: str):
    """
    Normalize a string value.
    """

    val = val.replace("'", "")
    return (val.isdecimal() and int(val) or float(val)) if val.isnumeric() else val
