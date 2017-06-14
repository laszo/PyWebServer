#! --encoding:utf8--

import os
import StringIO

DEFAULT_ROOT = '/usr/local/var/www/'
if os.name == 'nt':
    DEFAULT_ROOT = 'C:\\nginx-1.13.0\\html'
PASS_ARGS = ['proxy_pass', 'fastcgi_pass', 'uwsgi_pass', 'scgi_pass', 'memcached_pass']

import SimpleHTTPServer

RESP404 = """HTTP/1.0 404 Not Found


<head>
<title>Error response</title>
</head>
<body>
<h1>Error response</h1>
<p>Error code 404.
<p>Message: Not Found.
<p>Error code explanation: Nothing matches the given URI.
</body>
"""


class block(object):
    def __init__(self, line=None, prefix=""):
        self.prefix = prefix
        self.directives = list()
        self.blocks = list()
        self.last_block = None
        self._open = True
        self._finder = None
        self.args = None
        if line:
            self.name = line.replace('{', '').strip()
            words = self.name.split()
            self.command = words[0]
            self.args = words[1:]
        else:
            self.name = 'main'
            self.command = 'main'

    def check_open(self):
        if self.last_block:
            self._open = self.last_block.check_open()
        return self._open

    def push(self, line):
        if line.endswith(';'):
            if self.last_block:
                self.last_block.push(line)
            else:
                self.directives.append(line)
        elif line.endswith('{'):
            if self.last_block:
                self.last_block.push(line)
            else:
                self.last_block = block(line=line, prefix=self.prefix+'\t')
                self.blocks.append(self.last_block)
        elif line.endswith('}'):
            if self.last_block:
                self.last_block.push(line)
                if not self.last_block.check_open():
                    self.last_block = None
            else:
                self._open = False

    def printfoo(self, f):
        print >>f, self.prefix + self.name
        for i in self.directives:
            print >>f, self.prefix + '\t' + i
        for i in self.blocks:
            i.printfoo(f)
        return f.getvalue()

    def find(self, path):
        subp = path.split('.')
        if subp:
            if subp[0] != self.command:
                subp.insert(0, self.command)
            for i in self.subc(subp):
                yield i

    def subd(self, direct):
        for ddr in self.directives:
            if ddr.startswith(direct):
                return ddr

    def subc(self, paths):
        if not paths:
            return
        if self.command == paths[0]:
            if len(paths) == 1:
                yield self
            else:
                for blk in self.blocks:
                    if blk.command == paths[1]:
                        for i in blk.subc(paths[1:]):
                            yield i
                for dect in self.directives:
                    if dect.startswith(paths[1]):
                        yield dect

    def __str__(self):
        bufr = StringIO.StringIO()
        content = self.printfoo(bufr)
        bufr.close()
        return content

class config(object):
    def __init__(self, cfg_file):
        self.cfg_file = cfg_file
        self.main_context = block()
        for i in read_lines(cfg_file):
            self.main_context.push(i)

    def find(self, path):
        res = list()
        for i in self.main_context.find(path):
            res.append(i)
        return res

def init_mime_types(fpath):
    tmimes = dict()
    for line in open(fpath, 'rt'):
        line = line.strip().replace(';', '')
        if line.endswith('{') or line.endswith('}'):
            continue
        words = line.split()
        for word in words[1:]:
            tmimes[word] = words[0]
    return tmimes

PWD =  os.path.split(os.path.realpath(__file__))[0]
mimes = init_mime_types(os.path.join(PWD, 'mime.types'))

def get_mime_type(mtype):
    if mimes.has_key(mtype):
        return mimes[mtype]
    return 'application/octet-stream'

def read_lines(fn):
    f = open(fn, 'rt')
    for i in f:
        line = i.strip()
        if not line.startswith('#'):
            if not line == '':
                line = line.replace('{', '{\n')
                line = line.replace(';', ';\n')
                line = line.replace('}', '\n}\n')
                for j in line.split('\n'):
                    if len(j) > 0:
                        yield j
    f.close()


def error(msg):
    print 'Error: %s' % msg
    raise Exception

def parser(line):
    if line:
        return line.replace(';', '').split()[-1]
