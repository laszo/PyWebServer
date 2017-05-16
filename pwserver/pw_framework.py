import re


class application(object):
    def __init__(self, address, urlps):
        self.address = address
        self.urlspatterns = urlps

    def handle(self, url):
        for u, f in self.urlspatterns:
            ok, m = match(u, url)
            if ok:
                if not m:
                    return f()
                else:
                    return f(m)
            else:
                continue

def match(pattern, string):
    reg = re.compile(pattern)
    m = reg.match(string)
    if not m:
        return False, None
    if m.groupdict():
        return True, dict(m.groupdict())
    elif m.group():
        return True, m.group()
