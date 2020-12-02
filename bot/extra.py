import json
from typing import Any

class DotDict(dict):
    """Access dictionary with dot notation.
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__