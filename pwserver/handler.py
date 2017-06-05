import os
import sys
import shutil
from RequestType import rtype

class handler(object):
    MAX_READS = 65537

    def __init__(self, request, wsgi_app, env):
        self.request = request
        self.wsgi_app = wsgi_app
        self.wfile = None
        self.raw_request = None
        self.environ = None
        self.server_name = None
        self.server_port = None
        self.status = None
        self.headers = list()
        self.environ = env.copy()
        self.request_protocal = None
        self.request_path = None
        self.request_method = None
        self.request_string = None
        self.request_type = rtype.STATIC_FILE

    def handle(self):
        self.raw_request = self.request.recv(self.MAX_READS)
        self.wfile = self.request.makefile('wb', -1)
        if self.paser_request():
            self.handle_requst()
            self.close_request()
        else:
            self.send_error()

    def paser_request(self):
        lines = self.raw_request.split('\r\n')
        first = lines[0]
        words = first.split()
        if len(words) == 3:
            self.request_method = words[0]
            self.request_path = words[1]
            if '?' in self.request_path:
                self.request_path, self.request_string = self.request_path.split('?', 1)
            else:
                self.request_string = ''
            self.request_protocal = words[2]
        elif len(words) == 2:
            pass
        else:
            return False
        return self.det_request_type()

    def det_request_type(self):
        if not self.request_path:
            return False


    def handle_requst(self):
        pass

    def wsgi_requst(self):
        self.config_wsgi_environ()
        self.headers = list()
        result = self.wsgi_app(self.environ, self.start_response)
        self.write_headers()
        self.send_response(result)

    def send_error(self):
        self.close_request()

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
        environ = self.environ
        environ['SERVER_PROTOCOL'] = 'HTTP/1.0'
        environ['REQUEST_METHOD'] = self.request_method
        environ['PATH_INFO'] = self.request_path
        environ['QUERY_STRING'] = self.request_string
        # environ['SCRIPT_NAME'] = ''
        # environ['CONTENT_TYPE'] = ''
        # environ['CONTENT_LENGTH'] = ''

        environ['wsgi.url_scheme'] = 'http'
        environ['wsgi.input'] = sys.stdin
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once'] = True

    def start_response(self, status, headers):
        self.status = status
        for h in headers:
            self.headers.append(h)
        return self._write

    def _write(self, data):
        self.wfile.write(data)

    def close_request(self):
        self.request.close()


