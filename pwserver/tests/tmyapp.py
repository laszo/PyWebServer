from wsgiref.simple_server import make_server
from pwsmodule import pwserver as pw
from pwsmodule import app

def demoapp(env, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ['hello, world']

if __name__ == '__main__':
    # make_server('', 8181, pwapp()).serve_forever()
    # pw.launch(('127.0.0.1', 8181), demoapp)
    pw.launch(('127.0.0.1', 8181), app.demo.wsgi_app)
    # pw.launch(('127.0.0.1', 8181), pwapp(), cfg_file='config.conf')
    # pw.launch(cfg_file='config.conf')

