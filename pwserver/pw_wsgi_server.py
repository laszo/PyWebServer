# --encoding:utf-8--
import socket
import select
import threading
import os
import sys

class BaseServer(object):

    MAX_READS = 65537

    def __init__(self, address, wsgi_app):
        self.socket = socket.socket()
        self.address = address
        self.wsgi_app = wsgi_app
        self.wfile = None
        self.raw_request = None
        self.server_name = None
        self.server_port = None
        self.status = None
        self.headers = list()

    def run_server(self):
        try:
            self.socket.bind(self.address)
            self.socket.listen(5)

            host, port = self.socket.getsockname()[:2]
            self.server_name = socket.getfqdn(host)
            self.server_port = port

            print 'Server listen at %s:%s' % (self.server_name, str(self.server_port))
        except socket.error as error:
            print 'Server Error:' + error.message
            self.colse_server()
            return

        try:
            self.waiting_request()
        except KeyboardInterrupt:
            self.colse_server()
        finally:
            self.colse_server()

    def waiting_request(self):
        print 'Waiting request...'
        while True:
            rl, wl, el = select.select([self.socket], [], [])
            for r in rl:
                c, a = r.accept()
                print 'Get request at %s:%s' % c.getsockname()[:2]
                self.handle(c, self.wsgi_app)
                # t = threading.Thread(target=self.handle, args=(c, self.wsgi_app, ))
                # t.start()

    def handle(self, request, app):
        self.raw_request = request.recv(self.MAX_READS)
        self.wfile = request.makefile('wb', -1)
        environ = self.config_wsgi_environ()
        result = app(environ, self.start_response)
        self.write_headers()
        for res in result:
            self._write(res)
        self.wfile.flush()
        self.wfile.close()
        request.close()

    def write_headers(self):
        if not self.status.startswith('HTTP'):
            self.status = 'HTTP/1.0 ' + self.status
        self._write(self.status + '\r\n')
        for keyword, value in self.headers:
            self._write("%s: %s\r\n" % (keyword, value))
        self._write('\r\n')

    def config_wsgi_environ(self):
        environ = dict(os.environ.items()).copy()
        environ['REQUEST_METHOD'] = 'GET'
        # environ['SCRIPT_NAME'] = ''
        environ['QUERY_STRING'] = '121212'
        # environ['CONTENT_TYPE'] = ''
        # environ['CONTENT_LENGTH'] = ''
        environ['PATH_INFO'] = '/'
        environ['SERVER_NAME'] = self.server_name
        environ['SERVER_PORT'] = str(self.server_port)
        # environ['SERVER_PROTOCOL'] = 'HTTP/1.0'

        environ['wsgi.url_scheme'] = 'http'
        # environ['wsgi.input']        = sys.stdin.buffer
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once'] = True
        return environ

    def start_response(self, status, headers):
        self.status = status
        for h in headers:
            self.headers.append(h)
        return self._write

    def _write(self, data):
        self.wfile.write(data)

    def colse_server(self):
        print 'Server is about to close...'
        self.socket.close()

