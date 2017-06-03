from pwserver.server import BaseServer

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
    s = BaseServer(('127.0.0.1', 8097), app)
    s.run_server()

if __name__ == '__main__':
    flask()
