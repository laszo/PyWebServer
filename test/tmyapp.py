from wsgiref.simple_server import make_server
from pwsmodule import pwserver as pw

def hello1(context):
    print context
    return 'hello1'

def hello2(context):
    print context
    return 'hello2'

def makeapp():
    urls = [
        ('/', hello1),
        ('/hello1', hello1),
        ('/hello2', hello2),
        ]
    app = pw.application(urls)
    return app

def pwserve():
    pw.server.launch(('127.0.0.1', 8180), makeapp())

def wwsgiref():
    sver = make_server('', 8180, makeapp())
    sver.serve_forever()

if __name__ == '__main__':
    # pwserve()
    wwsgiref()
