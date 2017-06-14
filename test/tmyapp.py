from wsgiref.simple_server import make_server
from pwsmodule import pwserver as pw


def hello1(context):
    if context and isinstance(context, dict):
        if 'arg' in context:
            arg = context['arg']
            if isinstance(arg, dict):
                return ['%s: %s\r\n' % (k, arg[k]) for k in arg]
            elif isinstance(arg, list):
                return ['%s\r\n' % k for k in arg]
    return 'hello1'


def hello2(context):
    return 'hello2'


def pwapp():
    urls = [
        (r'/hello1\?name=(?P<name>\w+)', hello1),
        ('/hello2', hello2),
        ('/', hello1),
        ]
    app = pw.application(urls)
    return app


def demoapp(env, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ['hello, world']

if __name__ == '__main__':
    # make_server('', 8181, pwapp()).serve_forever()
    pw.launch(('127.0.0.1', 8181), demoapp)

