import socket
import sys

import os.path
import shutil

import pwserver.tools as t

MAX_READS = 65537


class VeryBaseHandler(object):
    def __init__(self, request):
        self.request = request

    def handle(self):
        self.request.recv(MAX_READS)
        self.request.send(t.RESP404)
        self.request.close()


class BaseHandler(object):

    def __init__(self, request, env):
        assert request
        self.request = request
        self.env = env.copy()
        self.wfile = self.request.makefile('wb', 0)
        self.rfile = self.request.makefile('rb', -1)
        self.server_name = None
        self.server_port = None
        self.status = None
        self.headers = list()
        self.request_protocal = None
        self.request_path = None
        self.request_method = None
        self.request_string = None
        self.raw_request = None
        self.should_close = False

    def handle(self):
        if self.recv_request():
            self.handle_requst()
        else:
            self.send_error()

    def recv_request(self):
        self.raw_request = self.request.recv(MAX_READS)
        # self.raw_request = self.rfile.readline(self.MAX_READS) # why this line blocks?
        return self.paser_request()

    def paser_request(self):
        raw = self.raw_request
        if isinstance(self.raw_request, bytes):
            raw = self.raw_request.decode()
        lines = raw.split('\r\n')
        first = lines[0]
        print('Request: %s' % first)
        words = first.split()
        if len(words) > 1:
            self.request_method = words[0]
            self.request_path = words[1]
            if len(words) > 2:
                self.request_protocal = words[2]
        else:
            return False
        if self.request_path:
            if '?' in self.request_path:
                self.request_path, self.request_string = self.request_path.split('?', 1)
            else:
                self.request_string = ''
        print('%s %s' % (self.request_method, self.request_path))
        return True

    def handle_requst(self):
        raise NotImplementedError

    def send_error(self):
        self._write(t.RESP404)
        self.finish()

    def send_status(self):
        if not self.status.startswith('HTTP'):
            self.status = 'HTTP/1.0 ' + self.status
        self._write(self.status + '\r\n')

    def send_header(self, keyword, value):
        self._write("%s: %s\r\n" % (keyword, value))

    def end_headers(self):
        self._write("\r\n")

    def _write(self, data):
        self.wfile.write(data.encode())

    def flush(self):
        self.wfile.flush()

    def finish(self):
        if not self.wfile.closed:
            try:
                self.flush()
            except socket.error:
                pass
        self.wfile.close()
        self.rfile.close()
        self.request.close()


class ConfigFileHandler(BaseHandler):
    def __init__(self, request, patterns, env):
        BaseHandler.__init__(self, request, env)
        self.patterns = patterns
        self.raw_request = None

    def handle_requst(self):
        location = self.find_location()
        uri = self.get_uri()
        if location and uri:
            root = self.get_root(location)
            if root:
                fpath = os.path.join(root, uri)
                self.send_file(fpath)
                self.finish()
                return
            else:
                for pasarg in t.PASS_ARGS:
                    targ = t.parser(location.subd(pasarg))
                    if targ:
                        print('%s: %s' % (pasarg, targ))
        self.send_error()

    def send_file(self, fpath):
        if not os.path.exists(fpath):
            print('not found: ', fpath)
            self.send_error()
            return
        print('sending: ', fpath)

        tfile = open(fpath)

        self.status = 'HTTP/1.0 200 OK'
        self.send_status()
        mtype = fpath.split('.')[-1]
        self.send_header("Content-type", t.get_mime_type(mtype))
        fst = os.fstat(tfile.fileno())
        self.send_header("Content-Length", str(fst[6]))
        self.end_headers()

        shutil.copyfileobj(tfile, self.wfile)

        self.flush()

    def send_pass(self, loc):
        pass

    def get_uri(self):
        if not self.request_path:
            return 'index.html'
        if self.request_path.startswith('/'):
            rpath = self.request_path[1:]
            if not rpath:
                rpath = 'index.html'
            return rpath
        return 'index.html'

    def get_root(self, location):
        if not location:
            return
        root = t.parser(location.subd('root'))
        if root:
            if root == 'html':
                root = t.DEFAULT_ROOT
        return root

    def find_location(self):
        mostmatch = 0
        location = None
        for pat, loc in self.patterns:
            if self.request_path.startswith(pat):
                if len(pat) > mostmatch:
                    mostmatch = len(pat)
                    location = loc
        return location


class WSGIHandler(BaseHandler):
    def __init__(self, request, wsgi_app, env):
        BaseHandler.__init__(self, request, env)
        self.wsgi_app = wsgi_app

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
        # todo: wsgi.input should be something
        environ['wsgi.input'] = self.rfile
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once'] = True

    def handle_requst(self):
        self.config_wsgi_environ()
        self.headers = list()
        result = self.wsgi_app(self.env, self.start_response)
        if result:
            self.write_headers()
            self.send_resutl(result)
            self.flush()
            self.finish()
        else:
            self.send_error()

    def start_response(self, status, headers):
        self.status = status
        for header in headers:
            self.headers.append(header)
        return self._write

    def send_resutl(self, result):
        if result:
            for res in result:
                self._write(res)

    def write_headers(self):
        self.send_status()
        for keyword, value in self.headers:
            self.send_header(keyword, value)
        self.end_headers()
