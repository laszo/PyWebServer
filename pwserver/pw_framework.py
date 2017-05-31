import re

class base_application(object):
    def __init__(self, urlpatterns):
        self.urlpatterns = urlpatterns

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

def match(pattern, string):
    reg = re.compile(pattern)
    m = reg.match(string)
    if not m:
        return False, None
    if m.groupdict():
        return True, dict(m.groupdict())
    elif m.group():
        return True, m.group()

class application(base_application):

    def wsgi_app(self, env, start_response):
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ['hello, pw framework']

_app = application('')
wsgi_app = _app.wsgi_app

