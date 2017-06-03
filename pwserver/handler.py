import os
import sys

class handler(object):
    MAX_READS = 65537

    def __init__(self, request, wsgi_app):
        self.request = request
        self.wsgi_app = wsgi_app
        self.wfile = None
        self.raw_request = None
        self.environ = None
        self.server_name = None
        self.server_port = None
        self.status = None
        self.headers = list()

    def handle(self):
        self.raw_request = self.request.recv(self.MAX_READS)
        self.wfile = self.request.makefile('wb', -1)
        self.config_wsgi_environ()
        self.paser_request()
        self.headers = list()
        result = self.wsgi_app(self.environ, self.start_response)
        self.write_headers()
        self.send_response(result)
        self.request.close()

    def paser_request(self):
        lines = self.raw_request.split('\r\n')
        first = lines[0]
        words = first.split()
        if len(words) > 1:
            return words[1]

    def send_response(self, result):
        for res in result:
            self._write(res)
        self.wfile.flush()
        self.wfile.close()

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
        environ['wsgi.input'] = sys.stdin
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once'] = True
        self.environ = environ

    def start_response(self, status, headers):
        self.status = status
        for h in headers:
            self.headers.append(h)
        return self._write

    def _write(self, data):
        self.wfile.write(data)
