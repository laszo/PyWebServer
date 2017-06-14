import re


def match(pattern, url):
    reg = re.compile(pattern)
    m = reg.match(url)
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

    def pre(self, env, start_response):
        self.env = env
        self.request = dict()
        self._start_response = start_response

    def start_response(self, status, headers):
        if self._start_response:
            self._start_response(status, headers)

    def process(self):
        func, mat = self.find_func()
        if func:
            context = self.env
            context['arg'] = None
            if mat:
                if isinstance(mat, list):
                    context['arg'] = mat
                elif isinstance(mat, dict):
                    context['arg'] = mat
            return func(context)

    def find_func(self):
        url = self.env['PATH_INFO']
        if self.env['QUERY_STRING']:
            url = '%s?%s' % (url, self.env['QUERY_STRING'])
        for pat, func in self.urlpatterns:
            mok, mat = match(pat, url)
            if mok:
                return func, mat

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
        res = self.process()
        if res:
            return self.after(res)
        else:
            self.start_response('404 NOT FOUND', [('Content-type', 'text/plain')])
            return 'not found'

