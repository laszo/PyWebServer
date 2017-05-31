from pw_wsgi_server import BaseServer

def test():
    def app(env, start_response):
        print 'run in the test app'
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ['hello, py world!']

    s = BaseServer(('127.0.0.1', 8091), app)
    s.run_server()

if __name__ == '__main__':
    test()
