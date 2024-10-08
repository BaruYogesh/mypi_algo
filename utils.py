from time import time
from uuid import uuid4
from typing import Union
import random

__all__ = ("get_time", "get_uuid")

def get_time(seconds_precision=True) -> Union[int, float]:
    """Returns the current time as Unix/Epoch timestamp, seconds precision by default"""
    return time() if not seconds_precision else int(time())


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())

def get_code() -> str:
    code_char = []

    for i in range(6):
        code_char.append(chr(random.randint(0, 25) + 65))

    return ''.join(code_char)
