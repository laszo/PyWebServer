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
    args = context['args']
    kwarg = context['kwarg']
    print args
    print kwarg
    return 'hello2'


def pwapp():
    urls = [
        (r'/hello1\?name=(?P<name>\w+)', hello1),
        ('/hello2', hello2),
        (r'/hello2\?name=\w+&age=\s+', hello2),
        ('/', hello1),
        ]
    app = pw.application(urls)
    return app

wsgi_app = pwapp()

if __name__ == '__main__':
    pw.launch(wsgiapp=wsgi_app)
