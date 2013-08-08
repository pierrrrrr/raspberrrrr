class Tunnel:
    def __init__(self, source, source_port, sink, sink_port):
        self.source = source
        self.source_port = source_port
        self.sink = sink
        self.sink_port = sink_port

    def flush(self):
        self.source.flush_port(self.source_port)
        self.source.events.wait('command_complete')
        self.sink.flush_port(self.sink_port)
        self.sink.events.wait('command_complete')

    def disable(self):
        self.source.disable_port(self.source_port)
        self.sink.disable_port(self.sink_port)

    #def teardown(self):
    #    self.source.teardown(self.source_port)
    #    self.sink.teardown(self.sink_port)
