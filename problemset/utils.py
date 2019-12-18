# -*- coding: utf-8 -*-

def normalize(val: str):
    """
    Normalize a string value.
    """
    
    val = val.replace("'", "")
    try:
        if val.isdecimal():
            val = int(val)
        else:
            val = float(val)
    except ValueError:
        pass

    return val
