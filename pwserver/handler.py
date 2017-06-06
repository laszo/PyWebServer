import sys
import re
import os.path
from pwserver.RequestType import rtype

class BaseHandler(object):
    MAX_READS = 65537

    def __init__(self, request, env):
        self.request = request
        self.env = env
        self.wfile = None
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

    def write_headers(self):
        if not self.status.startswith('HTTP'):
            self.status = 'HTTP/1.0 ' + self.status
        self._write(self.status + '\r\n')
        for keyword, value in self.headers:
            self._write("%s: %s\r\n" % (keyword, value))
        self._write('\r\n')

    def start_response(self, status, headers):
        self.status = status
        for header in headers:
            self.headers.append(header)
        return self._write

    def _write(self, data):
        self.wfile.write(data)

    def close_request(self):
        self.request.close()

class StaticFileHandler(BaseHandler):

    G_response = 'HTTP/1.0 200 OK\n'

    def __init__(self, request, locations, root, env):
        BaseHandler.__init__(self, request, env)
        self.locations = locations
        self.request_type = rtype.WSGI
        self.patterns = list()
        if root:
            self.root = root
        else:
            self.root = '/usr/local/var/www'
        for loc in self.locations:
            if loc.args:
                if loc.args[0] in '= | ~ | ~* | ^~':
                    pat = re.compile(loc.args[1])
                else:
                    pat = re.compile(loc.args[0])
                self.patterns.append((pat, loc))

    def handle_requst(self):
        if self.request_path == '/':
            self.request_path = '/index.html'
        print 'request: ', self.request_path
        pass_args = ['proxy_pass', 'fastcgi_pass', 'uwsgi_pass', 'scgi_pass', 'memcached_pass']
        for pat, loc in self.patterns:
            if pat.match(self.request_path):
                for root in loc.find('root'):
                    print 'root: %s' % root
                    self._write(self.G_response)
                    ft1 = root.replace(';', '').split()[-1]
                    pt1 = os.path.join(self.root, ft1)
                    fpath = os.path.join(pt1, self.request_path)
                    res = self.get_file('/usr/local/var/www/index.html')
                    self.send_response(res)
                    return

    def get_file(self, fpath):
        print 'reading: ', fpath
        tfile = open(fpath)
        boo = tfile.read()
        tfile.close()
        return boo


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
