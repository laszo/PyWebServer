import re

def match(pattern, string):
    print 'pattern: %s' % pattern
    print 'string: %s' % string
    reg = re.compile(pattern)
    m = reg.match(string)
    if not m:
        return False, None
    if m.groupdict():
        return True, dict(m.groupdict())
    elif m.group():
        return True, m.group()

class _application(object):
    def __init__(self, urlpatterns):
        if urlpatterns:
            self.urlpatterns = urlpatterns
        else:
            self.urlpatterns = list()
        self.request = None
        self.env = None
        self._start_response = None
        self.status_sent = False

    def pre(self, env, start_response):
        self.env = env
        self._start_response = start_response

    def start_response(self, status, headers):
        if not self.status_sent:
            self._start_response(status, headers)
            self.status_sent = True

    def find_func(self):
        url = self.env['PATH_INFO']
        for pat, func in self.urlpatterns:
            mok, mat = match(pat, url)
            if mok:
                print mat
                return func

    def after(self, result):
        self.start_response('200 OK', [('Content-type', 'text/plain')])
        return result

    def add_rule(self, url, func):
        self.urlpatterns.append((url, func))

class application(_application):
    def __init__(self, urlpatterns):
        _application.__init__(self, urlpatterns)

    def __call__(self, env, start_response):
        self.pre(env, start_response)
        func = self.find_func()
        if func:
            res = func(self.request)
            return self.after(res)
        else:
            self.start_response('404 NOT FOUND', [('Content-type', 'text/plain')])
            return 'not found'


