from pwserver.server import launch
import SimpleHTTPServer
from wsgiref.simple_server import make_server
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
import gunicorn.app
from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/hello1')
def hello_world():
    return 'Hello, flask World!'

@app.route('/hello2')
def hello2():
    return 'Hello, world 2'

import os, sys
if os.name == 'posix':
    sys.path.append('/Users/laszo/code/bootcamp')
import bootcamp.wsgi

def flask():
    # launch(cfg_file='pwserver/config.conf')
    # launch(('127.0.0.1', 8102), bootcamp.wsgi.application)
    server = make_server('', 8103, bootcamp.wsgi.application)
    print server.server_name
    server.serve_forever()
    # launch(('127.0.0.1', 8101), bootcamp.wsgi.application, 'pwserver/config.conf')

if __name__ == '__main__':
    flask()
