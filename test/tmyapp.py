from wsgiref.simple_server import make_server
from pwsmodule import pwserver as pw

def app(env, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ['hello, py world!']

def main():
    pw.server.launch(('127.0.0.1', 8180), app)

def wwsgiref():
    s = make_server('', 8180, app)
    s.serve_forever()

if __name__ == '__main__':
    main()
    # wwsgiref()

