import time
from itertools import count
from ctypes import byref, cast, sizeof
from ctypes import pointer

from collections import defaultdict

from core.openmax import *
import core.event
import core.buffering
import core.tunneling

from . import utils
from .utils import ensure



NAME_PREFIX = 'OMX.broadcom.'



class Component(object):
    def __init__(self, name):
        self.name = name

        self.app_data_p = c_char_p('some stuff')
        self.handle_p = c_handle_p()

        self.events = core.event.Manager(self)
        self.buffers = core.buffering.Manager(self)

        name = NAME_PREFIX + self.name
        callbacks_p = byref(self.events.callbacks)
        ensure(openmax.OMX_GetHandle(byref(self.handle_p), name, self.app_data_p , callbacks_p))

    def __repr__(self):
        return "<{}({!r})>".format(type(self).__name__, self.name)

    def wait_for(self, flag):
        return self.events.wait(flag)

    def get_state(self):
        state = c_int(0xaffedead)
        ensure(self.handle_p[0].GetState(self.handle_p, byref(state)))
        return state.value

    def change_state(self, state):
        if self.get_state() == state:
            return self
        utils.log("transitioning to state: {}".format(state))

        ensure(self.handle_p[0].SendCommand(self.handle_p, OMX_CommandStateSet, state, 0))

        for count in range(10):
            if self.get_state() == state:
                return self
            time.sleep(0.2)
        raise ValueError("state not reached")

    def get_ports(self, domain_index_param):
        ports = OMX_PORT_PARAM_TYPE()
        ports.nSize = 4*4
        ports.nVersion = OMX_VERSION
        ports_p = cast(pointer(ports), c_void_p)  # Use byref?
        ensure(self.handle_p[0].GetParameter(self.handle_p, domain_index_param, ports_p))
        assert ports.nSize == 4*4
        return ports

    def get_port_definition(self, port):
        portdef = OMX_PARAM_PORTDEFINITIONTYPE()
        portdef.nSize = 24*4
        portdef.nVersion = OMX_VERSION
        portdef.nPortIndex = port
        portdef_p = pointer(portdef)
        ensure(self.handle_p[0].GetParameter(self.handle_p, OMX_IndexParamPortDefinition, cast(portdef_p ,c_void_p)))
        assert portdef.nSize == 24*4
        return portdef

    def set_port_definition(self, port, portdef):
        portdef.nPortIndex = port
        ensure(self.handle_p[0].SetParameter(self.handle_p, OMX_IndexParamPortDefinition, cast(pointer(portdef), c_void_p)))
        assert portdef.nSize == 24*4
        return portdef

    def get_inout_ports(self, domain_index_param):
        ports = self.get_ports(domain_index_param)
        assert ports.nPorts == 2
        return ports.nStartPortNumber, ports.nStartPortNumber + 1

    def disable_port(self,x):
        ensure(self.handle_p[0].SendCommand(self.handle_p, OMX_CommandPortDisable, x, 0))
        return self

    def enable_port(self,x):
        ensure(self.handle_p[0].SendCommand(self.handle_p, OMX_CommandPortEnable, x, 0))
        return self

    def flush_port(self,x):
        ensure(self.handle_p[0].SendCommand(self.handle_p, OMX_CommandFlush, x, 0))
        return self

    def empty_this_buffer(self, buffer_header_p):
        return self.handle_p[0].EmptyThisBuffer(self.handle_p, buffer_header_p)

    def fill_this_buffer(self, buffer_header_p):
        utils.log("asking to fill: {}".format(buffer_header_p))
        return self.handle_p[0].FillThisBuffer(self.handle_p, buffer_header_p)

    def free_buffer(self, port, header_p):
        return self.handle_p[0].FreeBuffer(self.handle_p, port, header_p)

    def free_buffers(self, port):
        for header_p in self.buffers.available[port]:
            ensure(self.free_buffer(port, header_p))

    def allocate_buffer(self, header_p, *args):
        return self.handle_p[0].AllocateBuffer(self.handle_p, header_p, *args)

    def allocate_buffers(self, portdef):
        count, port, size = portdef.nBufferCountActual, portdef.nPortIndex, portdef.nBufferSize

        utils.log("allocating required buffers: {} (min: {})  on: {} on port: {}"
                  .format(count, portdef.nBufferCountMin, self, port))

        for x in range(count):
            header_p = c_buffer_header_p()
            ensure(self.allocate_buffer(header_p, port, c_void_p(), size))
            utils.log("* buffer: {} allocated".format(x+1))
            self.buffers.available[port].append(header_p)

    def transition_to_idle(self):
        return self.change_state(OMX_StateIdle)

    def transition_to_executing(self):
        return self.change_state(OMX_StateExecuting)

    def ensure_loaded(self):
        assert self.get_state() == OMX_StateLoaded
        utils.log("component: {} in state: {}".format(self, 'loaded'))

    def ensure_idle(self):
        assert self.get_state() == OMX_StateIdle
        utils.log("component: {} in state: {}".format(self, 'idle'))

    def ensure_executing(self):
        assert self.get_state() == OMX_StateExecuting
        utils.log("component: {} in state: {}".format(self, 'executing'))

    def tunnel(self, source_port, sink, sink_port):
        self.ensure_idle()

        #self.disable_port(source_port)
        #sink.disable_port(sink_port)

        ps = OMX_PARAM_U32TYPE()
        ps.nSize = 4*4
        ps.nVersion = OMX_VERSION
        ps.nPortIndex = source_port
        ps_p = pointer(ps)
        result = self.handle_p[0].GetParameter(self.handle_p, OMX_IndexParamNumAvailableStreams, cast(ps_p, c_void_p))
        if result == 0:
            if ps.nU32 == 0:
                raise ValueError("no streams available")
            ps.nU32 = 0
            assert ps.nSize==16
            ensure(self.handle_p[0].SetParameter(self.handle_p, OMX_IndexParamActiveStream, cast(ps_p, c_void_p)))

        ensure(openmax.OMX_SetupTunnel(self.handle_p, source_port, sink.handle_p, sink_port))

        self.enable_port(source_port)
        sink.enable_port(sink_port)

        return core.tunneling.Tunnel(self, source_port, sink, sink_port)

    def get_all_port_formats(self, port_index):
        formats = []
        try:
            for n in count():
                formats.append(self.get_port_format(port_index, n))
        except ValueError:
            return formats

