from __future__ import print_function

import time
import functools
from ctypes import Union, Structure


sleep = time.sleep


def _dump(structure, level=0, filling='  '):
    if level > 3:
        return
    for field, _ in structure._fields_:
        value = getattr(structure, field)
        print("{}{}: {!r}".format(filling*level, field, value))
        if isinstance(value, (Structure, Union)):
            _dump(value, level=level+1)

def dump(message, structure):
    print("{}: {}:".format(message, structure))
    _dump(structure, level=1)


def log(message, *args, **kwargs):
    return print(message.format(*args, **kwargs))

def trace(message):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
           #log("{}: args: {!r} kwargs: {!r}".format(message, args, kwargs))
            log("* {}".format(message.format(*args, **kwargs)))
            return function(*args, **kwargs)
        return wrapper
    return decorator


def ensure(result):
    if result == 0:
        return 0
    raise ValueError("failed with: {}".format(hex(result&0xffffffff)))


def read(path):
    log("reading path: {}".format(path))
    with open(path, 'rb') as f:
        data = f.read()
    log("* read data with length: {}".format(len(data)))
    return data

