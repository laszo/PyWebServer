#! --encoding:utf8--

import StringIO

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