class ImageReader(Component):
    def __init__(self):
        super(ImageReader, self).__init__('image_read')

    def set_conent_uri(self, uri):
        uri += '\0'
        uri_s = OMX_PARAM_CONTENTURITYPE()
        uri_s.nSize = 8+len(uri)
        uri_s.nVersion= OMX_VERSION
        uri_s.contentURI = uri
        uri_p = ctypes.pointer(uri_s)
        ensure(self.handle_p[0].SetParameter(self.handle_p, OMX_IndexParamContentURI, cast(uri_p,c_void_p)))

class VideoRenderer(Component):
    def __init__(self):
        super(VideoRenderer, self).__init__('video_render')

    def get_port_format(self, port_index, index=None):
        portformat = OMX_VIDEO_PARAM_PORTFORMATTYPE()
        portformat.nSize = sizeof(portformat)
        portformat.nVersion = OMX_VERSION
        portformat.nPortIndex = port_index

        if index is not None:
            portformat.nIndex = index

        portformat_p = cast(pointer(portformat), c_void_p)
        result = self.handle_p[0].GetParameter(self.handle_p, OMX_IndexParamVideoPortFormat, portformat_p)
        ensure(result)

        return portformat


class Image(Component):
    def set_port_format(self, port_index, compression=None, color=None):
        portformat = OMX_IMAGE_PARAM_PORTFORMATTYPE()
        portformat.nSize = sizeof(portformat)
        portformat.nVersion = OMX_VERSION
        portformat.nPortIndex = port_index

        if compression is not None:
            portformat.eCompressionFormat = compression
        if color is not None:
            portformat.eColorFormat = color

        portformat_p = cast(pointer(portformat), c_void_p)
        ensure(self.handle_p[0].SetParameter(self.handle_p, OMX_IndexParamImagePortFormat, portformat_p))

    def get_port_format(self, port_index, index=None):
        portformat = OMX_IMAGE_PARAM_PORTFORMATTYPE()
        portformat.nSize = sizeof(portformat)
        portformat.nVersion = OMX_VERSION
        portformat.nPortIndex = port_index

        if index is not None:
            portformat.nIndex = index

        portformat_p = cast(pointer(portformat), c_void_p)
        ensure(self.handle_p[0].GetParameter(self.handle_p, OMX_IndexParamImagePortFormat, portformat_p))

        return portformat


