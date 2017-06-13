from wsgiref.simple_server import make_server
from pwserver.server import launch

def app(env, start_response):
    print 'run in the test app'
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ['hello, py world!']

def test():
    launch(('127.0.0.1', 8091), app)

if __name__ == '__main__':
    test()

