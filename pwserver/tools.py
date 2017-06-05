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
        if line:
            self.name = line.replace('{', '').strip()
            self.command = self.name.split()[0]
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
        foo = path.split('.')
        if len(foo) > 0:
            if foo[0] != self.command:
                foo.insert(0, self.command)
            for i in self.__subc(foo):
                yield i

    def __subc(self, paths):
        if len(paths) > 0:
            if self.command == paths[0]:
                if len(paths) == 1:
                    yield self
                else:
                    for blk in self.blocks:
                        if blk.command == paths[1]:
                            for i in blk.__subc(paths[1:]):
                                yield i
                    for dect in self.directives:
                        if dect.startswith(paths[1]):
                            yield dect

    def __str__(self):
        f = StringIO.StringIO()
        foo = self.printfoo(f)
        f.close()
        return foo
