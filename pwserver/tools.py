#! --encoding:utf8--


class block(object):
    def __init__(self):
        self.directives = list()
        self.blocks = list()
        self.lines = list()
        self.last_block = None
        self._open = False

    def check_open(self):
        if self.last_block:
            self._open = self.last_block.check_open()
        return self._open

    def push(self, line):
        if line.endswith('}'):
            if self.last_block():
                self.last_block.push(line)
                self.check_open()
            else:
                # 在这里，关闭本机的open
                self._open = False

        elif line.endswith('{'): # { 之前应该还有指令名称，不应该仅仅以 { 开头判断block的开始
            if self.last_block:
                self.last_block.push(line)
            else:
                self.last_block = block()
                self.blocks.append(self.last_block)

                # 这边比较乱，应该拿个笔画一下

        elif line.endswith(';'):
            if self.last_block:
                self.last_block.push(line)
            else:
                self.directives.append(line)
            # lvxiaoyu 搞到这个函数了，只要判断好几个状态即可，先吃饭吧


    def pop(self):
        if self.lines.count() > 0:
            last = self.lines[-1]
            self.lines.remove(last)
            return last
        else:
            return None




