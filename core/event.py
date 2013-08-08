import time
from ctypes import c_int, c_void_p

from . import utils, openmax
from .openmax import CALLBACKS, c_app_data_p, c_handle_p
from .openmax import c_event_handler, c_fill_buffer_done, c_empty_buffer_done



class WaitTimeout(Exception):
    pass


class Manager(object):
    def __init__(self, component):
        self.component = component

        self.flags = {}

        self.callbacks = CALLBACKS()
        self.callbacks.EventHandler = c_event_handler(self.event_handler_callback)
        self.callbacks.EmptyBufferDone = c_empty_buffer_done(self.empty_buffer_done_callback)
        self.callbacks.FillBufferDone = c_fill_buffer_done(self.fill_buffer_done_callback)

    def clear(self, name):
        return self.flags.pop(name, False)

    # TODO: Make it possible to wait forever.
    def wait(self, name, timeout=1, period=0.01):
        left = timeout
        while left > 0:
            if name in self.flags:
                return self.clear(name)
            left -= period
            time.sleep(period)
        raise WaitTimeout(name)


    @utils.trace("event callback: {3}: {4}, {5}")
    def event_handler_callback(self, handle_p, app_data_p, event, data1, data2, event_data_p):
        if event == openmax.OMX_EventCmdComplete:
            self.flags['command_completed'] = True
        elif event == openmax.OMX_EventPortSettingsChanged:
            utils.log("*! port settings changed event")
            self.flags['port_settings_changed'] = True
        elif event == openmax.OMX_EventBufferFlag:
            utils.log("!! hurrah end of stream !!")
            self.flags['end_of_stream'] = True
        elif event == openmax.OMX_EventError:
            utils.log("error event: {}".format(hex(data1&0xffffffff)))
        else:
            utils.log("! unhandled event: {} {} {} {} {}"
                      .format(handle_p, app_data_p, event, data1, data2))
        return 0


    @utils.trace("fill buffer done callback")
    def fill_buffer_done_callback(self, handle_p, app_data_p, header_p):
        utils.dump("filled buffer", header_p[0])
        utils.log("** buffer contents: {!r}".format(header_p[0].get_buffer_p()[0][:64]))
        self.component.buffers.release(header_p)
        self.flags['buffer_filled'] = True
        return 0


    @utils.trace("empty buffer done callback")
    def empty_buffer_done_callback(self, handle_p, app_data_p, header_p):
        self.component.buffers.release(header_p)
        self.flags['buffer_emptied'] = True
        return 0

