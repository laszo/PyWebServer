from pwserver.server import launch
import SimpleHTTPServer
from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/hello1')
def hello_world():
    return 'Hello, flask World!'

@app.route('/hello2')
def hello2():
    return 'Hello, world 2'


def flask():
    launch(cfg_file='pwserver/config.conf')
    # launch(('127.0.0.1', 8094), app, 'pwserver/out.conf')

if __name__ == '__main__':
    flask()
