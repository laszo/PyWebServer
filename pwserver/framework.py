import re

class _application(object):
    def __init__(self, urlpatterns):
        self.urlpatterns = urlpatterns
        self.request = None
        self.env = None

    def preprocess_request(self, env):
        self.env = env
        self.env['path'] = '/'
        self.request = env['path']

    def process(self, url):
        for u, f in self.urlpatterns:
            ok, m = match(u, url)
            if ok:
                if not m:
                    return f()
                else:
                    return f(m)
            else:
                continue

    def built_response(self, response):
        return response

def match(pattern, string):
    reg = re.compile(pattern)
    m = reg.match(string)
    if not m:
        return False, None
    if m.groupdict():
        return True, dict(m.groupdict())
    elif m.group():
        return True, m.group()

class application(_application):
    def __init__(self, urlpatterns):
        _application.__init__(self, urlpatterns)

    def __call__(self, env, start_response):
        func = self.process(self.request)
        response = func(env)
        start_response('200 OK', [('Content-type', 'text/plain')])
        return self.built_response(response)

def _demo_app(env, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ['hello, pw framework']

app = application('')

from server import launch

launch(('', 8180), app)
