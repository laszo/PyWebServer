# --encoding:utf-8--
import socket
import select
import threading
import multiprocessing
import os
import sys
import handler
import tools as t


def launch(address=None, wsgiapp=None, cfg_file=None):
    if cfg_file:
        config = t.config(cfg_file)
        servers = config.find('http.server')
        for server in servers:
            worker = multiprocessing.Process(target=runserver, args=(server, ))
            worker.start()
    if address and wsgiapp:
        # runwsgi(address, wsgiapp)
        worker = threading.Thread(target=runwsgi, args=(address, wsgiapp, ))
        worker.start()

def runserver(config):
    server = ConfigServer(config=config)
    server.run_server()

def runwsgi(address, wsgiapp):
    server = WSGIServer(address, wsgiapp)
    server.run_server()


class BaseServer(object):

    MAX_READS = 65537

    # todo 读取配置文件，或者指定配置项，包括几个工作进程，运行哪些server等，给进程起名字，便于管理
    def __init__(self, address=None):
        self.server_name = None
        self.server_port = None
        self.address = address
        self.base_environ = None
        self.socket = socket.socket()

    def activate_server(self):
        try:
            self.socket.bind(self.address)
            self.socket.listen(5)
            host, port = self.socket.getsockname()[:2]
            self.server_name = socket.getfqdn(host)
            self.server_port = port
            self.setup_environ()
            print 'Server listen at %s:%s' % (self.server_name, str(self.server_port))
        except socket.error as err:
            print 'Server Error:' + err.message
            self.colse_server()
            return

    def run_server(self):
        try:
            self.waiting_request()
        finally:
            self.colse_server()

    def setup_environ(self):
        env = self.base_environ = dict(os.environ.items()).copy()
        env['SERVER_NAME'] = self.server_name
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PORT'] = str(self.server_port)
        env['REMOTE_HOST'] = ''
        env['CONTENT_LENGTH'] = ''
        env['SCRIPT_NAME'] = ''

    def waiting_request(self):
        print 'Waiting request...'
        while True:
            rdl, wrl, erl = select.select([self.socket], [], [])
            for req in rdl:
                conn, add = req.accept()
                self.handle_request(conn)
                # t = threading.Thread(target=self.handle, args=(c, ))
                # t.start()

    def handle_request(self, conn):
        raise NotImplementedError

    def colse_server(self):
        print 'Server is about to close...'
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
        print 'server port:%s' % port

        names = [i for i in config.find('server_name')]
        if names:
            self.server_name = names[0]
            print self.server_name

        for loc in config.find('location'):
            if loc.args:
                if loc.args[0] in '= | ~ | ~* | ^~':
                    patt = loc.args[1]
                else:
                    patt = loc.args[0]
                self.patterns.append((patt, loc))

    def handle_request(self, request):
        hdler = self.handlercls(request, self.patterns, self.base_environ.copy())
        hdler.handle()

class WSGIServer(BaseServer):
    def __init__(self, address, wsgiapp):
        BaseServer.__init__(self, address=address)
        self.wsgiapp = wsgiapp
        self.handlercls = handler.WSGIHandler
        self.activate_server()

    def handle_request(self, request):
        hdler = self.handlercls(request, self.wsgiapp, self.base_environ.copy())
        hdler.handle()


