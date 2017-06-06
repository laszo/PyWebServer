import sys
import shutil
import os.path
from pwserver.RequestType import rtype

class BaseHandler(object):
    MAX_READS = 65537

    def __init__(self, request, env):
        self.request = request
        self.env = env
        self.wfile = self.request.makefile('wb', -1)
        self.raw_request = None
        self.server_name = None
        self.server_port = None
        self.status = None
        self.headers = list()
        self.request_protocal = None
        self.request_path = None
        self.request_method = None
        self.request_string = None
        self.request_type = rtype.STATIC_FILE

    def handle(self):
        self.raw_request = self.request.recv(self.MAX_READS)
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
        return True

    def handle_requst(self):
        raise NotImplementedError

    def send_error(self):
        self.close_request()

    def send_response(self, result):
        for res in result:
            self._write(res)
        self.wfile.flush()
        self.wfile.close()

    def start_response(self, status, headers):
        self.status = status
        for header in headers:
            self.headers.append(header)
        return self._write

    def write_headers(self):
        if not self.status.startswith('HTTP'):
            self.status = 'HTTP/1.0 ' + self.status
        self._write(self.status + '\r\n')
        for keyword, value in self.headers:
            self.send_header(keyword, value)
        self._write('\r\n')

    def send_header(self, keyword, value):
        self._write("%s: %s\r\n" % (keyword, value))

    def _write(self, data):
        self.wfile.write(data)

    def close_request(self):
        self.request.close()

G_RESPONSE = 'HTTP/1.0 200 OK\n'
DEFAULT_ROOT = '/usr/local/var/www/'
if os.name == 'nt':
    DEFAULT_ROOT = 'C:\\nginx-1.13.0\\html'
PASS_ARGS = ['proxy_pass', 'fastcgi_pass', 'uwsgi_pass', 'scgi_pass', 'memcached_pass']

def parser(line):
    if line:
        return line.replace(';', '').split()[-1]

class ConfigFileHandler(BaseHandler):

    def __init__(self, request, config, env):
        BaseHandler.__init__(self, request, env)
        self.request_type = rtype.WSGI
        self.root = parser(config.subd('root'))
        self.patterns = list()

        for loc in config.find('location'):
            if loc.args:
                if loc.args[0] in '= | ~ | ~* | ^~':
                    patt = loc.args[1]
                else:
                    patt = loc.args[0]
                root = parser(loc.subd('root'))
                if root:
                    if root == 'html':
                        root = DEFAULT_ROOT
                    self.patterns.append((patt, FileHelper(root, self.wfile)))
                else:
                    for pasarg in PASS_ARGS:
                        targ = parser(loc.subd(pasarg))
                        print 'pass: ', targ

    def handle_requst(self):
        mostmatch = 0
        helper = None
        for pat, hlpr in self.patterns:
            if self.request_path.startswith(pat):
                if len(pat) > mostmatch:
                    mostmatch = len(pat)
                    helper = hlpr
        if helper:
            request = self.request_path.replace('/', '')
            if not request:
                request = 'index.html'
            helper.handle(request)

class FileHelper(object):
    def __init__(self, root, wfile):
        self.root = root
        self.wfile = wfile

    def handle(self, rpath):
        self.wfile.write(G_RESPONSE)
        fpath = os.path.join(self.root, rpath)
        self.send_file(fpath)

    def send_file(self, fpath):
        if not os.path.exists(fpath):
            return
        print 'sending: ', fpath
        with open(fpath) as tfile:
            shutil.copyfileobj(tfile, self.wfile)
        self.wfile.flush()
        self.wfile.close()

class PassHelper(object):
    def handle(self, fpath):
        pass
        # self.wfile.write(G_RESPONSE)

class WSGIHandler(BaseHandler):
    def __init__(self, request, wsgi_app, env):
        BaseHandler.__init__(self, request, env)
        self.wsgi_app = wsgi_app
        self.request_type = rtype.WSGI

    def config_wsgi_environ(self):
        environ = self.env
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

    def handle_requst(self):
        self.config_wsgi_environ()
        self.headers = list()
        result = self.wsgi_app(self.env, self.start_response)
        self.write_headers()
        self.send_response(result)
