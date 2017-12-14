# --encoding:utf-8--
import select
import socket

import os

import pwserver.tools as t
from pwserver import handler


class BaseServer(object):
    MAX_READS = 65537

    def __init__(self, address=None):
        self.server_name = None
        self.server_port = None
        self.address = address
        self.base_environ = None
        self.socket = None

    def activate_server(self):
        try:
            self.socket = socket.socket()
            self.socket.bind(self.address)
            self.socket.listen(1024)
            host, port = self.socket.getsockname()[:2]
            self.server_name = socket.getfqdn(host)
            self.server_port = port
            print('Server listen at %s:%s' % (self.server_name, str(self.server_port)))
        except socket.error as err:
            # print('Server Error: %s' % err.args)
            self.colse_server()
            return

    def run_server(self):
        try:
            self.waiting_request()
        finally:
            self.colse_server()

    def waiting_request(self):
        print('Waiting request...')
        while True:
            rdl, wrl, erl = select.select([self.socket], [], [])
            for req in rdl:
                conn, add = req.accept()
                print('Request from :%s:%d' % (add[0], add[1]))
                try:
                    self.handle_request(conn)
                except socket.error:
                    conn.close()

    def handle_request(self, conn):
        raise NotImplementedError

    def colse_server(self):
        print('Server is about to close...')
        self.socket.close()


class ConfigServer(BaseServer):
    def __init__(self, config):
        BaseServer.__init__(self)
        self.config = config
        self.handlercls = handler.ConfigFileHandler
        self.patterns = list()
        self.root = t.parser(config.subd('root'))
        self.read_config(config)
        self.activate_server()

    def read_config(self, config):
        listens = [i for i in config.find('listen')]
        if not listens:
            t.error('no port given')
        port = listens[0].replace(';', '').split()[1]
        self.address = ('', int(port))
        print('server port:%s' % port)

        names = [i for i in config.find('server_name')]
        if names:
            self.server_name = names[0]
            print(self.server_name)

        for loc in config.find('location'):
            if loc.args:
                if loc.args[0] in '= | ~ | ~* | ^~':
                    patt = loc.args[1]
                else:
                    patt = loc.args[0]
                self.patterns.append((patt, loc))

    def handle_request(self, request):
        hdler = self.handlercls(request, self.patterns, {})
        hdler.handle()


class WSGIServer(BaseServer):
    def __init__(self, address, wsgiapp):
        BaseServer.__init__(self, address=address)
        self.wsgiapp = wsgiapp
        self.handlercls = handler.WSGIHandler
        self.activate_server()
        self.setup_environ()

    def setup_environ(self):
        env = self.base_environ = dict(os.environ.items()).copy()
        env['SERVER_NAME'] = self.server_name
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PORT'] = str(self.server_port)
        env['REMOTE_HOST'] = ''
        env['CONTENT_LENGTH'] = ''
        env['SCRIPT_NAME'] = ''

    def handle_request(self, request):
        hdler = self.handlercls(request, self.wsgiapp, self.base_environ.copy())
        hdler.handle()


class _TestServer(BaseServer):
    def handle_request(self, request):
        hdler = handler.VeryBaseHandler(request)
        hdler.handle()


if __name__ == '__main__':
    tser = _TestServer(('', 8980))
    tser.activate_server()
    tser.run_server()
