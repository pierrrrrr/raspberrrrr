import time
from ctypes import memmove
from ctypes import pointer, cast
from ctypes import c_void_p

from collections import defaultdict
from contextlib import contextmanager

from . import utils
from .utils import ensure
from .openmax import OMX_BUFFERFLAG_EOS, OMX_BUFFERFLAG_TIME_UNKNOWN
from .openmax import CORE_BUFFERHEADER_EXTRATYPE



class Filler(object):
    def __init__(self, data, component, port):
        self.data = data

        self.component = component
        self.port = port

        self.filled = 0
        self.count = 0

    def rewind(self):
        self.filled = self.count = 0

    @property
    def length(self):
        return len(self.data)

    @property
    def left(self):
        return self.length - self.filled

    def fill_this_buffer(self, header_p, flags=0):
        assert header_p[0].nOffset == 0

        available = header_p[0].nAllocLen
        utils.log("? available: {} left: {}", available, self.left)
        fill = available if available < self.left else self.left

        utils.log("? moving from: {} to: {}", self.filled, self.filled+fill)
        memmove(header_p[0].pBuffer, self.data[self.filled:], fill)  # There's probably a better way.

        if available > self.left:
            utils.log("marking buffer with eos flag")
            flags |= OMX_BUFFERFLAG_EOS

        header_p[0].nFilledLen = fill
        header_p[0].nOffset = 0
        header_p[0].nFlags = flags

        ensure(self.component.empty_this_buffer(header_p))

        self.filled += fill
        self.count += 1

    def fill_one_buffer(self, *args, **kwargs):
        with self.component.buffers.acquire(self.port) as header_p:
            self.fill_this_buffer(header_p, *args, **kwargs)

    def fill_rest_of_data(self):
        while self.left > 0:
            self.fill_one_buffer()


# This could be simplified.
class Manager(object):
    def __init__(self, _):
        self.available = defaultdict(list)
        self.acquired = defaultdict(dict)

        self.aid = 0

    def generate_aid(self):
        self.aid = self.aid + 1
        return self.aid

    #
    # Buffer management using CORE_BUFFERHEADER_EXTRATYPE got a bit
    # out of hand...
    #

    def get(self, port, period=0.05):
        while True:
            try:
                header_p = self.available[port].pop()
            except IndexError:
                time.sleep(period)
            else:
                # TODO: Can we somehow avoid the bellow?
                if not cast(header_p[0].pAppPrivate, c_void_p).value:
                    header_p[0].pAppPrivate = pointer(CORE_BUFFERHEADER_EXTRATYPE())
                header_p[0].pAppPrivate[0].nAcquiredPortIndex = port
                header_p[0].pAppPrivate[0].nAid = self.generate_aid()
                self.acquired[port][self.aid] = header_p
                return header_p

    @utils.trace("acquiring buffer")
    @contextmanager
    def acquire(self, *args, **kwargs):
        yield self.get(*args, **kwargs)

    @utils.trace("releasing buffer")
    def release(self, header_p):
        # XXX: This should be done when allocating not acquring.
        try:
            port = header_p[0].pAppPrivate[0].nAcquiredPortIndex
        except ValueError:
            utils.log("  buffer never acquired: {}".format(header_p))
        else:
            aid = header_p[0].pAppPrivate[0].nAid
            self.available[port].append(self.acquired[port].pop(aid))

