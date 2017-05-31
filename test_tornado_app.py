import tornado.ioloop
import tornado.web
import tornado.wsgi
from wsgiref.simple_server import make_server
from pwserver.server import BaseServer


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, tornado world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def tornado_native():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

def with_wsgiref():
    wsgi_app = tornado.wsgi.WSGIAdapter(make_app())
    server = make_server('', 8888, wsgi_app)
    server.serve_forever()

def with_pw_server():
    wsgi_app = tornado.wsgi.WSGIAdapter(make_app())
    server = BaseServer(('', 8090), wsgi_app)
    server.run_server()

if __name__ == "__main__":
    # with_wsgiref()
    with_pw_server()
